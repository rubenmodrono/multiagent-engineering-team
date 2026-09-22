---
description: Full feature cycle — design, implementation, reviews and documentation update
argument-hint: <feature description or requirement id>
---

Coordinate the full cycle for: **$ARGUMENTS**

You are the coordinator. You do not implement: you delegate to the team's agents and act
as the gate between phases. Between phases, summarise in three lines and continue; stop
to ask only when a decision belongs to the user.

## Phase 1 — Design
Launch `architect`. If the change is local and touches neither contracts nor
infrastructure, skip this phase and say so.
**Gate:** if the architect needs a business decision, stop and ask the user.

## Phase 2 — Implementation
Launch `developer` with the ADR (if any) and the requirement. Require the implementation
note including its **documentation impact** section.

## Phase 3 — Technical reviews, in parallel
Launch `code-reviewer`, `security` and `qa-tester` together, in a single block.
**Gate:** BLOCKING and CRITICAL findings go back to `developer` and phase 3 repeats on the
new diff. Nothing advances with open blockers.

## Phase 4 — Traceability
Update `docs/traceability/matrix.csv` and run `python3 scripts/validate_traceability.py`.
Fix whatever it reports.

## Phase 5 — Documentation
Invoke `/sync-docs` with the scope of this change.

## Closing
Final report:
- what was delivered
- findings closed, and findings knowingly accepted with the reason
- real test suite result, with numbers
- documentation sections touched
- **what remains outstanding**, stated explicitly
