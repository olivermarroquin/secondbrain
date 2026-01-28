from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

from docx import Document

def norm(s: str) -> str:
    s = (s or "").lower()
    s = s.replace("\u2019", "'")
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def read_docx_lines(docx_path: Path) -> List[str]:
    if not docx_path.exists():
        raise FileNotFoundError(f"missing resume-master.docx: {docx_path}")
    doc = Document(str(docx_path))
    out: List[str] = []
    for p in doc.paragraphs:
        t = (p.text or "").rstrip()
        if not t.strip():
            out.append("")
            continue
        out.append(t)

    # collapse excessive blank runs
    cleaned: List[str] = []
    prev_blank = False
    for t in out:
        blank = (t.strip() == "")
        if blank and prev_blank:
            continue
        cleaned.append(t)
        prev_blank = blank
    return cleaned

def locate_sections(lines: List[str]) -> Tuple[List[str], List[str], List[str], List[str]]:
    """
    Deterministic locator aligned to templates:

    - HEADER: before PROFESSIONAL SUMMARY
    - SUMMARY: PROFESSIONAL SUMMARY..TECHNICAL SKILLS (or SKILLS)
    - SKILLS: TECHNICAL SKILLS..EXPERIENCE (or first job-ish line)
    - EXP: EXPERIENCE..end
    """
    def trim(block: List[str]) -> List[str]:
        while block and block[0].strip() == "":
            block = block[1:]
        while block and block[-1].strip() == "":
            block = block[:-1]
        return block

    idx_prof = None
    idx_tech = None
    idx_exp = None

    for i, t in enumerate(lines):
        tl = t.strip().lower()
        tl2 = tl.rstrip(":")
        if idx_prof is None and (tl2 in ("professional summary", "summary", "profile", "professional profile")):
            idx_prof = i
            continue
        if idx_tech is None and (("technical skill" in tl2) or tl2 in ("skills", "technical skills")):
            idx_tech = i
            continue
        if idx_exp is None:
            if tl2 in ("experience", "professional experience", "work experience"):
                idx_exp = i
                continue
            # job-ish line: Month YYYY -- Present/Month YYYY
            if re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\b.*\b\d{4}\b\s*[-–—]{1,2}\s*(?:present|\b\d{4}\b)", tl2):
                idx_exp = i
                continue
            if re.search(r"\b\d{4}\b\s*[-–—]{1,2}\s*(?:present|\b\d{4}\b)", tl2) and len(tl2) <= 120:
                idx_exp = i

    if idx_prof is None:
        idx_prof = 0
    if idx_tech is None:
        idx_tech = idx_exp if idx_exp is not None else min(len(lines), idx_prof + 12)
    if idx_exp is None:
        idx_exp = len(lines)

    header = trim(lines[:idx_prof])
    summary = trim(lines[idx_prof:idx_tech])
    skills = trim(lines[idx_tech:idx_exp])
    exp = trim(lines[idx_exp:])
    return header, summary, skills, exp

def format_blocks_for_prompt(header: List[str], summary: List[str], skills: List[str], exp: List[str], max_exp_lines: int = 80) -> str:
    """
    Backward-compatible (un-numbered) representation.
    """
    exp2 = exp[:max_exp_lines]
    if len(exp) > max_exp_lines:
        exp2 = exp2 + ["", f"... (truncated: {len(exp) - max_exp_lines} more lines)"]

    def join(block: List[str]) -> str:
        return "\n".join(block).strip()

    return (
        "=== RESUME_HEADER ===\n" + join(header) + "\n\n"
        "=== RESUME_SUMMARY ===\n" + join(summary) + "\n\n"
        "=== RESUME_SKILLS ===\n" + join(skills) + "\n\n"
        "=== RESUME_EXPERIENCE ===\n" + join(exp2) + "\n"
    )

def format_numbered_blocks_for_prompt(
    header: List[str],
    summary: List[str],
    skills: List[str],
    exp: List[str],
    max_exp_lines: int = 80
) -> Tuple[str, Dict[str, Dict[str, str]]]:
    """
    Numbered resume blocks for deterministic targeting.

    Returns:
      (prompt_text, line_index)

    line_index maps:
      ref -> { "section": "HEADER|SUMMARY|SKILLS|EXPERIENCE", "text": "<exact line>" }

    Refs:
      H001.., S001.., K001.., E001..
    """
    exp2 = exp[:max_exp_lines]
    if len(exp) > max_exp_lines:
        exp2 = exp2 + ["", f"... (truncated: {len(exp) - max_exp_lines} more lines)"]

    line_index: Dict[str, Dict[str, str]] = {}

    def emit(section: str, prefix: str, block: List[str]) -> str:
        out: List[str] = []
        n = 0
        for line in block:
            if not line.strip():
                out.append("")
                continue
            n += 1
            ref = f"{prefix}{n:03d}"
            line_index[ref] = {"section": section, "text": line}
            out.append(f"{ref} | {line}")
        return "\n".join(out).strip()

    txt = (
        "=== RESUME_HEADER (numbered) ===\n" + emit("HEADER", "H", header) + "\n\n"
        "=== RESUME_SUMMARY (numbered) ===\n" + emit("SUMMARY", "S", summary) + "\n\n"
        "=== RESUME_SKILLS (numbered) ===\n" + emit("SKILLS", "K", skills) + "\n\n"
        "=== RESUME_EXPERIENCE (numbered) ===\n" + emit("EXPERIENCE", "E", exp2) + "\n"
    )
    return txt, line_index
