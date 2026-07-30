# Design notes — avoid-ai-writing-zh

Maintainer notes — provenance and build process for this one skill.

## What this skill is, structurally

A zh-first bilingual skill with **one** canonical rule set. A rule carries both its Chinese and its English manifestation rather than living twice in two parallel catalogs.

```
SKILL.md                      — 110 lines: routing, the six-step spine, the shared vocabulary, severity, profiles
references/
  zh-rules.md                 — all 45 rules under the 8 classes, each with 抓 / 保留 / a before-after pair
  en-rules.md                 — the English manifestations, keyed to the same 8 classes
  structure-signals.md        — the detect-only 結構級訊號 aggregate: gate, threshold, 5 sub-signals
  zh-phrase-rules.md          — the seven zh「詞→替換」lookup tables (data, not rules)
  examples.md                 — 5 worked end-to-end scenarios (synthetic samples)
```

**The split rule.** `SKILL.md` holds what every branch needs; a reference file holds what only some branches reach. Language selects `zh-rules.md` or `en-rules.md`; the structure-signals route selects `structure-signals.md`; rewrite mode reaches `examples.md`. Pointer *wording* is the reliability risk, not pointer targets — if disclosed material under-fires, sharpen the pointer before pulling anything back inline.

## The 2.0.0 rewrite (2026-07-29/30)

1.5.0 was a fork of the English-only `avoid-ai-writing` by Conor Bronsdon, with a zh layer bolted on. It reached 966 lines against a 500-line ceiling and carried ~79 named rule surfaces, roughly half exercised by neither test instrument; 46 of 51 English headings had no 繁中 twin. At the same time 14 of 42 tagged eval cases were marked `（缺口`— no rule existed for them, so they passed vacuously. Overgrown and under-covered at once: re-carving fixes both, trimming fixes only one.

2.0.0 deletes the inherited English catalog and `references/english-phrase-rules.md` outright, ends the fork relationship (the directory `LICENSE` and the upstream `metadata.author` go with it), and rebuilds on `corpus.md`'s own **8 defect classes + 2 orthogonal mechanisms** — a taxonomy that was already tagged on all 32 corpus cases and 42 of 54 eval cases before the rewrite started, so the test data did not have to be re-invented to fit it.

**Sequencing that mattered:** taxonomy first, re-tag the test data, then write prose. Re-tagging touched labels only — every `flag`/`ok` verdict, every quoted span and every prompt stayed byte-identical, because a changed verdict silently rewrites the baseline and destroys the A/B.

**Consolidations worth remembering.** `結構級訊號` had three surface forms and `打破第四面牆` two; sub-signals are now always written `結構級訊號／<name>` and never as sibling rules. Two English/Chinese pairs turned out to name one defect each — `全文無立場` ≡ `Missing first-person perspective` → **立場真空**, and `只解釋不造像` ≡ `no original metaphor` → **只解釋不造像**. The old `Rhythm and uniformity` label was doing two unrelated jobs (genre uniformity in a spec vs voice absence in a blog); those separated into **節奏均質** and **立場真空**.

**Rules that did not survive:** curly quotation marks, immaculate typography in casual registers, wall-of-text replies, title-case headings, hyphenated-pair overuse. Each was either a pure false-positive surface, an English orthographic nit with no zh applicability, or already covered elsewhere. Roughly thirty further names were *merged* rather than cut — each is named as a form inside its new parent's trigger, so the detection knowledge survives even where the heading did not.

## No runtime scripts — a deliberate, revisitable decision

A phrase-scanner script was considered and rejected. Evidence: no runtime detection script exists in any of the four surveyed humanizer/skill projects; Codex's own guidance prefers instructions over scripts unless determinism is required; and this skill's observed failures are all judgment-tier, not lookup-tier, so a word-list scanner would not have caught them. `uv` is also not a safe runtime assumption — it is preinstalled only in Codex cloud images, not on a developer's machine.

