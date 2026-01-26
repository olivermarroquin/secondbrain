#!/usr/bin/env bash
set -euo pipefail

APP="${1:-}"
if [[ -z "$APP" ]]; then
  echo "usage: rf_smoke_test.sh /path/to/APP" >&2
  exit 2
fi

resume load-job --app "$APP" --write-debug >/dev/null
resume select-template --app "$APP" --write >/dev/null
resume emphasis-tags --app "$APP" --write >/dev/null
resume propose-changes --app "$APP" --force >/dev/null

# approve a mix: section ADDs + subsection ADD (adjust numbers if your proposer changes later)
resume apply-approvals --app "$APP" --approve "2,3,4,5" --force >/dev/null
resume build-docx --app "$APP" --force >/dev/null

echo "SMOKE OK: $APP"
