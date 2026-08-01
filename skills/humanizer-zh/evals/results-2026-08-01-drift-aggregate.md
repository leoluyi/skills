# 語體漂移 三輪聚合 — humanizer-zh 2.2.0 候選

- new arm: working tree, version 2.2.0（新增第 46 條規則 `語體漂移` ＋ ids 67-71）
- base arm: `3eedd0f`, version 2.1.0
- runner codex `gpt-5.6-luna` / grader claude `claude-opus-5`，三輪同設定
- 保護類失分 2-of-3 才算確認，沿用 `results-2026-08-01-run-case-aggregate.md` 的規約

## 輪次

| # | 報告 | 規則文字狀態 |
|---|---|---|
| r1 | `results-2026-08-01-run-case-r1-drift.md` | 初版規則 |
| r2 | `results-2026-08-01-run-case-r2-drift.md` | 保留條款補「句中處置式標記即授權」「冒號後另起完整句放行」；id 70 的 key 收窄到受測規則 |
| r3 | `results-2026-08-01-run-case-r3-drift.md` | 抓欄改成先找孤懸動詞，找不到就不是本條 |

## 分數

| class | arm | r1 | r2 | r3 | 平均 |
|---|---|---|---|---|---|
| 保護 | new | 99 | 99 | 104 | 100.7 |
| 保護 | base | 104 | 103 | 105 | 104.0 |
| 命中 | new | 62 | 59 | 63 | 61.3 |
| 命中 | base | 61 | 58 | 58 | 59.0 |

分母：保護 115、命中 64（絕對分母 179）。

## 新規則自己的列

| case | expectation | class | r1 | r2 | r3 |
|---|---|---|---|---|---|
| 67 | flags-register-drift | 命中 | new pass / base fail | new pass / base fail | new pass / base fail |
| 67 | fix-names-one-register | 命中 | new pass / base fail | 兩臂皆 fail | new pass / base fail |
| 67 | no-formal-convention-false-positive | 保護 | pass | pass | pass |
| 68 | flags-register-drift | 命中 | new pass / base fail | new pass / base fail | new pass / base fail |
| 68 | fix-picks-one-register | 命中 | pass | new pass / base fail | new pass / base fail |
| 69 | no-template-false-positive | 保護 | pass | **new fail** | pass |
| 69 | does-not-rewrite-in-detect | 保護 | pass | pass | **new fail** |
| 70 | no-weak-signal-stacking | 保護 | **new fail** | pass | pass |
| 70 | no-noun-phrase-item-false-positive | 保護 | **new fail** | pass | pass |
| 71 | 三列 | 保護 | pass | pass | pass |

規則抓得到它要抓的東西：base arm 在 67、68 的命中列三輪全數落空，new arm 三輪全中。保護側每輪掛一列、下一輪修好又換一列，沒有任何一列 2-of-3，屬未確認。

## 確認級的保護誤殺（2-of-3）

| case | expectation | 輪次 | 三輪同因 |
|---|---|---|---|
| 64 | 全域:不代筆 | 3/3 | 改寫時插入括號式編註（「原文是「跟本」喔！」），加進作者沒寫的字 |
| 64 | 全域:保真 | 2/3 | 同上，動到原文引句本身 |
| 57 | preserves-key-figures | 2/3 | 把有兩個數字撐著的結論再標為 `空降主張`、要求加註待確認 |

`64` 那兩列的形狀一致：**新版比 2.1.0 更愛在改寫裡加括號附註**。最可能的來源是 `語體漂移` 的 `改法` 寫著「降格成條目：時程降級成括號附註」——那句是給本規則的降格手段，但讀起來像通用許可。下一輪先改這句的作用域，再重跑。

## no-skill 對照（ids 67-71）

`tools/run-case` 的 base arm 必須展開出至少一個 skill 檔，表達不了 vanilla，因此這一項另跑：同一份 prompt 直接送 runner（無規則集），對照同樣只跑五案的 2.2.0 arm，判分沿用 `run-case` 的 grader brief 與 `判分標準`。逐列結果在
[`results-2026-08-01-vanilla-drift.txt`](results-2026-08-01-vanilla-drift.txt)。

- 19 列中：2.2.0 arm **17 pass**、vanilla **8 pass**
- 67、68 的命中列 vanilla 全數落空——沒有規則時，runner 只說「取得」的主詞不清楚，不會指出語體選擇
- vanilla 另外掛掉三條保真／不代筆列（把「第一次會議」改成「首次會議」、自行補上來源沒有的交付項）

## Gate

**NO-SHIP。** 三列確認級保護誤殺，且保護類平均自 104 退到 100.7。命中類平均進步（59 → 61.3），新規則本身有效，但代價落在既有 rewrite 案上。

下一輪的第一件事是 `改法` 那句括號附註的作用域；`57` 那列要再看一輪才知道是同源還是獨立。
