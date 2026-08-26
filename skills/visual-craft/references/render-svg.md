# Render: SVG — SVG 實作

角色落到 SVG 的畫法。角色的**意義**在 `roles.md`，本檔只講怎麼畫。

## 節點形狀

同形狀等於沒有 landmark。技術圖裡混類是常態——動作、元件、資料源、治理關卡
本質不同，畫成同一種圓角矩形，讀者每次都得重新讀字才知道那是什麼。

形狀是**第二通道**。掉成灰階或黑白列印後，型別區隔仍須成立，
所以型別靠形狀，不靠顏色。顏色留給類別（階段／泳道／層級）。

所有形狀以左上角 `(x, y)`、寬 `w`、高 `h` 定義，方便直接代入。

---

## node/action — 動作

最常見的節點。圓角矩形。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"
      fill="var(--cat-1-card)" stroke="var(--cat-1-base)" stroke-width="2"/>
```

## node/sub — 巢狀子節點

包在 action 內部的細項。圓角小一階、線細一階、底深一階，
形成視覺從屬，不需要額外的標題或框線去說明層級。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="var(--cat-1-card-sub)" stroke="var(--cat-1-base)" stroke-width="1.5"/>
```

## node/datasource — 資料源

圓柱體。上緣完整橢圓，側壁直下，下緣只畫前半弧——
這是資料庫圖示沿用數十年的慣例，讀者不需要圖例就認得。

`ry` 取 `h` 的 1/6，太扁會看起來像被壓壞的矩形。

```xml
<!-- ry = h/6 -->
<path d="M{x} {y+ry}
         a {w/2} {ry} 0 0 1 {w} 0
         v {h-2*ry}
         a {w/2} {ry} 0 0 1 {-w} 0 z"
      fill="var(--cat-2-card)" stroke="var(--cat-2-base)" stroke-width="2"/>
<path d="M{x} {y+ry} a {w/2} {ry} 0 0 0 {w} 0"
      fill="none" stroke="var(--cat-2-base)" stroke-width="2"/>
```

文字基線放在 `y + h/2 + ry/2`，避開上緣橢圓的視覺重心。

## node/gate — 治理關卡

需要人為核准、審查或放行的節點——主管核准、合規檢查、人工覆核。

外框加一道內縮 4px 的第二線，`stroke-dasharray` 留給註解用，
所以這裡用**雙實線**而非虛線。雙線在灰階與縮圖下都還看得出來。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"
      fill="var(--cat-3-card)" stroke="var(--cat-3-base)" stroke-width="2"/>
<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="7"
      fill="none" stroke="var(--cat-3-base)" stroke-width="1" opacity="0.55"/>
```

## node/rail — 貫穿層

全寬橫條，代表「上下都要透過我」的共用接取層——MCP／API 平台、
訊息匯流排、認證層。它是**設施不是動作**，所以用中性色，不佔用任何類別色。

```xml
<rect x="{x}" y="{y}" width="{w}" height="48" rx="10"
      fill="var(--infra-card)" stroke="var(--infra-base)" stroke-width="1.5"/>
```

橫條寬度要明顯大於任何單一節點，否則讀者會把它當成另一個並排的框。
實務上取畫布寬減兩側邊距。

## node/terminal — 終點

結論、產出、最終狀態。實心深色配白字，是全圖唯一的深塊，
讀者的視線自然停在這裡。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="var(--terminal)"/>
```

**一張圖只能有一個 terminal。** 兩個深塊就沒有終點，只有兩個吵架的重心。

---

## 註解框（不是節點）

對圖本身的說明——警告、例外、待確認事項。

**點線 `2 3`，不是虛線 `6 4`。** 虛線 `6 4` 屬於 `line/control`（控制流、非同步），
那是機制的一部分；註解不是。兩者共用同一個 dash pattern 時，
讀者無法判斷那條線是不是系統行為。規則是**機制用 dash，非機制用 dot**，
完整對照見 `roles.md`。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"
      fill="none" stroke="var(--ink-muted)" stroke-width="1.5"
      stroke-dasharray="2 3" opacity="0.7"/>
