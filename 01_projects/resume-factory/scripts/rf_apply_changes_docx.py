#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

# python-docx dependency (must exist in docgen venv)
try:
    from docx import Document  # type: ignore
except Exception as e:
    print("ERROR: python-docx not available. Run this using the docgen venv python:", file=sys.stderr)
    print("  ~/secondbrain/07_system/venvs/docgen/bin/python <script> ...", file=sys.stderr)
    print(f"Import error: {e}", file=sys.stderr)
    sys.exit(2)

LIB = Path("~/secondbrain/01_projects/resume-factory/lib").expanduser()
sys.path.insert(0, str(LIB))
from rf_paths import resolve_app, RFPathError  # type: ignore

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def read_json(p: Path):
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")

def parse_proposals(md: str) -> dict[int, dict]:
    """
    Parse proposed-changes.md into {num: {section, change, from?, to?}}.
    Locked format from Stage 4.
    """
    blocks: dict[int, dict] = {}
    current_n = None
    current: dict = {}

    for line in md.splitlines():
        m = re.match(r"^(\d+)\)\s*$", line)
        if m:
            if current_n is not None:
                blocks[current_n] = current
            current_n = int(m.group(1))
            current = {"num": current_n}
            continue

        if current_n is not None:
            if line.startswith("SECTION: "):
                current["section"] = line.replace("SECTION: ", "", 1).strip()
            elif line.startswith("CHANGE: "):
                current["change"] = line.replace("CHANGE: ", "", 1).strip().upper()
            elif line.startswith("FROM: "):
                current["from"] = line.replace("FROM: ", "", 1).strip()
            elif line.startswith("TO: "):
                current["to"] = line.replace("TO: ", "", 1).strip()

    if current_n is not None:
        blocks[current_n] = current

    return blocks

def load_section_aliases(rootp: Path) -> dict:
    p = rootp / "01_projects" / "resume-factory" / "schemas" / "section-aliases.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8", errors="replace"))

def find_heading_paragraph_index(doc: Document, candidates: list[str]) -> int:
    cand_norm = [c.strip().lower() for c in candidates if c and c.strip()]
    for idx, para in enumerate(doc.paragraphs):
        t = para.text.strip().lower()
        if not t:
            continue
        if t in cand_norm:
            return idx
    return -1

def list_heading_candidates(doc: Document) -> list[str]:
    out = []
    for para in doc.paragraphs:
        t = " ".join(para.text.split()).strip()
        if t and len(t) <= 60:
            out.append(t)
    return out

def apply_add(doc: Document, section: str, to_text: str, family: str, rootp: Path, anchor_para=None) -> object:
    aliases_doc = load_section_aliases(rootp)
    fam_map = (aliases_doc.get("families", {}) or {}).get(family, {}) or {}

    candidates = fam_map.get(section, [section])

    # resolve anchor: heading paragraph (first time) or last inserted paragraph (subsequent adds)
    if anchor_para is None:
        idx = find_heading_paragraph_index(doc, candidates)
        if idx < 0:
            heads = list_heading_candidates(doc)
            die(
                "ADD failed: section heading not found.\n"
                f"  SECTION: {section}\n"
                f"  CANDIDATES: {candidates}\n"
                "  DOCX headings seen (sample):\n    - " + "\n    - ".join(heads[:30])
            )
        anchor_para = doc.paragraphs[idx]

    new_para = doc.add_paragraph(to_text)
    anchor_para._p.addnext(new_para._p)  # type: ignore
    return new_para

    # canonical section -> candidate headings in DOCX
    candidates = fam_map.get(section, [section])

    idx = find_heading_paragraph_index(doc, candidates)
    if idx < 0:
        heads = list_heading_candidates(doc)
        die(
            "ADD failed: section heading not found.\n"
            f"  SECTION: {section}\n"
            f"  CANDIDATES: {candidates}\n"
            "  DOCX headings seen (sample):\n    - " + "\n    - ".join(heads[:30])
        )

    # Insert paragraph right after the matched heading
    p = doc.paragraphs[idx]
    new_para = doc.add_paragraph(to_text)
    p._p.addnext(new_para._p)  # type: ignore

