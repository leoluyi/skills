#!/usr/bin/env python3
"""Text-fit checker for infographic-design.

SVG <text> does not wrap — a line that is too long runs silently off its card
or off the canvas. This turns the skill's "budget the line length" rule from
guesswork into a measurement. Stdlib only.

Two modes:

  # A) Will this string fit in a box of a given inner width?
  python check_text_fit.py --text "server's public key. Only the server can open it." --size 13 --max 298

  # B) Scan an SVG: for every <text>, estimate width, find the rect it sits in,
  #     and flag any line that overflows its card (or the canvas).
  python check_text_fit.py --svg diagram.svg --pad 16

Width is estimated from embedded Helvetica advance widths (units/1000 em), a
good stand-in for any proportional sans (Inter, Segoe UI, Arial...). CJK/full-
width glyphs are counted as 1 em. Estimates run slightly generous so a PASS
has margin; still render-and-inspect. Mode B resolves nested translate()
transforms; groups with scale/rotate are reported as unchecked.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET

# Helvetica advance widths, units per 1000 em (AFM). Missing chars -> DEFAULT.
_W = {
    ' ': 278, '!': 278, '"': 355, '#': 556, '$': 556, '%': 889, '&': 667,
    "'": 191, '(': 333, ')': 333, '*': 389, '+': 584, ',': 278, '-': 333,
    '.': 278, '/': 278, '0': 556, '1': 556, '2': 556, '3': 556, '4': 556,
    '5': 556, '6': 556, '7': 556, '8': 556, '9': 556, ':': 278, ';': 278,
    '<': 584, '=': 584, '>': 584, '?': 556, '@': 1015, 'A': 667, 'B': 667,
    'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 722, 'I': 278,
    'J': 500, 'K': 667, 'L': 556, 'M': 833, 'N': 722, 'O': 778, 'P': 667,
    'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667, 'W': 944,
    'X': 667, 'Y': 667, 'Z': 611, '[': 278, '\\': 278, ']': 278, '^': 469,
    '_': 556, '`': 333, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556,
    'f': 278, 'g': 556, 'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222,
    'm': 833, 'n': 556, 'o': 556, 'p': 556, 'q': 556, 'r': 333, 's': 500,
    't': 278, 'u': 556, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 500,
    '{': 334, '|': 260, '}': 334, '~': 584,
}
DEFAULT = 556
BOLD_FACTOR = 1.06  # bold sets a touch wider


def text_width(s, size, bold=False):
    total = 0
    for ch in s:
        if ord(ch) >= 0x2E80:      # CJK / full-width
            total += 1000
        else:
            total += _W.get(ch, DEFAULT)
    w = total / 1000.0 * size
    return w * BOLD_FACTOR if bold else w


# ---------- Mode B: SVG scan ----------

def _strip_ns(tag):
    return tag.split('}', 1)[1] if '}' in tag else tag


def _parse_translate(transform):
    if not transform:
        return (0.0, 0.0), True
    simple = True
    tx = ty = 0.0
    for m in re.finditer(r'translate\(\s*([-\d.]+)[ ,]+([-\d.]+)?\s*\)', transform):
        tx += float(m.group(1))
        ty += float(m.group(2) or 0)
    if re.search(r'scale|rotate|matrix|skew', transform):
        simple = False
    return (tx, ty), simple


def _style_sizes(svg_text):
    """Map class name -> font-size(px) and whether it's bold, from <style>."""
    sizes, bolds = {}, {}
    style = ''.join(re.findall(r'<style.*?>(.*?)</style>', svg_text, re.S))
    for m in re.finditer(r'\.([A-Za-z0-9_-]+)\s*\{([^}]*)\}', style):
        cls, body = m.group(1), m.group(2)
        fs = re.search(r'font-size\s*:\s*([\d.]+)px', body)
        if fs:
            sizes[cls] = float(fs.group(1))
        fw = re.search(r'font-weight\s*:\s*(\d+)', body)
        bolds[cls] = bool(fw and int(fw.group(1)) >= 600)
    return sizes, bolds


