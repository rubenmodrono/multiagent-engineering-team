---
name: traceability
description: Maintain and query the traceability matrix linking requirements, code components, endpoints, tests and documentation sections. Use when implementing a requirement, updating documentation, designing tests, and auditing consistency between document and code.
---

# Traceability matrix

This is the mechanism that turns "the documentation is consistent with the code" into
something **checkable** rather than arguable. Without it, every audit starts from zero
again.

## The file

`docs/traceability/matrix.csv`, one row per requirement.

| column | content | example |
|---|---|---|
| `req` | requirement id | `RF-041` |
| `title` | short statement | `Customer deactivation with mandatory reason` |
| `status` | `implemented` / `partial` / `pending` / `withdrawn` | `implemented` |
| `version` | deliverable version it lands in | `2.4` |
| `section_fd` | Functional Design section | `4.3.2` |
| `section_td` | Technical Design section | `5.1.7` |
| `components` | code paths, `;`-separated | `svc-customers/src/deactivate/handler.go` |
| `endpoints` | method and path, `;`-separated | `DELETE /v1/customers/{id}` |
| `gateway_route` | route declared in the API gateway | `/api/customers/*` |
| `tests` | test paths, `;`-separated | `svc-customers/test/deactivate_test.go` |
| `adr` | ADRs affecting it | `0007` |
| `notes` | whatever does not fit above | |

## Who touches what

- `developer`: `status`, `components`, `endpoints` on implementation.
- `qa-tester`: `tests`, and spots rows with `status: implemented` and an empty `tests`.
- `functional-analyst` / `technical-writer`: `section_fd`, `section_td`.
- `contract-designer`: `endpoints`, and checks they match the served contract.
- `platform-devops`: `gateway_route`.
- `consistency-auditor`: does not edit it; uses it as a starting point and reports what is
  missing.

## Automated validation

```bash
python3 scripts/validate_traceability.py
```

Checks that code and test paths exist, that there are no duplicate requirement ids, that
every implemented requirement has a test and a documentation section, and that referenced
ADRs exist. It is a cheap gate: run it before every documentation review.

## Use in an audit

The matrix gives you **direction A** (requirement → code). **Direction B** (code →
document) cannot come out of the matrix by definition: it requires enumerating the
repository. Both directions are mandatory.
