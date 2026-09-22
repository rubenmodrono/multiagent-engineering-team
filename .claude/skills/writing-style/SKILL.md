---
name: writing-style
description: Writing and naturalness guide for documentation deliverables — how to make the text read as if written by someone on the team, in the original document's voice, without touching technical content. Use in the style pass of any delivery document, and whenever drafted text reads as generic, flat or mechanical.
---

# Style and naturalness in delivery documentation

Deliverables are written in the project's working language, which is often not English.
The tics catalogued here appear in every language; step 0 is what adapts the rest of this
skill to the one in front of you.

## What "humanising" means here

It is not disguising anything. It is a concrete, old editorial problem: a delivery
document is written by several hands over several rounds, in a hurry, and ends up with
seams — one dense section and one hollow one, one section impersonal and the next in the
first person plural, paragraphs that say nothing across six lines. The style pass sews
that up.

The operational goal is twofold:

1. **One voice**: the whole document sounds like the same team.
2. **Honest density**: every paragraph gives the reader something they did not know. What
   does not, goes.

Model-generated text has characteristic defects, but they are the same defects a human
produces writing without care and at speed: abstraction, excessive symmetry and a refusal
to commit. Fixing them is writing better, not camouflage.

## Step 0 — Calibrate the voice (mandatory, before touching anything)

Take two or three sections you know were written by the human team (earlier versions of
the document, other deliverables from the same project) and note:

- **Average sentence length and, above all, its variance.** Mechanical prose produces
  sentences of near-uniform length, one after another. Human prose alternates: one of 35
  words, one of 8, one of 20.
- **Person and address**: impersonal, first person plural, system-as-subject ("the module
  validates").
- **How much passive voice**, and which impersonal constructions the language offers.
- **When lists and when prose.** Many teams reserve lists for closed enumerations and
  explain processes in prose.
- **The client's terminology**: their exact word for the thing.
- **Degree of hedging**: whether the document says "is estimated to" or says "will".

Write the calibration down in two lines before you start. It is your yardstick, and it
overrides any preference of your own.

## Catalogue of tics, with the fix

**1. Uniform sentence length**
The most telling defect and the least obvious. Break it deliberately: mix a long sentence
carrying subordinate clauses, a medium one, and a short one that lands. A five-word
sentence after two long ones does more for naturalness than any other technique.

**2. Automatic tricolon** — always three items, out of habit.
> ❌ The solution delivers scalability, maintainability and traceability.
> ✅ The solution improves traceability of operations. On scalability it changes nothing
> relative to the previous version.

**3. Empty preambles**
`It is important to note that`, `it should be pointed out that`, `in this regard`, `the
following section details`, `the purpose of this document is to describe how`.
> ❌ It is important to note that the service validates the token on every request.
> ✅ The service validates the token on every request.

Rule: if deleting a paragraph's first sentence leaves the paragraph saying the same thing,
that sentence was surplus.

**4. A summary paragraph at the end of every section**
`In conclusion, this architecture allows…`. No section of a technical design needs to
summarise itself. Delete them.

**5. Excessive structural symmetry**
Every section the same shape: two-line intro, four-bullet list, two-line close. Reality is
not symmetrical: some components deserve two pages and others two lines. Let the document
be uneven, because the system is.

**6. Lists with perfect parallelism**
Six bullets all starting with a gerund and all the same length. If three of the six are
trivial, they go into one sentence of prose and the list keeps the three that matter.

**7. Paired adjectives with no content**
`robust and scalable`, `efficient and flexible`, `modern and decoupled`.
> ❌ A robust and scalable architecture has been implemented.
> ✅ Each service deploys separately, so a fault in settlement does not take down customer
> onboarding.

Always replace the adjective with the mechanism that justifies it. If there is no
mechanism, the adjective was a lie.

**8. Over-signalled connectives**
`Furthermore,` `On the other hand,` `Likewise,` `Consequently,` at the start of every
paragraph. Technical prose tolerates juxtaposition perfectly well. Keep a connective where
it marks a real relation; remove the rest.

**9. Abstraction with no anchor**
> ❌ Appropriate error-handling mechanisms have been applied.
> ✅ Gateway errors are retried three times with exponential backoff; beyond that the
> operation is marked as failed and moves to the manual review queue.

**10. Refusal to commit**
A design document that never says what was discarded or what hurts is a brochure. Wherever
there is a decision, the rejected alternative and the price paid should appear. That is
what most "sounds like a person", because only someone who was in the discussion writes
it.

**11. Em dashes and colons in excess**
Well used, a resource. Three per page, a tic. Count them and spread them out.

**12. Timeless present for what is not implemented**
`The system notifies the user` when it does not yet notify. This is not style, it is a
content defect: report it to the writer instead of rewriting it.

## Positive techniques

- **Start with the fact, not the frame.** "The gateway `timeout` is 30 seconds" before "as
  regards the configuration of waiting times…".
- **Name the agents.** "The gateway rejects" reads better, and audits better, than
  "requests are rejected".
- **Concrete detail wherever it exists.** A number, a filename, a real case are worth more
  than a paragraph of qualities.
- **Admit what is not known.** "We have not measured the impact on p99 beyond 200
  concurrent connections" is an excellent sentence in a technical design, and no generator
  writes it unprompted.
- **Read the paragraph aloud.** If you run out of breath or get bored, so does the reader.

## Invariants: do not touch

Identifiers, paths, endpoints, field/table/service names. Figures, thresholds, versions,
dates. `RF-nnn` codes and `§x.y` references. Tables, code blocks, diagrams. Glossary
terms. Headings and numbering.

Check after each section:

```bash
python3 scripts/text_invariants.py <before.md> <after.md>
```

If the script reports differences in identifiers, figures or references, the style pass has
corrupted content: revert that section.

**If improving the style requires changing an invariant, stop and report it.** Style never
beats content.
