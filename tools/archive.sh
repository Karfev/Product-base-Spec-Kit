#!/usr/bin/env bash
set -euo pipefail
# tools/archive.sh <INIT-ID> [--force] [--skip-graduation]
# Moves completed initiative from initiatives/ to archive/
# Reversible via tools/restore.sh

INIT="${1:?Usage: archive.sh <INIT-ID> [--force] [--skip-graduation]}"
FORCE=""
SKIP_GRAD=""
shift || true
for arg in "$@"; do
  case "$arg" in
    --force) FORCE="true" ;;
    --skip-graduation) SKIP_GRAD="true" ;;
  esac
done

SRC="initiatives/$INIT"
DST="archive/$INIT"

# --- Guards ---
[ ! -d "$SRC" ] && echo "ERROR: $SRC not found" && exit 1
[ -d "$DST" ] && echo "ERROR: $DST already exists in archive" && exit 1

# --- Check lifecycle status ---
STATUS=$(python3 -c "
import yaml
with open('$SRC/requirements.yml') as f:
    d = yaml.safe_load(f)
print(d.get('metadata', {}).get('initiative_status', 'active'))
")
if [ "$STATUS" != "completed" ] && [ "$FORCE" != "true" ]; then
  echo "ERROR: initiative_status is '$STATUS', not 'completed'."
  echo "Set initiative_status: completed first, or use --force"
  exit 1
fi

# --- Graduation pre-check (REQ-GRAD-006) ---
GRADUATED=$(python3 -c "
import yaml
with open('$SRC/requirements.yml') as f:
    d = yaml.safe_load(f)
print(d.get('metadata', {}).get('graduated', False))
")
PROFILE=$(python3 -c "
import yaml
with open('$SRC/requirements.yml') as f:
    d = yaml.safe_load(f)
print(d.get('metadata', {}).get('profile', 'minimal'))
")
if [ "$GRADUATED" != "True" ]; then
  if [ "$PROFILE" = "extended" ] || [ "$PROFILE" = "enterprise" ]; then
    echo "ERROR: Extended/Enterprise profile requires graduation before archive."
    echo "Run: /speckit-graduate $INIT"
    exit 1
  else
    echo "WARNING: Initiative not graduated. Knowledge may be lost."
    echo "Recommended: /speckit-graduate $INIT"
    if [ "$SKIP_GRAD" != "true" ]; then
      echo "Use --skip-graduation to proceed anyway."
      exit 1
    fi
  fi
fi

# --- Set status to archived ---
python3 - <<PYEOF
import yaml
with open('$SRC/requirements.yml') as f:
    d = yaml.safe_load(f)
d['metadata']['initiative_status'] = 'archived'
with open('$SRC/requirements.yml', 'w') as f:
    yaml.dump(d, f, allow_unicode=True, sort_keys=False)
PYEOF

# --- Git tag for easy rollback ---
TAG="archive/$INIT/$(date +%Y-%m-%d)"
git tag "$TAG" 2>/dev/null || echo "WARNING: tag $TAG already exists, skipping"

# --- Move to archive ---
mkdir -p archive
git mv "$SRC" "$DST"

# --- Move linked L4 specs ---
NNN=$(echo "$INIT" | sed 's/INIT-[0-9]*-\([0-9]*\)-.*/\1/')
SLUG=$(echo "$INIT" | sed 's/INIT-[0-9]*-[0-9]*-//')
SPEC_DIR=".specify/specs/${NNN}-${SLUG}"
if [ -d "$SPEC_DIR" ]; then
  mkdir -p "archive/.specify/specs"
  git mv "$SPEC_DIR" "archive/.specify/specs/${NNN}-${SLUG}"
  echo "  Moved L4 specs: $SPEC_DIR → archive/.specify/specs/${NNN}-${SLUG}"
fi

# --- Update INDEX.md ---
INDEX="archive/INDEX.md"
if [ ! -f "$INDEX" ]; then
  cat > "$INDEX" << 'INDEXEOF'
# Archive Index

| Initiative | Title | Owner | Archived | Profile |
|---|---|---|---|---|
INDEXEOF
  git add "$INDEX"
fi

TITLE=$(grep -m1 '^# PRD:' "$DST/prd.md" 2>/dev/null | sed 's/^# PRD: //' || echo "$INIT")
DATE=$(date +%Y-%m-%d)
OWNER=$(python3 -c "
import yaml
with open('$DST/requirements.yml') as f:
    d = yaml.safe_load(f)
print(d.get('metadata', {}).get('owner', 'unknown'))
")
PROF=$(python3 -c "
import yaml
with open('$DST/requirements.yml') as f:
    d = yaml.safe_load(f)
print(d.get('metadata', {}).get('profile', 'unknown'))
")

# Append new entry after header separator row
sed -i '' "/^|---|---|---|---|---|$/a\\
| [$INIT]($INIT/prd.md) | $TITLE | $OWNER | $DATE | $PROF |" "$INDEX"

echo ""
echo "✅ Archived: $INIT → archive/$INIT"
echo "   Tag: $TAG"
echo "   Run: make validate to confirm no regressions"
