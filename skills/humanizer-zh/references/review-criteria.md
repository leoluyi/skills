## Shared vocabulary

47 rules in 8 classes.
Detail, carve-outs and worked pairs live in the reference files; these names are what your flags cite.

| class | what it catches | rules |
|---|---|---|
| 內容類 (7) | words spent without a fact arriving | 意義膨脹 · 空話填充 · 抽象claim缺交付 · 萬用收尾 · 推廣語氣 · 原地踏步與段落失連 · 解說導引腔 |
| 語言句式 (13) | the sentence's shape doing the work its content should | 對比句式 · 避險堆疊 · 詞彙處理失真 · 節奏均質 · 破碎短句堆疊 · 零資訊警句與口號 · 口語化萬能詞 · 過度簡寫 · 語體漂移 · 翻譯腔 · 專有名詞過度翻譯 · 繫詞膨脹 · 使用／提及之分 |
| 風格版面 (6) | typography and layout standing in for structure | 破折號濫用 · 粗體與內聯標題濫用 · 條列膨脹與裸名詞條列 · 列舉代替論述 · 表情符號與標籤堆疊 · 表格誤用 |
| 溝通殘留 (4) | chat-turn and tooling residue surviving into a document | 對話介面殘留 · 諂媚語氣 · 知識截止免責 · AI 工具殘留標記 |
| 事實與引用 (3) | authority borrowed instead of earned | 模糊歸屬 · 幻覺引用與未查證主張 · 權威名號堆砌 |
| 立場與開場 (7) | judgement announced, deferred, or absent | 空降斷言開場 · 公式化開場 · 反問句開場與收尾 · 空降主張 · 立場真空 · 作者隱身 · 對讀者說教 |
| 人工戲劇 (3) | a beat manufactured where nothing happened | 罐頭式反應鏡頭 · 情緒宣告 · 懸念與自我貼標籤 |
| 打破第四面牆 (4) | the deliverable talking about itself | 文件自述 · 自我背書 · 思考過程外洩 · 併稿接縫 |

Two mechanisms cut across all eight: **保護清單** ([step 2](finished-prose-workflow.md)) decides what survives untouched, and **長文scope** ([step 3](finished-prose-workflow.md)) decides how large a unit each fix operates on.

## Severity

**P0 - mechanical fingerprints and trust killers.** AI 工具殘留標記, 知識截止免責, 對話介面殘留, 諂媚語氣, 幻覺引用與未查證主張, and the commissioning-echo form of 文件自述.
A reader who hits one of these stops trusting the whole document, so they come out even on a thirty-second pass, without weighing the surrounding prose.

**P1 - the default tier.** Every other rule.
This is what a pre-publication pass covers.

**P2 - polish.** 節奏均質, 繫詞膨脹, 詞彙處理失真.
Real, and safe to leave when time is short; they also carry the highest false-positive risk, so they are the first to yield to a carve-out.

## Context and voice profiles

**Context** sets how hard to press, per audience: `linkedin` (short-form social; punchy fragments and visual formatting are the register), `blog` (default, full strength), `technical-blog` (code and architecture; technical vocabulary and long option lists are legitimate), `investor-email` (high-trust; promotional language is the biggest risk, so press hardest there), `docs` (README, CONTRIBUTING, ADR, API docs, code comments; clarity over voice, and identifiers, commands and fenced blocks stay untouched), `casual` (Slack, notes, quick replies; P0, plus `破碎短句堆疊` - a chopped inference chain does not become readable because it was written in Slack).
Auto-detect when unstated - hashtags and under 300 words → `linkedin`; code blocks → `technical-blog`; salutation plus fundraising language → `investor-email`; step-by-step or parameter docs → `docs`; otherwise `blog` - and say which profile you picked and why, so the user can override.
The per-rule relaxations are written into the carve-outs beside each rule; this list only sets the baseline.

**Voice** sets how the prose should sound, and is an independent axis: `casual` (contractions, short sentences, at least one first-person or anecdotal touch), `professional` (active voice, one concrete claim per paragraph, explicit ask), `technical` (plain copulatives, one idea per sentence, lists only where content is list-shaped), `warm` (address the reader, stronger verbs over intensifiers, unhurried cadence), `blunt` (claim first, periods for emphasis, near-zero hedging).
Given a writing sample instead of a profile name, match its sentence-length pattern, contraction rate and word choices, and keep the writer's register rather than upgrading it.

Where context and voice govern the same rule and disagree, resolve toward the stricter.
Where a voice profile - including one authored by a sibling skill such as `blog-writing-zh` - declares positive features, those features are 保護清單 item ⑥: a declared stance, metaphor system or deliberate 口語破格 that also matches a rule stays in place and is noted in the audit.
That is what lets an additive pass and this subtractive one compose without the subtraction eating the addition.
