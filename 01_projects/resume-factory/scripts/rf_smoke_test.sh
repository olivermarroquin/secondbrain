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
RR="${RR_OCCURRENCE:-1}"
resume propose-changes --app "$APP" --rr-occurrence "$RR" --force >/dev/null

# approvals: default approve SAFE proposals (ADD + REPLACE_SECTION); optionally set APPROVE="1,3"
APPROVE_LIST="${APPROVE:-}"
PROP="$APP/resume_refs/resume_pipeline/proposed-changes.md"

# collect proposal numbers that exist and are safe
SAFE_NUMS=$(awk '
  /^[0-9]+\)$/ {gsub("\)", "", $1); n=$1}
  /^CHANGE: / {ch=$2}
  /^$/ { if (n != "" && (ch=="ADD" || ch=="REPLACE_SECTION")) print n; n=""; ch=""; }
' "$PROP" | paste -sd, -)

if [[ -n "$APPROVE_LIST" ]]; then
  # filter requested approvals to those that exist
  EXISTING=$(awk '/^[0-9]+\)$/ {gsub("\)", "", $1); print $1}' "$PROP" | sort -n | paste -sd, -)
  FILTERED=""
  IFS=, read -r -a req <<<"$APPROVE_LIST"
  for x in "${req[@]}"; do
    [[ ",$EXISTING," == *",$x,"* ]] && FILTERED+="${FILTERED:+,}$x"
  done
  [[ -z "$FILTERED" ]] && { echo "ERROR: none of APPROVE are in proposals. Existing: [$EXISTING]" >&2; exit 2; }
  APPROVE_FINAL="$FILTERED"
else
  [[ -z "$SAFE_NUMS" ]] && { echo "ERROR: no safe proposals found to approve" >&2; exit 2; }
  APPROVE_FINAL="$SAFE_NUMS"
fi

resume apply-approvals --app "$APP" --approve "$APPROVE_FINAL" --force >/dev/null
MAT="${MATERIALIZER:-stub}"
if [[ "$MAT" == "ai" ]]; then
  resume materialize-approved-ai --app "$APP" --force >/dev/null
else
  resume materialize-stub --app "$APP" --force >/dev/null
fi
resume build-docx --app "$APP" --force >/dev/null

echo "SMOKE OK: $APP"
