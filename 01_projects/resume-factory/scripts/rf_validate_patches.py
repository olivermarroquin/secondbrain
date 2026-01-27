#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def load_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Invalid JSON: {p} ({e})")

def contains_placeholder(obj) -> bool:
    if isinstance(obj, str):
        return ("[PROPOSED:" in obj) or ("[PLACEHOLDER:" in obj)
    if isinstance(obj, list):
        return any(contains_placeholder(x) for x in obj)
    if isinstance(obj, dict):
        return any(contains_placeholder(v) for v in obj.values())
    return False

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_validate_patches")
    ap.add_argument("--patches", required=True, help="Path to patches.json")
    ap.add_argument("--approvals", required=False, help="Optional approvals.json to cross-check")
    args = ap.parse_args()

    patches_p = Path(args.patches).expanduser().resolve()
    d = load_json(patches_p)

    if d.get("schema") != "rf_patches_v1":
        die(f"Unsupported schema (expected rf_patches_v1): {patches_p}")

    approved = d.get("approved_change_numbers")
    patches = d.get("patches")

    if not isinstance(approved, list) or not all(isinstance(x, int) for x in approved):
        die("approved_change_numbers must be a list[int]")
    if not isinstance(patches, list):
        die("patches must be a list")

    nums = []
    for i, p in enumerate(patches):
        if not isinstance(p, dict):
            die(f"patches[{i}] must be an object")
        n = p.get("num")
        op = p.get("op")
        if not isinstance(n, int):
            die(f"patches[{i}].num must be int")
        if op not in ("ADD", "REPLACE_SECTION", "DELETE"):
            die(f"patches[{i}].op invalid: {op}")
        nums.append(n)

        if op == "ADD":
            if not (isinstance(p.get("to_text"), str) and p["to_text"].strip()):
                die(f"patches[{i}] ADD requires non-empty to_text")
        if op == "REPLACE_SECTION":
            tp = p.get("to_paragraphs")
            tt = p.get("to_text")
            ok = (isinstance(tp, list) and all(isinstance(x, str) and x.strip() for x in tp)) or (isinstance(tt, str) and tt.strip())
            if not ok:
                die(f"patches[{i}] REPLACE_SECTION requires to_paragraphs[] or to_text")
        if op == "DELETE":
            if not (isinstance(p.get("from_text"), str) and p["from_text"].strip()):
                die(f"patches[{i}] DELETE requires non-empty from_text")

    if sorted(nums) != sorted(approved):
        die(f"patches[].num must match approved_change_numbers.\napproved={approved}\npatch_nums={nums}")

    if contains_placeholder(d):
        die("patches.json contains placeholders ([PROPOSED:...] or [PLACEHOLDER:...])")

    # Optional cross-check approvals.json
    if args.approvals:
        a = load_json(Path(args.approvals).expanduser().resolve())
        a_nums = a.get("approved_change_numbers", [])
        if a_nums != approved:
            die(f"approved_change_numbers mismatch vs approvals.json\npatches={approved}\napprovals={a_nums}")

    print("OK")

if __name__ == "__main__":
    main()
