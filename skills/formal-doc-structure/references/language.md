# Language, drafting patterns, and fixes

Self-contained language discipline for internal business documents. For broad AI-ism cleanup on arbitrary text with no structural work, `avoid-ai-writing` / `clean-ai-writing` go deeper — but everything needed for internal docs is here.

## Prohibited filler

Remove sentences that add none of: decision, requirement, constraint, risk, responsibility, deliverable, timeline, verification method, follow-up action, concrete explanation.

Empty slogans to delete or rewrite:

- 全面提升, 有效賦能, 打造完整生態, 建立堅實基礎, 邁向新里程碑, 深化整體效益
- 不僅……更能……, 不是……而是……

Do not restate the same idea in different words. Avoid filler transitions, broad claims, and abstract conclusions with no operational meaning.

## Affirmative planning language

Write what will be done, proposed, provided, and how it is verified:

- 預計採……, 規劃……, 建議……, 應提供……, 需完成……, 由……負責……, 成果包含……, 後續依……辦理……

Avoid negative framing — 不建議……, 不宜……, 不能只是……, 不是……而是……. When contrast is necessary, rewrite as a direct implementation statement.

> Poor: 不建議僅以會議討論作為結論，而是要形成後續追蹤項目。
> Better: 會議結論需整理為後續追蹤項目，並列明負責單位、預計完成時間及檢核方式。

## Avoid excessive adjectives

> Poor: 建立完整、穩健、高效、可持續的管理機制。
> Better: 建立可追蹤之分工、檢核、驗收及後續追蹤機制。

---

## Language preferences (Taiwan business usage)

Traditional Chinese, Taiwan-standard terms. Avoid PRC-style phrasing unless quoting source material.

Prefer: 計畫, 規劃, 執行, 檢核, 驗收, 單位, 廠商, 資訊, 系統, 作業, 文件, 專案, 講師, 顧問, 主管, 承辦單位, 權責單位, 待辦事項, 後續追蹤.

Keep common technical / workplace terms in English when that is standard in the workplace — do not force-translate: API, Lab, Git, CI/CD, Kubernetes, SRE, Open Source, Dashboard, Runbook, Incident Report, Namespace, Ingress, PVC, PoC, RFP, SLA.

Prefer concise Chinese headings, English only for technical terms: 文件定位與規劃前提, 現況與需求說明, 方案與執行方式, 權責分工, 課程與 Lab 設計, 廠商合作範圍, 評估與驗收方式, 後續追蹤事項.

---

## Drafting patterns

Reusable paragraph skeletons.

**1. Document purpose**
> 本文件用於說明……，作為後續……之依據。內容包含……，並聚焦於……。

**2. Background and need**
> 因應……，目前需先完成……。本案預計透過……方式辦理，以支援後續……作業。

**3. Execution model**
> 本案預計採「……、……、……」方式執行。前期以……為主，中期進行……，後續依……結果辦理。

**4. Responsibility split**
> 承辦單位負責……；協作單位負責……；廠商負責……。相關成果由……彙整，並定期提交……檢視。

**5. Vendor requirement**
> 廠商需提供……，範圍包含……。交付內容需可供本單位後續留存、複用及檢核。

**6. Risk and control**
> 本案主要風險為……。後續預計透過……方式控管，並由……定期追蹤處理情形。

**7. Acceptance**
> 驗收時需檢附……，並確認……。未完成項目列入問題追蹤表，由……於……前完成補正。

---

## Content style

### Be concrete enough to execute

Include details that let the user assign work, negotiate with vendors, brief executives, review, or verify: responsible unit, action owner, timeframe, scope boundary, required deliverables, acceptance criteria, review cadence, risk-control method, required evidence, follow-up mechanism.

> Poor: 需加強後續管理。
> Better: 後續由承辦單位每月彙整執行情形，內容包含進度、待辦事項、風險、需主管協調事項及預計完成時間。

### Connect proposals to daily operations

When a plan affects personnel, departments, or vendors, explain how it connects to regular work — which unit owns it, what daily tasks are involved, what outputs result, how supervisors review, how external parties support, how results are retained or reused.

> 承辦單位負責日常作業安排與成果確認；外部廠商負責工具設定、文件提供及問題排除支援；每月由專案窗口彙整進度與待處理事項。

### Specify where responsibilities belong

Name what each party does: responsible unit, supporting unit, review unit, vendor role, supervisor role, output owner, escalation path. Avoid 共同推動 unless followed by a clear division of work.

### Include verification and deliverables

Every important activity gets a corresponding output:

- Meeting → minutes, decisions, action items
- Review → assessment memo, findings, follow-up list
- Vendor work → deliverables, acceptance record, issue log
- Training / workshop → materials, attendance, assignments, evaluation
- System task → test record, deployment record, rollback plan
- Risk control → evidence, monitoring report, review record

---

## Common fixes

**Abstract claim → deliverables**
> Poor: 本案將提升管理效率並強化作業品質。
> Better: 本案完成後，需產出作業流程、檢核表、問題追蹤表及月度執行情形報告。

**Vague action → schedule and output**
> Poor: 後續持續追蹤。
> Better: 後續由承辦單位每月彙整進度，內容包含已完成事項、待辦事項、風險、需協調事項及預計完成時間。

**Broad collaboration → role split**
> Poor: 由內外部共同合作推動。
> Better: 承辦單位負責需求確認與成果驗收；協作單位負責資料提供與作業配合；廠商負責交付文件、環境設定與問題排除。

**Generic evaluation → evidence**
> Poor: 依執行情形進行評估。
> Better: 評估資料包含交付文件、測試紀錄、會議紀錄、問題追蹤表、驗收紀錄及主管評語。

**Excessive contrast → direct wording**
> Poor: 本案不是單純導入工具，而是建立完整管理機制。
> Better: 本案預計同步建立工具設定、作業流程、權責分工、檢核表及後續追蹤機制。

---

## Output expectations

1. Produce a usable draft, not just advice.
2. Prefer complete sections that paste into a document.
3. Use tables where they improve execution clarity.
4. Keep paragraphs short and direct.
5. Remove duplicated explanation.
6. Make assumptions explicit when needed.
7. Focus on what will be done, by whom, when, what will be delivered, and how it will be verified.
