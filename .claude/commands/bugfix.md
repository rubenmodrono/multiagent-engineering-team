---
description: Bug cycle — reproduce, failing test first, root cause, minimal fix, and a sweep for the same defect elsewhere
argument-hint: <symptom: what fails, where, and how it was observed>
---

Bug cycle for: **$ARGUMENTS**

A bug is not a small feature. It has a different discipline, and it is the discipline that
this workflow enforces — not the fix, which is usually the easy part.

## B0 — Reproduce

Before reading any code, establish how the failure is triggered: input, state, environment,
and what is observed versus what is expected.

**Gate: no reproduction, no fix.** If it cannot be reproduced, that is the finding, and the
next step is instrumentation, not a patch. A fix applied to a bug nobody could trigger
cannot be verified, so nobody will ever know whether it worked.

If the report comes from a ticket or a wiki, treat it per the `external-sources` skill: it
describes what someone believed, and it gets checked against the real system.

## B1 — The failing test comes first

Launch `qa-tester` to write the test that reproduces the bug. It goes in **before** the fix.

**Gate:** the test must fail, and fail for the right reason. A test that passes before the
fix is testing something else; a test that fails with a different error is not covering
this bug.

This ordering is the whole point. Write the fix first and you get a test written to match
whatever the code now does, which confirms the fix instead of checking it.

## B2 — Root cause

Launch `code-reviewer` on the reproduction path, and `developer` with the evidence. Keep
asking why until you reach something that explains **all** the observed evidence, not just
the symptom.

The test: if your explanation does not account for some detail of the reproduction —
why it only happens on retry, why only for that tenant — you are looking at a symptom.

If the root cause turns out to be a design decision rather than a defect, stop and hand it
to `/design`. Patching around an architectural problem creates two problems.

## B3 — Fix

`developer` applies the **minimum** change that removes the cause. Anything else you notice
goes into the implementation note; it does not get fixed in passing. A bugfix that also
refactors is a bugfix nobody can review.

## B4 — Verify

The test from B1 now passes. The rest of the suite still passes. Report real numbers.

**Gate:** if any other test broke, that is not collateral damage to be adjusted. Either the
fix is wrong or the other test was encoding the bug.

## B5 — Where else does this live?

The phase everyone skips, and the one that pays.

Launch `qa-tester` and `code-reviewer` to find the **same pattern** elsewhere: the same
missing null check, the same unguarded retry, the same unvalidated boundary. A defect that
appeared once in a codebase has usually been copied two or three times.

Report each occurrence with `path:line`, whether it is exploitable there too, and let the
user decide the scope. Do not fix them silently inside a bugfix.

## B6 — Documentation and traceability

Only if the behaviour a deliverable describes actually changed. Most bugfixes restore the
documented behaviour and need no document change — say so explicitly rather than leaving it
implied.

Update `docs/traceability/matrix.csv` (`tests` column) with the new regression test.

## Closing

```
Symptom and reproduction: ...
Root cause: <what explains all the evidence> (path:line)
Fix: <minimum change>
Regression test: <path> — failed before, passes now
Suite: X passed, Y failed
Same pattern elsewhere: <list with path:line, or "none found">
Documentation: <changed | restores documented behaviour, no change>
```
