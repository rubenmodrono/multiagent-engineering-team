---
description: Review of an already written document — consistency, style and format, without rewriting it
argument-hint: <document path>
---

Review the document **$ARGUMENTS** without rewriting it. Three passes, three agents, one
report.

1. `consistency-auditor` — against the current code, in both directions.
2. `style-editor` — **in report mode, no edits**: a list of paragraphs that read as
   filler, sections whose voice differs from the rest of the document, and claims with no
   concrete anchor. It must not apply any change.
3. `document-reviewer` — the full delivery checklist.

A single report, ordered by severity, naming the owner of each finding and an estimate of
the effort to fix it (low / medium / high).

Close by asking the user: shall I run `/sync-docs` to fix these, or deliver the report as
it stands?
