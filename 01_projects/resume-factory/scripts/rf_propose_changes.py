#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_propose_changes (STUB)")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    app = Path(args.app).expanduser().resolve()
    pipe = app / "resume_refs" / "resume_pipeline"
    pipe.mkdir(parents=True, exist_ok=True)

    out_md = pipe / "proposed-changes.md"
    if out_md.exists() and not args.force:
        die(f"Refusing to overwrite existing file (use --force): {out_md}")

    stub = (
        "# Proposed Resume Changes (STUB)\n\n"
        "[STUB MODE]\n"
        "This file exists only to validate pipeline wiring.\n"
        "Use `resume propose-changes-ai` for real proposals.\n"
    )

    out_md.write_text(stub, encoding="utf-8")
    print(str(out_md))


if __name__ == "__main__":
    main()
