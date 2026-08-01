#!/usr/bin/env python3
"""Build Claude-app-uploadable skill zips from this repo's skills/.

The Claude app (claude.ai > Settings > Capabilities > Skills) reads only the
`name`, `description`, and `license` frontmatter fields. claude.ai caps
`description` at 200 characters -- a tighter limit than the Agent Skills
spec's own 1024-char cap, which is what SKILL.md files in this repo are
normally written against. This script produces clean upload packages
without touching source:

  * copies each skill to dist/<name>/, dropping .DS_Store, design-notes.md,
    backlog.md, catalog.md, and the entire evals/ and research/ directories
    (development-only material that bloats the zip and adds nothing a
    packaged skill needs at load time)
  * rewrites frontmatter down to name / description / license
  * if the source SKILL.md defines `app-description` and/or `app-name`,
    those are used as the effective description/name for the packaged
    output instead of the plain `description`/`name` fields -- this is how
    a skill opts into a claude.ai-specific trimmed description or a
    different app-facing name without touching the fields other tooling
    reads. Neither field is ever written to the output SKILL.md.
  * hard-fails if the effective description is still over 200 chars, if the
    effective name fails claude.ai's name rules (<=64 chars, ^[a-z0-9-]+$,
    no "claude"/"anthropic" substring), if a skill directory contains a
    symlink (copytree would otherwise dereference it and package whatever
    it points at), or if two skills in the same build resolve to the same
    effective name (the second would silently overwrite the first's output)
  * warns (does not fail) if a SKILL.md body runs past 500 lines
  * zips dist/<name>/ -> dist/<name>.zip with a single top-level <name>/
    folder and no macOS resource-fork cruft

Usage:
  uv run scripts/build-app-skills.py plain-speak humanizer-zh  # named skills
  uv run scripts/build-app-skills.py --all                     # every skill
  uv run scripts/build-app-skills.py --list                    # status table, no build
  uv run scripts/build-app-skills.py                           # interactive menu (TTY only)
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO / "skills"
DIST = REPO / "dist"

KEEP_KEYS = ("name", "description", "license")
APP_ONLY_KEYS = ("app-description", "app-name")

# claude.ai's limit, distinct from the Agent Skills spec's 1024-char cap.
# https://claude.com/docs/skills/how-to: "Claude.ai limits descriptions to 200 characters"
APP_DESC_LIMIT = 200

NAME_LIMIT = 64
NAME_PATTERN = re.compile(r"^[a-z0-9-]+$")
RESERVED_NAME_SUBSTRINGS = ("claude", "anthropic")

BODY_LINE_WARN = 500

IGNORE = shutil.ignore_patterns(
    ".DS_Store",
    "design-notes.md",
    "backlog.md",
    "catalog.md",
    "*.swp",
    "*.swo",
    "evals",
    "research",
)


def split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("SKILL.md has no YAML frontmatter block")
    return m.group(1), m.group(2)


# Matches any YAML block scalar header: >, |, plus optional chomping (-/+)
# and/or an explicit indentation indicator digit, in either order (>-2, >2-).
_BLOCK_HEADER = re.compile(r"^[>|]([+-]?\d?|\d?[+-]?)$")
_QUOTED = re.compile(r'^(".*"|\'.*\')$')


def _fold_block(lines: list[str], i: int) -> tuple[str, int]:
    """Fold a block scalar (>, |, and their -/+/digit variants) starting at lines[i]."""
    block: list[str] = []
    i += 1
    while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
        block.append(lines[i].strip())
        i += 1
    return " ".join(x for x in block if x), i


def _unquote(val: str) -> str:
    """Strip a single matching pair of surrounding quotes, if present."""
    if _QUOTED.match(val):
        return val[1:-1]
    return val


def _reject_unhandled_continuation(lines: list[str], i: int, key: str) -> None:
    """Hard-fail if a plain scalar's next line looks like an unsupported
    multi-line continuation (YAML allows folding a plain scalar across
    indented lines; this parser only folds explicit >/|  block scalars, so
    silently accepting one here would truncate or blank out the value).
    """
    if i >= len(lines):
        return
    nxt = lines[i]
    if nxt.strip() and nxt.startswith(" ") and not re.match(r"^[a-zA-Z_-]+:", nxt.strip()):
        raise ValueError(
            f"'{key}' looks like a multi-line plain YAML scalar (an indented "
            f"continuation line follows) -- not supported by this parser. "
            f"Rewrite it as an explicit '{key}: >-' block."
        )


def parse_kept_fields(fm: str) -> dict[str, str]:
    """Extract name/license plus description/app-description/app-name.

    description, app-description, and app-name all use the same
    value-parsing logic, including the block-scalar-folding branch.
    """
    out: dict[str, str] = {}
    lines = fm.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(name|license):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = _unquote(m.group(2).strip())
            i += 1
            _reject_unhandled_continuation(lines, i, key)
            continue
        m = re.match(r"^(description|app-description|app-name):\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            if _BLOCK_HEADER.match(val):
                out[key], i = _fold_block(lines, i)
            else:
                out[key] = _unquote(val)
                i += 1
                _reject_unhandled_continuation(lines, i, key)
            continue
        i += 1
    return out


def validate_name(value: str, *, context: str) -> None:
    """Hard-fail if value violates claude.ai's skill name rules."""
    if len(value) > NAME_LIMIT:
        raise SystemExit(
            f"error: {context} '{value}' is {len(value)} chars (> {NAME_LIMIT} char limit)"
        )
    if not NAME_PATTERN.fullmatch(value):
        raise SystemExit(
            f"error: {context} '{value}' must match ^[a-z0-9-]+$ "
            "(lowercase letters, digits, hyphens only)"
        )
    lowered = value.lower()
    for reserved in RESERVED_NAME_SUBSTRINGS:
        if reserved in lowered:
            raise SystemExit(
                f"error: {context} '{value}' must not contain reserved word '{reserved}'"
            )


