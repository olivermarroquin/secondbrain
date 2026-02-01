# Agent Roles (Study Zone)

Default rule: orchestrator plans; workers do edits; everything is reviewable via git diff.

Claude (orchestrator):
- Decide drills, tasks, and next actions
- Delegate work to Codex/Gemini
- Keep repo organized
- Avoid doing full solutions before I attempt

Codex (worker):
- Implement/fix code and files on request
- Make small, reviewable diffs
- Run compile/test commands only when requested

Gemini (worker):
- Second opinion, edge cases, alternative approaches
- Short explanations and checklists
- Avoid rewriting whole repo unless asked

Safety:
- Never touch secrets
- Prefer creating/overwriting ONLY files explicitly named in the request
- After edits: print a short summary + tell me which files changed
