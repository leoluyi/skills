#!/usr/bin/env python3
"""Snapshot tests for derive.py.

    python scripts/test_themes.py            # check against fixtures
    python scripts/test_themes.py --update   # re-baseline after an intended change

Every theme's full derive output is stored under tests/fixtures/. Colour work
is easy to break silently: a parser tweak can drop a mode flag, or a message
change can mask which gate fired, and neither shows up until someone renders a
diagram and squints at it. Diffing the output makes those regressions loud.

The synthetic cases in tests/cases.json lock in the GATES rather than any
theme — they assert that four categories fail in outline mode, that five fail
anywhere, and so on. Those paths have no theme file to guard them.
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from derive import parse_theme  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIX = os.path.join(ROOT, "tests", "fixtures")
CASES = os.path.join(ROOT, "tests", "cases.json")
DERIVE = os.path.join(HERE, "derive.py")


def run(args):
    p = subprocess.run([sys.executable, DERIVE] + args,
                       capture_output=True, text=True, cwd=ROOT)
    return f"exit={p.returncode}\n{p.stdout}"


def themes():
    d = os.path.join(ROOT, "themes")
    return sorted(f[:-3] for f in os.listdir(d) if f.endswith(".md"))


def cases():
    if not os.path.exists(CASES):
        return []
    return json.load(open(CASES, encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true")
    a = ap.parse_args()
    os.makedirs(FIX, exist_ok=True)

    failed = []
    for name in themes():
        cfg = parse_theme(os.path.join(ROOT, "themes", name + ".md"))
        if cfg["canvas_white"].upper() != "#FFFFFF":
            failed.append((name, "canvas-white must be #FFFFFF"))
        if cfg["canvas_tint"].upper() == cfg["canvas_white"].upper():
            failed.append((name, "canvas-tint must be distinct from canvas-white"))

    jobs = [(t, ["themes/%s.md" % t]) for t in themes()]
    jobs += [(c["name"], c["args"]) for c in cases()]

    for name, args in jobs:
        got = run(args)
        path = os.path.join(FIX, name + ".txt")
        if a.update:
            open(path, "w", encoding="utf-8").write(got)
            print(f"  wrote {name}")
            continue
        if not os.path.exists(path):
            failed.append((name, "no fixture — run --update"))
            continue
        want = open(path, encoding="utf-8").read()
        if got != want:
            diff = []
            for i, (x, y) in enumerate(zip(want.splitlines(), got.splitlines())):
                if x != y:
                    diff.append(f"    line {i+1}\n      want: {x}\n      got:  {y}")
            wl, gl = want.splitlines(), got.splitlines()
            if len(wl) != len(gl):
                diff.append(f"    length {len(wl)} -> {len(gl)}")
            failed.append((name, "\n".join(diff[:6]) or "differs"))
        else:
            print(f"  ok   {name}")

    if a.update:
        print(f"\nbaselined {len(jobs)} case(s).")
        return 0
    if failed:
        print(f"\n{len(failed)} regression(s):")
        for n, d in failed:
            print(f"  FAIL {n}\n{d}")
        print("\nIf the change was intended, re-run with --update and review the diff.")
        return 1
    print(f"\n{len(jobs)} case(s) match.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
