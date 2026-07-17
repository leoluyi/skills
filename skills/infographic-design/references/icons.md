# Icon Vocabulary and Construction Grid

Drawing icons from scratch is where "consistent line icons" quietly falls
apart — stroke weights drift, sizes wobble, some end up filled and some
outlined, and the result reads as AI-generated. This file fixes that two
ways: a **construction grid** every icon obeys, and a **ready starter
library** of 30 verified icons you paste in rather than reinventing.

## Construction grid (obey for every icon, including new ones)

- **24×24 viewBox.** All icons live in `0 0 24 24`.
- **~2px padding.** Keep artwork inside roughly x/y 2–22 so icons optically
  align when placed side by side; nothing touches the edge.
- **2px stroke, `currentColor`.** `fill="none" stroke="currentColor"
  stroke-width="2"`. Colour comes from CSS `color` on the `<use>` — that is
  what makes the whole icon set restyle in one edit (see restyle section in
  `svg-construction.md`).
- **Round caps and joins.** `stroke-linecap="round"
  stroke-linejoin="round"` on every icon — this single choice is 80% of what
  makes a set look coherent.
- **Line, not filled.** This vocabulary is all-outline. Do not mix in filled
  glyphs; pick one language and hold it.
- **Dots** (status lights, the dot on an "i"/"!" mark) are drawn as a
  zero-ish-length stroke so the round cap becomes a dot: `d="M12 17h0.01"`.
  A literal `h0` renders as nothing in some converters — always use `.01`.

## How to use the library

Paste the `<symbol>` blocks you need into your SVG's `<defs>` once, then
reference each with `<use>`:

```xml
<defs>
  <!-- paste chosen symbols here -->
  <symbol id="ic-server" viewBox="0 0 24 24" fill="none" stroke="currentColor"
    stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="4" width="18" height="7" rx="1.5"/>
    <rect x="3" y="13" width="18" height="7" rx="1.5"/>
    <path d="M7 7.5h0.01"/><path d="M7 16.5h0.01"/>
  </symbol>
</defs>

<!-- place it: size via width/height, colour via CSS color -->
<use href="#ic-server" x="40" y="40" width="24" height="24"
     style="color:var(--theme)"/>
```

- **Size** with `width`/`height` on `<use>`. Stroke scales with the icon
  (2px at 24px, 4px at 48px) — usually right, since bigger icons should match
  bigger/bolder text. To hold a constant optical stroke regardless of size,
  add `vector-effect="non-scaling-stroke"` to the paths.
- **Colour** via `style="color:…"` or a class; because paths use
  `currentColor`, one CSS rule recolours every icon.
- Keep every icon the same rendered size within a tier (all section icons
  24px, all inline icons 16px, etc.). Mismatched icon sizes read as sloppy.

## Extending the set

When you need an icon not below: draw it on the **same 24 grid, same 2px
round-stroke language**, and borrow shapes already in the set (the same
rounded-rect corner radius, the same circle sizes) so it looks native. Then
render-and-inspect it next to its neighbours before shipping. If a concept
needs a filled shape to read, reconsider — usually an outline version exists.

## Starter library (30 icons, all verified rendering)

Common metaphors for infographics: actors, infrastructure, security, time,
documents, money, data, flow, and status. IDs are `ic-<name>`.

```xml
<symbol id="ic-user" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.5 4-7 8-7s8 2.5 8 7"/></symbol>
<symbol id="ic-users" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.3"/><path d="M2.5 20c0-3.8 3-6 6.5-6s6.5 2.2 6.5 6"/><path d="M16 5.2a3.3 3.3 0 0 1 0 6.6"/><path d="M18.5 14.4c2.3.6 3.5 2.4 3.5 5.6"/></symbol>
<symbol id="ic-server" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h0.01"/><path d="M7 16.5h0.01"/></symbol>
<symbol id="ic-database" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/><path d="M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/></symbol>
<symbol id="ic-cloud" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 18a4 4 0 0 1 0-8 5.5 5.5 0 0 1 10.5 1.5A3.5 3.5 0 0 1 17 18H7z"/></symbol>
<symbol id="ic-laptop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="11" rx="1.5"/><path d="M2 20h20"/></symbol>
<symbol id="ic-mobile" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/></symbol>
<symbol id="ic-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></symbol>
<symbol id="ic-key" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="16" r="4"/><path d="M11 13l9-9"/><path d="M16 8l3 3"/></symbol>
<symbol id="ic-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5.5"/></symbol>
<symbol id="ic-alert" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4l9 15.5H3z"/><path d="M12 10v4"/><path d="M12 17h0.01"/></symbol>
<symbol id="ic-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5.5l3.5 2"/></symbol>
<symbol id="ic-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 9.5h16"/><path d="M8 3v4"/><path d="M16 3v4"/></symbol>
<symbol id="ic-document" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h8l4 4v13a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z"/><path d="M14 3v4h4"/><path d="M9 13h6"/><path d="M9 16.5h6"/></symbol>
<symbol id="ic-folder" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></symbol>
<symbol id="ic-settings" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3.2M12 18.3v3.2M2.5 12h3.2M18.3 12h3.2M5.2 5.2l2.3 2.3M16.5 16.5l2.3 2.3M18.8 5.2l-2.3 2.3M7.5 16.5l-2.3 2.3"/></symbol>
<symbol id="ic-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3.5 3 14.5 0 18c-3-3.5-3-14.5 0-18z"/></symbol>
<symbol id="ic-money" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M15 8.5c-.8-.9-2-1.4-3-1.4-1.7 0-3 1-3 2.3 0 3 6 1.4 6 4.3 0 1.4-1.4 2.3-3 2.3-1.2 0-2.4-.5-3.2-1.4"/><path d="M12 5.5v13"/></symbol>
<symbol id="ic-bar-chart" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20V11"/><path d="M10 20V5"/><path d="M16 20v-6"/><path d="M3 20h18"/></symbol>
<symbol id="ic-trend-up" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/></symbol>
<symbol id="ic-arrow-right" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16"/><path d="M14 6l6 6-6 6"/></symbol>
<symbol id="ic-cycle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 0 1 13.5-5.8L20 8"/><path d="M20 4v4h-4"/><path d="M20 12a8 8 0 0 1-13.5 5.8L4 16"/><path d="M4 20v-4h4"/></symbol>
<symbol id="ic-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/></symbol>
<symbol id="ic-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M4 7.5l8 5.5 8-5.5"/></symbol>
<symbol id="ic-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.6-4.6"/></symbol>
<symbol id="ic-bolt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 3L5 13.5h6l-1 7.5 8-11h-6z"/></symbol>
<symbol id="ic-info" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v4"/><path d="M12 16h0.01"/></symbol>
<symbol id="ic-download" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M4 20h16"/></symbol>
<symbol id="ic-help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M9.2 9.3a3 3 0 0 1 5.6 1.2c0 2-3 2.5-3 4"/><path d="M12 16h0.01"/></symbol>
<symbol id="ic-tick" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5"/></symbol>
```

Names: user, users, server, database, cloud, laptop, mobile, lock, key,
check, alert, clock, calendar, document, folder, settings, globe, money,
bar-chart, trend-up, arrow-right, cycle, shield, mail, search, bolt, info,
download, help, tick.
