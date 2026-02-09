# 2026-02-09 — Resume Factory checkpoint

## What changed
- rf_docx_extract.py: SKILLS now stops before EDUCATION so K-refs never include education lines.
- resume-suggest-edits: rewrite behavior stabilized (no education refs touched; structural refs protected).
- AGENT_PROMPT.md: refined generic-JD handling + rewrite quality rules (kept prompt-based freedom).
- Added rf_mode.py (scaffold present).

## Why
- Prevented accidental anchoring/ADD_LINE into EDUCATION (e.g., K012–K014) when SKILLS are parsed.
- Improved consistency when JD is extremely short/generic.

## Verification
- print_skill_refs now shows only K001–K011 (no EDUCATION lines).
- resume-suggest-edits diff confirms: “OK: no education refs touched”.

## Notes
- This JD was weak (tool list + soft skills), so rewrite output quality will naturally cap; focus is correctness + no signal loss.
