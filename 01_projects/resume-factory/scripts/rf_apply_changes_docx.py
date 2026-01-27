from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime, timezone

try:
    from docx import Document  # type: ignore
except Exception as e:
    print("ERROR: python-docx not available. Use docgen venv python.", file=sys.stderr)
    print("  ~/secondbrain/07_system/venvs/docgen/bin/python <script> ...", file=sys.stderr)
    print(f"Import error: {e}", file=sys.stderr)
    sys.exit(2)

LIB = Path("~/secondbrain/01_projects/resume-factory/lib").expanduser()
sys.path.insert(0, str(LIB))
from rf_paths import resolve_app, RFPathError  # type: ignore

def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def _patches_to_internal_proposals(patches):
    '''
    Convert rf_patches_v1 patches.json into internal proposal dicts used by build-docx.
    Produces proposal dicts with keys: num, section, change, to, from, subsection, subsection_occurrence.
    REPLACE_SECTION joins to_paragraphs with newlines into 'to'.
    '''
    items = patches.get("patches")
    if not isinstance(items, list):
        die("patches.json invalid: patches must be a list")

    out = []
    for it in items:
        if not isinstance(it, dict):
            die("patches.json invalid: patch item must be an object")

        num = it.get("num")
        op  = it.get("op")
        sec = it.get("section")

        if not isinstance(num, int):
            die(f"patches.json invalid: patch.num must be int (got {num})")
        if op not in ("ADD", "REPLACE_SECTION", "DELETE"):
            die(f"patches.json invalid: patch.op invalid: {op}")
        if not isinstance(sec, str) or not sec.strip():
            die(f"patches.json invalid: patch.section missing for num {num}")

        pr = {"num": num, "section": sec, "change": op}

        if "subsection" in it:
            pr["subsection"] = it["subsection"]
        if "subsection_occurrence" in it:
            pr["subsection_occurrence"] = it["subsection_occurrence"]

        if op == "ADD":
            to_text = it.get("to_text")
            if not isinstance(to_text, str) or not to_text.strip():
                die(f"patches.json invalid: ADD missing to_text for num {num}")
            pr["to"] = to_text.strip()

        elif op == "REPLACE_SECTION":
            paras = it.get("to_paragraphs")
            to_text = it.get("to_text")
            if isinstance(paras, list) and len(paras) > 0:
                pr["to"] = "\n".join([str(x).strip() for x in paras if str(x).strip()])
            elif isinstance(to_text, str) and to_text.strip():
                pr["to"] = to_text.strip()
            else:
                die(f"patches.json invalid: REPLACE_SECTION missing to_paragraphs/to_text for num {num}")

        elif op == "DELETE":
            from_text = it.get("from_text")
            if not isinstance(from_text, str) or not from_text.strip():
                die(f"patches.json invalid: DELETE missing from_text for num {num}")
            pr["from"] = from_text.strip()

        out.append(pr)

    return out



def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"Missing required file: {path}")
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {path} ({e})")

def _require_patches_if_approved(app: Path) -> tuple[list[int] | None, dict | None]:
    """
    If approvals.json exists, patches.json must exist.
    Returns (approved_numbers, patches_json) or (None, None) if no approvals.json.
    """
    pipe = app / "resume_refs" / "resume_pipeline"
    approvals_path = pipe / "approvals.json"
    patches_path = pipe / "patches.json"

    if not approvals_path.exists():
        return None, None

    approvals = _load_json(approvals_path)
    approved = approvals.get("approved_change_numbers", [])
    if not isinstance(approved, list) or not all(isinstance(x, int) for x in approved):
        die(f"Invalid approvals.json approved_change_numbers: {approvals_path}")

    if not patches_path.exists():
        die(f"Missing patches.json for approved build: {patches_path}\nRun: resume materialize-approved-ai --app \"{app}\"")

    patches = _load_json(patches_path)
    if patches.get("schema") != "rf_patches_v1":
        die(f"Unsupported patches schema (expected rf_patches_v1): {patches_path}")

    pnums = patches.get("approved_change_numbers", [])
    if pnums != approved:
        die(f"patches.json approved_change_numbers does not match approvals.json\npatches: {pnums}\napprovals: {approved}")

    # hard ban placeholders
    def _contains_placeholder(obj) -> bool:
        if isinstance(obj, str):
            return "[PROPOSED:" in obj or "[PLACEHOLDER:" in obj
        if isinstance(obj, list):
            return any(_contains_placeholder(x) for x in obj)
        if isinstance(obj, dict):
            return any(_contains_placeholder(v) for v in obj.values())
        return False

    if _contains_placeholder(patches):
        die(f"patches.json contains placeholder text ([PROPOSED:...] or [PLACEHOLDER:...]): {patches_path}")

    return approved, patches

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def read_json(p: Path):
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")


