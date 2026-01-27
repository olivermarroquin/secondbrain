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
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        die(f"Missing required file: {p}")


def load_json(p: Path) -> dict:
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")


def parse_proposals(md: str) -> dict[int, dict]:
    """
    Parse proposed-changes.md into dict keyed by proposal number.
    Supports:
      - SECTION, CHANGE
      - SUBSECTION, SUBSECTION_OCCURRENCE
      - TO: (multi-line bullet block; ends on blank line)
      - TO: <single-line>
      - FROM: <single-line>
    """
    proposals: dict[int, dict] = {}
    lines = md.splitlines()

    cur_num: int | None = None
    cur: dict = {}
    in_to_block = False
    to_block: list[str] = []

    def flush() -> None:
        nonlocal cur_num, cur, in_to_block, to_block
        if cur_num is None:
            return
        if in_to_block:
            cur["to_paragraphs"] = [x.strip("- ").strip() for x in to_block if x.strip()]
        proposals[cur_num] = cur
        cur_num = None
        cur = {}
        in_to_block = False
        to_block = []

    for raw in lines:
        line = raw.rstrip("\n")

        m = re.match(r"^(\d+)\)\s*$", line)
        if m:
            flush()
            cur_num = int(m.group(1))
            cur = {"num": cur_num}
            continue

        if cur_num is None:
            continue

        if line.startswith("SECTION: "):
            cur["section"] = line.split("SECTION: ", 1)[1].strip()
            continue

        if line.startswith("CHANGE: "):
            cur["change"] = line.split("CHANGE: ", 1)[1].strip()
            continue

        if line.startswith("SUBSECTION: "):
            cur["subsection"] = line.split("SUBSECTION: ", 1)[1].strip()
            continue

        if line.startswith("SUBSECTION_OCCURRENCE: "):
            v = line.split("SUBSECTION_OCCURRENCE: ", 1)[1].strip()
            try:
                cur["subsection_occurrence"] = int(v)
            except ValueError:
                die(f"Invalid SUBSECTION_OCCURRENCE (not int): {v}")
            continue

        if line == "TO:":
            in_to_block = True
            to_block = []
            continue

        if in_to_block:
            if line.strip() == "":
                cur["to_paragraphs"] = [x.strip("- ").strip() for x in to_block if x.strip()]
                in_to_block = False
            else:
                to_block.append(line)
            continue

        if line.startswith("TO: "):
            cur["to_text"] = line.split("TO: ", 1)[1].strip()
            continue

        if line.startswith("FROM: "):
            cur["from_text"] = line.split("FROM: ", 1)[1].strip()
            continue

    flush()
    return proposals


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_materialize_stub")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--force", action="store_true", help="Overwrite patches.json if it exists")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    app = resolved.app_path
    pipe = app / "resume_refs" / "resume_pipeline"
    prop_md = pipe / "proposed-changes.md"
    appr_json = pipe / "approvals.json"
    patches_path = pipe / "patches.json"

    for req in (prop_md, appr_json):
        if not req.exists():
            die(f"Missing required pipeline artifact: {req}")

    if patches_path.exists() and not args.force:
        die(f"Refusing to overwrite existing patches.json (use --force): {patches_path}")

    approvals = load_json(appr_json)
    approved_nums = approvals.get("approved_change_numbers")
    if not isinstance(approved_nums, list) or not all(isinstance(x, int) for x in approved_nums):
        die(f"Invalid approvals.json approved_change_numbers list: {appr_json}")

    proposals_all = parse_proposals(read_text(prop_md))
    missing = [n for n in approved_nums if n not in proposals_all]
    if missing:
        die(f"Approved proposal numbers not found in proposed-changes.md: {missing}")

    patch_items: list[dict] = []
    for n in approved_nums:
        p = proposals_all[n]
        op = (p.get("change") or "").strip().upper()
        section = (p.get("section") or "").strip()

        if op not in ("ADD", "REPLACE_SECTION", "DELETE"):
            die(f"Unsupported CHANGE in proposal {n}: {op}")
        if not section:
            die(f"Proposal {n} missing SECTION")

        item: dict = {"num": n, "op": op, "section": section}

        if p.get("subsection"):
            item["subsection"] = p["subsection"]
        if p.get("subsection_occurrence") is not None:
            item["subsection_occurrence"] = int(p["subsection_occurrence"])

        # STUB content — but structurally correct for compiler + validator
        if op == "ADD":
            item["to_text"] = f"[STUB] Approved change #{n} for {section}."
        elif op == "REPLACE_SECTION":
            item["to_paragraphs"] = [
                f"[STUB] Approved change #{n} for {section}.",
                "This content was generated by rf_materialize_stub.",
                "Replace this with AI-generated content later.",
            ]
        elif op == "DELETE":
            # For DELETE, you MUST have a concrete from_text; stub cannot guess safely.
            ft = (p.get("from_text") or "").strip()
            if not ft:
                die(f"DELETE proposal {n} missing FROM (cannot stub DELETE safely)")
            item["from_text"] = ft

        patch_items.append(item)

    out = {
        "schema": "rf_patches_v1",
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "app": {
            "app_path": str(app),
            "family": resolved.family,
            "company": resolved.company,
            "role_slug": resolved.role_slug,
        },
        "approved_change_numbers": approved_nums,
        "patches": patch_items,
    }

    patches_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(str(patches_path))


if __name__ == "__main__":
    main()
