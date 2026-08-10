# Solarized Light — Solarized 淺色（微調版）

以 Ethan Schoonover 的 Solarized 淺色為底，兩處刻意偏離原始規格：

1. **畫布近白**：`base3` `#FDF6E3`（L94.1 S87）→ `#FDFDFC`（L99 S26）。
   幾乎是白色，只留極淡的暖調。
2. **cat-1 換色相**：從 `base02` 深板岩改為 Solarized `blue` 色相的深藍。
   原本 cat-1 (H192) 與 cat-3 cyan (H175) 只差 18°，兩者都是青綠家族，
   讀起來像同一個顏色的明暗版。
3. **cat-3 改用 Solarized yellow**：橘黃色系與藍、綠都能清楚分開。
4. **orange 轉為特殊色**：`#CB4B16` S80 → `#C45323` S70，作為 `cat-s`，不再混入平行類別。

**這不是官方 Solarized 值。** 需要與 Solarized 編輯器逐格對色時，
用檔末「原始值」那一節。

**適用**：技術讀者、長時間螢幕閱讀、與 Solarized 編輯器或終端機並排的文件。
**不適用**：需要黑白影印的場合——米底印出來會有網點；改用 `blueprint-mono`。
也不適合需要第四個類別的圖，理由見下。

```
mode: standard
```

> 預設階梯 region 4／card 10／card-sub 16

## Base 值

```css
:root{
  --cat-1-base:  #084D7F;   /* blue 色相 H205，壓暗至灰階 7% */
  --cat-2-base:  #899F00;   /* green 色相 H68，滿彩 */
  --cat-3-base:  #D9A60B;   /* yellow 色相 H45，橘黃色系，提亮以拉開灰階 */
  --cat-s-base:  #C45323;   /* orange-red，只用於 warning／issue 等異常狀態 */
  --infra-base:  #647C84;   /* base00 +8% 彩 */
  --terminal:    #002B36;   /* base03 — 原值 */
  --ink-strong:  #002B36;   /* base03 — 原值 */
  --ink-muted:   #576F76;   /* base01 +8% 彩 */
  --canvas:      #FDFDFC;   /* 近白，極淡暖調 */
  --accent:      #686EC8;   /* violet +8% 彩 */
  --highlight:   #F0DF6F;   /* 螢光筆 — 黃 H52 S82 — 跟隨主題的高飽和 */
}
```

`terminal` 與 `ink-strong` 維持原值：`base03` 已近黑，提彩看不出差別，
留著原值讓深色端仍可與 Solarized 對得上。

字型：`"Noto Sans CJK TC", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif`

灰階明度 **7% / 30% / 42%**，**遞增**，間距 23 與 12。

色相 **205° / 68° / 45°**。藍與暖色的距離很大，綠與橘黃則以明度及標籤作第二通道。
灰階間距解決的是黑白列印，色相間距解決的是彩色閱讀，兩者都要顧。

**cat-1 刻意不是最暗的。** `terminal` (base03, 灰階 2%) 在它下方，
若把 cat-1 壓到最暗，深藍卡片邊框會與終點實心塊撞成同一個調。

cat-3 從 Solarized yellow 的色相出發，但提高明度到 42%，讓它與 30% 的綠保有灰階距離。
原本位於 18% 的 orange 改為 `cat-s`，保留給 warning、issue、error、blocker 與異常狀態。

## 這是第一個非白畫布的主題

色階推導混的是 `canvas` 而不是白色，所以卡片底帶著畫布的暖調，與底色同溫。
若推導寫死白色，卡片會泛冷、跟底色打架。

畫布提亮到 L97.5 之後這件事更關鍵：色差變小，任何冷暖不一致都會更明顯。

## 為什麼三個類別無法全從強調色裡選

Solarized **刻意把八個強調色調成幾乎相同的明度**——官方 L\*a\*b\* 表裡
yellow、cyan、green 都是 L\*60，blue 是 L\*55。實測相對亮度：

| | |
|---|---|
| cyan / green / yellow | 28.2 / 27.8 / 27.7 |
| blue | 23.5 |
| violet / base00 / magenta / orange / red | 19.0 / 18.6 / 18.1 / 17.8 / 17.7 |

八個強調色全擠在 **17–28 這 11 點**裡。這不是缺陷，是設計目標——
Solarized 靠**色相**區分，明度刻意齊平，這樣切換淺／深色版時視覺重量不變。
但類別編碼需要的正好相反，所以三個類別無法全部從強調色裡選。

所以本主題不直接取用強調色，而是**保留 Solarized 的色相、重新指定明度**：
`blue` 的 H205 壓暗到灰階 8%，`green` 的 H68 提到 30%，中間放原值的 `orange`。
色相仍是 Solarized 的，明度則是為了類別可分而重排。

**上限是 3。** 第四個類別在 Solarized 裡沒有空間。

## 陷阱

**Solarized 正統內文色 base01 (#586e75) 過不了。** 它對純 `base3` 是 4.99:1
勉強及格，但放到帶色卡片底上只剩 **4.2:1**——低對比的名聲是真的。
所以 `ink-strong` 用 base03，base01 降級為 `ink-muted`（僅用於註記、來源）。

`cat-2` 橘與 `accent` 紫的明度分別是 18.4 與 19.0，灰階下幾乎同階。
accent 限 3 處以內且通常用於文字強調，不當類別面，實務上不衝突——
但**不要把 accent 拿去填任何卡片**。

## 原始值

需要與 Solarized 編輯器逐格對色時用這組。它**過不了灰階閘門**
（cat-2 與 cat-3 間距 10.4 仍可，但整體對比較低），僅供比對：

```css
--canvas:#FDF6E3; --cat-1-base:#073642; --cat-2-base:#CB4B16;
--cat-3-base:#2AA198; --infra-base:#657B83; --ink-muted:#586E75;
--accent:#6C71C4; --terminal:#002B36; --ink-strong:#002B36;
```
