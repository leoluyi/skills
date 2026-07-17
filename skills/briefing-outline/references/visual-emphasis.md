# Visual emphasis layer (optional, render-pipeline only)

A post-draft layer that marks a finished 提綱 so a 主管 can read from it aloud or scan it fast. Apply **only** when the output runs through a render pipeline (pandoc → PDF/HTML) whose CSS carries the classes below, and the occasion is a formal briefing. This layer is pure addition and the fastest way to wreck a 提綱's scannability — stay **sparse**: when in doubt, mark less.

Iron rule: **wrap, never edit.** Every mark is `[原文]{.class}` — never alter a character of the wrapped text.

Keep each section's `>` essence line **unmarked** — it is already the section's emphasis layer; a highlight on top is 疊床架屋.

## Three marks

**Yellow anchor `.k`** — sparse keyword anchors. Five categories only, nothing else: ①數字與規模 (80 人、6.3 萬缺口、12 個月) ②關鍵技術名詞 (Kubernetes、RAG、CKA/CKAD) ③關鍵活動 (故障排查、Demo、版本發布與回復) ④關鍵 stakeholder (學校、合作企業名) ⑤專有名詞 already marked in the umbrella source. **At most 2–3 per `###`**; when a section is full, swap out the weaker mark rather than stack. A section with no qualifying term (人格特質面試、委員會職掌) stays blank — don't hunt for something to mark. Confirm 活動 marks, and any change to an existing keyword, with the user first.

**Blue field `.kb`** — a definitional field's content: the whole span after the colon (規格門檻、情境、元件清單、治理項目). Lets the 主管 read the full spec in one glance. If a span goes blue, drop any yellow anchor inside it — one field, one colour.

**Black label-box `.bx`** — a definitional field's label: the text before the colon, paired with the blue field after it. Box only a **label**, never a sentence — box when the colon is followed by a 條列 (、-separated items) or a short value (校系：資訊工程、資訊管理…); leave it unboxed when the colon closes a narrative sentence (情境：文件服務由 1.2.0 升版後間歇性失敗…／要驗證：學員能…). Never box inside a 表格、標題、or `>` line. A label that is already yellow-anchored nests cleanly: `[容器[故障排查]{.k}]{.bx}`.

## A/B/C on parallel groups

Prefix a parallel `###` group that carries no number of its own (師資三類、三門課、三題型) with `A.` `B.` `C.`, restarting per group. Skip any group already numbered (來源一／來源二、專案一／專案二) — a second number 打架.

## CSS

Add these three classes to the render pipeline's stylesheet. A full working A4 print stylesheet that already carries them sits at `references/report.css`.

```css
/* yellow anchor: fill only the lower band of the glyph, bold, navy */
.k  { background: linear-gradient(180deg, transparent 60%, #ffe9a8 60%);
      padding: 0 1pt 4pt; font-weight: 600; color: #12336e;
      box-decoration-break: clone; -webkit-box-decoration-break: clone; }
/* blue field: full definitional span, no bold for long lines */
.kb { background: linear-gradient(180deg, transparent 60%, #b8e5fa 60%);
      padding: 0 1pt 4pt;
      box-decoration-break: clone; -webkit-box-decoration-break: clone; }
/* black label-box */
.bx { border: 1px solid #232830; border-radius: 2px; padding: 0 3pt; white-space: nowrap; }
```

## Apply flow

Draft the 提綱 first; only then judge whether this layer is warranted. If it is, mark **one section as a sample**, show the user, confirm density and colour, then roll out. Blank software/governance sections are a correct outcome, not a gap to fill.