Revisit only if a real 詞表層漏抓 shows up in the evals. Dev-side tooling is a different question and is welcome: `tools/check-labels` ships with this round.

## External sources drawn on

Attribution obligations are recorded in `NOTICE`; this section is the *why*.

- **speak-human-tw** — https://github.com/Raymondhou0917/speak-human-tw (MIT). Three separate uses, deliberately distinguished: (1) the 翻譯腔 entries in `zh-phrase-rules.md` are our own rewrite informed by its `taiwan-localization.md`; (2) `evals/evals.json` ids 15–54 are a *verbatim* adaptation of 40 of its 42 benchmark cases, with added structural fields — a different kind of use, so it gets its own NOTICE line; (3) the six-step procedure and the 保護清單 mechanism follow its design. SF-14/SF-15 (中國用語／半形標點) were excluded as `avoid-china-writing`'s axis.
- **blader/humanizer** and **x-humanizer** (both MIT) — pattern inventories distilled for `en-rules.md`. Conceptual distillation, re-classified into the 8 classes and rewritten; no prose copied.

## Research notes (dev material, not runtime)

`research/` holds faithful distillations of outside source material for authoring reference. **Dev/authoring material, not runtime** — they carry provenance headers and source citations, and must not be surfaced into `SKILL.md` or `references/`. If a distillation later informs a shipped rule, promote a provenance-stripped extract into the rule body and add attribution here and in `NOTICE`.

- **`research/ai-sentence-patterns-zh.md`** — distillation of 朱宥勳〈對「AI腔」厭煩了嗎？〉(YouTube, 2026-01-30). Centres on 「這不是⋯⋯而是⋯⋯」— now covered by **對比句式**.
- **`research/wikipedia-ai-signs-zh.md`** — distillation of Wikipedia's AI-writing signs.
- **`research/research-humanizer-landscape-2026-07-29.md`** — primary-source survey of Anthropic skill-authoring guidance and three humanizer projects; the basis for the no-runtime-scripts decision, the `research/` vs `references/` placement rule, and the two-layer examples design.

## Test instruments

Three files, none replacing another:

| file | answers |
|---|---|
| `evals/corpus.md` | on real text, which span should be flagged and which must not |
| `evals/evals.json` | given a prompt, does the skill behave as expected |
| `evals/judged-cases.md` | why a given rule is shaped the way it is |

`tools/check-labels` validates both instruments against the rule names the skill actually declares (derived from `zh-rules.md` headings and `structure-signals.md`, so there is no separate manifest to drift), plus the corpus 解析契約 — every 引文片段 must be an exact substring of its clean quote, `全文` excepted.

## Adversarial iteration log (rule-tuning rounds)

The method lives in `evals/adversarial-eval-protocol.md`. Each row = one GAN-style round; the `eval #N` in the Patch column maps to `id: N` in `evals/evals.json`.

