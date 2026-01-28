#!/usr/bin/env bash
set -euo pipefail

# Smoke tests must never depend on agent backends
unset RF_AGENT_BACKEND

APP="${1:-}"
if [[ -z "$APP" ]]; then
  echo "ERROR: APP path required" >&2
  exit 2
fi

echo "== RF SMOKE TEST =="

resume load-job --app "$APP" --write-debug
resume select-template --app "$APP" --write
resume emphasis-tags --app "$APP" --write

resume propose-changes --app "$APP" --stub --force
resume materialize-stub --app "$APP" --force

echo "SMOKE OK"