def wrap(text: str, width: int = 96, indent: str = "  ") -> str:
    lines, cur = [], ""
    for word in text.split(" "):
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(indent + cur)
            cur = word
        else:
            cur = word if not cur else f"{cur} {word}"
    if cur:
        lines.append(indent + cur)
    return "\n".join(lines)


def build_frontmatter(fields: dict[str, str]) -> str:
    out = f"name: {fields['name']}\ndescription: >-\n{wrap(fields['description'])}\n"
    if "license" in fields:
        out += f"license: {fields['license']}\n"
    return out


def zip_skill(skill_dir: Path, dest_zip: Path) -> None:
    """Deterministic zip containing a single top-level <name>/ folder."""
    files = sorted(p for p in skill_dir.rglob("*") if p.is_file() and p.name != ".DS_Store")
    with zipfile.ZipFile(dest_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.write(f, arcname=str(f.relative_to(DIST)))


def _dir_size(d: Path) -> int:
    return sum(f.stat().st_size for f in d.rglob("*") if f.is_file())


def discover_skills() -> list[str]:
    """Every skill directory name under skills/ that contains a SKILL.md."""
    return sorted(p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md"))


def _read_fields(name: str) -> dict[str, str]:
    src = SKILLS_DIR / name
    skill_md = src / "SKILL.md"
    if not skill_md.is_file():
        raise SystemExit(f"error: skills/{name}/SKILL.md not found")
    fm, _ = split_frontmatter(skill_md.read_text(encoding="utf-8"))
    return parse_kept_fields(fm)


def inspect_skill(name: str) -> dict[str, object]:
    """Non-failing status lookup for --list and the interactive menu."""
    try:
        fields = _read_fields(name)
    except (SystemExit, ValueError) as exc:
        return {"name": name, "error": str(exc)}
    for required in ("name", "description"):
        if required not in fields:
            return {"name": name, "error": f"frontmatter missing '{required}'"}
    if fields["name"] != name:
        return {
            "name": name,
            "error": (
                f"frontmatter name is '{fields['name']}', expected '{name}' "
                "(directory name must match source frontmatter name)"
            ),
        }
    effective_description = fields.get("app-description", fields["description"])
    effective_name = fields.get("app-name", fields["name"])
    try:
        validate_name(effective_name, context="effective name")
        name_error = None
    except SystemExit as exc:
        name_error = str(exc)
    return {
        "name": name,
        "error": None,
        "desc_len": len(effective_description),
        "has_app_description": "app-description" in fields,
        "has_app_name": "app-name" in fields,
        "app_name": fields.get("app-name"),
        "name_error": name_error,
    }


def _reject_symlinks(src: Path, name: str) -> None:
    """Hard-fail if the skill directory contains any symlink.

    shutil.copytree(symlinks=False) dereferences symlinks and copies the
    *target's* content into dist/, which would silently package whatever a
    symlink points at (e.g. a file outside the repo) into an uploadable
    zip. Refusing to build is safer than trying to preserve or sanitize it.
    """
    links = [p for p in src.rglob("*") if p.is_symlink()]
    if links:
        rel = ", ".join(str(p.relative_to(src)) for p in links)
        raise SystemExit(f"error: skills/{name} contains symlink(s) ({rel}) -- refusing to build")


def build_skill(name: str) -> None:
    src = SKILLS_DIR / name
    if not (src / "SKILL.md").is_file():
        raise SystemExit(f"error: skills/{name}/SKILL.md not found")
    _reject_symlinks(src, name)

    src_size = _dir_size(src)

    fm, body = split_frontmatter((src / "SKILL.md").read_text(encoding="utf-8"))
    fields = parse_kept_fields(fm)
    for required in ("name", "description"):
        if required not in fields:
            raise SystemExit(f"error: skills/{name} frontmatter missing '{required}'")
    if fields["name"] != name:
        raise SystemExit(
            f"error: skills/{name} frontmatter name is '{fields['name']}', "
            f"expected '{name}' (directory name must match source frontmatter name)"
        )

    n_lines = len(body.splitlines())
    if n_lines > BODY_LINE_WARN:
        print(f"  warning: {name} SKILL.md body is {n_lines} lines (>{BODY_LINE_WARN} recommended)")

    effective_description = fields.get("app-description", fields["description"])
    dlen = len(effective_description)
    if dlen > APP_DESC_LIMIT:
        raise SystemExit(
            f"error: {name} effective description is {dlen} chars (> {APP_DESC_LIMIT} char "
            f"claude.ai limit). Add or shorten the 'app-description' field in "
            f"skills/{name}/SKILL.md."
        )

    effective_name = fields.get("app-name", fields["name"])
    context = (
        f"skills/{name} SKILL.md 'app-name' field"
        if "app-name" in fields
        else f"skills/{name} SKILL.md 'name' field"
    )
    validate_name(effective_name, context=context)

    staged = DIST / effective_name
    if staged.exists():
        shutil.rmtree(staged)
    shutil.copytree(src, staged, ignore=IGNORE)
    staged_size = _dir_size(staged)

    out_fields = {"name": effective_name, "description": effective_description}
    if "license" in fields:
        out_fields["license"] = fields["license"]
    (staged / "SKILL.md").write_text(f"---\n{build_frontmatter(out_fields)}---\n{body}", encoding="utf-8")

    dest_zip = DIST / f"{effective_name}.zip"
    if dest_zip.exists():
        dest_zip.unlink()
    zip_skill(staged, dest_zip)

    print(
        f"  {name:22} desc={dlen:>4}  size={src_size / 1024:.1f}KB->{staged_size / 1024:.1f}KB"
        f"  ->  dist/{effective_name}.zip"
    )


def cmd_list(names: list[str]) -> None:
    print(f"  {'skill':30}{'desc_len':>9}  {'app-desc':>8}  {'app-name':>16}  status")
    for name in names:
        info = inspect_skill(name)
        if info["error"]:
            print(f"  {name:30}  ERROR: {info['error']}")
            continue
        status = "ok" if info["desc_len"] <= APP_DESC_LIMIT and not info["name_error"] else "FAIL"
        app_name = info["app_name"] or "-"
        print(
            f"  {name:30}{info['desc_len']:>9}  "
            f"{'yes' if info['has_app_description'] else 'no':>8}  "
            f"{app_name:>16}  {status}"
        )
        if info["name_error"]:
            print(f"    {info['name_error']}")


def _parse_index_token(token: str, count: int) -> list[int]:
    token = token.strip()
    if "-" in token:
        parts = token.split("-")
        if len(parts) != 2 or not all(p.strip().isdigit() for p in parts):
            print(f"error: invalid range '{token}'", file=sys.stderr)
            raise SystemExit(1)
        start, end = int(parts[0]), int(parts[1])
        if start < 1 or end > count or start > end:
            print(f"error: range '{token}' out of bounds (1-{count})", file=sys.stderr)
            raise SystemExit(1)
        return list(range(start, end + 1))
    if not token.isdigit():
        print(f"error: invalid selection '{token}'", file=sys.stderr)
        raise SystemExit(1)
    idx = int(token)
    if idx < 1 or idx > count:
        print(f"error: index {idx} out of range (1-{count})", file=sys.stderr)
        raise SystemExit(1)
    return [idx]


def prompt_selection(names: list[str]) -> list[str]:
    print("Skills available to build:")
    for idx, name in enumerate(names, start=1):
        info = inspect_skill(name)
        if info["error"]:
            print(f"  {idx:>3}. {name:30} ERROR: {info['error']}")
        else:
            status = "ok" if info["desc_len"] <= APP_DESC_LIMIT and not info["name_error"] else "FAIL"
            print(f"  {idx:>3}. {name:30} desc={info['desc_len']:>4}  {status}")

    try:
        raw = input("Select skills to build (e.g. 1,3-5, 'all', or empty to cancel): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\ncancelled")
        raise SystemExit(0)
    if not raw:
        print("cancelled")
        raise SystemExit(0)
    if raw.lower() == "all":
        return list(names)

    selected: set[int] = set()
    for token in raw.split(","):
        if not token.strip():
            continue
        selected.update(_parse_index_token(token, len(names)))
    return [names[i - 1] for i in sorted(selected)]


def _check_no_name_collisions(skills: list[str]) -> None:
    """Hard-fail if two skills in this batch resolve to the same effective
    (post app-name) output name -- otherwise the second build silently
    rmtree's and overwrites the first one's staged dir/zip, and both print
    a success line while dist/ ends up with only the second skill's content.
    """
    by_effective: dict[str, list[str]] = {}
    for skill_name in skills:
        try:
            fields = _read_fields(skill_name)
        except ValueError as exc:
            raise SystemExit(f"error: skills/{skill_name}: {exc}") from exc
        effective = fields.get("app-name", fields.get("name", skill_name))
        by_effective.setdefault(effective, []).append(skill_name)
    collisions = {k: v for k, v in by_effective.items() if len(v) > 1}
    if collisions:
        detail = "; ".join(f"'{k}' <- {v}" for k, v in collisions.items())
        raise SystemExit(f"error: multiple skills resolve to the same output name: {detail}")


def main() -> None:
    args = sys.argv[1:]
    all_skills = discover_skills()

    if "--list" in args:
        cmd_list(all_skills)
        return

    if "--all" in args:
        skills = all_skills
    elif args:
        skills = args
    elif sys.stdin.isatty():
        skills = prompt_selection(all_skills)
    else:
        print(
            "error: no skills specified and stdin is not interactive. "
            "Use --all, --list, or name skills explicitly, e.g.:\n"
            "  uv run scripts/build-app-skills.py --all\n"
            "  uv run scripts/build-app-skills.py --list\n"
            "  uv run scripts/build-app-skills.py plain-speak humanizer-zh",
            file=sys.stderr,
        )
        raise SystemExit(1)

    if not skills:
        print("cancelled")
        return

    _check_no_name_collisions(skills)

    DIST.mkdir(exist_ok=True)
    (DIST / ".keep").touch()
    print(f"Building {len(skills)} skill package(s) into dist/")
    for name in skills:
        build_skill(name)
    print("Done. Upload each dist/<name>.zip via claude.ai > Settings > Capabilities > Skills.")


if __name__ == "__main__":
    main()
