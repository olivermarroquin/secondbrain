# 2026-02-12 — Checkpoint

## Scope
Locked Separation of Concerns across Layers A/B/C and stabilized Layer C DOCX formatting output.

## What changed

### Layer A — RAW rewrite packet output
- `resume-map-ideal-edits` writes RAW AI output to:
  - `resume_refs/rewrite-packet.raw.json` (shape includes `payload.rewrite_packet`)

### Layer B — Deterministic proposal compiler
- `resume-filter-edits` compiles RAW → deterministic proposals:
  - Input: `resume_refs/rewrite-packet.raw.json`
  - Output: `resume_refs/edit-proposals.json`
- Policy behaviors:
  - Summary:
    - 1-line template summary → `REPLACE_LINE` (joined summary into S###)
    - multi-line template summary → `REPLACE_LINE` first line + `DELETE_LINE` the rest
  - Skills:
    - label-aware mapping to K### rows with fallback ordering

### Layer C — Apply proposals into DOCX (this checkpoint)
- `resume-approve-edits` now reliably produces a clean `resume_refs/resume.docx`:
  - Removes extra blank paragraphs created by SUMMARY `DELETE_LINE` ops (cleanup runs)
  - Summary spacing stabilized via `paragraph_format` (no blank-paragraph insertion)
    - space_after on `PROFESSIONAL SUMMARY:`
    - space_after on summary paragraph
    - space_before on `TECHNICAL SKILL:`
  - Skills formatting stabilized:
    - labels before `:` bold, values after `:` not bold
    - preserves template font name/size for label/value runs (prevents style drift)
  - Fixed a stray/indented duplicate `_cleanup_blank_paragraphs(doc)` call

## Verified evidence
- Reproduced on app:
  - `01_projects/jobs/qa_automation_engineer/cm_first_group/2026-02-11_workload-automation-engineer`
  - Template: `03_assets/templates/resumes/qa_automation_engineer/03_python_playwright/resume-master.docx`
- Output region now shows stable spacing and correct skills typography.

## Artifacts
- Checkpoint: `checkpoints/2026-02-12_checkpoint.md`


---

## Cross-template validation (Layer C proven)

Validated `resume-approve-edits` formatting stability across multiple template families:

- Template 03: `03_python_playwright` (cm_first_group workload automation engineer)
- Template 01: `01_java_selenium` (klap6 sr java sdet)
- Template 05: `05_typescript_cypress` (kforce lead software qa engineer)

Pass criteria met:
- No extra blank paragraph gaps after SUMMARY deletes
- Summary-to-skills spacing stable via paragraph_format (no empty paragraph reliance)
- Skills label/value formatting stable (label bold, value not bold)
- Font name/size preserved (no style drift)
