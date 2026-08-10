#!/usr/bin/env python3
"""Render the style reference sheet — roles, shapes, states, colours.

    python scripts/render_reference.py               # -> docs/style-reference.html
    python scripts/render_reference.py -o /tmp/x.html

Output lands in docs/, not references/ or assets/: it is human documentation,
not something Claude should read. Every number on it comes from the reference
files, so reading the generated HTML only spends context re-deriving what is
already stated in prose.

Everything is read from themes/*.md and derived through derive.py, so the
sheet cannot drift from the values in use. Re-run it whenever a theme changes
— a stale swatch sheet is worse than none, because it looks authoritative.

HTML rather than an image, for three reasons that matter here: hex values are
click-to-copy, which is most of what anyone opens a swatch sheet to do; CJK
renders in the reader's own fonts rather than depending on what the export
machine had installed; and the greyscale toggle can actually be toggled.

That last one is why shapes and states live on this page too rather than in a
separate picture. Both layers make the same promise — every distinction must
survive a mono photocopy — and one shared toggle tests all of them at once.
Two sheets would also drift apart the moment one is regenerated and the other
is not.
"""
import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from derive import parse_theme, derive_cat, hex2rgb, luminance, contrast  # noqa: E402

# Role, column heading, and what the role MEANS. The meaning column is the
# reason this sheet exists: a swatch grid without it is just colours.
ROLES = [
    ("region",    "區域底",      "一個範圍：階段、泳道、層"),
    ("card",      "卡片底",      "一個東西：元件、動作、角色"),
    ("card-sub",  "子卡片",      "巢狀子物件，從屬於某卡片"),
    ("line",      "邊框／色條",  "解過對比，也用於徽章底與圖示"),
    ("base",      "主題輸入值",  "只定色相，不直接畫任何東西"),
]
# Frame chrome comes from one theme so the sheet itself has a house style;
# each row still paints its own canvas, because the tints are canvas-relative
# and lining them all up on white would misrepresent every one of them.
FRAME = "muted-ledger"
MIN = dict(title=.035, section=.024, body=.020, support=.016, caption=.014)
W = 1160
L, SWW, GAP, CH, PAD = 32, 96, 10, 40, 14


def tw(s, z):
    return sum(z * (1.0 if ord(c) > 0x2E80 else 0.55) for c in s)


