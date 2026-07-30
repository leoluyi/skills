# English layer

The English rules are the same 45 canonical rules, wearing English clothes. Nothing here is a separate taxonomy — cite the same rule name you would cite in Chinese, and reach for the same carve-out. Twelve rules are Chinese-specific (抽象claim缺交付, 破碎短句堆疊, 零資訊警句與口號, 口語化萬能動詞, 過度簡寫, 翻譯腔, 專有名詞過度翻譯, 列舉代替論述, 空降斷言開場, 空降主張, 對讀者說教, 罐頭式反應鏡頭); this file covers the 33 that manifest in English too.

What the English tells have in common: a fixed phrase gets reached for at a moment where a fact belongs. So the working question is never "is this phrase banned" but "did a sentence arrive where a fact was due". Delete the phrase and see what is left standing — if a fact is still there, patch the span; if nothing is, that is a 空話 / 立場真空 finding for the author, not something to write your way out of.

Each rule's keep-clauses are alternatives, not a checklist: satisfying any one spares the span, whichever one it is. Quote the span's own evidence for the clause you invoke and say which rule it belongs to — a carve-out written under one rule never licenses a span under another — and if the evidence is not quotable from the text in front of you, the carve-out does not hold.

Example pairs below are synthetic.

## 內容類

**意義膨脹** — "marks a pivotal moment", "a watershed for the industry", "a testament to", "cements our position", plus treating a well-known concept as freshly coined ("I'd never heard anyone name this before"). Keep it when a concrete consequence, number or date follows.
> Sign-ups grew by a third after we moved checkout onto one page. ← *a watershed moment for our onboarding*

**空話填充** — "It is important to note that", "In terms of", "The reality is that"; hollow intensifiers on abstract nouns ("real utility", "genuine traction", "actual product-market fit"); false breadth ("Whether you're a solo founder or an enterprise architect", "from ancient civilisations to modern startups"). Keep "real"/"actual" when the sentence names the fake thing it is contrasted against, and keep an improvement claim that carries its metric.
> LCP went from 3.2s to 1.8s. ← *a comprehensive optimisation of the user experience*

**萬用收尾** — "In conclusion", "The future looks bright", "Only time will tell", "As we move forward"; the future-narrative shape (modal + "become" + "one of the most important [narrative / trend / chapter]"); social sign-offs ("Bookmark this.", "Thank me later."). Keep a falsifiable prediction or a closer that names the next action.
> Next release moves to Thursdays, and we'll A/B the digest subject line. ← *One thing is certain: the best is yet to come.*

**推廣語氣** — brochure prose ("a vibrant hub of innovation", "nestled in the foothills", "a thriving ecosystem") and parallel adjective strings ("robust, seamless, and intuitive"). Judge at paragraph scale: if the neighbouring sentences actually show the thing, the adjective is a topic sentence, not a claim.
> Twelve of the fourteen units are occupied, six by companies under three years old. ← *a thriving ecosystem of innovative startups*

**原地踏步與段落失連** — a writer-side read, mostly detect. Two probes: could you cut 40–60% of this paragraph and lose nothing, and could you swap two body paragraphs without a reader noticing? Summary sections are supposed to restate; genuine list content is supposed to be modular.
> Report it as: *paragraphs 3 and 4 restate paragraph 2; the argument stops advancing there.*

**解說導引腔** — "Here's what's interesting", "Notably", "It's worth noting that", "What's fascinating here", and the depth-asserting cousins "the real question is", "at its core", "fundamentally", "make no mistake". One in 2,000 words is nothing; flag on stacking — three or more inside 500 words.
> The three figures don't reconcile: 240 registered, 96 attended, 210 paid. ← *Here's the interesting part: these three numbers tell a story.*

## 語言句式

**對比句式** — "It's not X — it's Y", the split form across two sentences ("The headline isn't the speed. The real story is trust."), the multi-negation countdown, and false concession ("While X is impressive, Y remains a challenge"). One per piece, and only where the argument genuinely turns.
> The rewrite replaced the queue and changed how retries are counted. ← *This isn't just a rewrite — it's a rethink.*

