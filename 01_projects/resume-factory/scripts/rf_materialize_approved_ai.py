#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_materialize_approved_ai")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    app = Path(args.app).expanduser().resolve()
    pipe = app / "resume_refs" / "resume_pipeline"
    approvals = pipe / "approvals.json"
    proposed = pipe / "proposed-changes.md"

    if not approvals.exists():
        die(f"Missing approvals.json: {approvals}")
    if not proposed.exists():
        die(f"Missing proposed-changes.md: {proposed}")

    die(
        "materialize-approved-ai not implemented yet.\n"
        "Contract: 01_projects/resume-factory/schemas/AI_MATERIALIZER_CONTRACT_v1.md\n"
        "Expected output: APP/resume_refs/resume_pipeline/patches.json (schema rf_patches_v1)"
    )

if __name__ == "__main__":
    main()
