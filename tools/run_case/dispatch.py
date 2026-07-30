"""Subprocess dispatch and grading: build the coding-agent CLI command lines,
run runners and graders concurrently, parse what they return, and reconcile the
two arms' judgments into scored result rows.
"""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import re
import subprocess
from pathlib import Path

from run_case.errors import DispatchError, Row

CODEX_MODEL = "gpt-5.6-luna"
CODEX_EFFORT = "xhigh"
CLAUDE_MODEL = "claude-opus-5"

RUNNER_TIMEOUT = 3600
GRADER_TIMEOUT = 2400
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


def cli_command(family: str, prompt: str, empty_dir: Path, out_file: Path) -> list[str]:
    drop = [token for name in DROPPED_ENV for token in ("-u", name)]
    if family == "codex":
        # --ignore-user-config is load-bearing: without it $CODEX_HOME/config.toml
        # silently overrides -m and the reasoning-effort pin, and a run stops
        # being comparable to any other run.
        return [
            "env", *drop,
            "codex", "exec", "-s", "read-only",
            "-C", str(empty_dir),
            "--skip-git-repo-check", "--ignore-user-config",
            "-m", CODEX_MODEL, "-c", f"model_reasoning_effort={CODEX_EFFORT}",
            "-o", str(out_file), prompt,
        ]
    # --strict-mcp-config with no --mcp-config loads no MCP server, so the
    # grader — the component fed attacker-influenced runner text — has no live
    # tools. Note the asymmetry: this CLI still reads the operator's global
    # CLAUDE.md and has no flag to suppress it, so unlike codex's
    # --ignore-user-config the claude family is not fully pinned.
    return [
        "env", *drop,
        "claude", "-p", "--tools=", "--strict-mcp-config",
        "--model", CLAUDE_MODEL, prompt,
    ]


def dispatch(family: str, prompt: str, workspace: Path, tag: str, timeout: int) -> tuple[str, Path]:
    """Run one blind agent and return its stdout text plus the raw output path."""
    out_file = workspace / "raw" / f"{tag}.out"
    err_file = workspace / "raw" / f"{tag}.err"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    empty_dir = workspace / "empty"
    empty_dir.mkdir(parents=True, exist_ok=True)
    command = cli_command(family, prompt, empty_dir, out_file)
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
        raise DispatchError(
            f"{tag}: {family} exited {proc.returncode} — its output is not an "
            f"answer and is never scored; stderr tail: {stderr_tail(err_file)}"
        )
    if family == "claude":
        out_file.write_bytes(proc.stdout or b"")
    text = out_file.read_text(encoding="utf-8", errors="replace") if out_file.exists() else ""
    if not text.strip():
        raise DispatchError(
            f"{tag}: {family} produced no output (exit {proc.returncode}) — "
            f"stderr tail: {stderr_tail(err_file)}"
        )
    return text, out_file


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


def run_runners(plan: list[dict], jobs: int) -> dict[tuple[int, str], tuple[str, Path]]:
    results: dict[tuple[int, str], tuple[str, Path]] = {}
    errors: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {
            pool.submit(
                dispatch, item["family"], item["prompt"], item["workspace"],
                item["tag"], RUNNER_TIMEOUT,
            ): item
            for item in plan
        }
        for future in concurrent.futures.as_completed(futures):
            item = futures[future]
            try:
                results[(item["chunk"], item["arm"])] = future.result()
            except DispatchError as exc:
                errors.append(str(exc))
            except Exception as exc:
                errors.append(worker_failure(item, exc))
    if errors:
        raise DispatchError("runner dispatch failed:\n  " + "\n  ".join(sorted(errors)))
    return results


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


def run_graders(plan: list[dict], jobs: int) -> dict[int, tuple[dict, ...]]:
    results: dict[int, tuple[dict, ...]] = {}
    errors: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = {pool.submit(grade_chunk, item): item for item in plan}
        for future in concurrent.futures.as_completed(futures):
            item = futures[future]
            try:
                results[item["chunk"]] = future.result()
            except DispatchError as exc:
                errors.append(str(exc))
            except Exception as exc:
                errors.append(worker_failure(item, exc))
    if errors:
        raise DispatchError("grader dispatch failed:\n  " + "\n  ".join(sorted(errors)))
    return results


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
