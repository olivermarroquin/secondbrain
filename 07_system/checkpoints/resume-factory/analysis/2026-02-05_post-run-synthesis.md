# Post-Execution System Synthesis — 2026-02-05

Based on: `2026-02-05_full-run-log.md`, ChatGPT post-run reflection, and resume-factory codebase as exercised.

---

## SECTION 1 — What Was Done

### Workflows Executed

Six end-to-end job application workflows were run for QA Automation Engineer roles:

1. **Kforce** — Lead Software QA Engineer
2. **INSPYR Solutions** — Quality Assurance Engineer (Tosca-focused)
3. **Innominds Software** — QA Automation Engineer
4. **Pellera** — Senior Quality Assurance Engineer (AI practice)
5. **Business and Technology Solutions** — Consulting QA/Test Engineer (E-commerce)
6. **TechTalent Solutions** — TOSCA Tester/QA Automation Lead (Oracle)

Each job was taken through: intake → template selection → edit suggestions → edit approval → resume generation → browser application → status marking → session close.

### Pipeline Components Exercised

| Phase | Commands Used |
|-------|---------------|
| Intake | `job-intake-one` (stdin, clipboard, file), `job-intake-commit` |
| Verification | `jobs-list-unapplied`, `find`, `ls`, JSON validation |
| Template Selection | `resume-select --app` |
| Preview | `resume-preview --app` |
| Suggestions | `resume-suggest-edits --app --diff` |
| Approval | `resume-approve-edits --app --force --open`, `--numbers N` |
| Apply Flow | `jobs-apply-batch`, `jobs-queue-show`, `open $(cat .../job-post-url.txt)` |
| Marking | `jobs-mark-applied-last --date --apply --commit --push` |
| Session | `session-start`, `session-close` |

### Real-World Usage Patterns Observed

- Clipboard input (`--source clipboard`) was more reliable than stdin paste
- Multiple `resume-suggest-edits` runs were attempted to "get more keywords"
- Manual LibreOffice edits were made post-generation for final polish
- Queue file paths (`/tmp/applied-YYYY-MM-DD-batchN.txt`) required manual tracking
- Jobs were opened individually via `open "$(cat .../job-post-url.txt)"` workaround

---

## SECTION 2 — Current System Condition

### Solid and Reliable

- **Job folder scaffolding**: `job-intake-*` creates consistent structure (`jd/`, `tracking/`, `resume_refs/`, `notes/`)
- **Template selection scoring**: Reasonable matches when JD terms overlap expected stacks
- **Proposal application mechanics**: `resume-approve-edits` applies REPLACE_LINE/REPLACE_PHRASE deterministically
- **Git commit discipline**: Workflow supports frequent commits without fighting state
- **Safety drops**: Headers, role lines, duplicates are correctly refused

### Fragile or Awkward

- **STDIN paste capture**: Terminal paste freezes mid-text unpredictably; required abort/retry or workarounds
- **Batch queue UX**: Relationship between queue files, batch numbering, and which command opens what is confusing
- **Suggestion re-runs**: Each run generates fresh `edit-proposals.json` from template baseline; prior approved edits are lost
- **Status dual-write**: `job-meta.json.status` vs `application-record.json.current_status` can diverge

### Manual and Error-Prone

- Queue file selection requires knowing the exact `/tmp/applied-*` path
- Status reversal requires manual JSON edits (no `jobs-mark-not-applied` command)
- LibreOffice lock files (`.~lock.*#`) were accidentally tracked once
- Workaround for targeted job opening: no `jobs-open --app` command exists

### Assumptions That Held

- One template per family is sufficient for initial matching
- JD term extraction produces enough signal for proposal generation
- DOCX text extraction via `python-docx` works for current templates

### Assumptions That Failed

- "Applied" status was assumed to be a single source of truth — it is not
- Re-running `resume-suggest-edits` was assumed to be additive — it is not
- Queue-based batch apply was assumed to match "the job I just worked on" — it does not

---

## SECTION 3 — What Was Learned From Real Runs

### Theory vs Reality Divergence

| Expected | Actual |
|----------|--------|
| Update `application-record.json` → job shows as applied | `jobs-list-unapplied` reads `job-meta.json`, not `application-record.json` |
| Re-run suggestions to accumulate keywords | Each run overwrites proposals; baseline is always template |
| `jobs-apply-batch` opens "my job" | It opens first N unapplied in sorted order; no intent awareness |

### Highest Friction Steps

1. **Paste-to-stdin capture**: Required 2-3 retries or fallback to clipboard/file methods
2. **Batch apply intent mismatch**: Operator wants "open this specific job"; tooling offers "open next N jobs"
3. **State reconciliation**: Determining which file controls `jobs-list-unapplied` required investigation