def norm(s: str) -> str:
    return " ".join(s.strip().split()).lower()


def parse_proposals(md: str) -> dict[int, dict]:
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
            elif line.startswith("SUBSECTION: "):
                current["subsection"] = line.replace("SUBSECTION: ", "", 1).strip()
            elif line.startswith("SUBSECTION_OCCURRENCE: "):
                raw = line.replace("SUBSECTION_OCCURRENCE: ", "", 1).strip()
                try:
                    current["subsection_occurrence"] = int(raw)
                except ValueError:
                    die(f"Invalid SUBSECTION_OCCURRENCE (must be int): {raw}")
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
    cand_norm = [norm(c) for c in candidates if c and c.strip()]
    for idx, para in enumerate(doc.paragraphs):
        t = norm(para.text)
        if t and t in cand_norm:
            return idx
    return -1


def paragraph_is_major_heading(para_text: str, major_headings: list[str]) -> bool:
    t = norm(para_text)
    return t in {norm(h) for h in major_headings if h and h.strip()}


def delete_paragraph(doc: Document, para) -> None:
    p = para._p  # type: ignore
    p.getparent().remove(p)  # type: ignore


def list_heading_candidates(doc: Document) -> list[str]:
    out = []
    for para in doc.paragraphs:
        t = " ".join(para.text.split()).strip()
        if t and len(t) <= 60:
            out.append(t)
    return out


def resolve_family_maps(family: str, rootp: Path) -> tuple[dict, list[str], dict]:
    aliases_doc = load_section_aliases(rootp)
    fam_map = (aliases_doc.get("families", {}) or {}).get(family, {}) or {}
    major = fam_map.get("__MAJOR_HEADINGS__", []) or []
    subs = fam_map.get("__SUBSECTIONS__", {}) or {}
    return fam_map, major, subs


def section_bounds(doc: Document, section_candidates: list[str], major_headings: list[str]) -> tuple[int, int]:
    start = find_heading_paragraph_index(doc, section_candidates)
    if start < 0:
        return (-1, -1)

    end = len(doc.paragraphs)
    i = start + 1
    while i < len(doc.paragraphs):
        if paragraph_is_major_heading(doc.paragraphs[i].text, major_headings):
            end = i
            break
        i += 1
    return (start, end)


def find_nth_subsection_anchor(doc: Document, start: int, end: int, subsection_candidates: list[str], occurrence: int):
    cand = {norm(x) for x in subsection_candidates if x and x.strip()}
    hits = []
    for i in range(start, end):
        if norm(doc.paragraphs[i].text) in cand:
            hits.append(i)

    if not hits:
        return None, []
    if occurrence < 1 or occurrence > len(hits):
        return None, hits

    return doc.paragraphs[hits[occurrence - 1]], hits


def apply_add_section_fallback(doc: Document, section: str, to_text: str, family: str, rootp: Path, last_anchor_map: dict):
    fam_map, major, _subs = resolve_family_maps(family, rootp)
    section_candidates = fam_map.get(section, [section])
    sec_start, _sec_end = section_bounds(doc, section_candidates, major)
    if sec_start < 0:
        heads = list_heading_candidates(doc)
        die(
            "ADD failed: section heading not found (fallback).\\n"
            f"  SECTION: {section}\\n"
            f"  CANDIDATES: {section_candidates}\\n"
            "  DOCX headings seen (sample):\\n    - "
            + "\\n    - ".join(heads[:30])
        )

    anchor_key = ("SECTION_ONLY", section)
    if anchor_key in last_anchor_map:
        anchor_para = last_anchor_map[anchor_key]
        new_para = doc.add_paragraph(to_text)
        anchor_para._p.addnext(new_para._p)  # type: ignore
        last_anchor_map[anchor_key] = new_para
        return

    heading_para = doc.paragraphs[sec_start]
    new_para = doc.add_paragraph(to_text)
    heading_para._p.addnext(new_para._p)  # type: ignore
    last_anchor_map[anchor_key] = new_para


