#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

LIB = Path("~/secondbrain/01_projects/resume-factory/lib").expanduser()
sys.path.insert(0, str(LIB))
from rf_paths import resolve_app, RFPathError  # type: ignore

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def parse_change_numbers(md: str) -> list[int]:
    nums = []
    for m in re.finditer(r"(?m)^(\d+)\)\s*$", md):
        nums.append(int(m.group(1)))
    return nums

def parse_approve_arg(s: str) -> list[int]:
    s = s.strip().lower()
    if s == "all":
        return [-1]  # sentinel handled later
    if s == "0" or s == "":
        return []
    parts = [p.strip() for p in s.split(",") if p.strip()]
    out = []
    for p in parts:
        if not p.isdigit():
            die(f"Invalid approve token: '{p}' (expected comma-separated ints, or 'all', or '0')")
        out.append(int(p))
    # unique + sorted
    return sorted(set(out))

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_record_approvals")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--approve", required=True, help="Comma list (e.g. 1,3) or 'all' or '0'")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--force", action="store_true", help="Overwrite approvals.json if it exists")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    app = resolved.app_path
    pipe_dir = app / "resume_refs" / "resume_pipeline"
    proposed_path = pipe_dir / "proposed-changes.md"
    if not proposed_path.exists():
        die(f"Missing proposals: {proposed_path}\nRun: resume propose-changes --app \"$APP\"")

    md = read_text(proposed_path)
    existing_nums = parse_change_numbers(md)
    if not existing_nums:
        die("No numbered changes found in proposed-changes.md")

    approve_list = parse_approve_arg(args.approve)

    if approve_list == [-1]:  # all
        approved = sorted(existing_nums)
    else:
        # validate all requested approvals exist
        missing = [n for n in approve_list if n not in existing_nums]
        if missing:
            die(f"Requested approvals not found in proposals: {missing}\nExisting: {existing_nums}")
        approved = approve_list

    out_path = pipe_dir / "approvals.json"
    if out_path.exists() and not args.force:
        die(f"Refusing to overwrite existing: {out_path}\nUse --force if you intend to change approvals.")

    payload = {
        "schema": "rf_approvals_v1",
        "approved_at_utc": datetime.now(timezone.utc).isoformat(),
        "app": {
            "app_path": str(resolved.app_path),
            "family": resolved.family,
            "company": resolved.company,
            "role_slug": resolved.role_slug,
        },
        "proposals_path": str(proposed_path),
        "existing_change_numbers": existing_nums,
        "approved_change_numbers": approved,
        "approved_count": len(approved),
    }

    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(str(out_path))

if __name__ == "__main__":
    main()
