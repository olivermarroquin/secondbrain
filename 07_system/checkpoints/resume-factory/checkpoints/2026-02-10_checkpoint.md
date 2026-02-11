# 2026-02-10 — Resume Factory Stable Build (klap6)

## What changed (this chat)

- `resume-suggest-edits`: archives proposals + rewrite packets per run (timestamped history files).
- SKILLS `ADD_LINE` proposals no longer get dropped (dedupe fix) — new categories persist.
- `resume-approve-edits`: `apply_add_line()` now clones the anchor paragraph XML to preserve formatting (indent/tab stops/run styles).
  - Fix: added SKILLS lines now format exactly like existing “TECHNICAL SKILLS” rows (bold label + normal values) instead of appearing misaligned.
- `resume-approve-edits`: writes resume diffs to `resume_refs/diffs_history/<timestamp>_resume.diff` after apply.

## New outputs / where to look

- Proposal history:
  - `APP/resume_refs/proposals_history/*_edit-proposals.json`
- Rewrite packet history:
  - `APP/notes/rewrite_packets_history/*_rewrite-packet.json`
- Resume diffs:
  - `APP/resume_refs/diffs_history/*_resume.diff`

## Still to do

- Implement `resume-suggest-edits --from-latest` to use `APP/resume_refs/resume.docx` as input (iterate on last approved resume instead of template).
  MD

---

Other Chat Updates:

## What changed

- Introduced/used keyword-scout + ideal-profile + map-ideal-edits pipeline.
- Added wrapper command resume-ideal-edits for one-shot execution.
- resume-suggest-edits gained --mode ideal flow to run the pipeline.

## Key artifacts

- 07_system/bin/resume-keyword-scout
- 07_system/bin/resume-ideal-profile
- 07_system/bin/resume-map-ideal-edits
- 07_system/bin/resume-ideal-edits
- 07_system/bin/resume-suggest-edits (ideal mode)

## Notes

- rf-checkpoint does not generate these; it files them + updates LATEST.md.
  """