**避險堆疊** — a modal stacked on a hedging adverb: "could potentially", "may eventually", "might ultimately". Either word alone is fine; the stack asserts nothing. A single conversational qualifier ("I think") is not this rule, and precise conditional logic in a spec is not either.
> Weekday afternoon traffic drops 10–20%; weekends are unaffected. ← *This could potentially have some degree of impact on traffic.*

**詞彙處理失真** — synonym cycling inside a paragraph ("developers… engineers… practitioners… builders") and, in general prose over 200 words, a type-token ratio under 0.40 with the same abstract nouns recycled. TTR alone is never a flag: narrow topics, reference material and second-language writing compress vocabulary legitimately.
> Developers get the token at build time. Developers can rotate it from the CLI. ← *…engineers… practitioners…*

**節奏均質** — most sentences 15–25 words, every paragraph 3–5 sentences, symmetrical constructions, compulsive triads, and prose a text-to-speech engine could read without sounding odd. Formal genres (spec, SOP, API reference) are supposed to be uniform. The inverse is equally a defect: sanding away disfluency and odd word choices in the name of "fixing rhythm" produces the very flatness this catches.
> Rebuild it with a one-line paragraph, a fragment, and one long sentence that earns its length.

**繫詞膨脹** — "serves as", "boasts", "represents", "features", "presents" standing in for "is" and "has". Keep the fancier verb when it is genuinely more precise, and keep factual role assignment ("uses Postgres as its event store").
> The lobby screen is the building's notice board. ← *The lobby screen serves as a central hub for community information.*

**使用／提及之分** — the suppressor. A word being discussed rather than used, or sitting inside quotation marks, a code block or an explicit example, stays exactly as written. No exceptions; it outranks every other rule here.
> Leave *I used to write "leverage" in every deck, then cut all of them* completely alone.

## 風格版面

**破折號濫用** — em dashes and `--` doing the job of "because", "so", "for example", "that is". Ceiling of one connective dash per 1,000 words, headings included; anything clearer with an explicit connective gets converted. List separators (`**Label** — gloss`) don't count, a paired parenthetical dash counts once, quotations and titles don't count.
> The hard part is scheduling: one person knows how to run the mixer. ← *The hard part is scheduling — one person knows how to run the mixer.*

**粗體與內聯標題濫用** — bold scattered through prose (more than one instance per major section), bullets that open with a bold label and then restate it, and the label-period shape (`**Intros.** Years of…` where a person writes `**Intros:**`). A label that is a full sentence keeps its period; unbolded fragments only count when they are clearly 1–4 word verbless labels.
> `- Pickup: barcode from the SMS; the counter only handles parcels over 5kg.` ← `- **Pickup.** Pickup has been made more convenient.`

**條列膨脹與裸名詞條列** — lists chosen because structure feels safe: "Three key takeaways", numbered items that are really paragraphs, 8+ bullets inside 200 words, more than 3 headings inside 300 words, template headers ("Overview", "Key Points"). Plus five or more consecutive bullets that are all short verbless adjective+noun phrases, all the same shape, none checkable.

English also runs this defect *inside a sentence*, with no bullet in sight: a colon or "are all" frame introducing a bare list that the paragraph then drops — "There are several approaches: cache-aside, write-through, and write-behind", "Setting a schedule, creating a workspace, and taking breaks are all effective strategies". Same test as the bulleted form: is any item expanded anywhere? Three named options and no sentence saying when you would pick one is a list pretending to be an argument. Changelogs, todos and parameter docs are genuinely list-shaped; leave them, and leave an enumeration whose every item is itself concrete and checkable.
> Write-through costs you latency on every put; we took cache-aside because our reads outnumber writes 40:1. ← *There are several approaches: cache-aside, write-through, and write-behind. Each has its own trade-offs.*
> Median lunch-rush ticket time fell from 9:00 to 5:30 after prep moved to the night before. ← *Stable output quality / Efficient floor layout / Effective scheduling / …*

