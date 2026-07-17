#!/usr/bin/env python3
"""Quality gate for infographic-design — one command, pass/fail verdict.

Runs every deterministic check on a produced SVG and exits non-zero if any
HARD gate fails, so it can sit in front of "deliver". Stdlib only; reuses the
sibling scripts.

  python check.py out.svg --bg "#F7F9FC" --pad 16

HARD gates (fail -> exit 1, do not deliver):
  - text-fit     no <text> line overflows its card or the canvas
  - contrast     every TEXT colour meets WCAG 4.5:1 (>=24px: 3:1) vs its
                 actual background (nearest enclosing rect, else canvas)
  - font-family  named on the root <svg> (unnamed fonts break on export)
  - no-emoji     no emoji glyphs in text (render inconsistently; use icons)

SOFT gates (warn only -> still exit 0):
  - restyle      palette via :root var()/classes, semantic <g id=...> groups
                 (required only when the user wants to rebrand later)

Precise contrast: unlike check_contrast.py --svg (which lists every colour and
can't tell text from surface), this resolves each <text>'s own colour and its
real background, so a pass/fail is trustworthy.
"""
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_text_fit import scan as textfit_scan, text_width  # noqa: E402
from check_contrast import ratio  # noqa: E402

EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF]"      # pictographs, symbols, supplemental
    "|[\U00002600-\U000026FF]"     # miscellaneous symbols (emoji-like)
    "|[\U00002700-\U000027BF]"     # dingbats
    "|\uFE0F"                      # emoji variation selector
)
# Note: typographic arrows (U+2190-21FF), math and punctuation are NOT emoji.


def _strip_ns(t):
    return t.split('}', 1)[1] if '}' in t else t


def _style_map(raw):
    fills, sizes, bolds = {}, {}, {}
    style = ''.join(re.findall(r'<style.*?>(.*?)</style>', raw, re.S))
    for m in re.finditer(r'\.([A-Za-z0-9_-]+)\s*\{([^}]*)\}', style):
        cls, body = m.group(1), m.group(2)
        f = re.search(r'fill\s*:\s*(#[0-9A-Fa-f]{3,6})', body)
        if f:
            fills[cls] = f.group(1)
        s = re.search(r'font-size\s*:\s*([\d.]+)px', body)
        if s:
            sizes[cls] = float(s.group(1))
        w = re.search(r'font-weight\s*:\s*(\d+)', body)
        bolds[cls] = bool(w and int(w.group(1)) >= 600)
    return fills, sizes, bolds


def _resolve_translate(t):
    tx = ty = 0.0
    if t:
        for m in re.finditer(r'translate\(\s*([-\d.]+)[ ,]+([-\d.]+)?\s*\)', t):
            tx += float(m.group(1)); ty += float(m.group(2) or 0)
    return tx, ty


def contrast_gate(path, bg):
    raw = open(path).read()
    cls_fill, cls_size, cls_bold = _style_map(raw)
    root_fill = re.search(r'<svg[^>]*\bfill="(#[0-9A-Fa-f]{3,6})"', raw)
    default_fill = root_fill.group(1) if root_fill else '#000000'
    tree = ET.parse(path); root = tree.getroot()

    # collect filled shapes (rect/circle/ellipse) for background resolution
    rects = []

    def gather(node, off):
        ox, oy = off
        for c in node:
            dx, dy = _resolve_translate(c.get('transform'))
            coff = (ox + dx, oy + dy)
            tag = _strip_ns(c.tag)
            fill = c.get('fill')
            if not fill:
                for cl in (c.get('class') or '').split():
                    if cl in cls_fill:
                        fill = cls_fill[cl]
            try:
                if tag == 'rect':
                    rects.append((ox + dx + float(c.get('x', 0)),
                                  oy + dy + float(c.get('y', 0)),
                                  float(c.get('width', 0)),
                                  float(c.get('height', 0)), fill))
                elif tag == 'circle':
                    cx = ox + dx + float(c.get('cx', 0)); cy = oy + dy + float(c.get('cy', 0))
                    r = float(c.get('r', 0))
                    rects.append((cx - r, cy - r, 2 * r, 2 * r, fill))
                elif tag == 'ellipse':
                    cx = ox + dx + float(c.get('cx', 0)); cy = oy + dy + float(c.get('cy', 0))
                    rx = float(c.get('rx', 0)); ry = float(c.get('ry', 0))
                    rects.append((cx - rx, cy - ry, 2 * rx, 2 * ry, fill))
            except ValueError:
                pass
            gather(c, coff)
    gather(root, (0.0, 0.0))

    def bg_at(x, y):
        best = None
        for (rx, ry, rw, rh, f) in rects:
            if f and rx <= x <= rx + rw and ry <= y <= ry + rh:
                a = rw * rh
                if best is None or a < best[1]:
                    best = (f, a)
        return best[0] if best else bg

    fails = []

    def check_text(node, off):
        ox, oy = off
        for c in node:
            dx, dy = _resolve_translate(c.get('transform'))
            coff = (ox + dx, oy + dy)
            if _strip_ns(c.tag) == 'text':
                s = ''.join(c.itertext()).strip()
                if s:
                    classes = (c.get('class') or '').split()
                    fill = c.get('fill') or next((cls_fill[cl] for cl in classes if cl in cls_fill), default_fill)
                    size = next((cls_size[cl] for cl in classes if cl in cls_size), None)
                    if size is None:
                        fs = c.get('font-size'); size = float(re.sub('px', '', fs)) if fs else 16.0
                    bold = any(cls_bold.get(cl) for cl in classes) or \
                        (c.get('font-weight', '') in ('bold', '600', '700', '800'))
                    x = float(c.get('x', 0)) + ox + dx
                    y = float(c.get('y', 0)) + oy + dy
                    if fill.startswith('#'):
                        r = ratio(fill, bg_at(x, y))
                        # WCAG large text = >=24px, or >=18.66px bold; we treat
                        # bold >=16px as large (3:1), else 4.5:1.
                        large = size >= 24 or (bold and size >= 16)
                        thresh = 3.0 if large else 4.5
                        if r < thresh:
                            fails.append((s[:40], fill, round(r, 2), thresh))
            check_text(c, coff)
    check_text(root, (0.0, 0.0))
    return fails


