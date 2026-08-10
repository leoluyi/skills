# briefing — 寬鬆

柔和、寬鬆、線粗。掃讀速度優先。

```yaml
rx: 12
fill: filled
stroke-width: 2.5
depth: hairline
density: loose
routing: orthogonal
arrow: solid
```

**適合**：投影、會議、非技術聽眾。大圓角與寬鬆留白降低密度，
讓聽眾在幾秒內掃完；2.5px 框與實心箭頭撐得住投影衰減。

**代價是面積**。同樣內容比 `console` 多佔約三成畫布——
實測同一份九節點流程，`console` 640×568，`briefing` 816×664。
節點多時考慮拆頁。

低飽和主題在投影機上會比在紙上更淡。場地偏亮時把 `--cat-N-line`
再壓暗一階再交付，並說明這是媒材調整、不是換主題。

可搭配 `solarized-light`、`muted-ledger`、`tailwind-default` 任一主題。

## 這種筆調連帶的節奏

虛線長度隨線寬縮放、斜線紋間距隨密度縮放，公式在 `references/layer-pen.md`。
實際值不在這裡手寫——會與公式漂移。看 `docs/style-reference.html`。
