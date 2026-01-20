# Naming Conventions (LOCKED)

## Allowed characters
- Allowed: a-z 0-9 _ - .
- Forbidden: spaces, emojis, parentheses, commas, &,#, ?, !

## Folder naming
- snake_case only
- no spaces ever

## File naming
- kebab-case only
- Exceptions:
  - README.md
  - CLAUDE.md, GEMINI.md, AGENTS.md, DECISIONS.md
  - .gitignore, .env.example

## Dates
- YYYY-MM-DD

## Versions
- v001, v002, v003... (zero-padded)
- Reserved: draft, final, dead
- Never use"final-final-2"

## AI provenance
Preferred: directory-based separation via 05_outputs/
Suffix-based only when necessary:
- -ai
- -human
