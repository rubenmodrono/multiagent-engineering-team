---
description: Architecture design cycle before building — drivers, options, data, contracts, threat surface and a consolidated ADR
argument-hint: <what has to be designed>
---

Design cycle for: **$ARGUMENTS**

You are the coordinator. Nothing gets implemented in this workflow: the output is a
decision, written down, that someone can disagree with on the evidence.

Use it when the change crosses services, creates one, touches the shared data model, or
modifies a contract. For anything local, skip it and go to `/feature`.

## D0 — Scope and drivers

Launch `architect`. Before comparing anything, it must name the 3-5 quality attributes that
actually govern this decision, and the client constraints that are not negotiable.

**Gate:** if the drivers cannot be named, the problem is not understood yet. Stop and say
so rather than designing against a vague target — a decision matrix scored on invented
drivers is worse than no matrix, because it looks rigorous.

## D1 — Options

Same agent. Two or three real options, each with its cost to change and its cost to live
with, scored against the drivers. A straw option does not count.

**Gate:** the winning option must carry an explicit statement of what it makes worse. Every
architectural decision loses something; if nothing is lost, the alternatives were not real.

## D2 — Data *(only if the decision touches persistence)*

Launch `data-architect` with the chosen option. Ownership of each entity, consistency
declared with a number, and the migration shaped as expand/contract with its rollback.

**Gate:** no entity written by two services. If the design requires it, it goes back to D1
— that constraint usually invalidates the option rather than the data model.

## D3 — Contracts *(only if it touches an API or events)*

Launch `contract-designer`. The contract, classified as compatible or breaking, and if
breaking, the named list of affected consumers.

**Gate:** a breaking change with no consumer list does not pass. "It looks like nobody uses
it" is not a check.

## D4 — Threat surface of the design

Launch `security` against the **design**, not against code that does not exist yet: what
the proposed shape exposes, who can reach it and with what identity, and what the trust
boundary between gateway and service looks like.

This phase exists because an authorisation flaw found in an ADR costs a paragraph, and the
same flaw found after implementation costs a sprint.

## D5 — Consolidation

`architect` writes a single ADR in `docs/adr/`, folding in what D2, D3 and D4 produced,
with its mandatory **Documentation implications** section.

Register the decision in `docs/traceability/matrix.csv` (`adr` column) for the affected
requirements.

## Closing

```
Decision: <one line, in the indicative>
Drivers it was scored against: ...
Discarded options and why: ...
What this decision makes worse: ...
Data:      <ownership and migration | not applicable>
Contracts: <compatible | breaking + consumers | not applicable>
Security:  <findings on the design>
ADR: docs/adr/NNNN-...
Next: /feature <scope> — or stop here if the decision still needs a person
```

**Gate before building:** the user confirms the decision. A design nobody approved is a
draft, however well argued.
