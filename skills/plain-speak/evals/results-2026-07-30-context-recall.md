# v1.5.0 vs v1.4.0 — bare invocation targets the conversation (2026-07-30)

**Verdict: v1.5.0 ships.** On the three discriminating cases it passed 6/6 arms; v1.4.0 passed 1/6.
No regression on the pre-existing suite.

## Setup

- Arms: `skill-a.md` = v1.5.0, `skill-b.md` = v1.4.0 (`git show HEAD:skills/plain-speak/SKILL.md`).
  Neutral filenames so no agent could infer which side it was on.
- One independent agent per (case, arm, rep) — no agent saw more than one case, so the boundary
  cases could not be inferred from the pattern of the others. All on the current model.
- New cases 8–12: both arms, 2 reps each (20 agents). Regression cases 1–7: v1.5.0 only, 1 rep
  (7 agents). Every agent got the identical instruction: read the skill file, read the case file,
  write the user-facing response to a file.

**Contamination declared.** One author wrote the skill change, the assertions, and the verdicts.
The comparison supports "v1.4.0 fails these situations in a specific, reproducible way"; it is not
an unbiased measure of how much better v1.5.0 is. Most assertions here are objectively checkable
(does option C appear? is there a closing re-ask? is a third-party audience named?), which limits
the room for bias but does not remove it.

## Discriminating cases

| Case | v1.5.0 | v1.4.0 | Failure mode observed in baseline |
|------|--------|--------|-----------------------------------|
| 8 — preceding turn is a technical answer | 2/2 | 0/2 | Both reps invented a third-party audience the conversation never had (「換成跟非技術主管講的版本」/「我預設聽的人是不碰技術的主管」). One also added a claim absent from the source (「改動範圍小,不用動架構」). |
| 9 — preceding turn is a pending multiple-choice question | 2/2 | 1/2 | One rep appended its own decision tree (會出事→B / 不會→A / 寫入頻繁→C). The original question contained no recommendation: this is lowering turning into re-deciding. Both reps also opened by assuming a non-technical manager as the listener. |
| 10 — preceding turn holds nothing technical | 2/2 | 0/2 | Neither rep said "nothing here needs lowering". Both manufactured a whole task instead — promising a plain-language diff list, asking for the documents, negotiating granularity. Four paragraphs where the correct answer is two sentences. |

Both v1.4.0 failures on case 8 and case 10 reproduced across both reps in the same direction, so
this is a behavioural difference rather than sampling noise.

Secondary finding: the "lowering is not re-deciding" rule suppresses invented reassurance as well
as invented recommendations — the baseline's unsupported 「改動範圍小」 is the same failure wearing a
friendlier face.

## Non-discriminating cases — recorded as such

- **Case 11 (reader supplied, content not).** 2/2 both arms. The prompt states outright that no
  content was attached, which hands target resolution to the baseline for free, and a named reader
  is all v1.4.0 ever needed. The case confirms the reader-override half of the rule fires; it is
  **not** evidence of improvement. Kept as a should-fire regression stake.
- **Case 12 (must-not-fire boundary).** On what the boundary is actually for, both arms passed 2/2:
  all four outputs lowered the supplied index-change text and none retargeted the preceding turn.
  But the case's second assertion as originally written — "no 「剛剛」/「上一輪」 framing of the
  preceding turn" — failed in all four outputs, because all four referenced the previous turn to
  stop its p99 figures being attached to the index change. That is the accuracy guardrail working.
  Both arms violating one assertion identically is the signature of a mis-specified assertion, not a
  regression, so the assertion was reworded to target *retargeting* rather than *mention*.

## Regression — cases 1–7 on v1.5.0

7/7 pass. The new section does not leak into the ordinary translate and review paths:

- Case 7 (definitional): no invented 下一步 section, no headers or bullets, no inflation.
- Case 5 (plan with 4 moves): all four moves survive with their numbers, 下週三 kept.
- Case 3 (review mode): output shape unchanged — flat marked checklist plus corrected draft, and
  具體度 still correctly marked ✓-but-wrong-fact rather than "needs a number".
- Cases 1 and 6 (no-fabrication guards): both still refuse to invent numbers or actions.

Borderline, noted not fixed: case 7's output ran two paragraphs (~6 sentences) against a "roughly
2–4 sentences" assertion. No headers, no bullets, no structural inflation, and the second paragraph
is the reader-relative why plus the catch that §3 and §5 call for.

## Round 2 — the reader-hedge fix (same day)

Round 1's outputs exposed a defect in the *general* translate path, unrelated to bare invocation:
the assumed reader was being announced as a preamble the deliverable hung off, often paired with an
offer to redo it for a different reader (「若對象是看成本的財務長我再改成談機器與費用」). The skill's
own review example was modelling it. Fixed in §How to respond 1 plus that example, and the
`Reader locked` checklist criterion extended to cover two readers hedged against each other.

Arms for this round: `skill-p.md` = round-1 artifact + hedge fix, `skill-q.md` = round-1 artifact.
New cases 13 (reader choice shifts emphasis only) and 14 (reader choice changes substance), both
arms, 2 reps. Regression re-run of cases 3, 5, 8, 12 on the fixed version.

| Case | fixed | round-1 artifact | Failure mode |
|------|-------|------------------|--------------|
| 13 — no reader, emphasis-only choice | 2/2 | 0/2 | Both reps opened with a preamble the translation hung off (「給非技術主管聽的話可以這樣說:」/「給不碰技術的主管,可以這樣講:」). Neither offered an alternative version, so this case discriminates on the preamble form only. |
| 14 — no reader, substance-changing choice | 2/2 | 1/2 | One rep led with 「（假設是給看成本與損益的主管）」, wrapping the deliverable in a condition. |

No overcorrection: all four fixed-arm outputs still surfaced the substance-changing unknown in one
line after the deliverable, so the change did not suppress the ambiguity guardrail it had to coexist
with.

Regression 4/4, two of them visibly improved: case 12's reader preamble is gone and the response now
opens on the translation; case 5's closing 「如果對象是看成本的財務主管，重點要換成費用那一段」 was
replaced by a flag on the *source's* premise (「我是照『這批調整是為了解決尖峰撐不住』這個讀法翻的」) —
an alternative-version offer becoming a legitimate ambiguity note is exactly the intended migration.
Case 3 shows the extended checklist criterion firing (「讀者鎖定:✓ 你已指定業務主管,單一對象沒有搖擺」).
Case 8 confirms the bare-invocation path is unaffected.

**A third mis-specified assertion, same family as case 12's.** Case 14's `ambiguity-named-once`
originally demanded that the output name a *reader* ambiguity (cost owner vs customer-facing). All
four outputs, both arms, instead named whether the 99.9% is a contractual commitment or an internal
target — which is the unknown that actually governs the framing, the reader question being downstream
of it. The assertion was predicting a worse answer than the model gave; reworded to the real unknown.
Running tally for this skill's suite: assertions written as predictions of *how* the model will reason
keep failing; assertions written as checkable properties of the output hold up.

## Known limits of this run

The transcript in cases 8–12 is embedded in the prompt, so this measures target resolution against
a *stated* prior turn, not against genuine session state. Two behaviours in the new section are
therefore untested here and need real transcripts in `judged-cases.md`:

- stepping back over pure tool-work and status turns to reach the last turn that carried reasoning
  (resolution order, step 2);
- re-posing a question through the host's interactive question tool where one exists.
