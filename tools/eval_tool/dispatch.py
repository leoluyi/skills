"""Subprocess dispatch and grading: build the coding-agent CLI command lines,
run runners and graders concurrently, parse what they return, and reconcile the
two arms' judgments into scored result rows.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from .legacy_errors import DispatchError, Row

CODEX_MODEL = "gpt-5.6-luna"
CODEX_EFFORT = "high"
CLAUDE_MODEL = "claude-opus-5"

RUNNER_TIMEOUT = int(os.environ.get("SKILL_EVAL_RUNNER_TIMEOUT", "300"))
GRADER_TIMEOUT = int(os.environ.get("SKILL_EVAL_GRADER_TIMEOUT", "180"))
STDERR_TAIL_BYTES = 400

SECRET_RE = re.compile(
    r"sk-[A-Za-z0-9_-]+"
    r"|ey[A-Za-z0-9_-]{20,}"
    r"|github_pat_[A-Za-z0-9_]+"
    r"|ghp_[A-Za-z0-9]+"
    r"|AKIA[A-Z0-9]{8,}"
    r"|AIza[A-Za-z0-9_-]{10,}"
    r"|xox[bp]-[A-Za-z0-9-]+"
)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# Every environment variable that could route a dispatch onto a billed or
# non-default endpoint, on either family. Dropped on both command lines so the
# guarantee is one rule rather than two per-family ones: no eval dispatch
# carries an API key, an auth token, or a base-URL/gateway override.
DROPPED_ENV = (
    "OPENAI_API_KEY",
    "OPENAI_BASE_URL",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
)


def sanitize(text: str) -> str:
    """Strip control bytes and redact key-shaped substrings before surfacing."""
    return SECRET_RE.sub("<redacted>", CONTROL_RE.sub("", text))


def fence_re(nonce: str) -> re.Pattern[str]:
    """Only a fence carrying this run's nonce counts as the grader's answer."""
    return re.compile(r"```json-" + re.escape(nonce) + r"\s*\n(.*?)\n?```", re.DOTALL)


def stderr_tail(path: Path) -> str:
    """Tail, not head: these CLIs print a long startup banner before any error."""
    if not path.exists():
        return "(no stderr captured)"
    # Redact before slicing: a tail cut through the middle of a key would strip
    # the prefix the redaction matches on and print the remainder verbatim.
    text = sanitize(path.read_bytes().decode("utf-8", "replace"))
    return text[-STDERR_TAIL_BYTES:].strip() or "(empty)"


def cli_command(family: str, prompt: str, empty_dir: Path, out_file: Path,
                 effort: str = CODEX_EFFORT) -> list[str]:
    drop = [token for name in DROPPED_ENV for token in ("-u", name)]
    if family == "codex":
        codex_home = _isolated_codex_home(empty_dir)
        # --ignore-user-config is load-bearing: without it $CODEX_HOME/config.toml
        # silently overrides -m and the reasoning-effort pin, and a run stops
        # being comparable to any other run.
        return [
            "env", *drop,
            f"CODEX_HOME={codex_home}",
            "codex", "exec", "-s", "read-only",
            "-C", str(empty_dir),
            "--skip-git-repo-check", "--ignore-user-config",
            "--ignore-rules", "--ephemeral",
            "-m", CODEX_MODEL, "-c", f"model_reasoning_effort={effort}",
            "-o", str(out_file), prompt,
        ]
    # --strict-mcp-config with no --mcp-config loads no MCP server, so the
    # grader — the component fed attacker-influenced runner text — has no live
    # tools. Note the asymmetry: this CLI still reads the operator's global
    # CLAUDE.md and has no flag to suppress it, so unlike codex's
    # --ignore-user-config the claude family is not fully pinned. ``effort``
    # is unused here — this CLI has no reasoning-effort flag.
    return [
        "env", *drop,
        "claude", "-p", "--tools=", "--strict-mcp-config",
        "--model", CLAUDE_MODEL, prompt,
    ]


def _isolated_codex_home(empty_dir: Path) -> Path:
    """Give eval agents auth without loading the operator's agent instructions.

    Codex discovers ``AGENTS.md`` from ``CODEX_HOME`` independently of
    ``--ignore-user-config`` and ``--ignore-rules``. Loading the operator's
    large global instructions makes a supposedly read-only eval agent inspect
    tools and skills, which adds latency and can trigger unrelated shell
    snapshot failures. Keep only a symlink to the existing auth file in the
    per-run home; never copy credential contents into the eval workspace.
    """
    root = empty_dir.parent / "codex-home"
    root.mkdir(parents=True, exist_ok=True)
    source_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    auth = source_home / "auth.json"
    if not auth.is_file():
        raise DispatchError(
            f"Codex eval needs auth.json at {auth}; configure CODEX_HOME or authenticate Codex"
        )
    link = root / "auth.json"
    try:
        link.symlink_to(auth)
    except FileExistsError:
        if not link.is_symlink() or link.resolve() != auth.resolve():
            raise DispatchError(f"Codex eval home contains unexpected auth path: {link}") from None
    return root


class _RetryableFailure(Exception):
    """Non-zero exit or empty output: often transient CLI flakiness, worth a
    retry. Raised only inside this module and always resolved into a
    DispatchError before it can reach a caller.
    """


def _dispatch_once(family: str, prompt: str, workspace: Path, tag: str, timeout: int,
                    effort: str | None) -> tuple[str, Path]:
    """Run one CLI invocation under ``tag`` and return its output text and path.

    Timeout and OSError raise DispatchError directly — a retry cannot fix
    either, so they are fatal on the first attempt. Non-zero exit and empty
    output raise _RetryableFailure instead, for ``dispatch()`` to apply its
    configured retry budget.
    """
    out_file = workspace / "raw" / f"{tag}.out"
    err_file = workspace / "raw" / f"{tag}.err"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    empty_dir = workspace / "empty"
    empty_dir.mkdir(parents=True, exist_ok=True)
    command = cli_command(
        family, prompt, empty_dir, out_file,
        effort if effort is not None else CODEX_EFFORT,
    )
    # stderr goes to its own file and is only ever used for diagnostics: merged
    # into the parsed stream, a CLI error's text can satisfy the same parse that
    # reads the real answer and fabricate a result.
    with err_file.open("wb") as err_handle:
        try:
            proc = subprocess.run(
                command,
                cwd=str(empty_dir),
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE if family == "claude" else subprocess.DEVNULL,
                stderr=err_handle,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise DispatchError(
                f"{tag}: {family} timed out after {timeout}s — stderr tail: {stderr_tail(err_file)}"
            ) from None
        except OSError as exc:
            raise DispatchError(f"{tag}: cannot run {family} — {exc}") from None
    if proc.returncode != 0:
        # A non-zero exit having printed a usage/auth/model error to stdout is
        # the dangerous case: that error text would otherwise be scored as the
        # arm's answer and fail every row in the chunk.
        raise _RetryableFailure(
            f"{tag}: {family} exited {proc.returncode} — its output is not an "
            f"answer and is never scored; stderr tail: {stderr_tail(err_file)}"
        )
    if family == "claude":
        out_file.write_bytes(proc.stdout or b"")
    text = out_file.read_text(encoding="utf-8", errors="replace") if out_file.exists() else ""
    if not text.strip():
        raise _RetryableFailure(
            f"{tag}: {family} produced no output (exit {proc.returncode}) — "
            f"stderr tail: {stderr_tail(err_file)}"
        )
    return text, out_file


def dispatch(family: str, prompt: str, workspace: Path, tag: str, timeout: int,
             effort: str | None = None, retries: int = 1) -> tuple[str, Path]:
    """Run one blind agent and return its stdout text plus the raw output path.

    Retries transient non-zero or empty-output failures up to ``retries``
    times. Never retries a timeout or an OSError: a retried 1-hour timeout
    would double the worst-case wall-clock for a failure mode a retry cannot
    fix, since a CLI that hung once is likely to hang again — those stay fatal
    on the first attempt. The
    retry writes to a ``-r2``-suffixed tag so the first attempt's raw out/err
    files are preserved as evidence rather than overwritten.
    """
    attempts = max(1, retries + 1)
    failures = []
    for attempt in range(attempts):
        try:
            suffix = "" if attempt == 0 else f"-r{attempt + 1}"
            return _dispatch_once(family, prompt, workspace, f"{tag}{suffix}", timeout, effort)
        except _RetryableFailure as failure:
            failures.append(failure)
    if len(failures) == 1:
        raise DispatchError(str(failures[0])) from None
    raise DispatchError(
        f"{tag}: failed {len(failures)} times, giving up — "
        + "; ".join(str(failure) for failure in failures)
    ) from None


def label_for_new(run_id: str, chunk_index: int) -> str:
    """Per-run, per-chunk A/B assignment the grader is never told about."""
    digest = hashlib.sha256(f"{run_id}{chunk_index}".encode("utf-8")).hexdigest()
    return "A" if int(digest, 16) % 2 == 0 else "B"


def extract_rows(text: str, nonce: str) -> list[dict] | None:
    """Parse the grader's answer, accepting only nonce-tagged fenced blocks.

    Runner output is quoted inside the grader prompt and is model-written text
    the fixture can influence, so an untagged ``{"rows": [...]}`` block reaching
    here may be forged rather than graded. The nonce never appears in a runner
    prompt, so only the grader can produce a block carrying it.
    """
    parsed = None
    for block in fence_re(nonce).findall(text):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and isinstance(data.get("rows"), list):
            parsed = data["rows"]
    return parsed


def check_rows(returned: list[dict] | None, expected: tuple[Row, ...]) -> tuple[dict, ...] | str:
    """Return the normalized rows, or a one-line description of the mismatch."""
    if returned is None:
        return "no nonce-tagged fenced JSON block with a 'rows' array"
    got, bad = {}, []
    for item in returned:
        if not isinstance(item, dict):
            bad.append(f"non-object row {item!r}")
            continue
        key = (item.get("case_id"), str(item.get("expectation", "")).strip())
        if item.get("A") not in ("pass", "fail") or item.get("B") not in ("pass", "fail"):
            bad.append(f"row {key} has a verdict that is not pass/fail")
            continue
        got[key] = item
    want = {(row.case_id, row.slug) for row in expected}
    missing = sorted(want - set(got), key=lambda k: (k[0], k[1]))
    extra = sorted(set(got) - want, key=lambda k: (str(k[0]), k[1]))
    if bad or missing or extra:
        parts = []
        if missing:
            parts.append(f"missing {missing}")
        if extra:
            parts.append(f"unexpected {extra}")
        parts.extend(bad[:5])
        return "; ".join(parts)
    return tuple(got[(row.case_id, row.slug)] for row in expected)


def worker_failure(item: dict, exc: Exception) -> str:
    """Name the job an unexpected worker exception came from.

    Caught broadly: anything other than DispatchError escaping a pool thread
    would reach main as a bare traceback that says nothing about which chunk
    or arm died.
    """
    return (
        f"{item.get('tag', 'unknown job')}: unexpected "
        f"{type(exc).__name__}: {sanitize(str(exc)) or '(no message)'}"
    )


def grade_chunk(item: dict) -> tuple[dict, ...]:
    """Grade one chunk, redispatching once when the returned rows do not match."""
    problems = []
    for attempt in (1, 2):
        text, _ = dispatch(
            item["family"], item["prompt"], item["workspace"],
            f"{item['tag']}-try{attempt}", GRADER_TIMEOUT,
        )
        outcome = check_rows(extract_rows(text, item["nonce"]), item["rows"])
        if not isinstance(outcome, str):
            return outcome
        problems.append(f"attempt {attempt}: {outcome}")
    raise DispatchError(
        f"{item['tag']}: grader rows never matched the chunk key — "
        + " | ".join(problems)
        + " (a chunk is never scored partially)"
    )


def progress(done: int, total: int, tag: str, outcome: str) -> None:
    """One line per finished job, on stderr.

    stdout is the result surface — ``--dry-run``'s output has to stay
    parseable — so progress can only go to stderr. ``flush`` is load-bearing:
    redirected to a file, Python block-buffers, and an unflushed progress line
    stays invisible until the process exits, which is exactly the 20-minute
    black box this exists to remove.
    """
    print(f"[{done}/{total}] {tag} {outcome}", file=sys.stderr, flush=True)


def run_pipeline(runner_plan: list[dict], grader_item, jobs: int,
                 preseeded: dict[tuple[int, str], tuple[str, Path]] | None = None
                 ) -> tuple[dict[tuple[int, str], tuple[str, Path]], dict[int, tuple[dict, ...]]]:
    """Run every runner and grader in one pool, grading each chunk the moment
    both of its arms land.

    A chunk's grader depends only on that chunk's own pair, so the barrier
    between the two phases was costing a full wave of wall-clock for nothing:
    the last runner of chunk 5 held back the grading of chunk 0. Sharing one
    pool keeps the ``--jobs`` cap honest across both kinds of job.

    ``grader_item`` is called with the chunk index and that chunk's two runner
    texts, and returns the grader job dict — the A/B mapping and prompt cannot
    be built before the pair exists.

    ``preseeded`` supplies arm output that was never dispatched this run — a
    baseline read from the bank — keyed the same way a dispatched arm's result
    would be. It seeds ``runner_out`` before the pool starts, so the pairing
    check below sees a preseeded base as already landed the moment the new
    arm's own runner finishes, and no job is ever submitted to produce it.
    """
    runner_out: dict[tuple[int, str], tuple[str, Path]] = dict(preseeded or {})
    graded: dict[int, tuple[dict, ...]] = {}
    runner_errors: list[str] = []
    grader_errors: list[str] = []
    # A chunk whose sibling arm failed must never be graded: half a pair would
    # be scored against the full key and every row in it would read as a miss.
    dead_chunks: set[int] = set()
    # One grader per chunk, but only for chunks whose pair both land — so this
    # is the ceiling, not a promise. A run that loses runners finishes below it.
    total = len(runner_plan) + len({item["chunk"] for item in runner_plan})
    done_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        pending = {
            pool.submit(
                dispatch, item["family"], item["prompt"], item["workspace"],
                item["tag"], RUNNER_TIMEOUT,
            ): item
            for item in runner_plan
        }
        while pending:
            done, _ = concurrent.futures.wait(
                pending, return_when=concurrent.futures.FIRST_COMPLETED
            )
            for future in done:
                item = pending.pop(future)
                kind = item.get("kind", "runner")
                # Counted here, in the single thread that drains the pool — no
                # lock needed, and every job reports exactly once whether it
                # succeeded or died.
                done_count += 1
                tag = item.get("tag", "unknown job")
                try:
                    result = future.result()
                except DispatchError as exc:
                    (grader_errors if kind == "grader" else runner_errors).append(str(exc))
                    dead_chunks.add(item["chunk"])
                    progress(done_count, total, tag, "FAILED")
                    continue
                except Exception as exc:
                    (grader_errors if kind == "grader" else runner_errors).append(
                        worker_failure(item, exc)
                    )
                    dead_chunks.add(item["chunk"])
                    progress(done_count, total, tag, "FAILED")
                    continue
                progress(done_count, total, tag, "ok")
                if kind == "grader":
                    graded[item["chunk"]] = result
                    continue
                index = item["chunk"]
                runner_out[(index, item["arm"])] = result
                if index in dead_chunks:
                    continue
                if (index, "new") in runner_out and (index, "base") in runner_out:
                    job = dict(
                        grader_item(
                            index,
                            runner_out[(index, "new")][0],
                            runner_out[(index, "base")][0],
                        ),
                        kind="grader",
                    )
                    pending[pool.submit(grade_chunk, job)] = job

    if runner_errors:
        raise DispatchError("runner dispatch failed:\n  " + "\n  ".join(sorted(runner_errors)))
    if grader_errors:
        raise DispatchError("grader dispatch failed:\n  " + "\n  ".join(sorted(grader_errors)))
    return runner_out, graded


def reconcile(chunk_rows: dict[int, tuple[Row, ...]], graded: dict[int, tuple[dict, ...]],
              mapping: dict[int, str]) -> tuple[dict, ...]:
    out = []
    for index in sorted(chunk_rows):
        new_label = mapping[index]
        base_label = "B" if new_label == "A" else "A"
        for row, judgment in zip(chunk_rows[index], graded[index]):
            class_read = str(judgment.get("class_read", "")).strip()
            out.append({
                "chunk": index,
                "case_id": row.case_id,
                "expectation": row.slug,
                "class": row.klass,
                "origin": row.origin,
                "new": judgment[new_label],
                "base": judgment[base_label],
                "class_read": class_read,
                "class_read_agrees": class_read == row.klass,
                "reason": str(judgment.get("reason", "")).strip(),
            })
    return tuple(out)
