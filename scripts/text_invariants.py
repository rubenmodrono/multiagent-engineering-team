#!/usr/bin/env python3
"""Check that a style pass has not altered technical content.

Extracts from both versions the elements that rewriting must NEVER touch
-- requirement ids, section references, figures, identifiers, endpoints,
URLs, tables and code blocks -- and compares the sets.

Usage:  python3 scripts/text_invariants.py before.md after.md
Exit:   0 if the invariants hold, 1 if any of them changed.
"""
import re
import sys
from collections import Counter

PATTERNS = {
    "requirements": r"\bR(?:N)?F-\d{3,}\b",
    "references":   r"§\s?\d+(?:\.\d+)*",
    "adr":          r"\bADR-\d{3,}\b",
    "endpoints":    r"\b(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+/[^\s`\)\|]*",
    "urls":         r"https?://[^\s`\)\|]+",
    "identifiers":  r"`[^`\n]+`",
    "versions":     r"\bv?\d+\.\d+(?:\.\d+)*\b",
    "figures":      r"(?<![\w.])\d{1,3}(?:[.,]\d+)?\s?(?:ms|s|min|h|KB|MB|GB|%|€|\$|retries|retry|seconds?|minutes?)\b",
}
CODE_BLOCK = re.compile(r"```.*?```", re.S)
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.M)


def extract(text):
    out = {"code_blocks": Counter(b.strip() for b in CODE_BLOCK.findall(text))}
    out["table_rows"] = Counter(
        re.sub(r"\s+", " ", r).strip() for r in TABLE_ROW.findall(text))
    without_code = CODE_BLOCK.sub(" ", text)
    for name, pattern in PATTERNS.items():
        out[name] = Counter(m.strip() for m in re.findall(pattern, without_code))
    return out


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    before, after = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
    b, a = extract(before), extract(after)

    findings = 0
    for key in b:
        lost = b[key] - a[key]
        added = a[key] - b[key]
        if not lost and not added:
            continue
        findings += sum(lost.values()) + sum(added.values())
        print(f"\n[{key}]")
        for item, n in lost.items():
            print(f"  GONE   (x{n}): {item[:110]}")
        for item, n in added.items():
            print(f"  NEW    (x{n}): {item[:110]}")

    words_before = len(before.split())
    words_after = len(after.split())
    delta = (words_after - words_before) / max(words_before, 1) * 100

    print(f"\nWords: {words_before} -> {words_after} ({delta:+.1f} %)")
    if abs(delta) > 25:
        print("  WARNING: length changed by more than 25 %. A style pass rephrases;")
        print("           if the text grows or shrinks this much, content was added")
        print("           or removed.")

    if findings:
        print(f"\n{findings} invariants altered. REVIEW: the style pass touched content.")
        return 1
    print("\nInvariants preserved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
