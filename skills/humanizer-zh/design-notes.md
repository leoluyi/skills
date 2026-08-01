# Design notes — humanizer-zh

Maintainer notes — provenance and build process for this one skill.

## What this skill is, structurally

A zh-first bilingual skill with **one** canonical rule set. A rule carries both its Chinese and its English manifestation rather than living twice in two parallel catalogs.

```
SKILL.md                      — 114 lines: routing, the six-step spine, the shared vocabulary, severity, profiles
references/
  zh-rules.md                 — all 46 rules under the 8 classes, each with 抓 / 保留 / a before-after pair
  en-rules.md                 — the English manifestations, keyed to the same 8 classes
  hidden-author.md            — the detect-only 作者隱身 aggregate: gate, threshold, 5 sub-signals
  zh-phrase-rules.md          — the seven zh「詞→替換」lookup tables (data, not rules)
  examples.md                 — 6 worked end-to-end scenarios (synthetic samples)
```

[`docs/humanizer-zh.md`](../../docs/humanizer-zh.md) is the **user-facing** companion to this file: what the skill does to a draft, why a 公文 report says 「作者隱身不適用」 and still carries five flags, when to reach for `--expect-author`. Keep measurements, provenance and the reasoning behind a split here; keep behaviour-as-experienced there.

## 語體漂移 — 一條 provenance 判準被拆成 surface 判準 (2026-08-01)

規則的來源是作者提供的一句真實工作文字：「預期產出與時程：助教人力配置方案與 Lab 支援範圍，訪談後 3 至 4 週內取得。」句法上它同時想當條列標題與完整句子——前半名詞組無謂語，唯一的動詞卡在句末、跨過一個逗號回頭管前面的賓語，中間沒有任何授權前置的標記。

**作者原本要編碼的判準有三項，只有第一項照原形進了 skill。**

第二項是「缺陷與完成度不匹配」：人的失誤是減法（漏字、漏主詞、標點不一致），AI 的失誤是骨架歪掉但零件樣樣俱全，因此組裝感與高完成度同時出現才是決定性訊號。這句話問的是**誰寫的**，而 `SKILL.md` 的〈What this skill is and isn't〉明文只判 surface、不判 provenance。照字面寫成命中門檻，skill 就開始做它拒絕做的主張。處置是把它翻面：**組裝感伴隨完成度下降時放行**，寫進 `語體漂移` 的保留條款。非母語寫作、翻譯體、多來源剪貼因此照樣被保護，而規則一句話都沒說作者是誰。`backlog.md` 的 (H) 雙軸評分閘沒有放行，仍等盲測資料。

第三項是「結構訊號權重高於內容訊號」。它不屬於任何單一規則——內容可以從表格、模板或來源文件繼承，語法是當場生成的——所以落在 `SKILL.md` 步驟 4 的一行，而不是第 47 條規則。

**判準本身沒有證據支撐，這一點要說清楚。** 三項判準全部出自 2026-08-01 一場非盲測的 annotate session：判讀者知道答案，中途又拿到一份人寫的對照改寫。落地的理由是第一項屬 surface、可由既有的 run-case 儀器直接量測，不是那場 session 證明了什麼。

**量測結果：三輪 NO-SHIP。** 數字在 `evals/results-2026-08-01-drift-aggregate.md`。規則抓得到目標——ids 67、68 的命中列三輪都是新版過、2.1.0 落空，vanilla 對照也是 17:8——但保護類平均從 104 掉到 100.7，且 `64/全域:不代筆` 三輪皆失、`64/全域:保真` 兩輪失。兩者同因，而那個因很值得記著：**規則的 `改法` 寫了「降格成條目：時程降級成括號附註」，模型把它讀成了通用許可，在別的 rewrite 案裡也開始加括號編註**。一條寫給單一規則的改法手段，會外溢成整個 rewrite 模式的習慣——這是 `改法` 行第一次被觀察到有這種作用域外洩，下次寫任何 `改法` 都要把手段綁在該規則的形態上。

