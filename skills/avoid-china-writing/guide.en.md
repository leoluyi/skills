# Cross-Strait Chinese Localizer

This skill audits and rewrites Traditional Chinese text to strip mainland-China (PRC / 大陸) wording and convert it into natural Taiwan 正體中文 — vocabulary, workplace jargon, leaked Simplified characters, and transliterated proper nouns, without over-correcting real technical terms.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a avoid-china-writing -y
```

Update later with:

```
npx skills update avoid-china-writing
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/avoid-china-writing/SKILL.md)

## What it does

It checks a passage across four independent axes and reports findings tiered by how strongly they signal a mainland source:

- **詞彙 (vocabulary)** — everyday and technical words where Taiwan and the mainland simply differ: 視頻→影片, 軟件→軟體, 屏幕→螢幕, 網絡→網路, plus a set of homograph traps (信息, 數據, 質量, 程序, 文件, 水平, 用戶) where the Taiwan word only applies in one specific sense.
- **互聯網／職場黑話 (corp-speak)** — mainland tech/business jargon such as 賦能, 抓手, 對齊顆粒度, 閉環, 落地, 賽道, 內卷. The fix is usually not a synonym swap but naming the concrete thing the jargon is hiding.
- **簡體字殘留 (leaked Simplified characters)** — any Simplified codepoint sitting in otherwise-Traditional text, a near-definitive sign of a mainland source or a sloppy conversion. The hard part is choosing the right Traditional form when one Simplified character maps to several (发→發/髮, 面→面/麵, 里→里/裡).
- **音譯與專名／語法差異** — different transliterations of foreign names (奧巴馬→歐巴馬, 悉尼→雪梨, 硅谷→矽谷) and mainland grammar habits (通過→透過, 進行 + noun instead of a plain verb, 一條消息→一則訊息).

Findings are ranked P0 (unmistakable mainland source — change it), P1 (jargon and grammar tics — fix before publishing), and P2 (borderline or already-normalized-in-Taiwan usage — fix when there's time).

It runs in three modes: `rewrite` (default — flag and return a localized version), `detect` (flag only, grouped by tier, no rewriting), and `edit-in-place` (make minimal in-place edits to a named file with the Edit tool, touching only the flagged spans).

## When to use

Reach for this when a Traditional Chinese draft carries mainland wording, corp-speak, or leaked Simplified characters and needs to read naturally for a Taiwan audience — localizing an existing document, auditing a draft before publishing, or fixing a file someone else wrote in mainland-influenced Chinese.

## When not to

Skip it for stripping AI writing tells or polishing tone — that's `humanizer-zh`'s job, a different axis entirely (a passage can be fully human-written and still full of 陸用語, or idiomatically Taiwanese and still read as AI-generated). Also skip it for structuring formal business documents like 簽呈 or reports (`formal-doc-structure`), for RFPs (`rfp-writing`), for plain-language rewrites of technical terms (`plain-speak`), and for casual chat, creative writing, or code comments.

## How it works

The core judgment call is distinguishing a genuine 陸用語 defect from a term that merely looks like one. Several common words are homographs with a Taiwan-correct sense and a mainland-only sense, and swapping blindly changes meaning rather than fixing usage. For example:

- 信息 → 資訊 (general sense) or 訊息 (a single message) — but 資訊理論 (information theory) keeps 資訊 as a fixed technical term.
- 數據 → 資料 in ordinary prose — but 數據分析／數據科學／大數據 are accepted fixed compounds in Taiwan tech usage and stay as-is.
- 質量 → 品質 — except in physics, where 質量 correctly means mass, not quality.

The same discipline applies to jargon: 對齊 gets flagged and rewritten when it means the empty "對齊一下顆粒度" ("get on the same page" filler), but is left alone when it means model alignment (AI/ML) or layout alignment — a concrete technical referent, not filler. This term-of-art carve-out extends to any domain's standard vocabulary (finance, semiconductors, biomedical, compliance): verify a compound is actually filler before "correcting" it.

Proper nouns, brand names, direct quotes of mainland source material, and code identifiers are flagged with a note but never silently rewritten, since changing someone's quoted words or a brand name isn't the skill's call to make.

## Related skills

- **humanizer-zh** — strips AI writing tells and polishes tone; use it for AI-ism cleanup, orthogonal to this skill's cross-strait localization axis.
- **formal-doc-structure** — structures formal internal business documents (簽呈, 會議紀錄, 評估報告); use it when the task is document structure, not word choice.
- **rfp-writing** — drafts RFP / 需求規格書 documents; different structural conventions than general Traditional Chinese writing.
- **plain-speak** — lowers technical jargon to a non-technical audience; a register shift, not a cross-strait localization.
