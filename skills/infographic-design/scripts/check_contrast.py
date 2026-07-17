#!/usr/bin/env python3
"""WCAG contrast checker for infographic-design.

Turns the skill's step-8 contrast rule from "eyeball it" into a hard check.
Stdlib only — no install needed.

Usage:
  # Check one foreground/background pair:
  python check_contrast.py "#1A2733" "#F7F9FC"

  # Extract every fill/stroke color from an SVG and check all pairs,
  # flagging any that fail. Point --bg at your canvas background:
  python check_contrast.py --svg diagram.svg --bg "#F7F9FC"

Thresholds (WCAG 2.1):
  4.5:1  normal text
  3.0:1  large text (>=24px, or >=19px bold) AND non-text graphics
         (bars, icons, lines, borders that carry meaning)

Note: --svg mode cannot tell a text color from a surface fill, so card/panel
background colors (whites, tints) will show as "FAIL" against the canvas —
that's expected noise, ignore it. The tool surfaces candidates; you decide
which are actually foreground. Purely decorative marks are exempt from 3:1.
"""
import re
import sys

TEXT = 4.5
LARGE = 3.0  # large text and meaningful graphics


def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexcolor):
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def verdict(r):
    return {
        "normal_text": "PASS" if r >= TEXT else "FAIL",
        "large_text_or_graphic": "PASS" if r >= LARGE else "FAIL",
    }


def _fmt(fg, bg):
    r = ratio(fg, bg)
    v = verdict(r)
    flag = "" if v["normal_text"] == "PASS" else ("  <- FAIL text" if v["large_text_or_graphic"] == "PASS" else "  <- FAIL both")
    return f"{fg} on {bg}: {r:5.2f}:1  text={v['normal_text']} large/graphic={v['large_text_or_graphic']}{flag}"


def extract_colors(svg_text):
    found = set()
    for m in re.finditer(r'(?:fill|stroke)\s*[:=]\s*["\']?(#[0-9A-Fa-f]{3,6})', svg_text):
        found.add(m.group(1).lower())
    # normalize 3-digit to 6-digit for de-dup
    norm = {}
    for c in found:
        h = c.lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        norm["#" + h] = True
    return sorted(norm)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--svg":
        path = argv[1]
        bg = None
        if "--bg" in argv:
            bg = argv[argv.index("--bg") + 1]
        with open(path) as f:
            colors = extract_colors(f.read())
        if not colors:
            print("No fill/stroke hex colors found.")
            return 1
        print(f"Colors found: {', '.join(colors)}\n")
        fails = 0
        if bg:
            print(f"Each color vs background {bg}:")
            for c in colors:
                if c == bg:
                    continue
                line = _fmt(c, bg)
                print("  " + line)
                if "FAIL" in line:
                    fails += 1
        else:
            print("All unique pairs (pass --bg to check against one background):")
            for i, a in enumerate(colors):
                for b in colors[i + 1:]:
                    line = _fmt(a, b)
                    if "FAIL" in line:
                        fails += 1
                    print("  " + line)
        print(f"\n{fails} pair(s) fail normal-text contrast." if fails else "\nAll checked pairs pass normal-text contrast.")
        return 1 if fails else 0
    # two-arg pair mode
    fg, bg = argv[0], argv[1]
    print(_fmt(fg, bg))
    return 0 if ratio(fg, bg) >= TEXT else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
