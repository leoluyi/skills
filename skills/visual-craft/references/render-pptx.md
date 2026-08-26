# PPTX — 簡報媒材對映

角色相同，實作不同。本檔只講 PPTX 怎麼畫；角色定義在 `roles.md`。

檔案操作（解壓、改 XML、重壓、驗證）用 `pptx` skill，本檔不重複。

---

## 鐵則：重繪只碰格式，不碰文字

PPTX 的重繪特別容易誤改文字，因為最順手的 API 就是覆寫整個文字框。

- **python-pptx**：只寫 `run.font.*`、`shape.fill`、`shape.line`。
  **絕對不要寫 `text_frame.text`**——那不只會覆寫文字，還會把段落塌成單一無格式 run，
  原本的粗體、換行、混排全部消失。要改格式就逐 run 改 `run.font`，`run.text` 一律不碰。
- **直接改 XML**：只動 `<a:rPr>`（run 屬性）、`<a:solidFill>`、`<a:ln>`。
  `<a:t>` 內的字元一個都不動。
- **pptxgenjs**：只用於從零產生。重繪既有簡報一律走「解壓改 XML」路線，
  因為重新產生等於重打一次所有文字，那正是最容易出錯的地方。

**自我檢查**：如果你的程式碼裡出現任何指派文字內容的敘述，那就是 bug。
重繪的 diff 應該只有格式屬性。

---

## 角色對映

### 文字角色 → PPTX

| 角色 | 實作 |
|---|---|
| `text/title` | 版面既有的標題佔位符，只改 `run.font.size` / `bold` / `color` |
| `text/section` | 區塊標題文字框 |
| `text/body` | 圖形內文字，`margin: 0` 才能與圖形邊緣對齊 |
| `text/support` | 同 body 但小一級，用較淡的色而非透明度 |
| `text/caption` | 頁尾、來源標註 |
| `text/inverse` | 深色圖形上的白字 |

**PPTX 沒有可靠的文字透明度。** `text/support` 在 SVG 用 62% 不透明度，
在 PPTX 要換算成實色——把 `ink-strong` 對 `canvas` 混到 62% 再取 hex。
`derive.py` 的 `mix()` 可以直接算。

**文字框有內建內距。** 要讓文字與圖形邊緣對齊時 `margin: 0`，
否則所有節點標籤會整體偏移，看起來像沒對齊格線。

### 表面角色 → PPTX

| 角色 | 圖形 | 備註 |
|---|---|---|
| `surface/object` | `ROUNDED_RECTANGLE` | **`rectRadius` 只在圓角矩形有效**，一般矩形設了無效 |
| `surface/part` | `ROUNDED_RECTANGLE` | 半徑小一階 |
| `surface/region` | `RECTANGLE` 置底 | 加左側細長矩形當色條 |
| `surface/annotation` | `ROUNDED_RECTANGLE` 無填色 | 點線外框 |
| `surface/infra` | `RECTANGLE` 全寬 | 中性色 |
| `surface/terminal` | `ROUNDED_RECTANGLE` 實心 | 白字 |
| `surface/datasource` | `CAN`（圓柱預設圖形） | 不要自己畫路徑，PowerPoint 有原生的 |
| `surface/gate` | 圓角矩形 + 內縮第二個無填色矩形 | PPTX 沒有雙線邊框 |
| `surface/external` | `ROUNDED_RECTANGLE` 虛線框，照常填色 | |
| `state/planned` | `ROUNDED_RECTANGLE` 虛線框，`fill.background()` | 無填色是與 external 的唯一差別 |
| `state/deprecated` | `ROUNDED_RECTANGLE` ＋ 圖樣填色 | 見下 |

### 線條角色 → PPTX

PPTX 的虛線是**列舉值**，不是自訂 dash array。對映如下：

| 角色 | PPTX `prstDash` |
|---|---|
| `line/flow` | `solid` |
| `line/control` | `dash` |
| `line/reference` | `lgDash` |
| `line/leader` | `sysDot` |
| `line/optional` | `dashDot` |
| `line/boundary` | `sysDot` |

`sysDot` 是最接近 SVG `2 3` 點線的值，與 `dash` 在視覺上分得開——
**機制用 dash，非機制用 dot** 這條規則在 PPTX 一樣成立。

---

### deprecated 的斜線紋

PPTX 有原生圖樣填色（`patternFill`），不要疊兩個圖形。`ltUpDiag`（稀疏上斜線）
最接近本 skill 的 45° 疏紋：

```xml
<a:pattFill prst="ltUpDiag">
  <a:fgClr><a:srgbClr val="8A8F96"/></a:fgClr>
  <a:bgClr><a:srgbClr val="EFEFEF"/></a:bgClr>
</a:pattFill>
```

python-pptx 沒有包裝 `patternFill`，要直接改 XML。
**不要改用 `dkUpDiag`**（密上斜線）——密到會被讀成實心填色，
也就被讀成另一個類別。

## PPTX 特有的坑

- **色碼不帶 `#`，不用 8 位數。** `"FF0000"` 正確；`"#FF0000"` 與把透明度寫進 hex
  都會**損毀檔案**。要半透明用 `transparency: 0-100`。
- **沒有漸層填色支援**（pptxgenjs）。本 skill 本來就只用平色，不受影響。
- **陰影 offset 不可為負**，會損毀檔案。要往上打陰影用 `angle: 270` 配正的 offset。
  `tailwind` preset 的 `depth: shadow` 在 PPTX 要注意這點。
- **投影會吃掉細線。** `stroke-width: 1` 的 `bootstrap`／`tailwind` preset
  在投影機上邊框幾乎看不見。簡報媒材優先用 `briefing`，
  或把線寬提到 2 以上並在交付時說明這是媒材調整、不是換 preset。
- 改完一定跑 `pptx` skill 的 `scripts/office/validate.py`。

---

## 交付前核對

除了 `SKILL.md` 的共通核對，PPTX 另外要比對**文字逐字相同**：

```bash
markitdown before.pptx > /tmp/a.txt
markitdown after.pptx  > /tmp/b.txt
diff /tmp/a.txt /tmp/b.txt
```

**diff 必須為空。** 有任何一行差異就是動到文字了，回頭找。
這是本 skill 在 PPTX 上最重要的一道閘門，比任何視覺檢查都優先。