### Missing Validations

- No check that `job-meta.json.status` == `application-record.json.current_status`
- No warning when `resume-approve-edits` will overwrite manual edits
- No confirmation prompt before `jobs-apply-batch` opens URLs
- No pre-apply check that `resume.docx` matches intended job

### Cognitive Load Sources

- Remembering queue file naming convention and batch number
- Knowing which `-push` flags exist on which commands
- Understanding that suggestion runs are stateless against the template

---

## SECTION 4 — Limitations Observed

### Structural Limitations

| Limitation | Impact |
|------------|--------|
| Multiple status sources (`job-meta.json`, `application-record.json`, `status-history.md`) | State drift causes "applied" jobs to reappear in unapplied list |
| Resume baseline is always template | Manual edits are nuked on regeneration; no incremental mode |
| Proposal generation is stateless | Cannot "add Cypress on top of earlier RESTful edits" |

### Workflow Limitations

- Batch apply is queue-centric, not intent-centric; no `jobs-open --app <path>` command
- Re-running suggestions for "more keywords" doesn't accumulate; it replaces
- No single command to revert applied → not_applied across all tracking files

### CLI UX Limitations

| Issue | Commands Affected |
|-------|-------------------|
| Inconsistent `-push` flag | `jobs-mark-applied-last` has it; `jobs-batch-mark-applied` does not |
| No targeted job open | Requires `open "$(cat .../job-post-url.txt)"` workaround |
| stdin freeze failure mode | `job-intake-one --source stdin` hangs with no guidance |

### Automation Boundaries (Unsafe to Scale)

At 20+ jobs/day with current setup:
- Status drift compounds quickly across many job folders
- Queue confusion causes mis-targeted applications
- JD term extraction noise amplifies low-quality edits
- Repeated manual state corrections become unsustainable

---

## SECTION 5 — Recommended Enhancements (Prioritized)

### P0 — Must Fix Before Scaling to 20+ Runs

| Enhancement | Problem Solved | Files/Components | Effort |
|-------------|----------------|------------------|--------|
| **Unify status source of truth** | Drift between `job-meta.json` and `application-record.json` breaks `jobs-list-unapplied` trust | All `jobs-*` commands, tracking schema | Medium |
| **Add `jobs-status-set` / `jobs-mark-not-applied`** | Manual JSON edits are risky and incomplete | New command, shared status mutation utility | Small-Medium |
| **Make batch selection explicit** | "batch auto" opened wrong job | `jobs-apply-batch`, add `--pick <index\|company>` | Medium |
| **Fix stdin ingestion** | Terminal paste freezing forced workarounds | `job-intake-one`, promote `--source clipboard` as default | Small |

### P1 — High-Leverage Quality Improvements

| Enhancement | Problem Solved | Files/Components | Effort |
|-------------|----------------|------------------|--------|
| **Incremental resume editing** | Re-runs nuke prior edits | `resume-approve-edits`, add `-base resume_refs/resume.docx` option | Structural |
| **Improve JD term extraction** | Noisy terms ("az/mst", "and/or", "c2h", "database/sql") | `rf_jd_terms.py` | Small-Medium |
| **Proposal quality controls** | Awkward phrasing, keyword stuffing | Prompt rules, proposal validator | Medium |
| **Flag consistency** | `-push` exists in one command but not another | `jobs-mark-applied-last`, `jobs-batch-mark-applied` | Small |
| **Queue file ergonomics** | Multiple `/tmp/applied-*` accumulates; wrong queue used | `jobs-apply-batch`, `jobs-queue-show`, deterministic naming | Small |

### P2 — Nice-to-Have / Later

| Enhancement | Problem Solved | Files/Components | Effort |
|-------------|----------------|------------------|--------|
| **Add `jobs-open --app`** | No single-job targeted open | New command | Small |
| **LibreOffice lock file detection** | Lock artifacts contaminated repo | `session-close` check or pre-commit hook | Small |
| **R&R occurrence labeling** | Can't target specific "Roles and Responsibilities" blocks | `rf_docx_extract.py`, proposal output | Medium |

---

## SECTION 6 — Why AI-in-CLI Is the Right Next Step

### Continuous Codebase Access Improves Fix Quality

The failures observed (status drift, partial edits, queue confusion) are **stateful, multi-file, and workflow-dependent**. AI with repo access can:

- Trace which commands read which files (e.g., why `jobs-list-unapplied` ignored `application-record.json`)
- Find inconsistent flag behavior across commands quickly
- Implement changes consistently across all entrypoints without missing paths

### Context Loss Prevention