**保護側的失分每輪換一列，這件事本身是訊號。** r1 掛 id 70 的兩列、r2 掛 id 69 的欄位案、r3 掛 id 69 的另一列，改一次規則文字就換一個位置，沒有一列 2-of-3。單輪不足以定位一條新規則的誤判面，這是 aggregate 規約在這輪的第二個實例。

**邊界。** 與 `過度簡寫` 的分界是缺零件 vs 零件齊全而語體沒選定（該條的保留欄含「公文與法律的標準句架」，會直接放行本規則要抓的形態，所以兩邊互指）；與 backlog 已立案的 `體裁相稱` 候選規則的分界是句內 vs 篇章級語域。

## 文體類 and the two carve-out lists (2026-07-30)

The genre axis exists to gate exactly one rule, `作者隱身`, and nothing else. Three defects were fixed together in this round, all of them the same disease — a distinction stated in one file and contradicted in another.

**The flag's semantics were never settled.** `structure-signals.md` said `--structure-signals` was an override that forces the audit on any genre and reports anyway; `evals.json` ids 13/14 said the same flag must NOT trigger the audit on a 事務文體. Three graders scoring the same runner output reached three verdicts because the instrument and the skill disagreed, not because the runners differed. Resolved by making the flag a *genre declaration*: `--expect-author` sets the verdict to 署名文體 and the audit then runs normally, so there is no "ran it but everything found is genre-correct" state to describe. ids 13/14 dropped the flag from their prompts and became pure gate-default protection cases with their expectations untouched; ids 55/56 carry the identical text plus the flag, so the flag is the only variable between the pairs.

**The exclusion read as a blanket pass.** Nothing stated that the 事務文體 exclusion covers one rule, and the only worked 公文 example in the skill (`examples.md` 例 2) ends 「未發現須修改之處」. Every available signal pointed at 公文 → 沒事. Fixed with an explicit routing conditional in `hidden-author.md` (〈The exclusion stops here〉), a one-line restatement in `SKILL.md` step 1, and `examples.md` 例 3 — same genre, same mode, opposite outcome.

**`立場真空` and `作者隱身` had copy-pasted carve-out lists.** They should never have matched. 立場真空 asks whether the author exercised *judgement*; 作者隱身 asks whether the author is *present*. A 建議書 owes the reader the first and not the second, so 規劃書/建議書/計劃書/investor-email now sit inside 事務文體 (no 作者隱身 — a formal proposal has no colloquial breaks or rhythm variation by construction) while being removed from 立場真空's shorter carve-out list (a proposal that recommends nothing is exactly what that rule is for). 公文/簽呈 stay in both lists: the 擬辦 line is that genre's form of taking a position.

**Naming.** `結構級訊號` → `作者隱身` and `voice-bearing/voice-neutral` → `署名文體/事務文體`, on the maintainer's report that the old terms were unreadable. Two constraints shaped the result. The genre term must not imply a lower bar — 「不需要人味的文體」 was rejected mid-round for exactly that, since plain wording persuades in a way jargon does not, and it would have persuaded readers that a 公文 needs no de-AI-ing at all. And the rule name must not collide with the genre name: 隱身 (by design) belongs to one of them only, which is why the genre moved to 署名/事務 rather than the rule moving off 隱身.

**Default trigger.** `作者隱身` previously needed a routing condition (user complains the draft reads machine-written) *or* the flag, and then the genre gate on top. Two layers written in two files, and the net effect was that the check was off by default for an ordinary blog audit. Collapsed to one: the genre verdict is the whole trigger. Rejected alternative — running it everywhere unless explicitly excepted — would invert the skill's largest false-positive guard and break the zero-tolerance protection bar; the 2026-07-17 row below measured 事務文體 誤啟用 at FP 2/2.

