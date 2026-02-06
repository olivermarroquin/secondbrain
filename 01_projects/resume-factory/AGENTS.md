## PRE-FLIGHT (REQUIRED FOR ALL AI ASSISTANCE)

Before performing any task in this repository, you will be provided the output of:

rf-context --full

Treat that output as the ONLY authoritative context for:
- current system truth (CURRENT.md)
- latest checkpoint pointers (LATEST.md)
- operating rules (CONTEXT.md)

Rules:
- Do not assume information outside of the rf-context output.
- If your assumptions conflict with rf-context, defer to rf-context.
- Do not promote backlog items into CURRENT.md or checkpoints unless explicitly instructed.
- If required context is missing or unclear, stop and ask before proceeding.
This file defines roles and how they collaborate (critic, implementer, tester). It keeps your “multi-model” setup from becoming chaos.


## Agent Roles & Collaboration Model

This file defines agent roles and collaboration boundaries to prevent chaos in multi-model workflows.

Standard roles:
- Implementer: makes code or file changes exactly as requested.
- Critic: reviews proposals for correctness, scope creep, and unintended side effects.
- Tester: verifies behavior against expected outcomes and reports failures.

Rules:
- One agent acts in one role at a time.
- Critics do not implement.
- Implementers do not self-approve.
- Testers report results; they do not redesign.

Model usage:
- Claude is preferred for system reasoning, refactors, and synthesis.
- OpenAI models are preferred for structured transformations and diff-based edits.
- Gemini may be used for cross-checking or alternative perspectives.

If role boundaries conflict or are unclear, stop and ask before proceeding.