def structure_gate(path):
    raw = open(path).read()
    warns = []
    if 'var(--' not in raw:
        warns.append("no :root var() colours — a rebrand means hunting inline hexes")
    if not re.search(r'<g[^>]*\bid=', raw):
        warns.append("no semantic <g id=...> groups — later edits are hard to locate")
    return warns


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('svg', nargs='?')
    ap.add_argument('--bg', default='#FFFFFF')
    ap.add_argument('--pad', type=float, default=16)
    if not argv:
        print(__doc__); return 2
    a = ap.parse_args(argv)
    if not a.svg:
        print(__doc__); return 2

    raw = open(a.svg).read()
    hard_fail = False
    print(f"Quality gate: {a.svg}  (bg={a.bg}, pad={a.pad})\n")

    # 1. text-fit
    fits, unchecked, n = textfit_scan(a.svg, a.pad)
    if fits:
        hard_fail = True
        print(f"[FAIL] text-fit: {len(fits)} line(s) overflow")
        for s, over, kind, size in fits:
            print(f"         +{over}px past {kind}: \"{s[:48]}\"")
    else:
        print(f"[PASS] text-fit: {n} text elements, none overflow"
              + (f" ({unchecked} unchecked: complex transform)" if unchecked else ""))

    # 2. contrast (text only, vs real bg)
    cfails = contrast_gate(a.svg, a.bg)
    if cfails:
        hard_fail = True
        print(f"[FAIL] contrast: {len(cfails)} text colour(s) below WCAG")
        for s, fill, r, th in cfails:
            print(f"         {fill} = {r}:1 (need {th}:1): \"{s}\"")
    else:
        print("[PASS] contrast: all text meets WCAG")

    # 3. font-family named
    if re.search(r'font-family', raw):
        print("[PASS] font-family: named")
    else:
        hard_fail = True
        print("[FAIL] font-family: none named — will break on PNG/PDF export")

    # 4. no emoji
    texts = ''.join(re.findall(r'<text[^>]*>(.*?)</text>', raw, re.S))
    if EMOJI.search(texts):
        hard_fail = True
        print("[FAIL] no-emoji: emoji found in text — use inline vector icons")
    else:
        print("[PASS] no-emoji: none in text")

    # 5. restyle structure (soft)
    warns = structure_gate(a.svg)
    if warns:
        print("[WARN] restyle-structure:")
        for w in warns:
            print(f"         - {w}")
    else:
        print("[PASS] restyle-structure: :root vars + semantic groups")

    print()
    if hard_fail:
        print("GATE: FAIL — fix hard failures before delivering.")
        return 1
    print("GATE: PASS" + ("  (with restyle warnings)" if warns else ""))
    print(
        "\nDeterministic checks pass. Before delivering, also self-attest the\n"
        "JUDGMENT guard (not auto-checkable — answer honestly, fix if 'no'):\n"
        "  [ ] One message: a first viewer can state the single takeaway in ~8s?\n"
        "  [ ] Hierarchy: exactly one L1 element dominates (squint test)?\n"
        "  [ ] Charts honest: zero-baseline bars, no 3-D/dual-axis, title states the finding?\n"
        "  [ ] Nothing encoded by colour alone?\n"
        "  [ ] Data source credited (small, L3)?\n"
        "Deliver only when the gate is PASS AND every judgment box is checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
