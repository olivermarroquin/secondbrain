# WORKFLOW (Global - AI + Git, RWWLO)

## Hard rule: RWWLO
No work begins until NEXT.md is accurate.
Updating NEXT.md is always allowed as task #0.

## Resume Where We Left Off (RWWLO)
Run:
-cd ~/secondbrain
- git fetch --all --prune
- git status -sb
- git lg -10
- sed -n'1,200p' 07_system/state/STATUS.md
- sed -n'1,200p' 07_system/state/NEXT.md

## Session start (required)
Run: 07_system/bin/session-start
- Fetch safely: git fetch --all --prune
- Show: git status -sb, git lg -10
- Read: STATUS.md + NEXT.md

## Work loop
- Before coding: git status -sb
- After a chunk: git diff, git status -sb
- Prefer: git add -p → git diff --staged → git commit

## Session close (required)
Run: 07_system/bin/session-close
- Append to LOG.md
- Prompt to update STATUS/NEXT
- Show git status
- Remind to commit + push

## AI collaboration model (patch-first)
When asking for help, provide:
- git status -sb
- relevant git diff (or say “clean”)
- relevant sections of STATUS/NEXT
Responses should be patch-style steps or diffs, with exact commands and recovery paths.

## Focus contract (deterministic)
- Every continuous project MUST have: 01_projects/<project>/state/NEXT.md containing exactly one line:
  Focus: <one sentence, <= 120 chars>
- The active project's Focus line is the single source of truth for global “Current focus”.

## Global NEXT.md (routing only)
- Global 07_system/state/NEXT.md MUST NOT contain executable tasks.
- It must only point to the active project’s state/NEXT.md (and optionally a short note about why it’s active).
- Project tasks live only in 01_projects/<project>/state/NEXT.md.

## project-switch behavior (must be boring)
On switch to 01_projects/<project>:
- Refuse switch if there are uncommitted changes outside:
  - 07_system/state/*
  - 01_projects/*/state/*
- Read Focus: from target project state/NEXT.md
- Update global STATUS.md “Current focus” to match
- Rewrite global NEXT.md pointer to the active project (no accumulation)
- If Focus: is missing or duplicated → exit non-zero with a clear error