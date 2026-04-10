#!/usr/bin/env bash
# Bootstrap a new initiative + L4 spec from templates.
# Usage: ./tools/init.sh INIT-YYYY-NNN-slug [NNN-feature-slug] [--with-gsd]
# Example: ./tools/init.sh INIT-2026-042-user-auth 042-user-auth
# Example: ./tools/init.sh INIT-2026-042-user-auth 042-user-auth --with-gsd
set -euo pipefail

# Separate flags from positional arguments
positional_args=()
WITH_GSD=false
for arg in "$@"; do
  if [[ "$arg" == "--with-gsd" ]]; then
    WITH_GSD=true
  else
    positional_args+=("$arg")
  fi
done

INITIATIVE_ID="${positional_args[0]:-}"
FEATURE_SLUG="${positional_args[1]:-}"

if [[ -z "$INITIATIVE_ID" ]]; then
  echo "Usage: $0 INIT-YYYY-NNN-slug [NNN-feature-slug]"
  echo "Example: $0 INIT-2026-042-user-auth 042-user-auth"
  exit 1
fi

if ! echo "$INITIATIVE_ID" | grep -qE '^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$'; then
  echo "Error: initiative ID must match INIT-YYYY-NNN-slug (e.g., INIT-2026-042-user-auth)"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE_INIT="$REPO_ROOT/initiatives/{INIT-YYYY-NNN-slug}"
TEMPLATE_SPEC="$REPO_ROOT/.specify/specs/{NNN}-{slug}"
TARGET_INIT="$REPO_ROOT/initiatives/$INITIATIVE_ID"

if [[ ! -d "$TEMPLATE_INIT" ]]; then
  echo "Error: template not found at $TEMPLATE_INIT"
  exit 1
fi

if [[ -d "$TARGET_INIT" ]]; then
  echo "Error: $TARGET_INIT already exists"
  exit 1
fi

cp -r "$TEMPLATE_INIT" "$TARGET_INIT"

find "$TARGET_INIT" -type f | while read -r f; do
  sed -i.bak "s|{INIT-YYYY-NNN-slug}|$INITIATIVE_ID|g" "$f"
  sed -i.bak "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" "$f"
  rm -f "${f}.bak"
done

echo "✅ Created initiative: initiatives/$INITIATIVE_ID"

if [[ -n "$FEATURE_SLUG" ]]; then
  if ! echo "$FEATURE_SLUG" | grep -qE '^[0-9]{3}-[a-z0-9-]+$'; then
    echo "Warning: feature slug should match NNN-slug format (e.g., 042-user-auth)"
  fi

  if [[ ! -d "$TEMPLATE_SPEC" ]]; then
    echo "Warning: spec template not found at $TEMPLATE_SPEC, skipping L4 creation"
  else
    TARGET_SPEC="$REPO_ROOT/.specify/specs/$FEATURE_SLUG"
    if [[ -d "$TARGET_SPEC" ]]; then
      echo "Warning: $TARGET_SPEC already exists, skipping"
    else
      cp -r "$TEMPLATE_SPEC" "$TARGET_SPEC"
      find "$TARGET_SPEC" -type f | while read -r f; do
        sed -i.bak "s|{INIT-YYYY-NNN-slug}|$INITIATIVE_ID|g" "$f"
        sed -i.bak "s|{NNN}-{slug}|$FEATURE_SLUG|g" "$f"
        sed -i.bak "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" "$f"
        rm -f "${f}.bak"
      done
      echo "✅ Created L4 spec: .specify/specs/$FEATURE_SLUG"
    fi
  fi
fi

echo ""
echo "Next steps:"
echo "  1. Edit initiatives/$INITIATIVE_ID/requirements.yml (add your REQ-IDs)"
echo "  2. Run: make validate"
if [[ -n "$FEATURE_SLUG" ]]; then
  echo "  3. Open Claude Code and run: /speckit-specify $FEATURE_SLUG"
fi

# GSD integration (optional)
if [[ "$WITH_GSD" == true ]]; then
  echo ""
  echo "==> Installing GSD execution engine..."
  npx get-shit-done-cc@latest --claude --local

  # Create .planning directory
  mkdir -p "$REPO_ROOT/.planning"
  touch "$REPO_ROOT/.planning/.gitkeep"

  # Add .planning patterns to .gitignore
  if [[ ! -f "$REPO_ROOT/.gitignore" ]]; then
    touch "$REPO_ROOT/.gitignore"
  fi

  if ! grep -q '.planning/' "$REPO_ROOT/.gitignore" 2>/dev/null; then
    cat >> "$REPO_ROOT/.gitignore" << 'GITIGNORE'

# GSD planning artifacts (transient session state)
.planning/STATE.md
.planning/codebase/
.planning/phases/*/CONTEXT.md
.planning/todos/
.planning/threads/
.planning/seeds/
.planning/debug/
.planning/intel/
.planning/quick/
.planning/backlog/
.planning/config.json
# Keep SUMMARY.md and PLAN.md — they feed evidence/
!.planning/phases/*/*-SUMMARY.md
!.planning/phases/*/*-PLAN.md
GITIGNORE
  fi

  echo "  Created .planning/ directory"
  echo "  Updated .gitignore for GSD artifacts"
  echo ""
  SLUG_HINT="${FEATURE_SLUG:-<NNN-slug>}"
  echo "GSD commands available:"
  echo "  /speckit-gsd-bridge $SLUG_HINT  — Convert tasks.md to GSD phase plans"
  echo "  /speckit-gsd-verify $SLUG_HINT  — Post-execution verification"
  echo "  /speckit-gsd-map <product>      — Map existing codebase (brownfield)"
fi