def scan(path, pad):
    raw = open(path).read()
    cls_size, cls_bold = _style_sizes(raw)
    # default font-size from root
    root_fs = re.search(r'font-size="([\d.]+)', raw)
    default_size = float(root_fs.group(1)) if root_fs else 16.0

    tree = ET.parse(path)
    root = tree.getroot()
    vb = root.get('viewBox')
    canvas_w = float(vb.split()[2]) if vb else float(root.get('width', 0))

    rects = []   # (x, y, w, h)
    texts = []   # (x, y, size, bold, anchor, string, complex_flag)

    def walk(node, off, simple):
        (ox, oy) = off
        for child in node:
            (dx, dy), s2 = _parse_translate(child.get('transform'))
            coff = (ox + dx, oy + dy)
            csimple = simple and s2
            tag = _strip_ns(child.tag)
            if tag == 'rect':
                try:
                    rects.append((ox + dx + float(child.get('x', 0)),
                                  oy + dy + float(child.get('y', 0)),
                                  float(child.get('width', 0)),
                                  float(child.get('height', 0))))
                except ValueError:
                    pass
            elif tag == 'text':
                s = ''.join(child.itertext())
                x = float(child.get('x', 0)) + ox + dx
                y = float(child.get('y', 0)) + oy + dy
                cls = (child.get('class') or '').split()
                size = next((cls_size[c] for c in cls if c in cls_size), None)
                if size is None:
                    fs = child.get('font-size')
                    size = float(re.sub('px', '', fs)) if fs else default_size
                bold = any(cls_bold.get(c) for c in cls) or \
                    (child.get('font-weight', '') in ('bold', '700', '800'))
                anchor = child.get('text-anchor', 'start')
                texts.append((x, y, size, bold, anchor, s, csimple))
            walk(child, coff, csimple)

    walk(root, (0.0, 0.0), True)

    def enclosing(x, y):
        best = None
        for (rx, ry, rw, rh) in rects:
            if rx <= x <= rx + rw and ry <= y <= ry + rh:
                area = rw * rh
                if best is None or area < best[4]:
                    best = (rx, ry, rw, rh, area)
        return best

    fails, unchecked = [], 0
    for (x, y, size, bold, anchor, s, csimple) in texts:
        if not s.strip():
            continue
        w = text_width(s, size, bold)
        if anchor == 'middle':
            left, right = x - w / 2, x + w / 2
        elif anchor == 'end':
            left, right = x - w, x
        else:
            left, right = x, x + w
        box = enclosing(x, y)
        if not csimple:
            unchecked += 1
            continue
        if box:
            rx, ry, rw, rh, _ = box
            limit = rx + rw - pad
            if right > limit + 0.5:
                fails.append((s, round(right - limit, 1), 'card', round(size, 1)))
        else:
            if right > canvas_w - 2:
                fails.append((s, round(right - canvas_w, 1), 'canvas', round(size, 1)))
    return fails, unchecked, len(texts)


def main(argv):
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument('--text')
    ap.add_argument('--size', type=float, default=13)
    ap.add_argument('--max', type=float)
    ap.add_argument('--bold', action='store_true')
    ap.add_argument('--svg')
    ap.add_argument('--pad', type=float, default=16)
    if not argv:
        print(__doc__)
        return 2
    a = ap.parse_args(argv)

    if a.svg:
        fails, unchecked, n = scan(a.svg, a.pad)
        print(f"Scanned {n} <text> elements (pad={a.pad}px).")
        if unchecked:
            print(f"  {unchecked} skipped (scale/rotate transform — check by eye).")
        if fails:
            print(f"\n{len(fails)} line(s) OVERFLOW their box:")
            for s, over, kind, size in fails:
                disp = (s[:52] + '…') if len(s) > 53 else s
                print(f"  +{over:>5}px past {kind:6} @{size}px: \"{disp}\"")
            return 1
        print("No overflow detected. (Still render-and-inspect.)")
        return 0

    if a.text:
        w = text_width(a.text, a.size, a.bold)
        line = f'"{a.text[:48]}"  ->  {w:.0f}px at {a.size}px'
        if a.max is not None:
            ok = w <= a.max
            print(f'{line}  (box inner {a.max:.0f}px)  {"FITS" if ok else "OVERFLOWS by %.0fpx" % (w - a.max)}')
            return 0 if ok else 1
        print(line)
        # also report a safe char budget for this size/box
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