def apply_add_subsection(doc: Document, section: str, subsection_key: str, occurrence: int, to_text: str,
                         family: str, rootp: Path, last_anchor_map: dict):
    fam_map, major, subs = resolve_family_maps(family, rootp)

    section_candidates = fam_map.get(section, [section])
    sec_start, sec_end = section_bounds(doc, section_candidates, major)
    if sec_start < 0:
        die(f"ADD failed: section not found for subsection insert: {section} candidates={section_candidates}")

    subsection_candidates = subs.get(subsection_key)
    if not subsection_candidates:
        die(f"ADD failed: unknown SUBSECTION key '{subsection_key}' (not in __SUBSECTIONS__)")

    anchor_key = (section, subsection_key, occurrence)

    if anchor_key in last_anchor_map:
        anchor_para = last_anchor_map[anchor_key]
        new_para = doc.add_paragraph(to_text)
        anchor_para._p.addnext(new_para._p)  # type: ignore
        last_anchor_map[anchor_key] = new_para
        return

    sub_anchor, hits = find_nth_subsection_anchor(doc, sec_start, sec_end, subsection_candidates, occurrence)
    if sub_anchor is None:
        die(
            "ADD failed: subsection anchor not found or occurrence out of range.\\n"
            f"  SECTION: {section}\\n"
            f"  SUBSECTION: {subsection_key}\\n"
            f"  OCCURRENCE: {occurrence}\\n"
            f"  MATCHED_OCCURRENCES: {len(hits)}"
        )

    new_para = doc.add_paragraph(to_text)
    sub_anchor._p.addnext(new_para._p)  # type: ignore
    last_anchor_map[anchor_key] = new_para


def apply_replace_section(doc: Document, canonical_section: str, to_text: str, family: str, rootp: Path) -> None:
    fam_map, major, _subs = resolve_family_maps(family, rootp)
    candidates = fam_map.get(canonical_section, [canonical_section])
    if not major:
        die(f"REPLACE_SECTION failed: __MAJOR_HEADINGS__ missing for family '{family}'")

    start_idx, end_idx = section_bounds(doc, candidates, major)
    if start_idx < 0:
        heads = list_heading_candidates(doc)
        die(
            "REPLACE_SECTION failed: section heading not found.\\n"
            f"  SECTION: {canonical_section}\\n"
            f"  CANDIDATES: {candidates}\\n"
            "  DOCX headings seen (sample):\\n    - " + "\\n    - ".join(heads[:30])
        )

    i = start_idx + 1
    while i < end_idx and i < len(doc.paragraphs):
        delete_paragraph(doc, doc.paragraphs[i])
        end_idx -= 1

    heading_para = doc.paragraphs[start_idx]
    new_para = doc.add_paragraph(to_text)
    heading_para._p.addnext(new_para._p)  # type: ignore


def apply_replace_exact(doc: Document, from_text: str, to_text: str) -> None:
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
    delete_paragraph(doc, matches[0])


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
    approved, patches = _require_patches_if_approved(app)

    if approved is not None:
        # Approved build MUST use patches.json (AI-materialized), not proposed-changes.md.
        plist = _patches_to_internal_proposals(patches)
        proposals = {int(x["num"]): x for x in plist}
    else:
        # No approvals.json => legacy/stub path uses proposed-changes.md
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
    last_anchor_map = {}

    for n in approved_nums:
        p = proposals[n]
        ch = (p.get("change") or "").upper()
        section = (p.get("section") or "").strip()
        from_text = (p.get("from") or "").strip()
        to_text = (p.get("to") or "").strip()
        subsection = (p.get("subsection") or "").strip() if p.get("subsection") else ""
        occ = p.get("subsection_occurrence")

        if ch == "ADD":
            if not section or not to_text:
                die(f"ADD proposal {n} missing SECTION or TO")

            if subsection:
                if occ is None:
                    die(f"ADD proposal {n} has SUBSECTION but missing SUBSECTION_OCCURRENCE")
                apply_add_subsection(doc, section, subsection, int(occ), to_text, resolved.family, rootp, last_anchor_map)
            else:
                apply_add_section_fallback(doc, section, to_text, resolved.family, rootp, last_anchor_map)

        elif ch == "REPLACE_SECTION":
            if not section or not to_text:
                die(f"REPLACE_SECTION proposal {n} missing SECTION or TO")
            apply_replace_section(doc, section, to_text, resolved.family, rootp)

        elif ch == "REPLACE":
            if not from_text or not to_text:
                die(f"REPLACE proposal {n} missing FROM or TO")
            apply_replace_exact(doc, from_text, to_text)

        elif ch == "DELETE":
            if not from_text:
                die(f"DELETE proposal {n} missing FROM")
            apply_delete(doc, from_text)

        else:
            die(f"Unknown CHANGE type in proposal {n}: {ch}")

        applied.append({
            "num": n,
            "section": section,
            "subsection": subsection if subsection else None,
            "subsection_occurrence": occ if subsection else None,
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
        "outputs": {"resume_docx": str(out_docx)},
    }
    meta_path = out_meta_dir / "resume-meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(str(out_docx))
    print(str(meta_path))


if __name__ == "__main__":
    main()
