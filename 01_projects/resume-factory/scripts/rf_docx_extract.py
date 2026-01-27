from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

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
    Create a bounded, prompt-friendly representation.
    We deliberately cap EXPERIENCE lines to avoid huge prompts.
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