**表情符號與標籤堆疊** — emoji opening or punctuating consecutive sentences, emoji in headings, or six-plus trailing hashtags mixing one project tag with broad category tags. A social post may carry one or two emoji at end of line and two or three specific hashtags.
> October schedule is up; Wednesday evening free-weights intro, 12 places. #strengthtraining ← *🎉 New schedule! 💪 ✨ #fitness #health #life #discipline #grind #stronger*

**表格誤用** — a table whose structure is decoration: a column with no checkable values ("Significance", "Implications"), rows that are one-line prose crammed into cells, or a table where one sentence would be clearer. A real comparison matrix with concrete cell values stays.
> Columns: plan / monthly fee / contract length / early-exit cost. ← *Columns: plan / description / value.*

## 溝通殘留

**對話介面殘留** — "I hope this helps!", "Certainly!", "Feel free to reach out", "Let me know if you'd like me to adjust the tone", and restating the prompt before answering ("To answer your question…", "You're asking about…"). A real email closing on a named next step is not this.
> Renewal opens 30 days before expiry; after that the joining fee applies again. ← *Regarding your question about renewals, I hope this helps!*

**諂媚語氣** — "Great question!", "You're absolutely right", "That's a really insightful observation", and the opener that recaps someone's own work back at them as praise. A plain one-clause thank-you, or genuine self-criticism in the author's own voice, is fine.
> Yes — pricing changed in August; the site never got the update. ← *Great question! Your read on this is exactly right.*

**知識截止免責** — "As of my last update", "I don't have access to real-time data", "based on the information available". Operationally necessary disclaimers in payments, logistics and support are protected, not flagged ("delivery timing depends on the carrier's schedule"), and so is a dated as-of note in research output.
> Refunds are submitted within 3 business days; the payment processor sets the credit date. ← *I can't confirm current refund timelines with the information available.*

**AI 工具殘留標記** — mechanical fingerprints, cleaned on sight without weighing the surrounding prose: `utm_source=chatgpt.com` / `copilot.com` / `claude.ai` / `perplexity.ai`, `referrer=grok.com`, `citeturn0search2`, `contentReference[oaicite:0]`, `oai_citation`, `[attached_file:1]`, and unfilled placeholders (`[Your Name]`, `[INSERT SOURCE URL]`, `2025-XX-XX`). Keep a meaningful URL and drop only the parameter; placeholders inside a document declared as a template are correct.
> `https://example.com/faq` — contact: Amy Chen, ext. 214. ← `https://example.com/faq?utm_source=chatgpt.com` — contact: [Your Name].

## 事實與引用

**模糊歸屬** — "Experts believe", "Studies show", "Industry leaders agree", "Users have reported", plus the unnamed-third-party superlative ("independent testing confirms", "third-party testing puts us on top"). A named, checkable source stays, and so does first-hand experience stated as such.
> Of 87 survey responses, 62 preferred the new pickup window. ← *Users overwhelmingly prefer the new pickup window.*

**幻覺引用與未查證主張** — institution plus year plus suspiciously precise figure ("a 2024 Harvard Business School study found a 47.3% lift"), quotes nobody said, and the quieter form where hedged language fills a knowledge gap ("is believed to have", "likely began his career in"). Anything the author can actually produce, or a reader can actually check, stays — as does something explicitly marked as a guess.
> The owners date it to 1978; we couldn't find anything earlier. ← *The shop is believed to date to the early twentieth century.*

**權威名號堆砌** — stacked prestige ("cited in the NYT, BBC, and the Financial Times") and rapid-fire historical analogy ("like the printing press, the telegraph, and the internet"). One named source used with context, or one analogy that does actual analytical work, is the fix.
> A March 2025 trade-press piece covered the prep workflow; it solves what central kitchens solve — moving the highest-variance step off-site. ← *…like the printing press before it.*

## 立場與開場

**公式化開場** — "In the rapidly evolving world of…", "In today's landscape", "As technology continues to advance"; the speculative world opener ("Imagine a world where every deploy is instant"); the fill-in-the-blank social opener ("I recently had the pleasure of…"). Fiction, a thought experiment with a stated payoff, and the instructional "imagine you have a sorted array" all stay.
> Last year the office logged 412 maintenance tickets; 118 were the same leaking riser. ← *In today's rapidly evolving property-management landscape…*

