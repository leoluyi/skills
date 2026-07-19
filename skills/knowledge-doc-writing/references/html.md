# HTML 圖文版產出規則

Markdown 為正本。使用者要圖文並茂或互動比較時才另出 HTML 版，四型區塊在 HTML 中仍清楚分離呈現。

## inline SVG 與固定外殼

- **所有圖表（infographic）一律用 inline SVG**，不用 canvas、點陣圖、或外部圖片。理由：SVG 是文字，未來要調整（改標籤、換配色、加節點）時人和模型都能直接編輯，不必重畫。Markdown 正本裡的 Mermaid 圖轉 HTML 時**重繪為手工 inline SVG，不嵌 Mermaid runtime**——執行期渲染的圖無法離線閱讀，DOM 也難維護。
- **文件外殼固定套用預設模板，每次都一樣，不重新設計**。色彩、字體、版面、表格與區塊樣式一律用下方最低規範 CSS，不因主題另挑色票或字體。一致的外觀是知識庫的資產：讀者掃過十份文件會認得「這是我們的知識文件」。
- SVG 圖要能獨立讀懂：圖內標籤完整，不依賴周邊文字；配色與整體 token 一致。
- 條列項目符號用真正的 bullet，不用破折號充當（破折號在條列裡是「概念名 — 說明」的分隔符，兩者不可混用）；樣式含在下方 `ul.kv`。
- 尊重 `prefers-reduced-motion`，行動裝置可讀（下方 CSS 已含）。

## 最低規範 CSS（固定模板）

```css
:root{
  /* 固定色票，每份文件都用這組，不重新設計 */
  --paper:#F7F9FB; --panel:#FFFFFF; --ink:#1F3A5F; --text:#2A2F36; --muted:#5C6670;
  --accent-a:#41597A; --accent-a-bg:#E8EDF4;   /* 分類/對照 A */
  --accent-b:#0E7C7B; --accent-b-bg:#E3F2F1;   /* 分類/對照 B */
  --warn:#B97514; --warn-bg:#FBF3E4;           /* ADR、風險、成本區塊 */
  --line:#C9D3DE; --radius:6px;
  --font-body:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;
  --font-mono:ui-monospace,"SF Mono","Cascadia Mono",Menlo,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--text);font-family:var(--font-body);line-height:1.8;font-size:16px}
main{max-width:860px;margin:0 auto;padding:48px 24px 80px}
h1{font-size:1.85rem;color:var(--ink);margin:0 0 4px;font-weight:700}
h2{font-size:1.2rem;color:var(--ink);margin:2.4em 0 .7em;padding-bottom:.35em;border-bottom:2px solid var(--line)}
.kicker{font-family:var(--font-mono);font-size:.76rem;color:var(--muted);letter-spacing:.14em;text-transform:uppercase}

/* 開頭一句話 blockquote */
.thesis{background:var(--panel);border-left:4px solid var(--ink);border-radius:0 var(--radius) var(--radius) 0;
  padding:18px 22px;margin:22px 0;box-shadow:0 1px 3px rgba(31,58,95,.08)}
.scope{font-family:var(--font-mono);font-size:.78rem;color:var(--muted);margin-top:8px}

/* 條列 */
ul.kv{list-style:none;padding-left:0;margin:1em 0}
ul.kv li{margin:.55em 0;padding-left:1.3em;position:relative}
ul.kv li::before{content:"•";position:absolute;left:0;color:var(--muted);font-weight:700}
ul.kv b{color:var(--ink)}

/* 表格：殿後於論述，樣式素淨 */
table{width:100%;border-collapse:collapse;margin:1.1em 0;font-size:.92rem;background:var(--panel)}
th{background:var(--ink);color:#fff;text-align:left;padding:9px 12px;font-weight:500}
td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:none}

/* SVG 圖說明框 */
figure{margin:1.6em 0;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:18px}
figcaption{font-size:.85rem;color:var(--muted);margin-top:10px}
/* SVG 內文字與內文同字體，在 <svg><style> 裡覆用：font:600 14px var(--font-body) */

/* ADR 決策理由區塊 */
.adr{background:var(--warn-bg);border-left:4px solid var(--warn);border-radius:0 var(--radius) var(--radius) 0;padding:16px 22px;margin:1em 0}
.adr dt{font-weight:700;color:var(--warn);margin-top:.9em}
.adr dt:first-child{margin-top:0}
.adr dd{margin:.2em 0 0}

/* 一段話總結 */
.summary{background:var(--ink);color:#E8EDF4;border-radius:var(--radius);padding:20px 24px;margin:2em 0}
.summary p{margin:.4em 0}

/* 行內程式碼：深色區塊必須覆寫成深底淺字，否則淺字疊淺底看不清 */
code{font-family:var(--font-mono);background:var(--paper);color:var(--text);padding:.1em .35em;border-radius:3px;font-size:.9em}
.summary code{background:rgba(255,255,255,.15);color:#E8EDF4}

ul.src{font-size:.9rem;padding-left:1.2em}
a{color:var(--accent-b)}

/* 動畫尊重 prefers-reduced-motion */
@media (prefers-reduced-motion:no-preference){
  figure svg .flow{stroke-dasharray:6 4;animation:dash 1.6s linear infinite}
  @keyframes dash{to{stroke-dashoffset:-20}}
}

/* 行動裝置 */
@media (max-width:640px){body{font-size:15px} main{padding:32px 14px 60px}}
```

## 圖表內容設計掛法

需要設計圖表（架構圖、流程圖、對照圖）時，引用 `infographic-design` skill 處理**圖的內容設計**，只用在圖本身、不用在文件外殼。畫「這個協定／管線／架構怎麼運作」這類機制圖時，另讀該 skill 的 `references/bytebytego-style.md`，用編號走查（numbered walkthrough）把複雜流程講成可循序讀懂的序列，不是泛泛的方框加箭頭。

**文件外殼與整體視覺語言以本檔固定模板為準，覆蓋該 skill 自己的色彩與字體系統**：圖表顏色一律從文件既有 token（`--ink`、`--muted`、`--accent-a`、`--accent-b`、`--warn`）裡挑，不新開色票；字體沿用 `--font-body`／`--font-mono`。同一份文件裡圖表與正文永遠是同一套視覺語言，換主題也不重新設計外觀。
