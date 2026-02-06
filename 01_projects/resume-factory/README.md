# AI-in-CLI Context & Checkpoints Setup

This document defines how system truth, change history, logs, and future ideas are structured and consumed by AI tools operating in the CLI.

## Operator Helpers (07_system/bin)
- rf-context: print resume-factory context in the correct read order
- rf-checkpoint: create/update CURRENT + checkpoint + LATEST bundle after a run
- rf-idea: append an idea to backlog/resume-factory/ideas.md with timestamp


Goal

Make AI tools running in your CLI:

load only what matters now

avoid re-reading massive history

stay aligned with the current truth

scale cleanly as the system evolves

This re-organization separates truth, change, and history into distinct artifacts.

1️⃣ Canonical State File (Always Small, Always True)
File
07_system/checkpoints/resume-factory/CURRENT.md

Purpose

This file answers one question only:

“If I start work right now, what is true?”

Rules

~200–400 lines max (shorter is better)

Overwritten when reality changes

No history

No rationale debates

No obsolete paths or experiments

Contents

What CLI commands exist and work

What pipelines are valid end-to-end

What rules are locked

What is currently broken (if anything)

What is explicitly out of scope

How AI uses it

Read first

Treat as authoritative

Never contradict it unless explicitly instructed

2️⃣ Incremental Checkpoints (Diffs Only)
Location
07_system/checkpoints/resume-factory/

Naming
YYYY-MM-DD_checkpoint.md

Purpose

Record what changed since the last checkpoint, nothing more.

Rules

Short

Additive

No restating unchanged facts

No deep logs

Reference CURRENT.md as the baseline

Contents

What changed

What was added

What broke

What decisions were made or reversed

What is next

How AI uses them

Optional read

Used only to understand recent evolution

3️⃣ Deep Logs (Archive Only)
Location
07_system/checkpoints/resume-factory/logs/

Purpose

Preserve full execution history without polluting working context.

Examples

Full batch run outputs

Long reasoning chains

Tool evaluations

Debug transcripts

Rules

Never read by default

Never summarized inline

Never copied forward

Only opened when debugging

4️⃣ Deterministic Pointer File (Prevents Guessing)
File
07_system/checkpoints/resume-factory/LATEST.md

Purpose

Tell humans and AI what to read first.

Contents

Points to CURRENT.md

Points to the latest incremental checkpoint

Points to the latest relevant log (if any)

Why this matters

No ambiguity

No “which file do I read?”

Safe for automation and agents

5️⃣ Project-Local Context Pointer
File
01_projects/resume-factory/CONTEXT.md

Purpose

Bridge the project codebase to the checkpoint system.

Contents

Relative path to LATEST.md

Local execution rules

Change discipline (small steps, verify, commit)

How AI uses it

Read when operating inside /resume-factory/

Redirects to canonical system context

6️⃣ Mental Model (The Rule That Prevents Bloat)

If a fact is true now → CURRENT.md
If a fact changed → checkpoint
If it’s detail/history → logs

No exceptions.