**The split rule.** `SKILL.md` holds what every branch needs; a reference file holds what only some branches reach. Language selects `zh-rules.md` or `en-rules.md`; the 作者隱身 route selects `hidden-author.md`; rewrite mode reaches `examples.md`. Pointer *wording* is the reliability risk, not pointer targets — if disclosed material under-fires, sharpen the pointer before pulling anything back inline.

## The 2.0.0 rewrite (2026-07-29/30)

1.5.0 was a fork of the English-only `avoid-ai-writing` by Conor Bronsdon, with a zh layer bolted on. It reached 966 lines against a 500-line ceiling and carried ~79 named rule surfaces, roughly half exercised by neither test instrument; 46 of 51 English headings had no 繁中 twin. At the same time 14 of 42 tagged eval cases were marked `（缺口`— no rule existed for them, so they passed vacuously. Overgrown and under-covered at once: re-carving fixes both, trimming fixes only one.

2.0.0 deletes the inherited English catalog and `references/english-phrase-rules.md` outright, ends the fork relationship (the directory `LICENSE` and the upstream `metadata.author` go with it), and rebuilds on `corpus.md`'s own **8 defect classes + 2 orthogonal mechanisms** — a taxonomy that was already tagged on all 32 corpus cases and 42 of 54 eval cases before the rewrite started, so the test data did not have to be re-invented to fit it.

**Sequencing that mattered:** taxonomy first, re-tag the test data, then write prose. Re-tagging touched labels only — every `flag`/`ok` verdict, every quoted span and every prompt stayed byte-identical, because a changed verdict silently rewrites the baseline and destroys the A/B.

**Consolidations worth remembering.** `作者隱身` had three surface forms and `打破第四面牆` two; sub-signals are now always written `作者隱身／<name>` and never as sibling rules. Two English/Chinese pairs turned out to name one defect each — `全文無立場` ≡ `Missing first-person perspective` → **立場真空**, and `只解釋不造像` ≡ `no original metaphor` → **只解釋不造像**. The old `Rhythm and uniformity` label was doing two unrelated jobs (genre uniformity in a spec vs voice absence in a blog); those separated into **節奏均質** and **立場真空**.

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

`tools/check-labels` validates both instruments against the rule names the skill actually declares (derived from `zh-rules.md` headings and `hidden-author.md`, so there is no separate manifest to drift), plus the corpus 解析契約 — every 引文片段 must be an exact substring of its clean quote, `全文` excepted. Since 2026-07-30 the extraction is declared in `evals/label-check.json` rather than hardcoded in the tool, which is also what makes the gate opt-in for other skills; that file names the *files and regexes*, never the rule names, so the no-drift property is unchanged.

## Adversarial iteration log (rule-tuning rounds)

The method lives in `evals/adversarial-eval-protocol.md`. Each row = one GAN-style round; the `eval #N` in the Patch column maps to `id: N` in `evals/evals.json`.

