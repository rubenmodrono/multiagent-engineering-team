---
description: Behaviour-preserving change — characterisation tests first, then restructure, with the tests as the invariant
argument-hint: <what to restructure and why>
---

Refactor for: **$ARGUMENTS**

A refactor changes the shape of the code and **nothing else**. The moment observable
behaviour changes, this stops being a refactor and becomes a feature or a bug, and it needs
a different workflow and a different review.

## The rule that governs everything here

**If a test has to change, it is not a refactor.**

That is the sharpest line available, and it is what makes a refactor reviewable. A test
modified halfway through is the standard way an accidental behaviour change gets through:
the test goes red, it gets "adjusted", and the regression ships looking green.

If a test genuinely has to change, stop, say which one and why, and let the user decide
whether this is still a refactor.

## R0 — Boundary

Define what must not change: the public API, the events emitted, the persisted shape, the
error codes, the observable side effects. That set is the contract you are preserving.

State also what you **are** allowed to change: internal structure, private names, file
layout, the order of operations where order is not observable.

## R1 — Characterisation tests

Launch `qa-tester`. Before touching anything, the current behaviour must be covered — the
real behaviour, including the parts that look wrong.

**Gate: you cannot refactor what you cannot verify.** If coverage of the affected area is
thin, writing those tests *is* the first half of this task, and they go in as their own
commit before any restructuring.

A characterisation test documents what the code does today, not what it should do. If you
find behaviour that looks like a bug, capture it as it is and report it. Fixing it here
would break the one guarantee this workflow offers.

## R2 — Restructure

Launch `developer`. In behaviour-preserving steps, each one small enough that the suite can
run between them.

`developer` follows the repository's existing idiom, as always. A refactor that introduces
a pattern the codebase does not use has traded one inconsistency for another.

## R3 — Verify the invariant

The same tests, unmodified, with the same results.

**Gate:** zero test files modified. Run the check explicitly and report it:

```bash
git diff --name-only <base> -- '*test*' '*spec*'
```

An empty output is the proof that this was a refactor. Anything else needs an explanation
before the change is accepted.

## R4 — Reviews

Launch `code-reviewer` on the diff, looking for behaviour that drifted — the boundary
conditions, the order of side effects, the error paths, which is where refactors actually
leak.

If the code is on a hot path, launch `performance-engineer` too: measure before and after.
A restructure that is neutral in behaviour can be expensive in time, and the usual culprit
is an abstraction that turned one query into N.

## R5 — Documentation

Usually none: a refactor does not change what the document describes. If it moved a
component or renamed something the Technical Design names explicitly, that is a
`technical-writer` change and nothing more.

Update `docs/traceability/matrix.csv` (`components` column) if paths moved — stale paths
there will fail the traceability gate on the next documentation review.

## Closing

```
Boundary preserved: <API, events, persistence, error codes>
Characterisation tests added: <N, path>
Restructure: <what moved>
Test files modified: 0   ← if not zero, explain
Suite: X passed, Y failed
Performance: <before → after | not on a hot path>
Traceability: <paths updated | unchanged>
```
