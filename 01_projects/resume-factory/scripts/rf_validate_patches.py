#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def read_json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"Missing required file: {p}")
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_validate_patches")
    ap.add_argument("--patches", required=True, help="patches.json path")
    ap.add_argument("--approvals", required=True, help="approvals.json path")
    args = ap.parse_args()

    patches_p = Path(args.patches)
    approvals_p = Path(args.approvals)

    patches = read_json(patches_p)
    approvals = read_json(approvals_p)

    if patches.get("schema") != "rf_patches_v1":
        die(f"Invalid patches schema: {patches.get('schema')}")

    approved_nums = approvals.get("approved_change_numbers")
    if not isinstance(approved_nums, list):
        die("approvals.json missing approved_change_numbers list")

    patch_items = patches.get("patches")
    if not isinstance(patch_items, list):
        die("patches.json missing patches list")

    patch_nums = [p.get("num") for p in patch_items]
    if sorted(patch_nums) != sorted(approved_nums):
        die(
            f"Mismatch between approved_change_numbers and patches nums: "
            f"approved={approved_nums}, patches={patch_nums}"
        )

    print("OK")


if __name__ == "__main__":
    main()
