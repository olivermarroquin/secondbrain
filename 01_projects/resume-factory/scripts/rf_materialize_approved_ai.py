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


def normalize_section(section: str, template_headings: list[str]) -> str:
    # Exact match to the template heading text (prefers the template's punctuation/case)
    s = (section or "").strip().upper()

    def _match(name: str) -> str | None:
        u = (name or "").strip().upper()
        for h in template_headings:
            if h.rstrip(":").strip().upper() == u:
                return h
        return None

    hit = _match(section)
    if hit:
        return hit

    # Section aliases: logical names -> how the template actually labels it
    aliases = {
        "SUMMARY": "PROFESSIONAL SUMMARY",
        "PROJECT EXPERIENCE": "PROFESSIONAL EXPERIENCE",
        "CORE COMPETENCIES": "TECHNICAL SKILL",
        "TECHNICAL SKILLS": "TECHNICAL SKILL",
    }

    alias = aliases.get(s)
    if alias:
        hit2 = _match(alias)
        if hit2:
            return hit2

    return section


def extract_template_headings(master_docx: Path) -> list[str]:
    try:
        from docx import Document  # type: ignore
    except Exception as e:
        die(
            "python-docx not available. Run via docgen venv python:\n"
            "  ~/secondbrain/07_system/venvs/docgen/bin/python <script> ...\n"
            f"Import error: {e}"
        )

    doc = Document(str(master_docx))
    headings: list[str] = []
    for p in doc.paragraphs:
        t = (p.text or "").strip()
        if t.endswith(":"):
            headings.append(t)
    return headings


def _parse_proposed_changes(md: str) -> dict[int, dict]:
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

    def flush():
        nonlocal cur_num, cur, in_to_block, to_block
        if cur_num is None:
            return
        # If TO: bullet mode still open, finalize it
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

        # multiline TO block
        if line == "TO:":
            in_to_block = True
            to_block = []
            continue

        if in_to_block:
            if line.strip() == "":
                # finalize TO block on blank line
                cur["to_paragraphs"] = [x.strip("- ").strip() for x in to_block if x.strip()]
                in_to_block = False
            else:
                to_block.append(line)
            continue

        # single-line fields
        if line.startswith("TO: "):
            cur["to_text"] = line.split("TO: ", 1)[1].strip()
            continue

        if line.startswith("FROM: "):
            cur["from_text"] = line.split("FROM: ", 1)[1].strip()
            continue

        # ignore blanks/other lines
        continue

    flush()
    return proposals


def _make_patch_item(p: dict, template_headings: list[str]) -> dict:
    ch = (p.get("change") or "").strip().upper()
    if ch not in ("ADD", "REPLACE_SECTION", "DELETE"):
        die(f"Unsupported CHANGE in proposal {p.get('num')}: {ch}")

    section = p.get("section")
    if not isinstance(section, str) or not section.strip():
        die(f"Proposal {p.get('num')} missing SECTION")

    # normalize to exact template heading (e.g. TECHNICAL SKILL -> TECHNICAL SKILL:)
    section_norm = normalize_section(section, template_headings)

    item: dict = {
        "num": int(p.get("num")),
        "op": ch,
        "section": section_norm,
    }

    if "subsection" in p:
        item["subsection"] = p["subsection"]
    if "subsection_occurrence" in p:
        item["subsection_occurrence"] = int(p["subsection_occurrence"])

    if ch == "ADD":
        to_text = p.get("to_text")
        if not isinstance(to_text, str) or not to_text.strip():
            die(f"ADD proposal {p.get('num')} missing TO")
        item["to_text"] = to_text.strip()

    elif ch == "REPLACE_SECTION":
        paras = p.get("to_paragraphs")
        to_text = p.get("to_text")

        if isinstance(paras, list) and len(paras) > 0:
            clean = [str(x).strip() for x in paras if str(x).strip()]
            if not clean:
                die(f"REPLACE_SECTION proposal {p.get('num')} has empty TO paragraphs")
            item["to_paragraphs"] = clean
        elif isinstance(to_text, str) and to_text.strip():
            item["to_text"] = to_text.strip()
        else:
            die(f"REPLACE_SECTION proposal {p.get('num')} missing TO content")

    elif ch == "DELETE":
        from_text = p.get("from_text")
        if not isinstance(from_text, str) or not from_text.strip():
            die(f"DELETE proposal {p.get('num')} missing FROM")
        item["from_text"] = from_text.strip()

    return item


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_materialize_approved_ai")
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
    sel_json = pipe / "selection.json"
    patches_path = pipe / "patches.json"

    for req in (prop_md, appr_json, sel_json):
        if not req.exists():
            die(f"Missing required pipeline artifact: {req}")

    if patches_path.exists() and not args.force:
        die(f"Refusing to overwrite existing patches.json (use --force): {patches_path}")

    approvals = load_json(appr_json)
    approved_nums = approvals.get("approved_change_numbers")
    if not isinstance(approved_nums, list) or not all(isinstance(x, int) for x in approved_nums):
        die(f"Invalid approvals.json approved_change_numbers list: {appr_json}")

    sel = load_json(sel_json)
    try:
        template_dir = Path(sel["selected"]["template_dir"])
    except Exception:
        die(f"selection.json missing selected.template_dir: {sel_json}")

    master_docx = template_dir / "resume-master.docx"
    if not master_docx.exists():
        die(f"Missing resume-master.docx: {master_docx}")

    template_headings = extract_template_headings(master_docx)

    proposals_all = _parse_proposed_changes(read_text(prop_md))
    missing = [n for n in approved_nums if n not in proposals_all]
    if missing:
        die(f"Approved proposal numbers not found in proposed-changes.md: {missing}")

    patch_items: list[dict] = []
    for n in approved_nums:
        p = proposals_all[n]
        patch_items.append(_make_patch_item(p, template_headings))

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