def snap(v):
    return int(-(-v // 8) * 8)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def ink_on(bg_hex):
    """Label colour for a swatch, solved against that swatch's own fill.

    Reusing one ink across swatches is the bug this guards: a colour solved
    against the border tone is unreadable on the base tone beside it.
    """
    bg = hex2rgb(bg_hex)
    return "#FFFFFF" if contrast((255, 255, 255), bg) >= contrast((17, 17, 17), bg) else "#111111"


def purpose(path):
    """Pull the one-line '適用' summary out of a theme file."""
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"\*\*適用\*\*：(.+)", txt)
    if not m:
        return ""
    # Whole clauses only. A hard character cap slices mid-word and the sheet
    # ends up quoting half a sentence as if it were the summary.
    # Theme files are markdown; the summary line is rendered as plain text
    # here, so emphasis markers have to come off or they show up literally.
    raw = re.sub(r"\*\*(.+?)\*\*", r"\1", m.group(1))
    parts = re.split(r"[。\n]", raw)[0].split("、")
    out, width = [], 0.0
    for seg in parts:
        w = tw(seg, 1.0)
        if out and width + w > 15:
            break
        out.append(seg)
        width += w + 1
    return "、".join(out)


def themes():
    d = os.path.join(ROOT, "themes")
    out = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        p = os.path.join(d, f)
        t = parse_theme(p)
        mode = " ".join(k for k in ("outline", "print", "vivid")
                        if t.get(k)) or "standard"
        out.append((f[:-3], purpose(p), mode, t))
    return out




# Shape profiles live in pens/*.md as yaml-ish blocks; parse the few keys the
# sheet needs rather than pulling in a yaml dependency for six lines.
SHAPE_KEYS = ("rx", "fill", "stroke-width", "depth", "density", "arrow")
DENSITY = {"tight": (40, 24, 32), "normal": (48, 48, 40), "loose": (56, 56, 48)}
LINES = [("line/flow", "主資料流、執行順序", "solid"),
         ("line/control", "控制流、非同步、回饋", "dash"),
         ("line/reference", "邏輯關聯、參照", "long"),
         ("line/optional", "條件性連線", "dashdot"),
         ("line/leader", "註解引線（非機制）", "dot")]
STATES = [("一般", "實線框", "normal"),
          ("surface/external", "界外系統", "external"),
          ("state/planned", "尚未建置", "planned"),
          ("state/deprecated", "退場中", "deprecated")]


def dashes(sw):
    """Dash lengths scale with stroke width.

    A `6 4` pattern reads as dashed on a 1.5px line and as chunky on a 2.5px
    one — the gaps have to grow with the stroke or the rhythm disappears. The
    documented arrays (6 4 / 10 5 / 2 3) fall out of this at sw=1.5, which is
    console's width: those numbers were always console-calibrated, just not
    labelled as such.
    """
    r = lambda k: round(k * sw)
    return {"solid": "none",
            "dash": f"{r(4)} {r(2.7)}",
            "long": f"{r(6.7)} {r(3.3)}",
            "dashdot": f"{r(5.3)} {r(2)} {r(1.3)} {r(2)}",
            "dot": f"{r(1.3)} {r(2)}"}


def hatch_gap(density):
    """Texture spacing tracks card height, so the weave looks the same density
    relative to the box rather than absolutely."""
    return round(DENSITY[density][0] / 8)


def pens():
    d = os.path.join(ROOT, "pens")
    out = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".md"):
            continue
        txt = open(os.path.join(d, f), encoding="utf-8").read()
        blk = re.search(r"```yaml\n(.*?)```", txt, re.S)
        cfg = {}
        if blk:
            for line in blk.group(1).splitlines():
                k, _, v = line.partition(":")
                if k.strip() in SHAPE_KEYS:
                    cfg[k.strip()] = v.split("#")[0].strip()
        m = re.search(r"^# \S+ — (.+)$", txt, re.M)
        cfg["label"] = m.group(1).strip() if m else f[:-3]
        m = re.search(r"\*\*適合\*\*：(.+)", txt)
        cfg["fit"] = re.split(r"[。\n]", m.group(1))[0][:30] if m else ""
        out.append((f[:-3], cfg))
    return out