| 日期 | 真人桶 | AI 桶 | FP / recall | 主要發現 | Patch |
|---|---|---|---|---|---|
| 2026-07-17 | 5 篇：觀點（高見龍）、教學（保哥/miniasp）、newsletter（倉鼠）、docs（工程會使用手冊）、公文規格（工程會資安要求） | 3 篇自生 zh-TW voiceless 文（觀點／教學／分析，無 Tier-1 詞級病句） | 署名文體 真人 FP=0/3；事務文體 若誤啟用 FP=2/2；AI recall=3/3 | (1) 判準應為 署名文體 vs 事務文體，非 blog vs 非 blog——真人觀點/教學/newsletter 穩定帶齊 stance/specifics/metaphor/口語破格；docs/公文本就均質須維持排除。(2) AI voiceless 文常無詞級病句，詞表會漏標，結構層才抓得到（層的價值驗證）。(3) 密集教學文（保哥）缺自創比喻卻為真人 →『只解釋不造像』不可單獨觸發。樣本小（n=3/3），round 2 應擴語料。 | gating 從 casual-only 擴為 署名文體 文體集；只解釋不造像加 technical-blog 成群才觸發 carve-out；eval #3 #4 |
| 2026-07-20 | n/a（此輪測 rewrite 機制而非 detect gating，非真人桶對照） | 1 組合成 prompt：docs 語境三句連續教練口吻段（含實質內容）＋一段扣除語氣後無實質內容 | rewrite-mode baseline vs new，非 FP/recall 指標 | span-local baseline 在無實質內容段落捏造了原文沒有的主張以避免留空；new 版正確輸出挖空標記句、不代筆。含實質內容段落兩版皆寫出連貫第三人稱改寫，此樣本未能區分 no-residual-seam 這一半。 | 新增 scope 階梯＋兩條硬規則（reframe-not-delete、flag-hollow-don't-ghostwrite）；eval #6 |
| 2026-07-28 | 合成保護桶 6 段 | 合成病灶桶 2 段，皆為零可查核事實 | 首輪 FP 3/18、recall 6/6；修正後 FP 0/18、recall 6/6 | 四字評語規則初版把判準寫成「刪掉這四個字少了什麼事實」，agent 逐詞判恆為「沒有」，於是成語旁已寫滿具體內容的公文／docs 也被誤殺。病灶是判準作用域錯置：成語本身永不帶事實，該問的是成語所形容之事有無寫在鄰句。 | 判準改為段落級＋三條分支；carve-out 增列公文與技術文件總結語；eval #10 #11 #12 |
| 2026-07-28（語料階段） | H 桶 20 篇（見 `evals/corpus.md`） | A 桶 12 篇（8 篇對齊 H 例主題、4 篇 voiceless 探針） | 未跑分——本輪只建語料與 baseline | 建語料本身即發現兩個規則缺口：罐頭式反應鏡頭、幻覺引用查證。 | 無 patch |
| 2026-07-29/30（2.0.0 重寫） | H 桶 20 篇（`corpus.md` 52 個 `ok` 列） | A 桶 12 篇（37 個 `flag` 列） | 見 `evals/results-2026-07-29-corpus-baseline-1.5.0.md` 與 `results-2026-07-30-v2-ab.md` | 1.5.0 在 corpus 上是 89/89 滿分——所以 corpus 這一輪的角色是回歸偵測器，不是進步的證據；進步要由 evals.json 的 14 個 `（缺口` 案例證明。 | 全面重寫至 2.0.0 |

## 判別問題形狀（沿用中的寫作原則）

移植 speak-human-tw 案例時確認的一點，2.0.0 已據此改寫：**規則的判準壓成一句可以直接拿去問 agent 的判別問題**，而不是一段散文說明。「這個詞是使用還是提及？」比「判準：⋯⋯」加三行解釋緊湊得多，也更容易在 carve-out 上分岔。

## Trigger-query 診斷更正（2026-07-19 resweep 的 id 3／id 10）

`backlog.md` 記錄的「id 3、id 10 兩個未分診的 fail」**指的是 `evals/trigger-queries.json` 的 query id**（router 觸發判斷），不是 `evals.json` 的內容品質 case——兩份檔案剛好都有 id 3 與 id 10。兩條在 1.5.0 的 description 下即已判 TRIGGER，2026-07-28 用修好的 `tools/run-eval` 實測 10/10 確認。

**殘留風險。** id 3 的 query 含「blog intro」，與 description 結尾排除句的「blog」字面相鄰，router 可能被字面誤導去分流到 `blog-writing-zh`。2.0.0 改寫 description 時保留了該排除句（它是必要的邊界宣告），並把開頭改成「language-layer cleanup pass」，讓職責分界不只靠結尾那一句承擔。改寫後 10/10 仍全過，含 id 3 與 id 9（RFP structural authoring 的負例）。
