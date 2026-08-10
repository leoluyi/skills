# Tailwind Default — Tailwind 預設色

Tailwind CSS v4 的預設色階。v4 內部以 OKLCH 定義，此處取其 sRGB hex 後備值。

**適用**：專案已用 Tailwind、面向前端讀者、需要與既有介面視覺一致的圖。
**不適用**：黑白影印為主的正式文件——色階雖然拉得開，但飽和度偏高，
印出來的網點會比 `muted-ledger` 吵。

```
mode: standard
```

> 預設階梯 region 4／card 10／card-sub 16

## Base 值

```css
:root{
  --cat-1-base:  #2563EB;   /* blue-600 */
  --cat-2-base:  #10B981;   /* emerald-500 */
  --cat-3-base:  #FBBF24;   /* amber-400 */
  --cat-4-base:  #DDD6FF;   /* violet-200：v4 oklch(89.4% 0.057 293.283) 的 sRGB */
  --cat-s-base:  #DC2626;   /* red-600，只用於 warning／issue 等異常狀態 */
  --infra-base:  #64748B;   /* slate-500 */
  --terminal:    #1F2937;   /* gray-800 */
  --ink-strong:  #1F2937;
  --canvas-white: #FFFFFF;
  --canvas-tint:  #F8FAFC;   /* slate-50 */
  --accent:      #0E7490;   /* cyan-700，避開粉紅並與四個類別分離 */
  --highlight:   #F2E172;   /* 螢光筆 — 黃 H52 S84 — 跟隨主題的高飽和 */
}
```

## 為什麼不是清一色 -500

`blue-500` / `emerald-500` / `amber-500` 的灰階明度是 **24 / 36 / 44**，
emerald 與 amber 只差 8，過不了 10% 門檻。

Tailwind 的色階是**依感知明度均勻切分**的，所以同一階跨色相時明度相近——
這正是它適合做 UI 的原因（換色不換視覺重量），卻正好與類別區分的需求相反。

改取 `blue-600` / `emerald-500` / `amber-400` / `violet-200`，灰階明度 **15 / 36 / 58 / 70**，
間距 21 / 22 / 12。**跨色相時要換階，不要固定在同一階。**

`red-600` 不進平行類別，固定作 `cat-s`，只標示 warning、issue、error、blocker 與異常狀態。

## 陷阱

`amber-400` 明度 58%，`line` 推導會把它壓暗不少，
所以邊框與徽章看起來不會像 amber-400——那是對比要求，不是推導出錯。

`violet-200` 是 [Tailwind CSS v4 官方色票](https://github.com/tailwindlabs/tailwindcss/blob/main/packages/tailwindcss/theme.css)的 `--color-violet-200: oklch(89.4% 0.057 293.283)`；此處保存其 sRGB 轉換值 `#DDD6FF`，供只接受 hex 的推導器使用。
它很淺，只提供第四階需要的明度跨度；文字與邊框使用推導後的 `label`、`line`，不要直接使用 base。
