#!/usr/bin/env bash
set -euo pipefail
# tools/restore.sh <INIT-ID>
# Restores archived initiative from archive/ to initiatives/
# Reverse of tools/archive.sh

INIT="${1:?Usage: restore.sh <INIT-ID>}"
SRC="archive/$INIT"
DST="initiatives/$INIT"

# --- Guards ---
[ ! -d "$SRC" ] && echo "ERROR: $SRC not found in archive" && exit 1
[ -d "$DST" ] && echo "ERROR: $DST already exists — cannot overwrite" && exit 1

# --- Restore L4 specs first ---
NNN=$(echo "$INIT" | sed 's/INIT-[0-9]*-\([0-9]*\)-.*/\1/')
SLUG=$(echo "$INIT" | sed 's/INIT-[0-9]*-[0-9]*-//')
ARCHIVED_SPEC="archive/.specify/specs/${NNN}-${SLUG}"
if [ -d "$ARCHIVED_SPEC" ]; then
  git mv "$ARCHIVED_SPEC" ".specify/specs/${NNN}-${SLUG}"
  echo "  Restored L4 specs: .specify/specs/${NNN}-${SLUG}"
fi

# --- Move back to initiatives ---
git mv "$SRC" "$DST"

# --- Set status to active ---
python3 - <<PYEOF
import yaml
with open('$DST/requirements.yml') as f:
    d = yaml.safe_load(f)
d['metadata']['initiative_status'] = 'active'
with open('$DST/requirements.yml', 'w') as f:
    yaml.dump(d, f, allow_unicode=True, sort_keys=False)
PYEOF

# --- Remove from INDEX.md ---
INDEX="archive/INDEX.md"
if [ -f "$INDEX" ]; then
  sed -i '' "/\[$INIT\]/d" "$INDEX"
fi

echo ""
echo "✅ Restored: archive/$INIT → initiatives/$INIT"
echo "   Run: make validate to confirm"
