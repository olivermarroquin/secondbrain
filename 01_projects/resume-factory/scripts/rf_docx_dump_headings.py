#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from docx import Document  # type: ignore
except Exception as e:
    print("ERROR: python-docx not available. Use docgen venv python.", file=sys.stderr)
    print("  ~/secondbrain/07_system/venvs/docgen/bin/python <script> ...", file=sys.stderr)
    print(f"Import error: {e}", file=sys.stderr)
    sys.exit(2)

def norm(s: str) -> str:
    return " ".join(s.strip().split()).lower()

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True)
    args = ap.parse_args()

    p = Path(args.docx).expanduser().resolve()
    if not p.exists():
        print(f"ERROR: missing docx: {p}", file=sys.stderr)
        sys.exit(2)

    doc = Document(str(p))

    # Print all non-empty paragraphs with index
    for i, para in enumerate(doc.paragraphs):
        t = " ".join(para.text.split()).strip()
        if not t:
            continue
        # crude heuristic: headings are short-ish and mostly uppercase/titlecase
        if len(t) <= 60:
            print(f"{i:04d} | {t}")

if __name__ == "__main__":
    main()
