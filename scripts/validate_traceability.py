#!/usr/bin/env python3
"""Validate the traceability matrix: requirement -> code -> test -> documentation.

A cheap gate meant to run before every documentation review. No dependencies.

Usage:  python3 scripts/validate_traceability.py [matrix_path]
Exit:   0 if clean, 1 if there are errors.
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "docs/traceability/matrix.csv")

COLUMNS = ["req", "title", "status", "version", "section_fd", "section_td",
           "components", "endpoints", "gateway_route", "tests", "adr", "notes"]
STATUSES = {"implemented", "partial", "pending", "withdrawn"}

errors, warnings = [], []


def paths(cell):
    return [p.strip() for p in (cell or "").split(";") if p.strip()]


def main():
    if not os.path.exists(MATRIX):
        print(f"ERROR: no matrix found at {MATRIX}")
        return 1

    with open(MATRIX, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    if not rows:
        print("WARNING: the matrix is empty.")
        return 0

    missing = [c for c in COLUMNS if c not in rows[0]]
    if missing:
        errors.append(f"header: missing columns {missing}")

    seen = set()
    for i, row in enumerate(rows, start=2):
        req = (row.get("req") or "").strip()
        ref = f"row {i} ({req or 'no id'})"

        if not req:
            errors.append(f"{ref}: missing requirement id")
        elif not re.fullmatch(r"R(N?)F-\d{3,}", req):
            warnings.append(f"{ref}: unexpected id format (expected RF-nnn or RNF-nnn)")
        elif req in seen:
            errors.append(f"{ref}: duplicate requirement")
        seen.add(req)

        status = (row.get("status") or "").strip().lower()
        if status not in STATUSES:
            errors.append(f"{ref}: status '{status}' is not valid (allowed: {sorted(STATUSES)})")

        for column in ("components", "tests"):
            for path in paths(row.get(column)):
                if not os.path.exists(os.path.join(ROOT, path)):
                    errors.append(f"{ref}: {column} points at a non-existent path -> {path}")

        for adr in paths(row.get("adr")):
            pattern = re.compile(rf"^0*{re.escape(adr.lstrip('0') or '0')}\b")
            adr_dir = os.path.join(ROOT, "docs/adr")
            found = os.path.isdir(adr_dir) and any(
                pattern.match(n) for n in os.listdir(adr_dir))
            if not found:
                errors.append(f"{ref}: ADR {adr} referenced but not found in docs/adr/")

        if status == "implemented":
            if not paths(row.get("components")):
                errors.append(f"{ref}: implemented with no code components")
            if not paths(row.get("tests")):
                errors.append(f"{ref}: implemented with no tests -> coverage gap")
            if not (row.get("section_fd") or "").strip():
                errors.append(f"{ref}: implemented with no Functional Design section")
            if not (row.get("section_td") or "").strip():
                errors.append(f"{ref}: implemented with no Technical Design section")
            if (row.get("endpoints") or "").strip() and not (row.get("gateway_route") or "").strip():
                warnings.append(f"{ref}: exposes endpoints with no gateway route declared")

        if status == "pending" and paths(row.get("components")):
            warnings.append(f"{ref}: marked pending but already has code attached")

    shown = os.path.relpath(MATRIX, ROOT)
    if shown.startswith(".."):
        shown = MATRIX
    print(f"Matrix: {shown} — {len(rows)} requirements\n")
    for w in warnings:
        print(f"  WARN   {w}")
    for e in errors:
        print(f"  ERROR  {e}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
