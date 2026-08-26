# console — 緊湊

方正、緊湊、線細。資訊密度優先。

```yaml
rx: 4
fill: filled
stroke-width: 1.5
depth: hairline
density: tight
routing: orthogonal
arrow: open
```

**適合**：技術文件、螢幕閱讀、節點多的長流程。技術讀者願意近距離看，
不需要寬鬆留白。微圓角與細框把視覺重量壓到最低，讓節點文字成為主角。

**不適合投影**：1.5px 細框在投影機上會消失，改用 `briefing`。

可搭配 `solarized-light`、`muted-ledger`、`tailwind-default` 任一主題。

## 這種筆調連帶的節奏

虛線長度隨線寬縮放、斜線紋間距隨密度縮放，公式在 `references/layer-pen.md`。
實際值不在這裡手寫——會與公式漂移。看 `docs/style-reference.html`。
