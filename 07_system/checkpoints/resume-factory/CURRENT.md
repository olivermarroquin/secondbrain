# CURRENT (Resume Factory)

## 2026-02-10 — Ideal Profile pipeline wired end-to-end

- Added/verified CLI tools:
  - resume-keyword-scout → notes/keyword-scout.json (JD terms/tools)
  - resume-ideal-profile → notes/ideal-profile.json (structured candidate target)
  - resume-map-ideal-edits → resume_refs/edit-proposals.json (anchored edits)
  - resume-suggest-edits --mode ideal (runs the above chain)
  - resume-ideal-edits (thin wrapper to run select + keyword-scout + ideal-profile + map-ideal-edits in one shot)
- Fixed schema enforcement issues in keyword-scout output (type must be keyword|tool), added deterministic dedupe.
- Ideal-profile output normalized: top-level ideal_profile object + notes.
- Current state: resume-map-ideal-edits produces higher-quality anchored edits (SUMMARY/SKILLS/EXPERIENCE) than classic suggest-edits for this JD.
- Next: upgrade resume-map-ideal-edits to call generate_rewrite_packet_openai (treat ideal-profile as structured signals) for stronger full-resume rewrites.

## 2026-02-10 — Stable Build (klap6)

Checkpoint: `checkpoints/2026-02-10_checkpoint.md`

- Proposal + rewrite packet history archiving added (timestamped snapshots per run).
- SKILLS ADD_LINE no longer dropped; categories persist into proposals.
- DOCX insertion fix: `apply_add_line()` clones anchor paragraph XML so added SKILLS lines inherit exact formatting (bold label + normal values + indentation).
- Resume diff tracking added in `resume_refs/diffs_history/` after `resume-approve-edits`.

Next:

- Add `resume-suggest-edits --from-latest` to iterate on `resume_refs/resume.docx`.
  MD


---

## 2026-02-12 (run10) — Layers A/B/C locked + Layer C formatting stabilized
- Layer A: `resume-map-ideal-edits` writes RAW rewrite packet → `resume_refs/rewrite-packet.raw.json`
- Layer B: `resume-filter-edits` compiles RAW → deterministic `resume_refs/edit-proposals.json`
- Layer C: `resume-approve-edits` stabilized summary spacing + skills typography; no extra blank paragraphs
- Checkpoint: checkpoints/2026-02-12_checkpoint.md
- Synthesis: analysis/2026-02-12_run10_post-run_synthesis.md
- Log: logs/2026-02-12_run10_full-run-log.md
- Archive: archives/2026-02-12_run10_archive-notes.md
