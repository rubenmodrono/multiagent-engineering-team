---
description: Full feature cycle — design, data, contract, implementation, reviews and documentation, with the phases that do not apply skipped out loud
argument-hint: <feature description or requirement id>
---

Coordinate the full cycle for: **$ARGUMENTS**

You are the coordinator. You do not implement: you delegate and act as the gate between
phases. Between phases, summarise in three lines and continue; stop to ask only when a
decision belongs to the user.

Several phases are conditional. **Skipping one is a decision, so say it out loud and say
why** — a phase silently omitted is indistinguishable from a phase forgotten.

## F0 — Triage

Before starting, check this is the right workflow:

| If the task is… | Use |
|---|---|
| Something that used to work and no longer does | `/bugfix` |
| Restructuring with no behaviour change | `/refactor` |
| A decision that crosses services, data or contracts, and is not yet taken | `/design` first, then come back |
| An operational failure in deployment or routing | `/gateway-diagnosis` |

If it is a feature, continue.

## F1 — Design

- Crosses services, creates one, or the shape is not decided → invoke `/design` and come
  back with the ADR.
- Contained, but with a non-obvious technical decision → launch `architect` alone.
- Local, following an established pattern → skip, and say so.

**Gate:** if a business decision is needed, stop and ask the user.

## F2 — Data and contract *(conditional, in parallel where independent)*

- Touches persistence → `data-architect`: ownership, consistency, migration as
  expand/contract with rollback.
- Touches an API or events → `contract-designer`: the contract, classified as compatible or
  breaking, and if breaking, the named consumers.

**Gate:** a breaking change does not proceed without its consumer list and a migration plan.

These two phases exist because `developer` is explicitly forbidden from deciding either.
Skipping them when they apply means the decision gets taken anyway, just by whoever is
writing the code at the time and without it being written down.

## F3 — Implementation

Launch `developer` with the ADR, the contract and the requirement. Require the
implementation note with its **documentation impact** section.

## F4 — Technical reviews, in parallel

Launch `code-reviewer`, `security` and `qa-tester` together, in a single block.

**Gate:** BLOCKING and CRITICAL findings go back to `developer` and this phase repeats over
the new diff. Nothing advances with open blockers.

## F5 — Non-functional *(conditional)*

- Touches a hot path, data access, or loops over collections → `performance-engineer`:
  measurement before and after, and a budget a test can check.
- Expected change in volume, or a new dependency that can fail → `nonfunctional-testing`:
  load, behaviour with the dependency degraded, and recovery time.

Neither runs against shared environments without explicit confirmation for that run.

## F6 — Traceability

Update `docs/traceability/matrix.csv` and run:

```bash
python3 scripts/validate_traceability.py
```

Fix what it reports. A requirement marked implemented with no test or no documentation
section fails the gate, and that is the gate working.

## F7 — Documentation

Invoke `/sync-docs` with the scope of this change.

## Closing

```
Delivered: ...
Phases skipped and why: ...          ← never leave this blank
Design:    <ADR | architect only | none needed>
Data:      <migration | not applicable>
Contract:  <compatible | breaking + consumers | not applicable>
Findings:  closed A / knowingly accepted B (with reason) / open C
Tests:     X passed, Y failed        ← real numbers, from a real run
Performance / load: <measured | not applicable>
Documentation sections touched: ...
Outstanding: ...                     ← explicit, even if empty
```
