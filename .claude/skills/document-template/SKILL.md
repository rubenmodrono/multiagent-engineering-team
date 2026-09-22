---
name: document-template
description: Extract, pin down and respect the template and format of an existing documentation deliverable (Functional Design, Technical Design or other). Use before editing any delivery document, when the template profile for a new document has to be created, or whenever there is doubt about whether a change respects the client's format.
---

# Deliverable template and format

The client's document rules. There is no such thing as "my way of structuring a technical
design": there is this document's way.

## 1. Extract the template profile

From the current version of the deliverable, extract and save to
`docs/templates/<document>-profile.yaml`:

```yaml
document: Technical Design
code: DT-PROJ-001
source_format: docx | confluence | markdown | asciidoc
analysed_version: "2.3"

cover:
  fields: [title, code, version, date, client, project, classification, author, approver]

version_control:
  location: "section 0.1"
  columns: [version, date, author, description, approved_by]
  version_convention: "major.minor — major if scope changes"

structure:
  - { n: "1",   title: "Introduction",  required: true }
  - { n: "1.1", title: "Purpose",       required: true }
  - { n: "1.2", title: "Scope",         required: true }
  - { n: "2",   title: "Architecture",  required: true }
  # ... the real structure, in full

conventions:
  section_numbering: "1.2.3 down to the third level"
  figures: "Figure N: <title>, caption below, referenced from the text"
  tables: "Table N: <title>, caption above"
  pending_marker: "[PENDING v2.4]"   # how THIS document marks what is not implemented
  requirements: "RF-nnn / RNF-nnn"
  cross_references: "see §4.2.1"
  diagrams: { tool: plantuml, source: "docs/diagrams/*.puml" }

client_terminology:
  - use "case file", never "case" or "ticket"
  - use "caseworker", never "backoffice user"

prohibitions:
  - do not renumber existing sections
  - do not change the diagramming tool
  - do not introduce new sections without recorded approval
```

If the profile already exists, **verify it against the current document** before using it:
client templates change without warning.

## 2. Editing rules

- **Numbering is an external contract.** Client minutes, emails and tickets reference
  "§4.2.1". Renumbering breaks traceability outside your control. If something must be
  inserted, use a suffix (4.2.1.bis) or propose the renumbering explicitly.
- **A new section is a decision, not an initiative.** It is proposed in the change-list;
  the user decides.
- **Level of abstraction per document**: the functional one does not descend into
  technology, the technical one does not rise into business narrative. If content sits in
  the wrong document, report it; do not move it on your own initiative.
- **What is not implemented is marked with the template's marker.** Never described in the
  present tense.
- **Version control**: a new row per delivery, following the document's convention.

## 3. Working with each source format

**Markdown / AsciiDoc in the repository** — the comfortable case. Direct editing,
reviewable diff. It is the recommended target format if the client can ever be persuaded.

**.docx** — use the `docx` skill. Preserve named styles (`Heading 2`, `Client-Table`), not
direct formatting: the table of contents and automatic numbering depend on them. If the
client reviews with tracked changes, deliver with changes marked.

**Confluence** — the content lives in *storage format* (XHTML with macros). When editing:

- Preserve the macros (`toc`, `status`, `expand`, `jira`, `info`) exactly; breaking a macro
  breaks the page for everyone.
- Preserve the anchors: inbound links from other pages depend on them.
- Confluence versions every save. One edit = one version, with a descriptive version
  comment.
- **Never publish an edit the user has not reviewed.** A Confluence page is visible to the
  whole client the moment it is saved.

## 4. Mandatory output: change-list before editing

```
§4.2.1 <title>  — MODIFY        — <what and why, with the evidence>
§4.3   <title>  — ADD           — <what and why>
§6.1   <title>  — MARK PENDING  — <not implemented in this version>
§7     <title>  — NO CHANGES
```

It is presented, confirmation is awaited, and only then is anything edited.