| 日期 | 真人桶 | AI 桶 | FP / recall | 主要發現 | Patch |
|---|---|---|---|---|---|
| 2026-07-17 | 5 篇：觀點（高見龍）、教學（保哥/miniasp）、newsletter（倉鼠）、docs（工程會使用手冊）、公文規格（工程會資安要求） | 3 篇自生 zh-TW voiceless 文（觀點／教學／分析，無 Tier-1 詞級病句） | voice-bearing 真人 FP=0/3；voice-neutral 若誤啟用 FP=2/2；AI recall=3/3 | (1) 判準應為 voice-bearing vs voice-neutral，非 blog vs 非 blog——真人觀點/教學/newsletter 穩定帶齊 stance/specifics/metaphor/口語破格；docs/公文本就均質須維持排除。(2) AI voiceless 文常無詞級病句，詞表會漏標，結構層才抓得到（層的價值驗證）。(3) 密集教學文（保哥）缺自創比喻卻為真人 →『只解釋不造像』不可單獨觸發。樣本小（n=3/3），round 2 應擴語料。 | gating 從 casual-only 擴為 voice-bearing 文體集；只解釋不造像加 technical-blog 成群才觸發 carve-out；eval #3 #4 |
| 2026-07-20 | n/a（此輪測 rewrite 機制而非 detect gating，非真人桶對照） | 1 組合成 prompt：docs 語境三句連續教練口吻段（含實質內容）＋一段扣除語氣後無實質內容 | rewrite-mode baseline vs new，非 FP/recall 指標 | span-local baseline 在無實質內容段落捏造了原文沒有的主張以避免留空；new 版正確輸出挖空標記句、不代筆。含實質內容段落兩版皆寫出連貫第三人稱改寫，此樣本未能區分 no-residual-seam 這一半。 | 新增 scope 階梯＋兩條硬規則（reframe-not-delete、flag-hollow-don't-ghostwrite）；eval #6 |
| 2026-07-28 | 合成保護桶 6 段 | 合成病灶桶 2 段，皆為零可查核事實 | 首輪 FP 3/18、recall 6/6；修正後 FP 0/18、recall 6/6 | 四字評語規則初版把判準寫成「刪掉這四個字少了什麼事實」，agent 逐詞判恆為「沒有」，於是成語旁已寫滿具體內容的公文／docs 也被誤殺。病灶是判準作用域錯置：成語本身永不帶事實，該問的是成語所形容之事有無寫在鄰句。 | 判準改為段落級＋三條分支；carve-out 增列公文與技術文件總結語；eval #10 #11 #12 |
| 2026-07-28（語料階段） | H 桶 20 篇（見 `evals/corpus.md`） | A 桶 12 篇（8 篇對齊 H 例主題、4 篇 voiceless 探針） | 未跑分——本輪只建語料與 baseline | 建語料本身即發現兩個規則缺口：罐頭式反應鏡頭、幻覺引用查證。 | 無 patch |
| 2026-07-29/30（2.0.0 重寫） | H 桶 20 篇（`corpus.md` 52 個 `ok` 列） | A 桶 12 篇（37 個 `flag` 列） | 見 `evals/results-2026-07-29-corpus-baseline-1.5.0.md` 與 `results-2026-07-30-v2-ab.md` | 1.5.0 在 corpus 上是 89/89 滿分——所以 corpus 這一輪的角色是回歸偵測器，不是進步的證據；進步要由 evals.json 的 14 個 `（缺口` 案例證明。 | 全面重寫至 2.0.0 |

## 判別問題形狀（沿用中的寫作原則）

移植 speak-human-tw 案例時確認的一點，2.0.0 已據此改寫：**規則的判準壓成一句可以直接拿去問 agent 的判別問題**，而不是一段散文說明。「這個詞是使用還是提及？」比「判準：⋯⋯」加三行解釋緊湊得多，也更容易在 carve-out 上分岔。

## Trigger-query 診斷更正（2026-07-19 resweep 的 id 3／id 10）

`backlog.md` 記錄的「id 3、id 10 兩個未分診的 fail」**指的是 `evals/trigger-queries.json` 的 query id**（router 觸發判斷），不是 `evals.json` 的內容品質 case——兩份檔案剛好都有 id 3 與 id 10。兩條在 1.5.0 的 description 下即已判 TRIGGER，2026-07-28 用修好的 `tools/run-eval` 實測 10/10 確認。

**殘留風險。** id 3 的 query 含「blog intro」，與 description 結尾排除句的「blog」字面相鄰，router 可能被字面誤導去分流到 `blog-writing-zh`。2.0.0 改寫 description 時保留了該排除句（它是必要的邊界宣告），並把開頭改成「language-layer cleanup pass」，讓職責分界不只靠結尾那一句承擔。改寫後 10/10 仍全過，含 id 3 與 id 9（RFP structural authoring 的負例）。
