# Warm Clarity — 暖白解說

取自 MCP 與 API 解說投影片的共通視覺：暖白紙底、深藍黑標題、藍與綠的流程分工，以及橘色關鍵字與標題引導線。

**適用**：教學簡報、概念解說、產品流程與面向非技術聽眾的架構導讀。
**不適用**：黑白影印、純框線附錄，或需要四個以上一般類別的圖。

```text
mode: standard
```

> 預設階梯 region 4／card 10／card-sub 16

## Base 值

```css
:root{
  --cat-1-base:  #245282;   /* 深藍 */
  --cat-2-base:  #458F70;   /* 柔綠 */
  --cat-3-base:  #EC902F;   /* 亮橘 */
  --cat-s-base:  #C4473A;   /* 橘紅，只用於 warning／issue 等異常狀態 */
  --infra-base:  #749195;
  --terminal:    #0C1123;
  --ink-strong:  #0B162C;
  --ink-muted:   #58616C;
  --canvas-white: #FFFFFF;
  --canvas-tint:  #FCFBF8;   /* 近中性的暖白紙底 */
  --accent:      #C04C00;   /* 高飽和純橘，供關鍵字、標題引導線與 hero */
  --highlight:   #F1D37A;   /* 黃色畫記，只供圖表 highlight */
}
```

字型：`"Noto Sans CJK TC", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif`

類別灰階明度為 **8 / 22 / 38**，依藍、綠、橘順序遞增。
附件原色保留色相，類別 base 則重新排列明度，讓彩色與灰階都能辨識。

## 投影片語意

主標題與正文使用深藍黑 `ink-strong`。
關鍵字、標題區塊引導線與大標數字／hero 共用高飽和純橘 `accent`，由推導器針對所選 canvas 解出 `--slide-emphasis`。
藍、綠、橘三個 category 對應資訊輸入、執行處理與輸出／重點等平行類別；每張圖仍須自行指派意義。
橘紅 `cat-s` 只用於警示、失敗、風險與需要處理的問題。

## 陷阱

橘色 category 與黃色 `highlight` 色相接近。
底線式文字畫記仍可使用 `highlight`，但不要在 cat-3 卡片後方加同色偏移陰影。

附件中的大面積圖示與對話框使用同一組藍、綠類別色。
不要為每種圖示另建顏色角色；形狀已經提供第二辨識通道。
