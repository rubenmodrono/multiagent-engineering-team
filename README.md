# Multiagent engineering team

Fifteen specialised agents, four workflows and two automated gates, on Claude Code. Covers
the engineering cycle and, above all, keeping the Functional Design and Technical Design
deliverables consistent with the code.

## The team

Each agent has one scope and an explicit list of what it does **not** do. That boundary is
the point: if two agents review the same thing, the second confirms the first instead of
contributing.

### Architecture and contracts

| Agent | What it does | Where it stops |
|---|---|---|
| `architect` | Decides the shape of the system. Drivers, real options, decision matrix, ADR | Does not implement, does not write deliverables |
| `data-architect` | Data model, data ownership between services, expand/contract migrations | Does not set service boundaries, does not run remote migrations |
| `contract-designer` | REST and event contracts. Classifies every change as compatible or breaking before designing it | Does not implement the endpoint, does not configure the gateway |

### Build and verify

| Agent | What it does | Where it stops |
|---|---|---|
| `developer` | Scoped implementation, copying the repository's existing idiom | Does not touch contracts without an ADR, nor infrastructure, nor deliverables |
| `code-reviewer` | Correctness defects in the diff, each with a concrete failure scenario | Does not opine on style, security or coverage |
| `security` | Threat surface, OWASP API checklist, secrets, gateway ↔ service boundary | Does not attack real environments |
| `qa-tester` | Functional test design and execution, coverage against requirements | Does not modify production to make a test pass |
| `performance-engineer` | Turns declared latency drivers into measurements with a budget a test can check | Does not optimise without measuring, does not touch indexes or schema |
| `nonfunctional-testing` | Load, resilience, recovery. Synthetic test data | Does not fix what it finds, never copies production data |
| `platform-devops` | Deployment, Kubernetes, CI/CD, API gateway diagnosis | Does not apply remote changes without confirmation |

### Documentation

| Agent | What it does | Where it stops |
|---|---|---|
| `functional-analyst` | Functional Design, in business language | Does not descend into technology |
| `technical-writer` | Technical Design, every claim anchored to `path:line` | Does not describe the unimplemented in the present tense |
| `consistency-auditor` | Contrasts document against code, in both directions | **Edits nothing** |
| `style-editor` | Voice and naturalness, section by section | Does not touch technical content |
| `document-reviewer` | Template, format, metadata. FIT / NOT FIT verdict | Does not correct, reports |

## How agents are activated

Three ways, escalating from suggestion to guarantee.

**1. Automatically.** Claude reads the `description` field of each agent and delegates when
your request matches it. You do not have to name anyone:

> The customer deactivation endpoint returns a 500 on retry

That reaches `code-reviewer` or `qa-tester` on its own, because their descriptions say when
they apply. This is what makes the descriptions in the frontmatter worth writing carefully:
they are not documentation, they are the routing table.

**2. By name, in natural language.** A suggestion — Claude still decides:

> Use the consistency-auditor subagent on section 5 of the Technical Design

**3. `@agent-<name>` — guaranteed.** Type `@` and pick from the list, or write it out. This
one always runs that specific agent:

> @agent-security review the new deactivation endpoint

Use the third form when you know exactly who you want and do not want Claude reinterpreting
the request. The workflows in `.claude/commands/` orchestrate several agents in sequence,
with a gate between phases.

> Agent files are watched: edit one and the change is picked up within seconds, with no
> restart. A restart is only needed when you create the `agents` directory for the first
> time.

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

For a single agent, see [How agents are activated](#how-agents-are-activated) above.

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