```

註解畫成卡片，讀者會把說明讀成機制的一部分，圖裡於是多出一個不存在的元件。
這是混用表面語彙最常見、也最貴的一次失誤。

## 狀態角色

### state/planned — 規劃中

虛線框、**不填色**。與 `surface/external`（虛線框但照常填色）的差別就在填色。

```xml
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none"
      stroke="var(--cat-N-line)" stroke-width="{sw}" stroke-dasharray="6 4"/>
```

`blueprint` 筆調下所有東西都沒有填色，這個區別失效——該筆調改用斜線紋加虛線框。

### state/deprecated — 退場中

中性色 ＋ 45° 斜線紋。**紋理是必要的**，只降飽和在灰階下會完全消失。

```xml
<defs>
  <pattern id="hatch" width="6" height="6" patternTransform="rotate(45)"
           patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="6" stroke="var(--infra-base)"
          stroke-width="1" opacity="0.35"/>
  </pattern>
</defs>
<rect … fill="var(--infra-card)" stroke="var(--infra-base)" stroke-width="{sw}"/>
<rect … fill="url(#hatch)" aria-hidden="true"/>
```

紋理疊在填色之上，用兩個矩形。間距 6 是刻意的疏——密到看起來像實心時，
讀者會把它當成另一個類別而非同一元件的狀態。

### line/optional — 條件性連線

```xml
<path class="cn" d="…" stroke-dasharray="8 3 2 3" opacity="0.7"/>
```

點劃線，不是第三種長度的虛線——`6 4` 與 `10 5` 已被佔用，
再加一種純虛線時三者在縮圖下分不出來。

## 裝飾性圖形要標 `aria-hidden`

螢光筆底線、實心偏移陰影這類**不承載內容**的圖形，一律加 `aria-hidden="true"`。

兩個理由同時成立：螢幕閱讀器該跳過它們；而 `check_fit.py` 也靠這個標記
判斷哪些矩形是容器——沒標的話，文字下方的螢光筆色塊會被當成該文字的容器，
於是每個被畫記的標籤都會報一次假的溢出。

```xml
<rect x="…" y="…" width="…" height="…" fill="var(--highlight)" aria-hidden="true"/>
<text class="body" …>被畫記的文字</text>
```

## 輸出結構

palette 放 `:root`，語意分組，讓換主題只是一次變數置換：

```xml
<svg viewBox="0 0 1120 640" xmlns="http://www.w3.org/2000/svg">
  <title>…</title>
  <style>
    :root{
      --cat-1-base:#2A78D6; --cat-1-card:#EAF1FB; …
      --ink-strong:#12336E; --connector:#8595A8;
    }
    .card{rx:10;stroke-width:2}
  </style>
  <g id="region-1">…</g>
  <g id="region-2">…</g>
</svg>
```

**CJK 字型必須明寫**，且 `"Noto Sans CJK TC"` 排第一：

```
"Noto Sans CJK TC", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif
```

`Noto Sans CJK TC` 與 `Noto Sans TC` 是**不同的 family name**。
Linux 上 `fonts-noto-cjk` 裝的是前者，只寫後者會 fallback 失敗、整片變豆腐字（□）。
先 `fc-list :lang=zh-tw family` 確認實裝名稱，匯出後務必開圖檢查一次。

**`var()` 不能用在要匯出的 SVG。** cairosvg 等多數 SVG→PNG／PDF 轉檔器
不支援 CSS 自訂屬性，`fill="var(--x)"` 會靜默解析成黑色，整張圖變全黑。
`:root` 變數只在瀏覽器內有效。要匯出就**輸出字面色值**——
換主題靠重跑 `derive.py` 重新產生，不是手改變數，這樣值也不會跟主題檔失去同步。

---
