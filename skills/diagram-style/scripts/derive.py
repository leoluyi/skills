#!/usr/bin/env python3
"""Derive a full token set from a theme's base hex values, and verify contrast.

Usage:
    python derive.py themes/signal-stages.md      # parse a theme file
    python derive.py --cat 2A78D6,1BAF7A,EDA100 --canvas FFFFFF --ink 12336E

Emits a ready-to-paste :root block plus a contrast report.
Exit code 1 if any text-carrying pair fails WCAG.
"""
import argparse
import colorsys
import re
import sys

# Lightness mix steps, as fractions of base over canvas.
# Warm hues (20-60 deg) get a bump; pale warm tints read lighter than they are.
STEPS = {
    "region":      0.04,
    "region-line": 0.16,
    "card":        0.10,
    "card-sub":    0.16,
}
# Offset and laser cannot hold a tint below roughly 8%: it either drops out
# entirely or breaks into visible mottling. Print themes need a raised floor,
# which compresses the ladder and costs some separation between steps.
PRINT_STEPS = {
    "region":      0.08,
    "region-line": 0.22,
    "card":        0.14,
    "card-sub":    0.22,
}
PRINT_GREY_GAP = 0.15   # photocopying is harsher than greyscale rendering
# The default ladder was tuned for muted palettes, where a 10% card tint is
# already visible. On a saturated source it erases the very thing that makes
# the palette recognisable: the colour survives only as a hairline border.
# Contrast has room — ink clears 7:1 even against a 45% tint — so vivid themes
# push the surfaces up rather than settling for a wash.
# A fixed mix proportion is not a fixed result. 38% of a very dark base lands
# at L=50 — a card heavy enough that dark text on it reads as reversed-out,
# even though the contrast ratio passes. Cards need a lightness floor so the
# ladder behaves the same whether the base is light or dark.
CARD_MIN_L = 0.78
VIVID_STEPS = {
    "region":      0.14,
    "region-line": 0.40,
    "card":        0.38,
    "card-sub":    0.50,
}
WARM_BUMP = 0.07
MIN_GREY_GAP = 0.10     # adjacent categories, relative luminance
HIGHLIGHT_HUE_GAP = 30  # below this, warn about surface/emphasis only
# A highlighter tints, it does not contrast. Real ones land near 1.1-1.3:1 on
# white paper; demanding 1.5 forces a chrome yellow that shouts over the text
# it is meant to mark. The safety requirement is the ink ON it, not the mark
# against the page.
HIGHLIGHT_MIN_CANVAS = 1.25
MAX_CATS_OUTLINE = 3    # falls out of MIN_GREY_GAP under the L<=30 border cap
SOFT_CAT_LIMIT = 5      # reader load, not physics — a warning, never a failure
LABEL_MIN_RATIO = 4.6   # region-label ink: it is TEXT, on its own region
LINE_MIN_RATIO = 3.2    # card border: a graphic object, WCAG asks 3:1
# A dark base already clears the border ratio, so the solver leaves it alone
# and `line` comes out identical to `base`. On the swatch sheet the two
# columns then read as one, and there is no visual cue that the border is a
# derived, deeper tone. Force a minimum separation so `base` is always the
# lighter of the pair.
LINE_MIN_DARKER = 0.82  # line luminance <= base luminance * this
# These were one value for a long time, which quietly held borders to the text
# threshold. A border is not text — solving it at 4.6 pushes a saturated amber
# down to a deep burnt orange that no longer looks like the colour it came
# from. Splitting them lets the border stay near its base while the label,
# which really is read as text, stays dark enough.


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb2hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, round(c))) for c in rgb))


def mix(base, canvas, p):
    """Mix base over canvas at proportion p. Works for light OR dark canvases."""
    return tuple(b * p + c * (1 - p) for b, c in zip(base, canvas))


def hue(rgb):
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        return 0.0
    if mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60


def is_warm(rgb):
    return 20 <= hue(rgb) <= 60


