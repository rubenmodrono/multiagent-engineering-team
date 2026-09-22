---
description: Full documentation cycle with review rounds — updates Functional and Technical Design and leaves them fit for delivery
argument-hint: <scope: version, feature or "everything">
---

Documentation cycle for scope: **$ARGUMENTS**

The rounds are sequential and each one has a gate. Skipping a round invalidates the
cycle: say so if the user asks for it, and do it only if they insist.

## R0 — Baseline
1. Identify the current version of each deliverable in `docs/deliverables/`.
2. Verify or extract the template profiles (skill `document-template`).
3. Gather the delta: implementation notes, ADRs, delivered diff, traceability matrix.

## R1 — Prior audit
Launch `consistency-auditor` over the current deliverables against the current code, in
**both directions**.
Output: a list of findings, each with its owner. That list is the brief for the following
rounds — nothing gets written that does not come from it or from the delta.

## R2 — Writing
Launch `functional-analyst` and `technical-writer` in parallel.
Both deliver a **change-list first**. Present the two change-lists to the user together.
**Gate:** the user confirms before anything is applied. New sections need explicit
approval.

## R3 — Verification audit
Launch `consistency-auditor` again, now over the edited documents.
**Gate:** zero BLOCKING findings. Open IMPORTANT findings require written justification
from the user. If blockers remain, back to R2 — and the iteration is counted.

## R4 — Style pass
Launch `style-editor` over the modified sections, never over the whole document.
After each section, verify invariants with `scripts/text_invariants.py`.
**Gate:** if the editor reports that an improvement required touching content, go back to
R2 for that section.

## R5 — Delivery review
Launch `document-reviewer`.
**Gate:** a FIT verdict. Each blocker goes back to its owner and R5 repeats.

## Closing
```
Deliverables updated: <file> vX.Y → vX.Z
R2↔R3 iterations: N
Findings: closed A / accepted B (with reason) / open C
Delivery verdict: FIT | NOT FIT
Traceability: requirements with no documentation section → list
Sections touched: ...
```
