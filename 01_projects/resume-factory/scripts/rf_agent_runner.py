#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime, timezone


def die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        die(f"Missing required file: {p}")


def write_text(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def load_json(p: Path) -> dict:
    try:
        return json.loads(read_text(p))
    except json.JSONDecodeError as e:
        die(f"Invalid JSON: {p} ({e})")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _contains_placeholders(s: str) -> bool:
    return ("[PROPOSED:" in s) or ("[PLACEHOLDER:" in s) or ("[STUB" in s)


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


def normalize_section(section: str, template_headings: list[str]) -> str:
    s = (section or "").strip().upper()
    for h in template_headings:
        if h.rstrip(":").strip().upper() == s:
            return h
    return section


@dataclass
class AgentContext:
    app_path: Path
    family: str
    company: str
    role_slug: str
    jd_text: str
    job_json: dict
    selection_json: dict
    emphasis_json: dict
    template_dir: Path
    template_headings: list[str]


def build_context(app: Path) -> AgentContext:
    pipe = app / "resume_refs" / "resume_pipeline"
    job_json_p = pipe / "job.json"
    sel_json_p = pipe / "selection.json"
    emph_json_p = pipe / "emphasis.json"
    jd_raw_p = app / "jd" / "jd-raw.txt"

    for req in (job_json_p, sel_json_p, emph_json_p, jd_raw_p):
        if not req.exists():
            die(f"Missing required input: {req}")

    jobj = load_json(job_json_p)
    sel = load_json(sel_json_p)
    emph = load_json(emph_json_p)
    jd = read_text(jd_raw_p)

    try:
        template_dir = Path(sel["selected"]["template_dir"])
    except Exception:
        die(f"selection.json missing selected.template_dir: {sel_json_p}")

    master_docx = template_dir / "resume-master.docx"
    if not master_docx.exists():
        die(f"Missing resume-master.docx: {master_docx}")

    headings = extract_template_headings(master_docx)

    # These fields exist in your resolve_app-derived artifacts; keep robust fallbacks.
    family = (jobj.get("app") or {}).get("family") or sel.get("app", {}).get("family") or ""
    company = (jobj.get("app") or {}).get("company") or sel.get("app", {}).get("company") or ""
    role_slug = (jobj.get("app") or {}).get("role_slug") or sel.get("app", {}).get("role_slug") or ""

    if not family:
        family = (sel.get("app") or {}).get("family") or "unknown_family"
    if not company:
        company = (sel.get("app") or {}).get("company") or "unknown_company"
    if not role_slug:
        role_slug = (sel.get("app") or {}).get("role_slug") or "unknown_role"

    return AgentContext(
        app_path=app,
        family=family,
        company=company,
        role_slug=role_slug,
        jd_text=jd,
        job_json=jobj,
        selection_json=sel,
        emphasis_json=emph,
        template_dir=template_dir,
        template_headings=headings,
    )


def _propose_local(ctx: AgentContext, rr_occurrence: int) -> str:
    """
    V1 local proposer:
    - Produce *real* content (no placeholders).
    - Keep it conservative.
    - Use template headings/sections to avoid compiler mismatch.
    """
    selected_slug = Path(ctx.template_dir).name

    # Minimal: always propose a SUMMARY replace + a couple TECHNICAL SKILL adds + one RR add.
    # You will replace this logic later with an actual model call, but the format stays stable.
    lines: list[str] = []
    lines.append("# Proposed Resume Changes (AI)")
    lines.append("")
    lines.append(f"- APP: {ctx.app_path}")
    lines.append(f"- FAMILY: {ctx.family}")
    lines.append(f"- SELECTED_TEMPLATE: {selected_slug}")
    lines.append(f"- GENERATED_UTC: {now_utc()}")
    lines.append("")

    # Always target SUMMARY (non-colon) — compiler replace-section logic anchors off headings anyway.
    n = 1

    lines += [
        f"{n})",
        "SECTION: SUMMARY",
        "CHANGE: REPLACE_SECTION",
        "TO:",
        "- Senior QA Automation Engineer with 7+ years building Java/Selenium automation, CI-driven regression suites, and API/data validation for enterprise systems.",
        "- Strong in risk-based test strategy, SQL validation, and cross-functional Agile delivery (Scrum).",
        "- Known for stabilizing flaky suites, improving coverage on critical workflows, and producing decision-ready QA reporting.",
        "",
    ]
    n += 1

    tech_section = "TECHNICAL SKILL"  # will be normalized later for patches.json
    lines += [
        f"{n})",
        f"SECTION: {tech_section}",
        "CHANGE: ADD",
        "TO: API Testing: REST, Postman, response/schema validation, workflow chaining, negative testing.",
        "",
    ]
    n += 1

    lines += [
        f"{n})",
        f"SECTION: {tech_section}",
        "CHANGE: ADD",
        "TO: CI/CD & Execution: GitHub Actions/Jenkins, Dockerized test runs, reports/artifacts, gated regressions.",
        "",
    ]
    n += 1

    lines += [
        f"{n})",
        "SECTION: PROJECT EXPERIENCE",
        "CHANGE: ADD",
        "SUBSECTION: ROLES_AND_RESPONSIBILITIES",
        f"SUBSECTION_OCCURRENCE: {rr_occurrence}",
        "TO: • Added API assertions and SQL validation to reduce regression risk on critical workflows; integrated suites into CI for faster feedback and higher release confidence.",
        "",
    ]

    out = "\n".join(lines).rstrip() + "\n"
    if _contains_placeholders(out):
        die("Proposer produced placeholder/stub text — forbidden.")
    return out


def _parse_proposed_changes(md: str) -> dict[int, dict]:
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
            cur["subsection_occurrence"] = int(v)
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


def _make_patch_item(p: dict, template_headings: list[str]) -> dict:
    ch = (p.get("change") or "").strip().upper()
    if ch not in ("ADD", "REPLACE_SECTION", "DELETE"):
        die(f"Unsupported CHANGE in proposal {p.get('num')}: {ch}")

    section = p.get("section")
    if not isinstance(section, str) or not section.strip():
        die(f"Proposal {p.get('num')} missing SECTION")

    item: dict = {"num": int(p.get("num")), "op": ch, "section": normalize_section(section, template_headings)}

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

    # hard ban placeholders inside patch content
    blob = json.dumps(item, ensure_ascii=False)
    if _contains_placeholders(blob):
        die(f"Patch contains placeholders/stubs — forbidden (num {item.get('num')}).")

    return item


def run_propose(app: Path, rr_occurrence: int, out_md: Path, force: bool) -> None:
    if out_md.exists() and not force:
        die(f"Refusing to overwrite existing file (use --force): {out_md}")
    ctx = build_context(app)
    md = _propose_local(ctx, rr_occurrence=rr_occurrence)
    write_text(out_md, md)
    print(str(out_md))


def run_materialize(app: Path, in_md: Path, approvals_json: Path, out_patches: Path, force: bool) -> None:
    if out_patches.exists() and not force:
        die(f"Refusing to overwrite existing patches.json (use --force): {out_patches}")

    ctx = build_context(app)

    approvals = load_json(approvals_json)
    approved_nums = approvals.get("approved_change_numbers")
    if not isinstance(approved_nums, list) or not all(isinstance(x, int) for x in approved_nums):
        die(f"Invalid approvals.json approved_change_numbers list: {approvals_json}")

    proposals_all = _parse_proposed_changes(read_text(in_md))
    missing = [n for n in approved_nums if n not in proposals_all]
    if missing:
        die(f"Approved proposal numbers not found in proposed-changes.md: {missing}")

    patch_items: list[dict] = []
    for n in approved_nums:
        patch_items.append(_make_patch_item(proposals_all[n], ctx.template_headings))

    out = {
        "schema": "rf_patches_v1",
        "built_at_utc": now_utc(),
        "app": {
            "app_path": str(ctx.app_path),
            "family": ctx.family,
            "company": ctx.company,
            "role_slug": ctx.role_slug,
        },
        "approved_change_numbers": approved_nums,
        "patches": patch_items,
    }

    write_text(out_patches, json.dumps(out, indent=2) + "\n")
    print(str(out_patches))


def main() -> None:
    ap = argparse.ArgumentParser(prog="rf_agent_runner")
    ap.add_argument("--mode", required=True, choices=["propose", "materialize"], help="Agent runner mode")
    ap.add_argument("--app", required=True, help="Job folder path (APP)")
    ap.add_argument("--root", default="~/secondbrain", help="Secondbrain root (default: ~/secondbrain)")
    ap.add_argument("--rr-occurrence", type=int, default=1, help="1-indexed RR occurrence (propose mode)")
    ap.add_argument("--force", action="store_true", help="Overwrite outputs")
    args = ap.parse_args()

    app = Path(args.app).expanduser().resolve()
    pipe = app / "resume_refs" / "resume_pipeline"

    proposed_md = pipe / "proposed-changes.md"
    approvals_json = pipe / "approvals.json"
    patches_json = pipe / "patches.json"

    if args.mode == "propose":
        run_propose(app, rr_occurrence=args.rr_occurrence, out_md=proposed_md, force=args.force)
    else:
        # materialize
        for req in (proposed_md, approvals_json):
            if not req.exists():
                die(f"Missing required file for materialize: {req}")
        run_materialize(app, in_md=proposed_md, approvals_json=approvals_json, out_patches=patches_json, force=args.force)


if __name__ == "__main__":
    main()
