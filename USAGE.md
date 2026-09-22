# Usage guide, step by step

## The main idea, before anything else

This repository is the **master copy** of the template. The agents do not work from here:
they are copied **into the project's repository**, because they need the code and the
documents in front of them at the same time. That is the whole mechanic.

```
~/Documents/multiagent-engineering-team/   ← master. Improved here and propagated.
   └── copied into →  ~/code/client-project/   ← where they work
                        ├── .claude/     (agents, skills, commands)
                        ├── CLAUDE.md
                        ├── docs/
                        ├── scripts/
                        └── src/ ...     (the project's real code)
```

If you copy only `.claude/` you will have the agents but neither the gates nor the
templates. Copy everything the first time.

---

## Step 1 — Install into a project

```bash
cp -R .claude CLAUDE.md docs scripts /path/to/the-project-repo/
```

If the repo already has a `CLAUDE.md`, **do not overwrite it**: open both and merge the
content by hand. The project's file rules on code conventions; the template's contributes
the agent team's rules.

Open a Claude Code session at the root of that repository. Check it loaded by typing `/` —
`feature`, `sync-docs`, `docs-review` and `gateway-diagnosis` should appear. For agents,
asking for one by name is enough.

---

## Step 2 — Put the client's deliverables in place

```
docs/deliverables/
├── functional-design/
│   ├── DF-PROJ-001_v2.3.docx     ← last delivered version
│   └── DF-PROJ-001_v2.4.docx     ← working copy
└── technical-design/
    ├── DT-PROJ-001_v2.3.docx
    └── DT-PROJ-001_v2.4.docx
```

Rule: **a delivered version is never edited**. You start from it and write the next one.
The history is what lets you justify to the client what changed and when.

> These files are excluded by `.gitignore`. They are the client's documents and they do not
> belong in this repository.

---

## Step 3 — Extract the template (mandatory, once per document)

The profiles in `docs/templates/` are empty (`extracted: false`) and the documentation
agents are instructed to **refuse to edit** while they stay that way. This is deliberate:
without this step they would write in an invented format instead of the client's.

Ask:

> Extract the Technical Design template profile from
> `docs/deliverables/technical-design/DT-PROJ-001_v2.3.docx` and save it to
> `docs/templates/technical-design-profile.yaml`

Repeat for the functional one. Then **review the YAML yourself**, particularly three
fields:

- `structure` — that every section is there, with its exact numbering.
- `pending_marker` — how *this* document marks what is not yet implemented.
- `client_terminology` — the words the client uses and their forbidden synonyms. This is
  the field with the best return per minute invested: it is what stops the client's
  reviewer sending the document back because you said "user" where they say "caseworker".

---

## Step 4 — Load the traceability matrix

Edit `docs/traceability/matrix.csv` with the real requirements (delete the sample row). One
row per requirement. You do not have to fill everything at once: leave blank whatever you
do not know. Then:

```bash
python3 scripts/validate_traceability.py
```

The first run is uncomfortable on purpose: it surfaces the implemented requirements with no
test and no documentation section. That is its job. Do not fix it yet — it is your starting
photograph.

---

## Step 5 — A first dry run

Before letting anyone write, look at the state of what you already have:

```
/docs-review docs/deliverables/technical-design/DT-PROJ-001_v2.3.docx
```

Three agents review without touching anything: consistency against the code, style in
report mode, and the delivery checklist. Out comes a report with severities and owners.

This is also your calibration test: if the report says things you know are false, the
problem is in the template profile or in the matrix, and it gets fixed there before going
on.

---

## Step 6 — The full documentation cycle

```
/sync-docs version 2.4
```

Five rounds with a gate on each. You step in at two moments:

1. **After R2**, when it presents you the change-lists for both documents: which section is
   touched, what is done and why. That is where you decide. Read them: approving blind here
   is approving the whole cycle blind.
2. **After R3**, if IMPORTANT findings remain open and have to be justified in writing.

What happens inside:

| Round | Who | What |
|---|---|---|
| R0 | — | current version, template profile, code delta |
| R1 | `consistency-auditor` | what the document says that the code contradicts, and what exists in the code undocumented |
| R2 | `functional-analyst` + `technical-writer` | change-list → your approval → writing |
| R3 | `consistency-auditor` | audits what was just written. With blockers, R2 repeats |
| R4 | `style-editor` | naturalness pass, section by section, with invariant checking |
| R5 | `document-reviewer` | FIT / NOT FIT verdict |

**The order matters.** Style goes last because polishing text that is still going to change
is wasted work, and because polishing before verifying only makes a false sentence sound
better.

---

## Step 7 — The feature cycle

```
/feature RF-041 customer deactivation with mandatory reason
```

Architecture (if relevant) → implementation → code, security and QA review **in parallel**
→ traceability → documentation. Blockers go back to the developer and the review phase
repeats over the new diff.

If the change is small and local, skip the command and ask the `developer` directly.
`/feature` earns its keep when the change crosses services or touches a contract.

---

## Step 8 — Deployment and gateway diagnosis

```
/gateway-diagnosis 502 on /api/customers from pre-production, Kong 3.4
```

It imposes diagnosis before change: reproduce, read the **effective** configuration (not
the repo's), compare, and walk the usual suspects marking each as ruled out or confirmed
with evidence.

Built-in constraint: read commands free, write commands against any non-local environment
**only with your explicit confirmation**. It lives in `.claude/settings.json` and does not
depend on the agent behaving well.

---

## Invoking a single agent

You do not need a command for everything:

> Run `consistency-auditor` over section 5 of the Technical Design
> Have `style-editor` do a pass over section 4.2, report only
> `security`: review the new deactivation endpoint

This is what you will use most day to day.

---

## Things worth knowing

**Each agent starts without your conversation.** It has its own context and sees only what
it is given in the brief plus whatever it reads from the repository. If an important
decision was made talking to me and is not written down anywhere, the agent does not know
it. That is why the ADRs and the matrix are not bureaucracy: they are the channel through
which the agents find things out.

**The style pass has a safety net.** After each section:

```bash
python3 scripts/text_invariants.py before.md after.md
```

It fails if an identifier, a figure, a `§x.y`, an `RF-nnn`, an endpoint, a table row or a
code block changed. That is what lets you allow prose to be rewritten without watching every
line. It only works with text documents (Markdown); with `.docx` you will have to export the
section to compare.

**Style does not fix emptiness.** If a section says nothing, the fix is content, not
wording. `style-editor` rephrases; it does not invent.

**`NOT VERIFIABLE` is not a failure.** Claims of intent or of business cannot be checked
against the code. They come out marked and a person resolves them.

**None of this replaces your review before delivering.** It shortens the road to it.

---

## Maintaining the template

When you refine something on a project and it works — a writing tic typical of your client,
a new gateway suspect, a formatting rule — bring it back to the master copy so the next
project inherits it. That is what turns this into an asset rather than a throwaway
configuration.
