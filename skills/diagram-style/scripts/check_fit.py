#!/usr/bin/env python3
"""Check an SVG's text against role minimums and container overflow.

    python check_fit.py out.svg --roles cd=body,sb=support,h1=title

Font size is checked as a fraction of the canvas WIDTH, because an SVG scales
to its container: displayed size is container_width / canvas_width * font_size.
An absolute px value says nothing on its own — 14px is fine on an 800-wide
canvas and half-legible on a 1600-wide one.

Exit 1 if any text is below its role minimum or overflows its container.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"

# Fraction of canvas width. Calibrated against two very different display
# contexts that happen to agree: a 6.5in document figure at 9pt minimum body,
# and a 13.3in slide at 18pt minimum projected body — both land near 1.9%.
MIN_RATIO = {
    "title":   0.035,
    "section": 0.024,
    "body":    0.020,
    "support": 0.016,
    "caption": 0.014,
    "kicker":  0.014,
}
FALLBACK = "caption"   # loosest line, used for unmapped classes


def text_width(s, size):
    """CJK glyphs ~1.0em, latin/digits ~0.55em."""
    return sum(size * (1.0 if ord(c) > 0x2E80 else 0.55) for c in s)


def css_anchor(raw, cls):
    m = re.search(r"text-anchor:\s*(\w+)", raw.get(cls, ""))
    return m.group(1) if m else None


def css_sizes(root):
    """font-size per class from the <style> block."""
    out, raw = {}, {}
    for st in root.iter(NS + "style"):
        for m in re.finditer(r"\.([\w-]+)\s*\{([^}]*)\}", st.text or ""):
            cls, body = m.group(1), m.group(2)
            raw[cls] = body
            fs = re.search(r"font-size:\s*([\d.]+)", body)
            if fs:
                out[cls] = float(fs.group(1))
    return out, raw


def parse_viewbox(root):
    vb = root.get("viewBox")
    if not vb:
        return None, None
    p = [float(x) for x in vb.replace(",", " ").split()]
    return p[2], p[3]


def rects(root):
    """Every rect as (x, y, w, h), resolving nested translate()."""
    out = []

    def walk(node, dx, dy):
        t = node.get("transform", "")
        m = re.search(r"translate\(\s*([-\d.]+)[ ,]+([-\d.]+)", t)
        if m:
            dx, dy = dx + float(m.group(1)), dy + float(m.group(2))
        # Decorative fills — highlighter underlines, offset shadows — are not
        # containers. Treating them as one reports a phantom overflow on every
        # highlighted label. aria-hidden is the right marker anyway: screen
        # readers should skip them too.
        if node.get("aria-hidden") == "true":
            return
        if node.tag == NS + "rect":
            try:
                out.append((float(node.get("x", 0)) + dx, float(node.get("y", 0)) + dy,
                            float(node.get("width", 0)), float(node.get("height", 0))))
            except (TypeError, ValueError):
                pass
        for c in node:
            walk(c, dx, dy)

    walk(root, 0.0, 0.0)
    return out


def container_of(tx, ty, boxes, canvas_w):
    """Smallest rect containing the point, ignoring full-canvas backdrops."""
    best = None
    for x, y, w, h in boxes:
        if w >= canvas_w * 0.95:      # page background, not a card
            continue
        # Baseline must sit inside the box vertically. A loose test here
        # matches backdrops the text merely sits above, which reads as a
        # phantom overflow on every section heading.
        if x <= tx <= x + w and y <= ty <= y + h:
            if best is None or w * h < best[2] * best[3]:
                best = (x, y, w, h)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg")
    ap.add_argument("--roles", default="", help="cls=role,cls=role")
    ap.add_argument("--pad", type=float, default=24.0, help="card inner padding")
    a = ap.parse_args()

    role_of = {}
    for pair in filter(None, a.roles.split(",")):
        cls, _, role = pair.partition("=")
        if role not in MIN_RATIO:
            sys.exit(f"unknown role '{role}'. known: {', '.join(MIN_RATIO)}")
        role_of[cls.strip()] = role

    root = ET.parse(a.svg).getroot()
    W, H = parse_viewbox(root)
    if not W:
        sys.exit("no viewBox — cannot judge size without a canvas reference")
    sizes, sizes_raw = css_sizes(root)
    boxes = rects(root)

    fails, checked, unmapped = [], 0, set()
    largest = 0.0

    for t in root.iter(NS + "text"):
        content = "".join(t.itertext()).strip()
        if not content:
            continue
        cls = (t.get("class") or "").split()[0] if t.get("class") else ""
        size = None
        if t.get("font-size"):
            size = float(re.sub(r"[^\d.]", "", t.get("font-size")))
        elif cls in sizes:
            size = sizes[cls]
        if size is None:
            continue
        checked += 1
        largest = max(largest, size)

        role = role_of.get(cls)
        if role is None:
            role = FALLBACK
            if cls:
                unmapped.add(cls)
        need = MIN_RATIO[role] * W
        if size < need - 0.01:
            fails.append(f"  {size:.0f}px  {size/W*100:.2f}% of width  "
                         f"< {role} min {need:.0f}px ({MIN_RATIO[role]*100:.1f}%)  "
                         f"— \u201c{content[:22]}\u201d")

        # overflow against the smallest containing rect
        try:
            tx, ty = float(t.get("x", 0)), float(t.get("y", 0))
        except (TypeError, ValueError):
            continue
        w = text_width(content, size)
        box = container_of(tx, ty, boxes, W)
        if box is None:
            # No card contains it — headings, captions, floating labels. These
            # still have to stay inside the canvas, and nothing else checks
            # that, so text can silently run off the right edge and "pass".
            anchor = t.get("text-anchor") or css_anchor(sizes_raw, cls) or "start"
            lo = tx - w / 2 if anchor == "middle" else (tx - w if anchor == "end" else tx)
            if lo < -0.5 or lo + w > W + 0.5:
                over = max(-lo, lo + w - W)
                fails.append(f"  runs off the canvas by {over:.0f}px  "
                             f"text {w:.0f}, canvas {W:.0f}  — \u201c{content[:22]}\u201d")
            continue
        if box:
            anchor = (t.get("text-anchor")
                      or css_anchor(sizes_raw, cls) or "start")  # noqa: E501
            if anchor == "middle":
                lo, hi = tx - w / 2, tx + w / 2
            elif anchor == "end":
                lo, hi = tx - w, tx
            else:
                lo, hi = tx, tx + w
            bl, br = box[0] + a.pad, box[0] + box[2] - a.pad
            if lo < bl - 0.5 or hi > br + 0.5:
                over = max(bl - lo, hi - br)
                fails.append(f"  overflow by {over:.0f}px  box {box[2]:.0f} wide, "
                             f"text {w:.0f}  — \u201c{content[:22]}\u201d")

    # Shapes have to fit too. Checking only text passes a card that has run
    # clean off the edge, because its label is still inside its own box.
    for x, y, w, h in boxes:
        if w >= W * 0.95 and x <= 0:
            continue                      # page backdrop
        if x < -0.5 or x + w > W + 0.5 or y < -0.5 or y + h > H + 0.5:
            over = max(-x, x + w - W, -y, y + h - H)
            fails.append(f"  shape runs off the canvas by {over:.0f}px  "
                         f"box {w:.0f}x{h:.0f} at ({x:.0f},{y:.0f}), canvas {W:.0f}x{H:.0f}")

    print(f"canvas {W:.0f}x{H:.0f}, {checked} text elements checked, "
          f"{len(boxes)} shapes")
    if unmapped:
        print(f"unmapped classes checked at the '{FALLBACK}' floor: "
              f"{', '.join(sorted(unmapped))}")
    if largest and largest < MIN_RATIO["title"] * W:
        print(f"note: largest text is {largest:.0f}px ({largest/W*100:.2f}%), below the "
              f"title floor {MIN_RATIO['title']*W:.0f}px — the graphic may have no L1 "
              "headline, so it cannot explain itself when reposted alone.")
    if fails:
        print(f"\n{len(fails)} problem(s):")
        print("\n".join(fails))
        print("\nFix by widening boxes, wrapping labels, or narrowing the canvas — "
              "never by shortening text.")
        return 1
    print("all text clears its role minimum and fits its container.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
