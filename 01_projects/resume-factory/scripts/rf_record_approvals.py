#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"Missing required file: {p}")
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_record_approvals")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--approve", required=True, help='Comma-separated proposal numbers, e.g. "1,3"')
    ap.add_argument("--root", default="~/secondbrain")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    app = Path(args.app).expanduser().resolve()
    pipe = app / "resume_refs" / "resume_pipeline"
    pipe.mkdir(parents=True, exist_ok=True)

    proposed_md = pipe / "proposed-changes.md"
    if not proposed_md.exists():
        die(f"Missing proposed-changes.md: {proposed_md}")

    out = pipe / "approvals.json"
    if out.exists() and not args.force:
        die(f"Refusing to overwrite approvals.json (use --force): {out}")

    try:
        approved_nums = [int(x.strip()) for x in args.approve.split(",") if x.strip()]
    except ValueError:
        die("Invalid --approve list (must be integers)")

    approvals = {
        "schema": "rf_approvals_v1",
        "approved_at_utc": now_utc(),
        "app": {
            "app_path": str(app),
        },
        "approved_change_numbers": approved_nums,
        "approved_count": len(approved_nums),
    }

    out.write_text(json.dumps(approvals, indent=2) + "\n", encoding="utf-8")
    print(str(out))


if __name__ == "__main__":
    main()
