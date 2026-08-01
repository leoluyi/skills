# Technical RFP Writing & Review

This skill drafts and reviews technical RFPs (需求規格書 / 需求規劃書 / 招標規格) in Traditional Chinese, written from the issuer's perspective — the organization putting out the requirement, not the vendor bidding on it. It applies a fixed set of structural checks before touching language, then enforces a formal plain-language style so every requirement reads as a complete, verifiable sentence. Manual trigger only — invoke it by name rather than expecting it to fire automatically.

## Install

```
npx skills add https://github.com/leoluyi/skills -g -a rfp-writing -y
```

Update later with:

```
npx skills update rfp-writing
```

[Source](https://github.com/leoluyi/skills/blob/main/skills/rfp-writing/SKILL.md)

## What it does

Reviewing an existing RFP or drafting a new section both run through the same structural audit before any language pass:

- **Redundancy elimination** — cross-cutting concerns (signing, scanning, audit logging) belong in one general section, not repeated per domain. Cross-references are fine; restating the same requirement twice is not.
- **Appendix bloat control** — an appendix earns its place only by adding concrete, quantifiable information not already in the main body. Appendices full of "由廠商提出" rows, or ones that just restate main-body requirements in table form, get deleted; any numbers worth keeping move into their parent section.
- **Thin-section consolidation** — a section with only 1-2 bullets and no opening context gets merged into the nearest parent or sibling rather than standing alone.
- **Section justification** — a section only survives if it has both a concrete current-or-next-phase use case and enough substance (opening context plus 3+ requirements) to warrant standalone treatment. Speculative "might need later" content gets demoted to a one-sentence remark.
- **Formal plain-language style** — every bullet must be a complete sentence stating what and why, not a noun-phrase fragment:

  ```
  BAD:  - 持久卷（PV/PVC）
  GOOD: - 所有儲存須透過 CSI 驅動掛載為持久卷（PV/PVC），不依賴節點本地磁碟。
  ```

  A fixed prohibited-pattern list catches AI filler (確保, 從而, 賦能), slash enumeration in Chinese (輸入/輸出 → 輸入、輸出), hedging (可能, 若), and other AI-writing tics, while an allowed-pattern list protects legitimate RFP notation (bold requirement labels, English term slashes like `JWT / OAuth2`, em dashes for technical explanation) from being flagged.
- **Section placement** — content belonging to two or more owning sections (e.g., canary deployment strategy sitting under "service lifecycle" instead of "deployment & release") gets split and merged into the correct parent.
- **Reference integrity** — after any structural edit (move, delete, renumber), it greps the full document for the old section number and updates every cross-reference — tables, footnotes, appendices.

## When to use

Use it when you are drafting or reviewing a technical RFP, 需求規格書, 需求規劃書, or 招標規格書 — i.e., a vendor requirement specification being sent out for bidding, from the issuing side.

## When not to

Skip it for anything adjacent but structurally different:

- Migration plans, test plans, deployment plans
- Runbooks, SOPs, operational procedures
- ADR / ARB / architecture decision records
- Internal design docs or technical specifications
- Meeting minutes, decision memos, stakeholder pre-reads
- General technical documentation (README, onboarding, API docs)
- Vendor-side bid proposals or RFP responses (投標提案) — this skill is for the issuer, not the responder
- General formal Chinese writing with no RFP-specific structure — RFP conventions (bullet-heavy, structured uniformity, no "rhythm variation") actively conflict with general formal-writing conventions

## How it works

Two rules do most of the structural work. First, the **thin-section test**: if removing a section's header and indenting its content under a neighboring section loses zero information, the section should not exist independently — merge it. Second, the **appendix bloat test**: an appendix is boilerplate, not a real baseline, if most of its rows just say "由廠商提出" or restate numbers already implied by main-body sections (e.g., generic 99.9% uptime or RPO/RTO figures) — kill it and fold any genuinely new numbers into the section that owns them. Both tests exist to stop an RFP from accumulating sections that look thorough but add no verifiable requirement.

A related check, the **infrastructure-standard-practice test**, catches the opposite failure mode: if a section could appear verbatim in any cloud or Kubernetes RFP with zero modification (secret management, HA control plane, CPU sizing, backup/restore), it isn't a domain-specific requirement — delete it or fold it into the infrastructure layer rather than giving it a standalone section under the application.

Language cleanup runs only after structural changes are confirmed, using a grep-based audit of prohibited patterns (AI filler, contrarian structure, hedging, significance inflation) against an explicit allow-list, so legitimate RFP notation (bold labels, technical slashes, bullet-heavy formatting) survives untouched. Reviewing an existing document and drafting a new section both end the same way: a final grep pass to confirm zero prohibited patterns remain, with `humanizer-zh` offered — never run automatically — as an optional deeper de-AI pass on the finished draft.

## Related skills

- **humanizer-zh** — general Traditional Chinese de-AI language cleanup; use it for a deeper pass after this skill's structural and language rules are satisfied, or for any document that isn't an RFP. Its conventions apply broadly, while this skill's structural rules (bullet-heavy, uniform formatting) are RFP-specific and would conflict if merged into a general-purpose style guide.
