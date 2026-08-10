# Gridline Studio — 網格工作室

取自 Enterprise AI Architecture 系列投影片的共通視覺語彙：暖白網格紙、藍黑主字、亮藍焦點，以及藍、綠、琥珀、紫四色卡片。
珊瑚紅只保留給警示與風險，不列入一般類別。

**適用**：技術簡報、架構導讀、需要強烈標題與清楚階段卡片的螢幕投影片。
**不適用**：黑白影印、低彩度正式文件，或需要五個以上一般類別的圖。

```text
mode: standard
```

> 預設階梯 region 4／card 10／card-sub 16

## Base 值

```css
:root{
  --cat-1-base:  #1E4CA2;   /* 深藍 */
  --cat-2-base:  #488867;   /* 網格綠 */
  --cat-3-base:  #D68C0E;   /* 琥珀 */
  --cat-4-base:  #BCACEA;   /* 淡紫 */
  --cat-s-base:  #DD5145;   /* 珊瑚紅，只用於 warning／issue 等異常狀態 */
  --infra-base:  #697078;
  --terminal:    #080E18;
  --ink-strong:  #171C25;
  --ink-muted:   #5F6368;
  --canvas-white: #FFFFFF;
  --canvas-tint:  #FBFAF6;   /* 暖白網格紙底 */
  --accent:      #2764D6;   /* 亮藍，供關鍵字、標題引導線與 hero */
  --highlight:   #F1D66A;   /* 黃色畫記，只供圖表 highlight */
}
```

字型：`"Noto Sans CJK TC", "Noto Sans TC", "PingFang TC", "Microsoft JhengHei", sans-serif`

類別灰階明度為 **8 / 20 / 33 / 46**，依投影片流程順序遞增。
原圖中的藍、綠、琥珀、紫保留色相，但重新排列明度，讓四個類別在灰階下仍有至少 10 點間距。

## 投影片語意

主字體使用藍黑 `ink-strong`。
關鍵字、標題區塊引導線與大標數字／hero 共用亮藍 `accent`，由推導器針對所選 canvas 解出 `--slide-emphasis`。
珊瑚紅只映射 `cat-s`，用於警示、風險、失敗或需要處理的問題；正常焦點仍使用亮藍。

## 陷阱

琥珀類別與黃色 `highlight` 色相接近。
底線式文字畫記仍可使用 `highlight`，但不要在 cat-3 卡片後方加同色偏移陰影，否則會被讀成類別延伸而非強調。

背景網格是筆調或媒材效果，不屬於顏色 token。
只使用 `canvas-tint` 不會自動產生格線；需要格線時由 SVG pattern 或投影片背景另外實作。
