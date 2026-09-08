# Finished-prose routing

**Language.** CJK present → the zh layer, [zh-rules.md](zh-rules.md).
Pure English → the English layer, [en-rules.md](en-rules.md).
Mixed zh/en → audit each language under its own layer, and leave English technical terms (API, Kubernetes, CI/CD) standing inside the Chinese prose; that is correct Taiwan usage.

**Lookup.** The zh layer's rules are judgements; [zh-phrase-rules.md](zh-phrase-rules.md) is its word-level lookup - 空話、確保家族、至關重要、AI 句式、慣用詞（含「節奏」譬喻）、四字評語、台灣用語偏好, one row per term.
Read it whenever zh text is in scope.
A term that matches a row is flagged as its own item under the row's canonical rule, and the row's Fix column *is* the direction you report - the tables exist so that six idioms in one sentence come back as six named entries with six concrete replacements, not one lumped span.

**作者隱身 audit** - detect-only, and it reports absence rather than rewriting.
[Step 1](finished-prose-workflow.md)'s genre verdict is the entire trigger: every 署名文體 draft gets this audit whether or not the user asked for it, and 事務文體 never does.
`--expect-author` reaches it by setting that verdict, not by bypassing it.
Its five sub-signals and threshold live in [hidden-author.md](hidden-author.md); read that file before reporting anything under this heading, because the 事務文體 exclusion there is what keeps this from firing on 公文 and docs.
This exclusion covers this rule only.
The ordinary pass still evaluates the other rules, and each rule's own carve-outs decide whether it fires, so a 簽呈 stuffed with 「奠定堅實基礎」 is flagged like any other draft.

Worked end-to-end scenarios: [examples.md](examples.md).