def apply_replace(doc: Document, from_text: str, to_text: str) -> None:
    """
    Replace exact paragraph text match (stripped) with to_text.
    Hard fail if not found exactly once.
    """
    target = from_text.strip()
    matches = [p for p in doc.paragraphs if p.text.strip() == target]
    if len(matches) == 0:
        die(f"REPLACE failed: FROM text not found exactly: {from_text}")
    if len(matches) > 1:
        die(f"REPLACE failed: FROM text matched multiple paragraphs ({len(matches)}). Must be unique.")
    matches[0].text = to_text

def apply_delete(doc: Document, from_text: str) -> None:
    target = from_text.strip()
    matches = [p for p in doc.paragraphs if p.text.strip() == target]
    if len(matches) == 0:
        die(f"DELETE failed: FROM text not found exactly: {from_text}")
    if len(matches) > 1:
        die(f"DELETE failed: FROM text matched multiple paragraphs ({len(matches)}). Must be unique.")
    p = matches[0]._p  # type: ignore
    p.getparent().remove(p)  # type: ignore

def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_apply_changes_docx")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--force", action="store_true", help="Overwrite output resume.docx if it exists")
    args = ap.parse_args()

    try:
        resolved = resolve_app(args.app, root=args.root)
    except RFPathError as e:
        die(str(e))

    rootp = Path(args.root).expanduser().resolve()

    app = resolved.app_path
    pipe_dir = app / "resume_refs" / "resume_pipeline"
    sel_json = pipe_dir / "selection.json"
    prop_md = pipe_dir / "proposed-changes.md"
    appr_json = pipe_dir / "approvals.json"

    for req in (sel_json, prop_md, appr_json):
        if not req.exists():
            die(f"Missing required pipeline artifact: {req}")

    sel = read_json(sel_json)
    approvals = read_json(appr_json)

    approved_nums = approvals.get("approved_change_numbers", [])
    if approved_nums is None or not isinstance(approved_nums, list):
        die("approvals.json missing approved_change_numbers list")

    template_dir = Path(sel["selected"]["template_dir"])
    master_docx = template_dir / "resume-master.docx"
    if not master_docx.exists():
        die(f"Missing resume-master.docx: {master_docx}")

    proposals = parse_proposals(read_text(prop_md))

    missing = [n for n in approved_nums if n not in proposals]
    if missing:
        die(f"Approvals reference missing proposal numbers: {missing}")

    out_resume_dir = resolved.outputs_root / "resume"
    out_meta_dir = resolved.outputs_root / "meta"
    out_resume_dir.mkdir(parents=True, exist_ok=True)
    out_meta_dir.mkdir(parents=True, exist_ok=True)

    out_docx = out_resume_dir / "resume.docx"
    if out_docx.exists() and not args.force:
        die(f"Refusing to overwrite existing output: {out_docx} (use --force)")

    shutil.copy2(master_docx, out_docx)

    doc = Document(str(out_docx))

    applied = []
    last_added_anchor = {}

    for n in approved_nums:
        p = proposals[n]
        ch = (p.get("change") or "").upper()
        section = (p.get("section") or "").strip()
        from_text = (p.get("from") or "").strip()
        to_text = (p.get("to") or "").strip()

        if ch == "ADD":
            if not section or not to_text:
                die(f"ADD proposal {n} missing SECTION or TO")
            anchor = last_added_anchor.get(section)
            newp = apply_add(doc, section, to_text, resolved.family, rootp, anchor_para=anchor)
            last_added_anchor[section] = newp
        elif ch == "REPLACE":
            if not from_text or not to_text:
                die(f"REPLACE proposal {n} missing FROM or TO")
            apply_replace(doc, from_text, to_text)
        elif ch == "DELETE":
            if not from_text:
                die(f"DELETE proposal {n} missing FROM")
            apply_delete(doc, from_text)
        else:
            die(f"Unknown CHANGE type in proposal {n}: {ch}")

        applied.append({
            "num": n,
            "section": section,
            "change": ch,
            "from": from_text if from_text else None,
            "to": to_text if to_text else None,
        })

    doc.save(str(out_docx))

    meta = {
        "schema": "rf_build_meta_v1",
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "app": {
            "app_path": str(resolved.app_path),
            "family": resolved.family,
            "company": resolved.company,
            "role_slug": resolved.role_slug,
        },
        "selected_template": sel["selected"],
        "approved_change_numbers": approved_nums,
        "applied_changes": applied,
        "outputs": {
            "resume_docx": str(out_docx),
        }
    }
    meta_path = out_meta_dir / "resume-meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(str(out_docx))
    print(str(meta_path))

if __name__ == "__main__":
    main()
