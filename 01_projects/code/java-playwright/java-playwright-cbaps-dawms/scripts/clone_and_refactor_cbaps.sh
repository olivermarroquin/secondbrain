#!/usr/bin/env bash
set -euo pipefail

ROOT="$HOME/secondbrain/01_projects/code/java-playwright/java-playwright-cbaps-dawms"
DEST="$ROOT/src/CBAPS_DAWMS"
OUT="$DEST/.ai_refactor"

# Change this to your actual command if different (e.g. "claude", "claude-code", etc.)
CLAUDE_CMD="claude"

mkdir -p "$OUT"

[[ -d "$DEST" ]] || { echo "Missing DEST: $DEST"; exit 1; }
[[ -f "$DEST/README.md" ]] || { echo "Missing README: $DEST/README.md"; exit 1; }

# Build deterministic file list for Claude (code + config only)
(
  cd "$DEST"
  find . -type f \
    \( -name "*.java" -o -name "pom.xml" -o -name "*.xml" -o -name "*.properties" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" -o -name "*.md" \) \
    ! -path "./target/*" \
    ! -path "./test-output/*" \
    ! -path "./.ai_refactor/*" \
  | LC_ALL=C sort
) > "$OUT/files.txt"

cat > "$OUT/prompt.md" <<'EOF'
You are refactoring a Java + Playwright + TestNG Page Object Model automation project.

AUTHORITATIVE SPEC:
- Follow: src/CBAPS_DAWMS/README.md

GOAL:
- Refactor the copied baseline code in src/CBAPS_DAWMS to be CBAPS/DAWMS specific.
- Preserve framework architecture (Base, PlaywrightManager wrapper, POM structure, reporting approach).
- Rename packages/classes/page objects/tests away from demo/training names (e.g., thegreatcourses, week1-week5) into CBAPS/DAWMS domain.

OUTPUT FORMAT (NON-NEGOTIABLE):
- Output ONLY a unified diff patch (git-style). No commentary.

RULES:
- Keep changes minimal and consistent.
- Ensure filenames match public class names.
- Keep imports valid.
- Do NOT touch generated folders (target/, test-output/).
EOF

{
  echo ""
  echo "==================== README (AUTHORITATIVE) ===================="
  cat "$DEST/README.md"
  echo ""
  echo "==================== FILE LIST ===================="
  cat "$OUT/files.txt"
} >> "$OUT/prompt.md"

echo "Prompt: $OUT/prompt.md"
echo "Running Claude command: $CLAUDE_CMD"

cat "$OUT/prompt.md" | $CLAUDE_CMD -p --output-format text | tee "$OUT/changes.patch" >/dev/null

echo "Patch: $OUT/changes.patch"
echo "Checking patch applies cleanly..."
cd "$ROOT"
git apply --check "$OUT/changes.patch"

echo "Applying patch..."
git apply "$OUT/changes.patch"

echo "Done. Review changes with:"
echo "  cd \"$ROOT\" && git diff"

