# Checkpoint — 2026-02-05

Based on CURRENT.md baseline (first production batch).

---

## What Was Done

- Executed 6 end-to-end job application workflows (QA Automation Engineer roles)
- Companies: Kforce, INSPYR Solutions, Innominds Software, Pellera, Business and Technology Solutions, TechTalent Solutions
- All pipeline phases exercised: intake → template selection → suggestions → approval → browser apply → status marking → session close

## What Worked

- Job folder scaffolding creates consistent structure
- Template selection scoring produces reasonable matches
- Proposal application mechanics (REPLACE_LINE/REPLACE_PHRASE) are deterministic
- Safety drops correctly refuse headers, role lines, duplicates
- Git commit discipline supported frequent commits without state conflicts

## What Broke / Was Discovered Broken

- `job-meta.json.status` and `application-record.json.current_status` can drift
- `jobs-list-unapplied` reads only `job-meta.json`, not `application-record.json`
- `--source stdin` paste capture freezes unpredictably mid-text
- `jobs-apply-batch` opens jobs in sorted order, not intent order
- No command exists to revert applied → not_applied

## What Was Learned

- Canonical status source is `job-meta.json.status` (not `application-record.json`)
- Suggestion runs are stateless against template baseline — prior approved edits lost on re-run
- Queue-based batch apply is queue-centric, not intent-centric
- `--source clipboard` is more reliable than `--source stdin`
- `jobs-mark-applied-last` has `-push`; `jobs-batch-mark-applied` does not

## Decisions Made

- Promote `--source clipboard` as recommended default over `--source stdin`
- Workaround for targeted job open: `open "$(cat .../job-post-url.txt)"`
- Manual JSON edits required for status reversal until `jobs-status-set` is built
- No batching beyond 6 jobs until P0 issues are fixed

## What Is Next

P0 fixes before scaling:
1. Unify status source of truth across all `jobs-*` commands
2. Add `jobs-status-set` / `jobs-mark-not-applied` command
3. Make batch selection explicit (`--pick`)
4. Fix stdin ingestion or document clipboard as primary path

---

*Checkpoint written: 2026-02-06*
*Source: 2026-02-05_full-run-log.md, post-run synthesis*
