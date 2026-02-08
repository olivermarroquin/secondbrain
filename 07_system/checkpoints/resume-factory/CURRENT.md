# CURRENT — Resume Factory

Last updated: 2026-02-06
Baseline: 6 production runs on 2026-02-05

---

## Overview

Resume Factory is a CLI-driven system for:
- Capturing job descriptions (intake)
- Selecting resume templates based on JD analysis
- Generating keyword-aligned edit proposals
- Producing tailored resume.docx files
- Tracking application status across job folders

Primary job family: `qa_automation_engineer`
Templates: 4 variants (Java/Selenium, Java/Playwright, Python/Playwright, TypeScript/Playwright)

---

## Working Commands

### Session Management
| Command | Purpose |
|---------|---------|
| `session-start` | Load repo context, show git status, print state files |
| `session-close` | Append to LOG.md, prompt for commit/push |

### Job Intake
| Command | Purpose |
|---------|---------|
| `job-intake-one --family --company --role --date --url --source` | Create job folder + capture JD |
| `job-intake-commit --app <path>` | Commit + push intake artifacts |

Source options: `stdin`, `clipboard`, `url`, `file:<path>`

### Resume Pipeline
| Command | Purpose |
|---------|---------|
| `resume-select --app <path>` | Score templates against JD, show best pick |
| `resume-preview --app <path>` | Show template info, JD stats, keyword hits |
| `resume-suggest-edits --app <path> --diff` | Generate edit proposals + narrative, write edit-proposals.json |
| `resume-approve-edits --app <path> --force --open` | Apply proposals, write resume.docx |
| `resume-approve-edits --app <path> --numbers 1 3 5` | Apply selected proposals only |

### Job Status Management
| Command | Purpose |
|---------|---------|
| `jobs-list-unapplied --date YYYY-MM-DD` | List jobs not yet applied (reads job-meta.json) |
| `jobs-apply-batch N --date YYYY-MM-DD` | Open N unapplied jobs in browser, write queue file |
| `jobs-queue-show` | Display current queue contents |
| `jobs-queue-prune` | Remove entries from queue interactively |
| `jobs-mark-applied-last --date --apply --commit --push` | Mark queue as applied, commit, push |
| `jobs-batch-mark-applied --paths-file <file> --apply --commit` | Mark specific paths as applied |

---

## Valid Pipelines

### Single Job (Golden Run)
```
session-start
job-intake-one ... --source clipboard
job-intake-commit --app <path>
resume-select --app <path>
resume-preview --app <path>
resume-suggest-edits --app <path> --diff
resume-approve-edits --app <path> --force --open
[manual: apply in browser]
jobs-mark-applied-last --date ... --apply --commit --push
session-close
```

### Batch Jobs
```
session-start
[repeat intake for N jobs]
jobs-list-unapplied --date ...
[build resumes for batch]
jobs-apply-batch N --date ...
[manual: apply in browser, prune if partial]
jobs-mark-applied-last --date ... --apply --commit --push
session-close
```

---

## Job Folder Structure

```
01_projects/jobs/<family>/<company>/<date>_<role>/
├── jd/
│   ├── jd-raw.txt
│   └── job-post-url.txt
├── tracking/
│   ├── job-meta.json        # canonical status source
│   ├── application-record.json
│   └── status-history.md
├── resume_refs/
│   ├── edit-proposals.json
│   ├── edits-applied.json
│   └── resume.docx
└── notes/
```

---

## Locked Rules

1. **Status canonical source**: `job-meta.json.status` drives `jobs-list-unapplied`
2. **Proposal baseline**: `resume-suggest-edits` always generates from template, not current resume.docx
3. **Safety drops**: Proposals targeting headers, role lines, or duplicates are refused
4. **No auto-push**: Most commands require explicit `--push` or separate `git push`
5. **Session discipline**: `session-close` prompts for commit if dirty

---

## Known Issues / Broken Items

