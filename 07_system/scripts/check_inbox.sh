#!/usr/bin/env bash

INBOX="$HOME/secondbrain/00_inbox"
DAYS=7

echo "=== Inbox Hygiene Check ==="
echo "Inbox: $INBOX"
echo "Threshold: files older than $DAYS days"
echo "Run date: $(date)"
echo

if [ ! -d "$INBOX" ]; then
  echo "ERROR: Inbox directory not found."
  exit 1
fi

FOUND=0

# Find files older than N days
while IFS= read -r -d '' file; do
  FOUND=1

  # File age in days
  mod_time=$(stat -f "%Sm" -t "%Y-%m-%d" "$file")
  size=$(du -h "$file" | cut -f1)

  echo "⚠️  STALE FILE"
  echo "Path : ${file#$HOME/}"
  echo "Date : $mod_time"
  echo "Size : $size"
  echo
done < <(find "$INBOX" -type f -mtime +"$DAYS" -print0)

if [ "$FOUND" -eq 0 ]; then
  echo "✅ Inbox is clean. No files older than $DAYS days."
fi
