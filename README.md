# Multiagent engineering team

Fifteen specialised agents, four workflows and two automated gates, on Claude Code. Covers
the engineering cycle and, above all, keeping the Functional Design and Technical Design
deliverables consistent with the code.

## Installation

Copy the `.claude/` folder, `CLAUDE.md`, `docs/` and `scripts/` into the root of the
project's repository. The agents and commands become available as soon as you open a
session there.

```
.claude/agents/      15 specialised agents
.claude/skills/      shared knowledge (templates, style, traceability, external sources)
.claude/commands/    the four workflows
.claude/settings.json permissions: reads free, writes against environments need confirmation
docs/templates/      template profile extracted from the client's documents
docs/deliverables/   current versions of the documents
docs/traceability/   matrix requirement ↔ code ↔ test ↔ section
docs/adr/            architecture decisions
scripts/             automated gates
```

## Getting started, in order

1. **Extract the real templates.** The profiles in `docs/templates/` are empty. With the
   current version of each deliverable in front of you:

   > Extract the Technical Design template profile from
   > `docs/deliverables/technical-design/DT-…v2.3.docx`

   Without this step, the documentation agents must not touch the deliverables. It is the
   step that makes the documentation come out in the client's format rather than an
   invented one.

2. **Load the traceability matrix** with the real requirements, and run the validator:

   ```bash
   python3 scripts/validate_traceability.py
   ```

   The first run is usually uncomfortable: it surfaces the requirements with no tests and
   the implemented ones with no documentation section. That is exactly its job.

3. **Calibrate the document's voice.** The first time you use `style-editor`, ask it to
   write the voice calibration down and save it. Later rounds start from there.

4. **A first dry run**: `/docs-review docs/deliverables/…` over the current version,
   changing nothing. It tells you the real starting state.

## Usage

```
/feature RF-041 customer deactivation with mandatory reason
/sync-docs version 2.4
/docs-review docs/deliverables/technical-design/DT-PROJ-001_v2.4.md
/gateway-diagnosis 502 on /api/customers from pre-production
```

You can also invoke a single agent: *"run consistency-auditor over section 5"*.

## The documentation cycle

```
R0 baseline ─→ R1 audit ─→ R2 writing ─→ R3 verification ─→ R4 style ─→ R5 delivery
                   ▲                          │
                   └───────── while blockers ─┘
                              remain open
```

Three design decisions hold the result up:

- **The auditor does not write and the writer does not audit itself.** An agent correcting
  what it wrote itself confirms its own work. The separation is what makes the review worth
  anything.
- **The audit runs in both directions.** From document to code (is what it says true?) and
  from code to document (is what exists documented?). The second is the one nobody does,
  and the one that surfaces the endpoints, configuration parameters and error codes that
  never made it into the deliverable.
- **Style comes last.** Polishing text that is still going to change is wasted work, and
  polishing before verifying only makes a false sentence sound better.

## Automated gates

`validate_traceability.py` — duplicate requirements, non-existent paths, implemented items
with no test or no documentation section, endpoints with no gateway route, phantom ADRs.

`text_invariants.py` — compares the text before and after the style pass and fails if
identifiers, figures, `§x.y` references, `RF-nnn` codes, endpoints, tables or code blocks
have changed. It is the safety net that lets you allow prose to be rewritten without fearing
that the content will be corrupted.

## Limits worth knowing

- The agents read the repository, not the mind of whoever wrote the document a year ago.
  Claims of intent or of business come out as `NOT VERIFIABLE` and a person has to resolve
  them.
- The style pass improves prose; it does not turn an empty document into a good one. If a
  section says nothing, the fix is content, not wording.
- None of this replaces human review before delivering to the client. It shortens the road
  to it.

## A note on language

The agents' instructions are in English. The deliverables they maintain are written in the
project's working language, following the client's own document — the `writing-style` skill
calibrates against it before touching anything.