**反問句開場與收尾** — "But what does this mean for developers?", "So why should you care?", "What's next?" used to stall before a point or to moralise at the end. A genuine conversational aside in a 署名文體 piece stays, and so does a run of questions where each names a different concrete worry; `linkedin` allows one as a hook.
> For residents it's money: the fee goes from NT$65 to NT$72 per ping. ← *So what does this really mean for residents?*

**立場真空** — the systematic refusal to take a position in a genre that calls for one: "there are pros and cons either way", "it depends on your use case", "ultimately, both approaches have merit" as the conclusion, and no sentence anywhere carrying the author's judgement. Genres that only state information — docs, README, reference, RFP, spec, SOP — are supposed to read this way, and 公文/簽呈 take their stance in the 擬辦 line rather than in a voice. A proposal, plan or investor email is not on that list: it exists to recommend, so surveying the options and recommending none is precisely what this catches. One clear stance anywhere in the piece clears the flag.
> I'd take the gas hob. ← *Both hob types have their advantages, depending on personal preference.*

**作者隱身** — detect-only, aggregate, gated to 署名文體 genres, two or more sub-signals required. Full rules in [hidden-author.md](hidden-author.md).

## 人工戲劇

**情緒宣告** — "What surprised me most", "What struck me was", "I was fascinated to discover", "The most interesting part", and the bare header form ("Interesting part of the project:").

Its flatter and commoner English form asserts the feeling *about the topic* with nobody in the sentence: "X can be frustrating to debug", "this is a common source of confusion", "the process is often painful". It reads as experience but reports none — no occasion, no cost, no one who felt it. Ask who felt this and when; if the text cannot say, it is a declared emotion standing in for the specific one. A genuine intensity marker that the surrounding 400 words earn stays; in a 署名文體 piece it is the *absence* of these that reads as machine-written.
> I lost an afternoon to this before checking whether kube-proxy was even running. ← *Networking issues can be frustrating to debug.*
> The stock has been going since 1978 — strained every night, topped up every morning. ← *What struck me most was their remarkable dedication.*

**懸念與自我貼標籤** — forward teasers ("The catch?", "Here's the thing.", "Plot twist:", "The best part?") and backward labels pointing at your own last sentence and calling it clever, contrarian, counterintuitive or key. If the explanation that follows makes the label redundant, deleting the label is the whole fix.
> We moved prep to the night before; chilled scallions actually hold their aroma better at 12 hours. ← *Here's the counterintuitive part: we moved prep to the night before.*

## 打破第四面牆

**文件自述** — "As requested, this report…", "Based on the scenario you described", "Per your prompt", and meta-narration openers ("In this article, we will explore…", "Let's dive in", "Let's break this down"). A deliberate persona sustained through the whole piece is a voice feature, not a commissioning echo, and a decision memo may genuinely call for action.
> Only vendor C can add a Saturday collection. ← *As requested, this report will explore a comparison of three vendors.*

**思考過程外洩** — fingerprint form ("Let me think step by step", "Step 1:", "First, let's consider", "Breaking this down") and the unmarked fluent-prose form ("I started with option A, hit a wall on latency, and moved to B"). Reader-facing rationale the argument depends on stays; so does a comparison that *is* the deliverable, as in an ADR options section, and so do real numbered steps a reader is meant to follow.
> Vendor A's truck is 2.6m; the basement clears 2.3m. Vendor B's compactor fits. ← *I first evaluated A, found the truck wouldn't fit, and moved on to B.*

**併稿接縫** — pointers standing in for content ("see the other doc", "as above", "per the previous section", "同上") and orphaned references to a figure or table that didn't survive the merge ("as shown below"). Formal citation of an external authority a reader can independently obtain — a law, a standard, an RFC, a paper — stays, and so does a cross-reference inside a document set declared to be read together.
> The fee is NT$72 per unit per month, plus NT$200 per parking space. ← *Fees are as previously described; see the table below.*