CSS = """
:root{--pg:#F2F3F5;--ink:#1B2430;--dim:#606B7A;--rule:#D9DEE5;--mono:ui-monospace,
"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;padding:0 0 72px;background:var(--pg);color:var(--ink);
font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;
font-size:15px;line-height:1.6}
.wrap{max-width:1100px;margin:0 auto;padding:26px 28px 0}
h1{font-size:30px;font-weight:700;letter-spacing:-.01em;margin:0 0 4px}
.lede{color:var(--dim);margin:0 0 26px;font-size:14px}
h2{font-size:15px;font-weight:700;margin:36px 0 12px;padding-bottom:7px;
border-bottom:1px solid var(--rule);letter-spacing:.04em;scroll-margin-top:64px}
h2 small{font-weight:400;color:var(--dim);letter-spacing:0;margin-left:8px}
table{border-collapse:collapse;width:100%;font-size:14px}
td{padding:7px 12px 7px 0;vertical-align:top;border-bottom:1px solid var(--rule)}
td.k{font-weight:700;white-space:nowrap;width:150px}
td.d{color:var(--dim)}
code{font-family:var(--mono);font-size:12.5px;color:var(--dim)}
.singles{font-size:13.5px;color:var(--dim);margin-top:14px;line-height:1.9}
.singles b{color:var(--ink);font-weight:700}
.bar{position:sticky;top:0;z-index:9;background:var(--pg);
border-bottom:1px solid var(--rule)}
.bar .in{max-width:1100px;margin:0 auto;padding:10px 28px;display:flex;
align-items:center;gap:12px}
.who{font-size:13px;color:var(--dim);margin-right:auto}
button{font:inherit;font-size:13px;padding:6px 13px;border-radius:6px;
border:1px solid var(--rule);background:#fff;color:var(--ink);cursor:pointer}
button[aria-pressed=true]{background:var(--ink);color:#fff;border-color:var(--ink)}
button:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.panel{border:1px solid var(--rule);border-radius:8px;margin-bottom:14px;
overflow:hidden;background:#fff}
.phead{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;
padding:14px 18px 12px}
.pname{font-size:17px;font-weight:700}
.meta{font-size:13px;color:var(--dim)}
.flag{font-family:var(--mono);font-size:11px;border:1px solid currentColor;
border-radius:3px;padding:1px 5px;opacity:.65}
.grid{display:grid;gap:6px;padding:0 18px 16px}
.row,.hd{display:grid;grid-template-columns:56px repeat(5,1fr) 1.5fr;gap:6px}
.row{align-items:stretch}
.hd{padding:0 18px 6px;font-size:12px;color:var(--dim)}
.hd span{text-align:center}
.rl{font-family:var(--mono);font-size:12px;align-self:center;opacity:.75}
.sw{border-radius:4px;padding:9px 6px;text-align:center;font-family:var(--mono);
font-size:11.5px;cursor:pointer;border:1px solid rgba(0,0,0,.10);
transition:transform .08s}
.sw:hover{transform:translateY(-1px)}
.demo{border-radius:4px;display:flex;align-items:center;justify-content:center;
font-size:13px;font-weight:700}
.flow{display:flex;align-items:center;gap:0;flex-wrap:wrap}
.node{display:flex;align-items:center;justify-content:center;font-weight:700;
font-size:15px;text-align:center}
.arrow{flex:0 0 auto;display:flex;align-items:center;color:var(--dim)}
.arrow svg{display:block}
.sub{font-size:12px;font-weight:700;letter-spacing:.06em;
padding:12px 18px 2px;border-top:1px solid rgba(0,0,0,.07)}
.sub:first-child{border-top:0}
.sub .hint{font-weight:400;color:var(--dim);letter-spacing:0;margin-left:8px}
.foot{font-size:12.5px;color:var(--dim);margin:0;padding:2px 18px 14px}
.foot code{font-size:12px}
.srow{display:grid;grid-template-columns:1fr 150px 96px;gap:18px;
align-items:center;padding:14px 18px 16px}
.mini{display:flex;flex-direction:column;align-items:center;gap:5px;
font-size:11.5px;color:var(--dim)}
.mini i{font-style:normal;font-size:11px;opacity:.8}
.mini b{font-family:var(--mono);font-weight:400}
.mini svg{width:100%}
.tex{display:block;width:56px;height:28px;border-radius:3px}
.states{display:grid;grid-template-columns:230px 1fr;gap:8px 18px;
align-items:center;padding:10px 18px 14px}
.stlab{font-size:14px}
.stlab b{display:block;font-family:var(--mono);font-size:12.5px}
.stlab span{color:var(--dim);font-size:12.5px}
.lines{display:grid;grid-template-columns:130px 1fr 230px;gap:8px 16px;
align-items:center;padding:10px 18px 16px;font-size:13px}
.lines code{font-size:12px}
.lines .rt{color:var(--dim);text-align:right;font-family:var(--mono);font-size:12px}
.toast{position:fixed;left:50%;bottom:22px;transform:translateX(-50%) translateY(8px);
background:var(--ink);color:#fff;font-size:13px;padding:7px 14px;border-radius:6px;
opacity:0;pointer-events:none;transition:.18s}
.toast.on{opacity:1;transform:translateX(-50%)}
body.grey .panel{filter:grayscale(1)}
@media(max-width:900px){.srow{grid-template-columns:1fr}}
@media(max-width:860px){.row,.hd{grid-template-columns:44px repeat(3,1fr)}
.row>*:nth-child(n+5),.hd span:nth-child(n+4){display:none}
.states{grid-template-columns:1fr}.lines{grid-template-columns:1fr}
.lines .rt{text-align:left}}
"""

