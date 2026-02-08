# Resume Factory Checkpoint — 2026-02-08

## Summary
We moved Resume Factory closer to “ChatGPT-quality tailoring” while preserving deterministic approvals.

## Key changes
- Updated `AGENT_PROMPT.md` with ChatGPT-style tailoring behaviors:
  - Stack coherence + substitution rules
  - Paradigm-aware rewriting for domain pivots (e.g., UI QA → Snowflake/data validation QA)
  - Skills category coherence expectations
- `resume-suggest-edits`:
  - SKILLS mapping is now category-aware (match by label left of `:`)
  - Supports `ADD_LINE` for new categories and `DELETE_LINE` for irrelevant categories (when emitted)
- `resume-approve-edits`:
  - Successfully applied the expanded ops set end-to-end in real runs
- Proposal schema:
  - Expanded allowlist to include `ADD_LINE` / `DELETE_LINE`
  - Adjusted `DELETE_LINE` validation so empty `after` is acceptable

## Validation performed
- Cypress-primary JD test produced coherent Cypress substitutions and improved tailoring.
- Applied proposals produced a generated `resume.docx` successfully.

## Issues observed
- Some residual Playwright mentions can persist after stack pivot → need enforcement.
- Some structural/heading lines risk being targeted (e.g., “Roles and Responsibilities:”).
- Skills category label formatting remains bold due to template DOCX styles (acceptable for now).

## Next steps
1) Enforce no mixed-stack unless JD demands it (hard rule + post-check).
2) Add “ecosystem-aware” rewriting rules for adjacent tools + realistic actions.
3) Tighten SKILLS keep/delete logic so we delete only when safe and JD-reasoned.
