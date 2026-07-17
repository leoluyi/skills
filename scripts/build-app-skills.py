#!/usr/bin/env python3
"""Build Claude-app-uploadable skill zips from this repo's skills/.

The Claude app (claude.ai > Settings > Capabilities > Skills) reads only the
`name`, `description`, and `license` frontmatter fields, and enforces a
1024-character limit on `description`. Several of our SKILL.md files carry
richer multi-platform frontmatter and, in one case, a description longer than
the limit. This script produces clean upload packages without touching source:

  * copies each skill to dist/<name>/ (dropping .DS_Store / DEVELOPMENT.md)
  * rewrites frontmatter down to name / description / license
  * substitutes a trimmed description when scripts/app-skill-overrides/<name>.txt
    exists (used when the source description exceeds 1024 chars)
  * hard-fails if any resulting description is still over the limit
  * zips dist/<name>/ -> dist/<name>.zip with a single top-level <name>/ folder
    and no macOS resource-fork cruft

Usage:
  uv run scripts/build-app-skills.py               # build the default set
  uv run scripts/build-app-skills.py plain-speak   # build only named skills
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
OVERRIDES = Path(__file__).resolve().parent / "app-skill-overrides"

DEFAULT_SKILLS = [
    "learn",
    "plain-speak",
    "avoid-ai-writing-zh",
    "infographic-design",
    "knowledge-doc-writing",
]

KEEP_KEYS = ("name", "description", "license")
DESC_LIMIT = 1024
IGNORE = shutil.ignore_patterns(".DS_Store", "DEVELOPMENT.md", "*.swp", "*.swo")


def split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("SKILL.md has no YAML frontmatter block")
    return m.group(1), m.group(2)


def parse_kept_fields(fm: str) -> dict[str, str]:
    """Extract name/description/license, folding a >- or | description block."""
    out: dict[str, str] = {}
    lines = fm.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(name|license):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip()
            i += 1
            continue
        m = re.match(r"^description:\s*(.*)$", line)
        if m:
            val = m.group(1).strip()
            if val in (">-", ">", "|", "|-"):
                block, i = [], i + 1
                while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                    block.append(lines[i].strip())
                    i += 1
                out["description"] = " ".join(x for x in block if x)
            else:
                out["description"] = val
                i += 1
            continue
        i += 1
    return out


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


def build_skill(name: str) -> None:
    src = SKILLS_DIR / name
    if not (src / "SKILL.md").is_file():
        raise SystemExit(f"error: skills/{name}/SKILL.md not found")

    staged = DIST / name
    if staged.exists():
        shutil.rmtree(staged)
    shutil.copytree(src, staged, ignore=IGNORE)

    fm, body = split_frontmatter((staged / "SKILL.md").read_text(encoding="utf-8"))
    fields = parse_kept_fields(fm)
    for required in ("name", "description"):
        if required not in fields:
            raise SystemExit(f"error: skills/{name} frontmatter missing '{required}'")
    if fields["name"] != name:
        raise SystemExit(f"error: skills/{name} frontmatter name is '{fields['name']}'")

    override = OVERRIDES / f"{name}.txt"
    source = "source"
    if override.is_file():
        fields["description"] = override.read_text(encoding="utf-8").strip()
        source = "override"

    dlen = len(fields["description"])
    if dlen > DESC_LIMIT:
        raise SystemExit(
            f"error: {name} description is {dlen} chars (> {DESC_LIMIT}). "
            f"Add a trimmed scripts/app-skill-overrides/{name}.txt."
        )

    (staged / "SKILL.md").write_text(f"---\n{build_frontmatter(fields)}---\n{body}", encoding="utf-8")

    dest_zip = DIST / f"{name}.zip"
    if dest_zip.exists():
        dest_zip.unlink()
    zip_skill(staged, dest_zip)
    print(f"  {name:22} desc={dlen:>4} ({source})  ->  dist/{name}.zip")


def main() -> None:
    skills = sys.argv[1:] or DEFAULT_SKILLS
    DIST.mkdir(exist_ok=True)
    (DIST / ".keep").touch()
    print(f"Building {len(skills)} skill package(s) into dist/")
    for name in skills:
        build_skill(name)
    print("Done. Upload each dist/<name>.zip via claude.ai > Settings > Capabilities > Skills.")


if __name__ == "__main__":
    main()