JS = """
const b=document.body,t=document.getElementById('t');
document.getElementById('g').onclick=e=>{const on=b.classList.toggle('grey');
e.currentTarget.setAttribute('aria-pressed',on)};
let timer;
document.querySelectorAll('.sw').forEach(el=>el.onclick=()=>{
  navigator.clipboard?.writeText(el.dataset.hex);
  t.textContent=el.dataset.hex+' 已複製';t.classList.add('on');
  clearTimeout(timer);timer=setTimeout(()=>t.classList.remove('on'),1100);});
"""


def arrow_svg(kind, colour, sw=2):
    """Open V or solid triangle, matching the shape profile's `arrow`."""
    tip = (f'<path d="M1 1L9 5L1 9" fill="none" stroke="{colour}" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round"/>') if kind == "open" else \
          f'<path d="M0 0L10 5L0 10z" fill="{colour}"/>'
    return (f'<svg width="46" height="10" viewBox="0 0 46 10">'
            f'<line x1="0" y1="5" x2="34" y2="5" stroke="{colour}" stroke-width="{sw}" '
            f'stroke-linecap="round"/><g transform="translate(34,0)">{tip}</g></svg>')


def node_style(cfg, c, t):
    fill = "transparent" if cfg["fill"] == "outline" else c["card"]
    h, pad, _ = DENSITY[cfg["density"]]
    return (f'border-radius:{cfg["rx"]}px;border:{cfg["stroke-width"]}px solid '
            f'{c["line"]};background:{fill};color:{t["ink"]};'
            f'min-height:{h}px;padding:0 {pad}px')