Manual debugging today required discovering that `job-meta.json.status` is the canonical driver. AI-in-CLI retains this knowledge across sessions and can:

- Enforce invariants (e.g., "these three tracking files must agree")
- Surface inconsistencies during code changes
- Maintain awareness of which files affect which commands

### Step-by-Step Changes Are Safer

Manual "fixing" led to partial corrections until the real driver file was discovered. AI-assisted changes can:

- Add validations that prevent partial edits from being accepted
- Run local checks after each patch (syntax, JSON validity, expected output)
- Produce deterministic diffs and reduce accidental drift

### Problem Categories AI Is Well-Suited For

Based on 2026-02-05 observations:

| Category | Examples from Today |
|----------|---------------------|
| **Edge case hunting** | stdin paste freeze, queue-file mismatch, status drift |
| **Consistency enforcement** | unify flags, unify status handling |
| **Refactor-with-constraints** | incremental resume base support without redesign |
| **Invariant checks** | "these three tracking files must agree" assertions |
| **Prompt/schema tightening** | stop low-quality keyword stuffing and banned-term injection |

---

## SECTION 7 — Where AI Should Focus First

### Top 5 Areas for AI-Assisted Fixes

| Priority | Area/File | Why AI ROI Is High |
|----------|-----------|-------------------|
| **1** | `jobs-list-unapplied`, `jobs-mark-applied-last`, `jobs-batch-mark-applied`, tracking writers | Status source-of-truth unification requires consistent changes across all readers/writers |
| **2** | New `jobs-status-set` command + shared status mutation utility | Safe reversible status transitions with consistent history logging; touches multiple modules |
| **3** | `jobs-apply-batch`, queue file naming, `jobs-queue-show` | Queue UX and selection logic have subtle state dependencies |
| **4** | `job-intake-one` input handling | stdin capture has silent failure modes; AI can add better error handling and fallback paths |
| **5** | `rf_jd_terms.py`, `resume-suggest-edits` proposal generation | Term filtering and prompt rules require iterative refinement with quality feedback loops |

### Specific Files/Modules

```
07_system/bin/jobs-list-unapplied       # reads status; must match writers
07_system/bin/jobs-mark-applied-last    # writes status; has -push
07_system/bin/jobs-batch-mark-applied   # writes status; missing -push
07_system/bin/jobs-apply-batch          # queue creation; selection logic
07_system/bin/job-intake-one            # stdin capture; source selection
01_projects/resume-factory/scripts/rf_jd_terms.py  # term extraction filters
07_system/bin/resume-suggest-edits      # proposal generation; gating logic
```

### Where Repetition/Subtle Bugs Are Likely

- Status field names (`status` vs `current_status`) across JSON schemas
- Queue file naming patterns (`batch1`, `batch2`, etc.) and date parsing
- Term normalization edge cases (slashes, hyphens, case sensitivity)
- DOCX text matching for REPLACE_LINE (whitespace, bullet formatting)

---

## Summary

The 2026-02-05 batch run successfully exercised the full resume-factory pipeline but exposed:

1. **Status drift** from multiple sources of truth
2. **Stateless suggestion runs** that don't accumulate
3. **Queue-centric batch apply** that doesn't match operator intent
4. **Inconsistent CLI UX** across related commands

AI-in-CLI is the right approach because these issues require:
- Multi-file awareness during fixes
- Consistent application of changes across entrypoints
- Iterative refinement with quality feedback

**Recommended first AI-assisted fix**: Unify status source of truth across `job-meta.json`, `application-record.json`, and all `jobs-*` commands.

---

*Generated: 2026-02-06*
*Source: 2026-02-05_full-run-log.md + post-run reflection*
*Classification: Analysis artifact for human decision-making*

  Summary of findings:

  What worked well:  
  - Job folder scaffolding, template selection, proposal application mechanics, git discipline, safety drops
  
  Key issues identified:
  - Status drift between job-meta.json and application-record.json
  - Stateless suggestion runs (can't accumulate edits)
  - Queue-centric batch apply doesn't match operator intent
  - Inconsistent -push flag across commands
  - stdin paste freezing

  P0 fixes (must-do before scaling or refactoring):
  1. Unify status source of truth
  2. Add jobs-status-set / jobs-mark-not-applied command
  3. Make batch selection explicit
  4. Fix stdin ingestion reliability

  Top AI focus areas:
  1. Status readers/writers across all jobs-* commands
  2. New status mutation command
  3. Queue UX and selection logic
  4. Input handling in job-intake-one
  5. rf_jd_terms.py and proposal quality controls

  The synthesis is classified as an analysis artifact for human decision-making — it does not replace or overwrite CURRENT.md.  