def luminance(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


WARM_SHIFT = 15.0       # degrees a yellow rotates toward orange when darkened


def solve_ink(rgb, backdrop, target_ratio):
    """Push base away from its backdrop until it clears target_ratio.

    Contrast-driven rather than luminance-target-driven: a fixed lightness
    target passes for blues and quietly fails for yellows, because equal
    lightness is not equal contrast across hues. Solving for the ratio
    directly means any hue lands on the legal side by construction.

    Works in HLS, not by scaling RGB toward black. Scaling drains chroma along
    with lightness, so an amber border comes out mud-brown — the border stops
    looking like it belongs to its category. Holding saturation keeps it amber.

    Yellows and yellow-greens also get a hue rotation toward orange as they
    darken, because a dark yellow simply IS brown colorimetrically; the shift
    is what makes it read as deep amber instead. This is not invented: Tailwind
    does the same thing, amber-400 (H43) to amber-700 (H28), and solving with
    a 15 degree shift reproduces amber-700 to within a hair.

    Direction depends on the backdrop. Darkening is right on a light page and
    actively wrong on a dark one — there it reduces contrast, and the solver
    walks the colour all the way to white-point while still failing.
    """
    r, g, b = (c / 255 for c in rgb)
    h0, start_l, sat0 = colorsys.rgb_to_hls(r, g, b)
    dark_bg = luminance(backdrop) < 0.18
    # Only genuinely saturated warms need the rescue. A muted clay darkened
    # with the same shift comes out terracotta, a louder colour than the theme
    # chose — the correction would break the character a low-saturation
    # palette exists for.
    warm = not dark_bg and 30 <= h0 * 360 <= 80 and sat0 >= 0.70

    def solve(h, sat):
        lo, hi = (start_l, 1.0) if dark_bg else (0.0, start_l)
        for _ in range(48):
            mid = (lo + hi) / 2
            cand = tuple(c * 255 for c in colorsys.hls_to_rgb(h, mid, sat))
            if contrast(cand, backdrop) >= target_ratio:
                if dark_bg:
                    hi = mid
                else:
                    lo = mid
            else:
                if dark_bg:
                    lo = mid
                else:
                    hi = mid
        return hi if dark_bg else lo

    h, sat = h0, sat0
    edge = solve(h, sat)
    if warm:
        # The rotation changes contrast, and how far to rotate depends on how
        # far the colour was pushed — which is what we are solving for.
        # Iterate: shift from the current depth, re-solve at that hue, repeat.
        # Applying the shift after a single solve silently invalidates the
        # contrast just solved for; that showed up as two themes failing by 0.1.
        for _ in range(3):
            drop = max(0.0, (start_l - edge) / start_l) if start_l else 0.0
            h = ((h0 * 360 - WARM_SHIFT * drop) % 360) / 360
            sat = min(sat0 * 1.05, 1.0)
            edge = solve(h, sat)
    return tuple(c * 255 for c in colorsys.hls_to_rgb(h, edge, sat))


def derive_cat(base_hex, canvas_hex, outline=False, for_print=False,
               vivid=False):
    """outline=True: surfaces stay unfilled, so every tint collapses to the
    canvas and the border becomes the only thing separating a card from the
    page. Contrast then has to be solved against the canvas, not against a
    tint that no longer exists — the shape layer's fill choice changes what
    the colour layer must solve against, so the two are not fully independent.
    """
    base, canvas = hex2rgb(base_hex), hex2rgb(canvas_hex)
    bump = WARM_BUMP if is_warm(base) else 0.0
    # vivid wins the ladder when both are set: it is strictly deeper than the
    # print floor, so ink coverage is satisfied either way.
    steps = VIVID_STEPS if vivid else (PRINT_STEPS if for_print else STEPS)
    if outline:
        out = {name: rgb2hex(canvas) for name in steps}
    else:
        out = {}
        for name, p in steps.items():
            pr = p + bump
            if name in ("card", "card-sub"):
                # Back the mix off until the surface clears the lightness
                # floor. Only the fillable surfaces need this; region is
                # already light and the border tone is solved separately.
                floor = CARD_MIN_L - (0.08 if name == "card-sub" else 0.0)
                while pr > 0.02 and luminance(mix(base, canvas, pr)) < floor:
                    pr -= 0.01
            out[name] = rgb2hex(mix(base, canvas, pr))
    out["base"] = rgb2hex(base)
    # One contrast-solved ink per category, used for every job that must stay
    # visible: region label, card border, accent bar, badge fill. Solving once
    # and reusing beats solving per job — and it frees the theme to pick a base
    # on hue alone, since the base itself never has to carry contrast.
    out["label"] = rgb2hex(solve_ink(base, hex2rgb(out["region"]), LABEL_MIN_RATIO))
    line = solve_ink(base, hex2rgb(out["card"]), LINE_MIN_RATIO)
    if luminance(line) > luminance(base) * LINE_MIN_DARKER:
        h_, l_, s_ = colorsys.rgb_to_hls(*[c / 255 for c in base])
        want = luminance(base) * LINE_MIN_DARKER
        lo, hi = 0.0, l_
        for _ in range(40):
            mid = (lo + hi) / 2
            if luminance(tuple(c * 255 for c in colorsys.hls_to_rgb(h_, mid, s_))) < want:
                lo = mid
            else:
                hi = mid
        line = tuple(c * 255 for c in colorsys.hls_to_rgb(h_, hi, s_))
    out["line"] = rgb2hex(line)
    # Badge text sits ON the line colour, so it cannot assume white. Choosing
    # between white and the canvas is not enough either: on a light theme the
    # canvas IS white, so both candidates collapse to the same colour and a
    # mid-tone line ends up with unreadable white text. Pick between white and
    # near-black, which always offers one legal side.
    line_rgb = hex2rgb(out["line"])
    dark = (17.0, 17.0, 17.0)
    out["badge-ink"] = rgb2hex((255, 255, 255)) if \
        contrast((255, 255, 255), line_rgb) >= contrast(dark, line_rgb) else rgb2hex(dark)
    out["_outline"] = outline
    out["_warm"] = bool(bump)
    return out


def _mode(text, key):
    m = re.search(r"^mode:\s*(.+)$", text, re.M)
    if m:
        return key in m.group(1).lower().split()
    return f"{key}: true" in text.lower()


def parse_theme(path):
    full = open(path, encoding="utf-8").read()
    text = full
    # Only the FIRST css block is the live theme. Files often carry a second
    # block for reference — original upstream values, a rejected variant — and
    # scanning the whole file silently merges them, producing twice as many
    # categories as the theme actually defines.
    blocks = re.findall(r"```css\n(.*?)```", text, re.S)
    if blocks:
        text = blocks[0]
    grab = lambda k: (re.search(rf"--{k}:\s*(#[0-9A-Fa-f]{{6}})", text) or [None, None])[1]
    cats = re.findall(r"--cat-\d+-base:\s*(#[0-9A-Fa-f]{6})", text)
    return {
        "cats": cats,
        "special": grab("cat-s-base"),
        "canvas": grab("canvas") or "#FFFFFF",
        "ink": grab("ink-strong") or "#111111",
        "terminal": grab("terminal"),
        "accent": grab("accent"),
        "highlight": grab("highlight"),
        # Read the mode flag from the WHOLE file: it lives outside the css
        # block, so scoping this to `text` silently loses it and the theme
        # renders filled when it should be outline-only.
        # Modes are declared on one explicit line so a theme never leaves the
        # reader guessing which ladder it is on. The older `key: true` form is
        # still read, since a theme that predates the line should not silently
        # lose its mode.
        "outline": _mode(full, "outline"),
        "print": _mode(full, "print"),
        "vivid": _mode(full, "vivid"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("theme", nargs="?")
    ap.add_argument("--cat", help="comma-separated base hexes")
    ap.add_argument("--canvas", default="#FFFFFF")
    ap.add_argument("--ink", default="#111111")
    ap.add_argument("--terminal")
    ap.add_argument("--accent")
    ap.add_argument("--highlight")
    ap.add_argument("--cat-s", help="special warning/issue base hex; excluded from category ordering")
    ap.add_argument("--outline", action="store_true",
                    help="unfilled surfaces; solve contrast against the canvas")
    ap.add_argument("--print", dest="for_print", action="store_true",
                    help="print-safe tint floor and a wider greyscale gap")
    ap.add_argument("--vivid", action="store_true",
                    help="heavier surface tints, for saturated source palettes")
    a = ap.parse_args()

    norm = lambda h: ("#" + h.lstrip("#").upper()) if h else h
    if a.theme:
        cfg = parse_theme(a.theme)
    else:
        if not a.cat:
            ap.error("give a theme file or --cat")
        cfg = {"cats": [norm(c.strip()) for c in a.cat.split(",")],
               "canvas": norm(a.canvas), "ink": norm(a.ink),
               "terminal": norm(a.terminal), "accent": norm(a.accent),
               "highlight": norm(a.highlight),
               "special": norm(a.cat_s),
               "outline": False, "print": False, "vivid": a.vivid}

    canvas, ink = cfg["canvas"], cfg["ink"]
    outline = a.outline or cfg.get("outline", False)
    for_print = a.for_print or cfg.get("print", False)
    vivid = a.vivid or cfg.get("vivid", False)
    # print and vivid compose. Every vivid step already sits above the print
    # floor (14>8, 38>14, 50>22, 40>22), so the vivid ladder satisfies ink
    # coverage on its own; print's other two rules — pure white canvas and the
    # wider greyscale gap — are independent of tint depth. They were wrongly
    # rejected as exclusive.
    derived = [derive_cat(c, canvas, outline, for_print, vivid) for c in cfg["cats"]]
    special = derive_cat(cfg["special"], canvas, outline, for_print, vivid) \
        if cfg.get("special") else None
    global MIN_GREY_GAP
    MIN_GREY_GAP = PRINT_GREY_GAP if for_print else 0.10
    # Only outline mode has a hard ceiling, and it is derived: the border must
    # clear 3:1 against the canvas, which caps lightness near L=30, and 10%
    # spacing over 0-30 fits three categories. Filled mode has no such bound —
    # `line` is solved for contrast, so an arbitrarily light base still yields
    # a readable border. There the greyscale gap check is the only real gate.

    print(":root{")
    print(f"  --canvas:{canvas.upper()}; --ink-strong:{ink.upper()};")
    for i, d in enumerate(derived, 1):
        print(f"  --cat-{i}-base:{d['base']}; --cat-{i}-card:{d['card']}; "
              f"--cat-{i}-card-sub:{d['card-sub']};")
        print(f"  --cat-{i}-region:{d['region']}; --cat-{i}-region-line:{d['region-line']}; "
              f"--cat-{i}-label:{d['label']};")
    if special:
        print(f"  --cat-s-base:{special['base']}; --cat-s-card:{special['card']}; "
              f"--cat-s-card-sub:{special['card-sub']};")
        print(f"  --cat-s-region:{special['region']}; --cat-s-region-line:{special['region-line']}; "
              f"--cat-s-label:{special['label']};")
    if cfg.get("terminal"):
        print(f"  --terminal:{cfg['terminal'].upper()};")
    if cfg.get("accent"):
        print(f"  --accent:{cfg['accent'].upper()};")
    if cfg.get("highlight"):
        print(f"  --highlight:{cfg['highlight'].upper()};")
    print("}")

    print("\n| pair | ratio | verdict |")
    print("|---|---|---|")
    fails = 0
    for i, d in enumerate(derived, 1):
        for surface in ("card", "region"):
            r = contrast(hex2rgb(ink), hex2rgb(d[surface]))
            ok = r >= 4.5
            fails += not ok
            print(f"| ink on cat-{i}-{surface} | {r:.1f}:1 | {'PASS' if ok else 'FAIL body text'} |")
        r = contrast(hex2rgb(d["line"]), hex2rgb(d["card"]))
        ok = r >= 3.0
        fails += not ok
        print(f"| cat-{i}-line on card (border) | {r:.1f}:1 | "
              f"{'PASS' if ok else 'FAIL graphic contrast'} |")
        bi = d["badge-ink"]
        r = contrast(hex2rgb(bi), hex2rgb(d["line"]))
        ok = r >= 4.5
        fails += not ok
        lbl = "white" if bi == "#FFFFFF" else "dark"
        print(f"| {lbl} on cat-{i}-line (badge) | {r:.1f}:1 | {'PASS' if ok else 'FAIL'} |")
        r = contrast(hex2rgb(d["label"]), hex2rgb(d["region"]))
        ok = r >= 4.5
        fails += not ok
        print(f"| cat-{i}-label on region | {r:.1f}:1 | {'PASS' if ok else 'FAIL'} |")
    if special:
        for surface in ("card", "region"):
            r = contrast(hex2rgb(ink), hex2rgb(special[surface]))
            ok = r >= 4.5
            fails += not ok
            print(f"| ink on cat-s-{surface} | {r:.1f}:1 | {'PASS' if ok else 'FAIL body text'} |")
        r = contrast(hex2rgb(special["line"]), hex2rgb(special["card"]))
        ok = r >= 3.0
        fails += not ok
        print(f"| cat-s-line on card (border) | {r:.1f}:1 | {'PASS' if ok else 'FAIL graphic contrast'} |")
        r = contrast(hex2rgb(special["badge-ink"]), hex2rgb(special["line"]))
        ok = r >= 4.5
        fails += not ok
        lbl = "white" if special["badge-ink"] == "#FFFFFF" else "dark"
        print(f"| {lbl} on cat-s-line (badge) | {r:.1f}:1 | {'PASS' if ok else 'FAIL'} |")
        r = contrast(hex2rgb(special["label"]), hex2rgb(special["region"]))
        ok = r >= 4.5
        fails += not ok
        print(f"| cat-s-label on region | {r:.1f}:1 | {'PASS' if ok else 'FAIL'} |")
    if cfg.get("highlight"):
        hl = hex2rgb(cfg["highlight"])
        r = contrast(hex2rgb(ink), hl)
        fails += r < 4.5
        print(f"| ink on highlight | {r:.1f}:1 | {'PASS' if r >= 4.5 else 'FAIL body text'} |")
        # Deliberately far below the 3:1 asked of graphical objects, and below
        # the 1.5 this once used. A highlighter is emphasis, not structure —
        # if it disappears the text still reads.
        r = contrast(hl, hex2rgb(canvas))
        fails += r < HIGHLIGHT_MIN_CANVAS
        print(f"| highlight on canvas | {r:.2f}:1 | "
              f"{'PASS' if r >= HIGHLIGHT_MIN_CANVAS else 'FAIL — invisible against the page'} |")
        # A highlight near a category's hue is only a real hazard for
        # surface/emphasis — the offset block behind a card, which sits on the
        # same kind of surface a category owns. The underline form is a 0.4em
        # strip under text: different geometry, no confusion, and yellow is
        # what a highlighter is. So this reports, it does not block.
        hh = hue(hl)

        def hue_gap(other):
            x = abs(hh - hue(hex2rgb(other)))
            return min(x, 360 - x)

        gap, nearest = min((hue_gap(d["base"]), d["base"]) for d in derived)
        if gap < HIGHLIGHT_HUE_GAP:
            print(f"note: highlight is {gap:.0f}° from {nearest}. Fine as a text "
                  "underline; avoid surface/emphasis on that category, where the "
                  "offset block would read as the category itself.")
    if for_print and canvas.upper() != "#FFFFFF":
        fails += 1
        print(f"FAIL: print theme on canvas {canvas} — use #FFFFFF. Printing a "
              "near-white background wastes ink and leaves a visible box edge "
              "where the graphic meets the page.")
    if cfg.get("terminal"):
        term = hex2rgb(cfg["terminal"])
        ti = (255, 255, 255) if contrast((255, 255, 255), term) >= \
            contrast((17.0, 17.0, 17.0), term) else (17.0, 17.0, 17.0)
        r = contrast(ti, term)
        fails += r < 4.5
        lbl = "white" if ti == (255, 255, 255) else "dark"
        print(f"| {lbl} on terminal | {r:.1f}:1 | {'PASS' if r >= 4.5 else 'FAIL'} |")

    # Greyscale separability: categories must survive a mono print.
    # This is a hard gate, not advice. Colour that collapses under photocopying
    # was never carrying the distinction in the first place.
    print("\ngreyscale L: " + "  ".join(
        f"cat-{i}={luminance(hex2rgb(d['base']))*100:.0f}%" for i, d in enumerate(derived, 1)))
    raw = [luminance(hex2rgb(d["base"])) for d in derived]
    if len(raw) > 1:
        mono = all(b > a_ for a_, b in zip(raw, raw[1:]))
        # Not a failure: unordered categories (lanes, actors, layers) have no
        # reading order to agree with. It IS a failure for ordered ones, and
        # nothing else surfaces it, so say which way round this theme sits.
        print("category lightness: "
              + ("ascending — safe for ordered stages" if mono else
                 "NOT ascending — fine for lanes/actors, but for ordered stages "
                 "the shading will run against the reading order"))
    ls = sorted(raw)
    gaps = [b - a_ for a_, b in zip(ls, ls[1:])]
    if gaps and min(gaps) < MIN_GREY_GAP:
        fails += 1
        print(f"FAIL: two categories within {MIN_GREY_GAP:.0%} luminance — "
              "indistinguishable in greyscale. Spread the lightness ladder.")
    if outline and len(derived) > MAX_CATS_OUTLINE:
        fails += 1
        print(f"FAIL: {len(derived)} categories in outline mode, ceiling is "
              f"{MAX_CATS_OUTLINE} — borders must clear 3:1 against the canvas, "
              f"which caps lightness near L=30, and {MIN_GREY_GAP:.0%} spacing "
              "fits no more below that. Group them, or fill the surfaces.")
    elif len(derived) > SOFT_CAT_LIMIT:
        print(f"note: {len(derived)} categories. The ladder holds, but readers "
              f"lose track past about {SOFT_CAT_LIMIT} — check that every one of "
              "them is a distinction the reader actually needs to make.")

    warm = [i for i, d in enumerate(derived, 1) if d["_warm"]]
    if warm:
        print(f"note: warm bump (+{WARM_BUMP:.0%}) applied to cat-{', cat-'.join(map(str, warm))}")

    if fails:
        print(f"\n{fails} contrast failure(s).")
        return 1
    print("\nall text-carrying pairs pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