def hatch(colour, gap=6):
    return (f'repeating-linear-gradient(45deg,{colour} 0 1px,'
            f'transparent 1px {gap}px)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out",
                    default=os.path.join(ROOT, "docs", "style-reference.html"))
    a = ap.parse_args()
    ts = themes()
    shs = pens()
    # One palette carries every demo above the colour section. Those sections
    # are about geometry, and rotating the palette between them would imply a
    # colour meaning that is not there. tailwind-default is the pick because
    # its categories sit highest in lightness (15/36/58) — the borders and
    # tints stay legible at the small sizes these demos use.
    DEMO = "tailwind-default"
    base = next(t for n, _, _, t in ts if n == DEMO)
    bc = derive_cat(base["cats"][0], base["canvas"])
    infra = derive_cat(base.get("infra", "#657B83"), base["canvas"])

    p = []
    p.append('<h1>樣式參考</h1>')
    p.append('<p class="lede">點色票複製 hex。'
             '每一項區別在灰階下都必須依然成立。</p>')

    # ---- 1. roles: the contract ----
    p.append('<h2>角色 <small>樣式掛在角色上，不掛在圖元上</small></h2>')
    p.append('<table>')
    for key, name, desc in ROLES:
        p.append(f'<tr><td class="k">{name}</td><td class="d">{esc(desc)}</td>'
                 f'<td><code>--cat-N-{key}</code></td></tr>')
    p.append('</table>')
    p.append('<p class="singles">'
             '<b>文字</b>　ink-strong 主文字　·　ink-muted 註記　·　'
             'badge-ink 徽章字（白或近黑，取對比高者）<br>'
             '<b>單值</b>　canvas 畫布　·　infra 共用設施　·　terminal 終點實心　·　'
             'accent 強調，限 3 處　·　highlight 螢光筆，限 2 處<br>'
             '<b>cat-N 無語意</b>　位置槽，意義每張圖各自指派。'
             '固定的只有「單圖內獨佔」與「明度遞增」。</p>')

    # State and line roles are roles, not shape variants: the meaning is fixed
    # and only the rendering parameters scale with the chosen shape. Showing
    # them here rather than nested under each shape keeps the page's structure
    # honest about which layer owns what.
    ref = dict(shs)["console"]
    rsw = float(ref["stroke-width"])
    rd = dashes(rsw)
    rgap = hatch_gap(ref["density"])
    cats = [derive_cat(x, base["canvas"]) for x in base["cats"]]

    p.append(f'<section class="panel" style="background:{base["canvas"]}">')
    p.append('<div class="sub">表面狀態　<span class="hint">不靠顏色區分</span></div>')
    p.append('<div class="states">')
    for lab, desc, kind in STATES:
        c = cats[0]
        box = (f'border-radius:{ref["rx"]}px;min-height:44px;padding:0 24px;'
               f'color:{base["ink"]}')
        if kind == "deprecated":
            box += (f';border:{rsw}px solid {infra["base"]};'
                    f'background:{infra["card"]};background-image:'
                    f'{hatch(infra["base"] + "59", rgap)}')
        else:
            st = "dashed" if kind in ("external", "planned") else "solid"
            bg = "transparent" if kind == "planned" else c["card"]
            box += f';border:{rsw}px {st} {c["line"]};background:{bg}'
        p.append(f'<div class="stlab"><b>{lab}</b><span>{esc(desc)}</span></div>')
        p.append(f'<div class="node" style="{box};max-width:240px">結算服務</div>')
    p.append('</div>')

    p.append('<div class="sub">線條　<span class="hint">機制用 dash，非機制用 dot</span></div>')
    p.append('<div class="lines">')
    for ln, desc, key in LINES:
        da = "" if rd[key] == "none" else f' stroke-dasharray="{rd[key]}"'
        op = ' opacity="0.7"' if key in ("dashdot", "dot") else ''
        p.append(f'<div><code>{ln}</code></div>'
                 f'<div><svg width="100%" height="8" viewBox="0 0 320 8" '
                 f'preserveAspectRatio="none"><line x1="0" y1="4" x2="320" y2="4" '
                 f'stroke="#8B9096" stroke-width="{rsw}" stroke-linecap="round"'
                 f'{da}{op}/></svg></div>'
                 f'<div class="rt">{esc(desc)}</div>')
    p.append('</div>')
    p.append('<p class="foot">以 <code>console</code> 的線寬呈現。'
             '語意固定，長度與間距隨筆調縮放。</p>')
    p.append('</section>')

    # ---- 2. shape layer ----
    p.append('<h2>筆調 <small>三選一</small></h2>')
    order = ["console", "briefing", "blueprint"]
    for name, cfg in sorted(shs, key=lambda x: order.index(x[0])):
        sw = float(cfg["stroke-width"])
        d = dashes(sw)
        gap = hatch_gap(cfg["density"])
        outline = cfg["fill"] == "outline"
        cc = [derive_cat(x, base["canvas"], outline) for x in base["cats"]]
        spec = " · ".join([f'rx{cfg["rx"]}', f'{cfg["stroke-width"]}px',
                           cfg["density"], cfg["fill"], f'{cfg["arrow"]} 箭頭'])
        p.append(f'<section class="panel" style="background:{base["canvas"]}">')
        p.append(f'<div class="phead"><span class="pname">{name}</span>'
                 f'<span class="meta">{cfg["label"]}　{esc(cfg["fit"])}</span>'
                 f'<span class="flag">{spec}</span></div>')
        p.append('<div class="srow">')
        p.append('<div class="flow">')
        for i, lab in enumerate(["輸入", "處理", "輸出"]):
            if i:
                p.append(f'<span class="arrow">'
                         f'{arrow_svg(cfg["arrow"], "#8B9096", sw)}</span>')
            p.append(f'<span class="node" style="{node_style(cfg, cc[i], base)}">'
                     f'{lab}</span>')
        p.append('</div>')
        p.append(f'<div class="mini"><i>控制流虛線</i>'
                 f'<svg width="100%" height="10" viewBox="0 0 120 10" '
                 f'preserveAspectRatio="none"><line x1="0" y1="5" x2="120" y2="5" '
                 f'stroke="#8B9096" stroke-width="{sw}" stroke-linecap="round" '
                 f'stroke-dasharray="{d["dash"]}"/></svg>'
                 f'<b>{d["dash"]}</b></div>')
        p.append(f'<div class="mini"><i>斜線紋</i><span class="tex" '
                 f'style="background-image:{hatch(infra["base"] + "59", gap)};'
                 f'border:1px solid {infra["base"]}55"></span><b>{gap}px</b></div>')
        p.append('</div>')
        if outline:
            p.append('<p class="foot">純框線沒有填色通道：'
                     '<code>state/planned</code> 改用虛線框 ＋ 斜線紋，'
                     '與 <code>deprecated</code> 的實線框 ＋ 斜線紋靠邊框分開。</p>')
        p.append('</section>')

    # ---- colours ----
    p.append('<h2>顏色 <small>四選一</small></h2>')
    p.append('<div class="hd"><span></span>'
             + "".join(f'<span>{n}</span>' for _, n, _ in ROLES)
             + '<span>示範</span></div>')
    for tn, pur, mode, t in ts:
        cats = [derive_cat(c, t["canvas"], t.get("outline"), t.get("print"),
                           t.get("vivid")) for c in t["cats"]]
        gl = " · ".join(f'{luminance(hex2rgb(c["base"]))*100:.0f}' for c in cats)
        flags = "".join(f'<span class="flag">{m}</span>' for m in mode.split() if m)
        p.append(f'<section class="panel" style="background:{t["canvas"]};'
                 f'color:{t["ink"]}">')
        p.append(f'<div class="phead"><span class="pname">{tn}</span>'
                 f'<span class="meta">{esc(pur)}</span>'
                 f'<span class="meta">灰階 {gl}</span>{flags}</div>')
        p.append('<div class="grid">')
        for k, c in enumerate(cats):
            p.append(f'<div class="row"><span class="rl">cat-{k+1}</span>')
            for key, _, _ in ROLES:
                p.append(f'<span class="sw" data-hex="{c[key]}" title="{key}" '
                         f'style="background:{c[key]};color:{ink_on(c[key])}">'
                         f'{c[key]}</span>')
            hl = t.get("highlight")
            if k == 0 and hl:
                p.append(f'<span class="demo" style="background:{c["card"]};'
                         f'border:1.5px solid {c["line"]};'
                         f'box-shadow:5px 5px 0 {hl}">卡片＋實心陰影</span>')
            elif k == 1 and hl:
                p.append(f'<span class="demo" style="background:{c["card"]};'
                         f'border:1.5px solid {c["line"]}">'
                         f'<span style="background:linear-gradient(transparent 62%,'
                         f'{hl} 62%)">螢光筆畫記</span></span>')
            else:
                p.append(f'<span class="demo" style="background:{c["card"]};'
                         f'border:1.5px solid {c["line"]}">卡片樣貌</span>')
            p.append('</div>')
        p.append('</div></section>')


    doc = ('<!doctype html><html lang="zh-Hant"><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>diagram-style 樣式參考</title><style>{CSS}</style>'
           '<div class="bar"><div class="in">'
           '<span class="who">diagram-style · 樣式參考</span>'
           '<button id="g" aria-pressed="false">灰階檢視</button></div></div>'
           f'<div class="wrap">{"".join(p)}</div>'
           f'<div class="toast" id="t"></div><script>{JS}</script></html>')

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(doc)
    print(f"{a.out}  {len(shs)} pens, {len(ts)} themes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
