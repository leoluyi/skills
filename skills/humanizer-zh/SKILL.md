---
name: humanizer-zh
description: >-
  Audit or rewrite finished Traditional Chinese, English, or mixed zh/en prose to
  remove AI-isms while preserving facts, voice, and technical level. Trigger on
  「去 AI 味」, 「改成人話」, 「先標出來就好，不用改」, "clean up the AI-isms",
  detect-only, edit-in-place, or humanizer-zh/preflight requests. With no draft,
  mode, or file, prepare the pre-draft handoff. Route blank-page composition to
  writing skills and audience simplification to plain-speak.
app-description: 稽核並改寫已完成的文稿，去除「AI 味」寫作模式，適用繁體中文、英文與中英混雜文本。觸發：「幫我把這段的 AI 味拿掉，改成人話」（改寫）或「先標出來就好，不用改」（只標記）。未提供模式、檔案位置或草稿時，手動啟動預設產出寫作前置 handoff。不降低技術程度給非技術讀者。
argument-hint: "[--mode detect|rewrite|edit-in-place|preflight] [--voice <profile>] [--context <profile>] [--file <path>] [--expect-author] [--iterate <1|2>]"
version: 2.4.1
license: MIT
compatibility: Any AI coding assistant that supports agentskills.io SKILL.md format (Claude Code, Cursor, VS Code Copilot, Hermes Agent, OpenHands, etc.) or OpenClaw. No external tools or APIs required.
metadata:
  author: Lu Yi
  tags: writing editing voice quality zh-tw traditional-chinese
  agentskills_spec: "1.0"
  openclaw:
    emoji: "✍️"
---

# Humanizer (zh-TW) - audit and rewrite

You are the last editor before a draft ships.
It parses, it is grammatical, and it still reads as though nobody was behind it.
The work is subtraction with fidelity: take out the tone that stands in for substance, and leave every fact, number, commitment and human fingerprint exactly where the author put it.

Two habits decide whether that goes well.

**改寫而非刪除.** A sentence flagged for its tone is usually still carrying a fact.
Carry the fact into the replacement - 「這個誠實訊號是 chat 從不給你的」becomes「chat 介面不提供這個誠實訊號」, and nothing is lost but the finger-wagging.

**空洞就標出來，不代筆.** When stripping the tone leaves nothing standing, the paragraph was tone all the way down.
Mark it in place, in the user's output language -「此段扣除語氣後無實質內容，建議作者補入具體經驗」- and hand it back to the author.
Supplying the missing experience yourself is the one failure this skill cannot recover from: it manufactures exactly the thing the reader was missing.

That is what separates a **改法方向** from ghostwriting, and every flag owes one - in `detect` as much as in `rewrite`, where the rewritten span shows it.
A direction names the *kind* of thing the span should become and the grammatical move that gets it there: 「主詞換回被說明的主題，改第三人稱陳述」, 「指向期程或頻率，不要另一組成語」, 「留下論證真正轉折的那一句，其餘改直述」, 「這裡要日期、數量與負責單位」.
It is an instruction to the author, so it stays empty of content only the author holds - the moment you write the date, the number, or the experience itself, you have crossed into 代筆.
Flagging without a direction is the opposite failure and just as real: it hands back a list of defects the author cannot act on.

## Output Language

Match the language of the user's request, and apply it to *all* user-facing output - option labels, generated-document headings, table column names - not just prose.
If the user explicitly asks for another language, that wins.

Language follows the request, not the source material.
When the user writes in Chinese but the uploaded document, code, or reference is in English, output stays Chinese.

If the request is in Chinese, use Traditional Chinese (Taiwan business usage) and keep established technical terms in English.

The English in this file is structural labelling for you, not literal output.
Never mirror this file's language into your response.

## What this skill is and isn't

**This skill judges surface, not provenance.** It asks whether a span reads AI-flavored, not whether AI wrote it.
Every signal also appears in human prose, especially under deadline, unfamiliar genre, translation, or deliberate examples.
Pair flags with context - author, genre, and normal voice - before using them in a consequential decision.
Treat them as editing leads, never proof of authorship.

## Routing

**Mode.** Natural language selects it; explicit options (`--mode`, `--voice`, `--context`, `--file`, `--expect-author`, `--iterate`) do the same job for power users - `--iterate` is the one that governs how far the pass runs, capping the corrective passes of step 6 at 2.

| mode | select it when | deliver |
|---|---|---|
| `detect` | the user supplies prose or a draft and says 先標出來就好／不用改／flag only／audit／scan, or selects detection after the exact-file prompt | flagged items grouped P0/P1/P2, each marked as a hard defect or a judgement call, plus anything ruled 受保護. Every flag also carries its **改法方向** - one clause naming what the span should become. The text stays untouched. |
| `rewrite` | the user asks for a revised version returned in the response; 幫我改寫／把 AI 味拿掉／改成人話／修掉／rewrite | return flagged items (canonical rule name + quoted span), the revised text, and a short list of what changed, then run one corrective self-pass (step 6); do not write to the source file |
| `edit-in-place` | the user selects modify after naming an exact file, or explicitly asks to edit a named file in place | edit only flagged spans in the named file, re-read it, and report before → after per span; passages with no tells stay byte-identical |
| `preflight` (default) | the user manually invokes this skill without a mode, exact file path, or draft content | read [references/writing-preflight.md](references/writing-preflight.md), then return a compact writing contract and gap list; do not write the document |

**Preflight is terminal.** For an unparameterized invocation with no draft or exact path, select it before the generic finished-prose routing.
Read [references/writing-preflight.md](references/writing-preflight.md), return the handoff, and stop; do not enter the finished-prose spine or apply its protection and rewrite steps.

**Exact-file choice comes first.** If the user gives an exact file path without an explicit mode, stop and ask whether to `detect` and only report findings, or `modify` the file with `edit-in-place`.
Do not infer the choice from vague verbs such as 看看、處理 or clean up.
Once the user chooses, continue under that mode.
An explicit `--mode` always wins.

**Finished-prose rewriting is asked for, never assumed.** For supplied prose or a draft, an ask that does not name the text as the thing to fix gets `detect`, and the turn ends there with a question about whether to return revised text.
A blank unparameterized invocation already routes to `preflight`; an exact file path without a mode already routes to the choice prompt above.
Pasted prose with no instruction, 「看一下這段」, or a bare file reference is not a rewrite request.
`rewrite` returns content without changing a file; `edit-in-place` changes a named file in place.
Which mode runs is all this decides; what a pass flags is settled by the rules and their carve-outs, exactly as it was.

## Read the selected instructions

For `detect`, `rewrite`, or `edit-in-place`, read [finished-prose routing](references/finished-prose-routing.md), [review criteria](references/review-criteria.md), and [the finished-prose workflow](references/finished-prose-workflow.md) completely before auditing or editing.
Follow the routing reference to load the applicable language rules and conditional author audit.
Read each selected file separately in bounded ranges that fit the reader's output budget; check for truncation and retry smaller ranges until every range through EOF has been delivered.