### P0 — Blocking Scale
| Issue | Impact | Workaround |
|-------|--------|------------|
| Status drift | `job-meta.json` and `application-record.json` can diverge | Edit job-meta.json manually |
| No status reversal command | Cannot revert applied → not_applied safely | Manual JSON edit |
| stdin paste freezing | `--source stdin` hangs unpredictably | Use `--source clipboard` |
| Batch opens wrong job | Queue-centric, not intent-centric | Use `open "$(cat .../job-post-url.txt)"` |

### P1 — Quality Issues
| Issue | Impact |
|-------|--------|
| Suggestion re-runs not additive | Prior approved edits lost on regeneration |
| JD term noise | Terms like "az/mst", "and/or", "c2h" pass through |
| LLM proposal quality drift | Chat-style narrative may suggest low-signal edits without tighter JD term suppression |
| Inconsistent `-push` flag | `jobs-mark-applied-last` has it; `jobs-batch-mark-applied` does not |
| No `jobs-open --app` | Must use manual `open $(cat ...)` workaround |

---

## Explicit Non-Goals

- Cover letter generation (backlog idea, not active)
- Multi-family template management (single family for now)
- Automated job discovery/scraping
- R&R occurrence targeting (backlog idea, not implemented)
- Incremental resume editing mode (backlog idea, not implemented)

---

## File Locations

| Artifact | Path |
|----------|------|
| CLI commands | `07_system/bin/` |
| Python modules | `01_projects/resume-factory/scripts/` |
| Templates | `03_assets/templates/resumes/qa_automation_engineer/` |
| Job folders | `01_projects/jobs/qa_automation_engineer/<company>/` |
| Checkpoints | `07_system/checkpoints/resume-factory/checkpoints/` |

---

## AI Context

When operating on resume-factory:
1. Read this file first
2. `job-meta.json.status` is the canonical status field
3. Do not assume `application-record.json` drives status queries
4. Proposal generation is stateless — changes are not cumulative
5. Check `07_system/checkpoints/resume-factory/LATEST.md` for pointer to latest checkpoint

---

## 2026-02-08 — Progress Update

### What changed (working)
- Added/expanded **ChatGPT-style tailoring behaviors** in `AGENT_PROMPT.md`, including:
  - Stack coherence + substitution (primary tool consistency)
  - Paradigm-aware rewriting (domain pivots like UI QA → data validation, AWS/Snowflake-style rewrites)
  - Skills category coherence guidance
- `resume-suggest-edits` now compiles **category-aware SKILLS proposals**:
  - Match SKILLS lines by category label (left of `:`) → `REPLACE_LINE`
  - New category not present → `ADD_LINE`
  - Non-JD-relevant categories → `DELETE_LINE` (when emitted)
- End-to-end support for proposal ops now includes:
  - `REPLACE_LINE`, `REPLACE_PHRASE`, `ADD_LINE`, `DELETE_LINE`
- Schema validation updated to allow `DELETE_LINE` to carry empty `after` payloads (e.g., `[""]` / `[]`) without failing.

### What we validated
- Cypress-primary JD test produced coherent substitutions (Playwright → Cypress) across Summary/Skills/Experience.
- `resume-approve-edits` applied selected proposals successfully and generated `resume_refs/resume.docx`.
- Category-aware SKILLS logic prevented nonsense category swaps (e.g., Networking → CI/CD).

### Known issues / next fixes
- **Residual stack mentions** can remain (e.g., Playwright references) → need stronger “no conflicting stack mentions unless JD explicitly requires both.”
- **Heading targeting**: ensure structural lines like “Roles and Responsibilities:” are never replaced.
- **DOCX formatting**: skills category labels remain bold (template styling). Keep for now; revisit later.

### Next steps
1) Tighten stack-pivot enforcement (no leftover conflicting tool mentions).
2) Improve “ecosystem-aware” rewriting (adjacent tools/actions: Snowflake → SQL/JDBC, AWS → S3/CloudWatch, API → contracts/validation).
3) Improve SKILLS delete/keep logic so we don’t delete generally valuable categories unless explicitly instructed by JD.

