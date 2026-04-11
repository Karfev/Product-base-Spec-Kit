#!/usr/bin/env bash
# Bootstrap a new initiative + L4 spec from canonical templates.
# Usage: ./tools/init.sh INIT-YYYY-NNN-slug [NNN-feature-slug] [--profile minimal|standard|extended|enterprise] [--product name] [--owner @team] [--with-gsd] [--preset archkom]
# Example: ./tools/init.sh INIT-2026-042-user-auth 042-user-auth --profile enterprise --product platform --owner @platform-team
# Example: ./tools/init.sh INIT-2026-042-user-auth 042-user-auth --with-gsd
set -euo pipefail

INITIATIVE_ID="${1:-}"
FEATURE_SLUG=""
PROFILE="standard"
PRODUCT=""
OWNER=""
WITH_GSD=false
PRESET=""

# Parse remaining arguments
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="${2:-}"
      shift 2
      ;;
    --profile=*)
      PROFILE="${1#--profile=}"
      shift
      ;;
    --product)
      PRODUCT="${2:-}"
      shift 2
      ;;
    --product=*)
      PRODUCT="${1#--product=}"
      shift
      ;;
    --owner)
      OWNER="${2:-}"
      shift 2
      ;;
    --owner=*)
      OWNER="${1#--owner=}"
      shift
      ;;
    --with-gsd)
      WITH_GSD=true
      shift
      ;;
    --preset)
      PRESET="${2:-}"
      shift 2
      ;;
    --preset=*)
      PRESET="${1#--preset=}"
      shift
      ;;
    *)
      if [[ -z "$FEATURE_SLUG" ]]; then
        FEATURE_SLUG="$1"
      fi
      shift
      ;;
  esac
done

VALID_PROFILES="minimal standard extended enterprise"
if ! echo "$VALID_PROFILES" | grep -qw "$PROFILE"; then
  echo "Error: --profile must be one of: $VALID_PROFILES"
  exit 1
fi

if [[ "$PRESET" == "archkom" && "$PROFILE" == "minimal" ]]; then
  echo "Error: --preset archkom requires at least --profile standard (needs design.md and decisions/)"
  exit 1
fi

if [[ -z "$INITIATIVE_ID" ]]; then
  echo "Usage: $0 INIT-YYYY-NNN-slug [NNN-feature-slug] [--profile minimal|standard|extended|enterprise]"
  echo "Example: $0 INIT-2026-042-user-auth 042-user-auth --profile enterprise"
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
  if [[ -n "$PRODUCT" ]]; then
    sed -i.bak "s|{product}|$PRODUCT|g" "$f"
  fi
  if [[ -n "$OWNER" ]]; then
    # Strip leading @ to avoid duplication (templates already have @{team})
    OWNER_BARE="${OWNER#@}"
    sed -i.bak "s|{team}|$OWNER_BARE|g" "$f"
    sed -i.bak "s|{team-or-person}|$OWNER|g" "$f"
  fi
  rm -f "${f}.bak"
done

# Patch profile in requirements.yml (match any value in profile field)
REQ_FILE="$TARGET_INIT/requirements.yml"
if [[ -f "$REQ_FILE" ]]; then
  sed -i.bak 's|profile: ".*"|profile: "'"$PROFILE"'"|' "$REQ_FILE"
  rm -f "${REQ_FILE}.bak"
fi

# Remove placeholder-named files and ensure schemas/ directory exists
rm -f "$TARGET_INIT/contracts/schemas/{entity}.schema.json" 2>/dev/null || true
mkdir -p "$TARGET_INIT/contracts/schemas" 2>/dev/null || true
touch "$TARGET_INIT/contracts/schemas/.gitkeep" 2>/dev/null || true

# Replace placeholder requirements with empty array
if [[ -f "$REQ_FILE" ]]; then
  python3 -c "
import sys, yaml
path = sys.argv[1]
with open(path) as f:
    data = yaml.safe_load(f)
# Clear placeholder requirements (those with {braces} in id)
reqs = data.get('requirements', [])
data['requirements'] = [r for r in reqs if '{' not in r.get('id', '')]
with open(path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
" "$REQ_FILE"
fi

# Profile-based file filtering
EXTENDED_ONLY=("compliance" "ops/threat-model.md"
               "ops/nfr-validation.md" "delivery/migration.md")
ARCHKOM_ONLY=("brd.md" "hld.md")

if [[ "$PROFILE" == "minimal" ]]; then
  # Remove Standard + Extended files
  rm -rf "$TARGET_INIT"/{design.md,trace.md,contracts,decisions}
  rm -rf "$TARGET_INIT"/delivery/rollout.md
  rm -rf "$TARGET_INIT"/ops/{slo.yaml,prr-checklist.md}
  for f in "${EXTENDED_ONLY[@]}"; do rm -rf "$TARGET_INIT/$f"; done
  find "$TARGET_INIT" -type d -empty -delete 2>/dev/null || true
elif [[ "$PROFILE" == "standard" ]]; then
  for f in "${EXTENDED_ONLY[@]}"; do rm -rf "$TARGET_INIT/$f"; done
  find "$TARGET_INIT" -type d -empty -delete 2>/dev/null || true
  # Remove Extended-only sections from PRR checklist
  PRR="$TARGET_INIT/ops/prr-checklist.md"
  if [[ -f "$PRR" ]]; then
    python3 -c "
import re, sys
text = open(sys.argv[1]).read()
# Remove Security & privacy section (Extended-only)
text = re.sub(r'## Security & privacy.*?(?=\n## |\Z)', '', text, flags=re.DOTALL)
# Remove individual Extended-only items marked with (Extended)
text = re.sub(r'^- \[[ x]\].*\(Extended\).*\n?', '', text, flags=re.MULTILINE)
# Remove Security row from summary table (section was removed)
text = re.sub(r'\| Security \|[^\n]*\n', '', text)
open(sys.argv[1], 'w').write(text)
" "$PRR"
  fi
fi

# Remove archkom-only artifacts unless --preset archkom is used
if [[ "$PRESET" != "archkom" ]]; then
  for f in "${ARCHKOM_ONLY[@]}"; do rm -rf "$TARGET_INIT/$f"; done
fi

# Enterprise-specific artifacts
if [[ "$PROFILE" = "enterprise" ]]; then
  mkdir -p "$TARGET_INIT/architecture-views"
  cat > "$TARGET_INIT/architecture-views/README.md" <<MD
# Architecture Views: $INITIATIVE_ID

Папка содержит дополнительные архитектурные представления по методологии АИС.
Основные схемы (Д-1, Д-3, П-1, Т-1) располагаются в \`design.md\`.

| Тип | Файл | Статус |
|-----|------|--------|
| Д-2: Внутреннее взаимодействие деятельности | \`d2-internal-activity.md\` | н/п |
| Д-4а: Процесс деятельности — Контекст | \`d4a-process-context.md\` | н/п |
| Д-4б: Процесс деятельности — Состав | \`d4b-process-composition.md\` | н/п |
| Д-5: Внутренние потоки данных | \`d5-internal-data-flow.md\` | н/п |
| Д-6: Функциональная карта | \`d6-functional-map.md\` | н/п |
| П-2: Внутреннее взаимодействие компонентов | \`p2-internal-components.md\` | н/п |
| О-1: Схема связи слоёв | \`o1-layer-links.md\` | н/п |

> Для генерации заготовок запусти: \`/speckit-architecture $INITIATIVE_ID\`
> Справочник элементов: \`domains/is-ontology/canonical-model/model.md\`
MD

  cat > "$TARGET_INIT/subsystem-classification.yaml" <<YAML
# Классификация подсистемы по онтологии АИС
# Валидация: make validate (при profile=enterprise)
# Схема: tools/schemas/subsystem-classification.schema.json
initiative: "$INITIATIVE_ID"
classification:
  system_scale: "С.М.М"          # С.М.М | С.М.С | С.М.Б
  subsystem_type: "ПС.Т.П"       # ПС.Т.И | ПС.Т.ПТ | ПС.Т.П
  subsystem_owner: "@team"
  activity_domain: "{вид деятельности}"
architecture_views:
  - type: "Д-1"
    status: "в работе"
    path: "design.md#д-1"
  - type: "Д-3"
    status: "в работе"
    path: "design.md#д-3"
  - type: "П-1"
    status: "в работе"
    path: "design.md#п-1"
  - type: "Т-1"
    status: "в работе"
    path: "design.md#т-1"
ontology_ref: "domains/is-ontology/canonical-model/model.md"
YAML

  echo "✅ Created enterprise artifacts: architecture-views/ + subsystem-classification.yaml"
fi

echo "✅ Created initiative: initiatives/$INITIATIVE_ID (profile: $PROFILE)"

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
      # Copy canonical L4 template as-is; substitute placeholders.
      find "$TARGET_SPEC" -type f | while read -r f; do
        sed -i.bak "s|{INIT-YYYY-NNN-slug}|$INITIATIVE_ID|g" "$f"
        sed -i.bak "s|{NNN}-{slug}|$FEATURE_SLUG|g" "$f"
        sed -i.bak "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" "$f"
        if [[ -n "$OWNER" ]]; then
          OWNER_BARE="${OWNER#@}"
          sed -i.bak "s|{engineer-or-team}|$OWNER_BARE|g" "$f"
          sed -i.bak "s|@{owner}|@$OWNER_BARE|g" "$f"
        fi
        rm -f "${f}.bak"
      done
      # Replace profile placeholder using python (contains pipe chars)
      python3 -c "
import sys
path = sys.argv[1]
profile = sys.argv[2]
text = open(path).read()
text = text.replace('{Minimal|Standard|Extended}', profile.capitalize())
open(path, 'w').write(text)
" "$TARGET_SPEC/spec.md" "$PROFILE"
      echo "✅ Created L4 spec: .specify/specs/$FEATURE_SLUG"
    fi
  fi
fi

# Archkom preset (optional)
if [[ "$PRESET" == "archkom" ]]; then
  echo ""
  echo "==> Applying archkom preset..."

  TARGET_INIT="$REPO_ROOT/initiatives/$INITIATIVE_ID"

  # Ensure archkom-only files exist (may have been removed by profile filtering)
  for f in "${ARCHKOM_ONLY[@]}"; do
    if [[ ! -f "$TARGET_INIT/$f" && -f "$TEMPLATE_INIT/$f" ]]; then
      cp "$TEMPLATE_INIT/$f" "$TARGET_INIT/$f"
      sed -i.bak "s|{INIT-YYYY-NNN-slug}|$INITIATIVE_ID|g" "$TARGET_INIT/$f"
      sed -i.bak "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" "$TARGET_INIT/$f"
      if [[ -n "$PRODUCT" ]]; then
        sed -i.bak "s|{product}|$PRODUCT|g" "$TARGET_INIT/$f"
      fi
      if [[ -n "$OWNER" ]]; then
        OWNER_BARE="${OWNER#@}"
        sed -i.bak "s|{team}|$OWNER_BARE|g" "$TARGET_INIT/$f"
        sed -i.bak "s|{team-or-person}|$OWNER|g" "$TARGET_INIT/$f"
      fi
      rm -f "${TARGET_INIT}/${f}.bak"
    fi
  done

  for f in "$TARGET_INIT/prd.md" "$TARGET_INIT/decisions/ADR-template.md"; do
    if [[ -f "$f" ]]; then
      sed -i.bak '/<!-- optional: archkom/d; /<!-- ## /{s/<!-- //;s/ -->//;}; /^-->$/d' "$f"
      rm -f "${f}.bak"
    fi
  done

  if [[ -f "$TARGET_INIT/hld.md" ]]; then
    sed -i.bak '/<!-- archkom:/d; /<!-- ## /{s/<!-- //;s/ -->//;}; /<!-- |/d; /^-->$/d' "$TARGET_INIT/hld.md"
    rm -f "${TARGET_INIT}/hld.md.bak"
  fi

  echo "  Archkom sections enabled in prd.md, hld.md, ADR-template.md"
  echo ""
  echo "Archkom artifact chain:"
  echo "  brd.md → prd.md → hld.md → decisions/АТР → design.md"
fi

echo ""
echo "Next steps:"
echo "  1. Edit initiatives/$INITIATIVE_ID/requirements.yml (add your REQ-IDs)"
echo "  2. Run: make validate"
if [[ "$PROFILE" = "enterprise" ]]; then
  echo "  3. Fill subsystem-classification.yaml (owner, activity_domain)"
  echo "  4. Run: /speckit-architecture $INITIATIVE_ID  (generates design.md layers + Mermaid stubs)"
  if [[ -n "$FEATURE_SLUG" ]]; then
    echo "  5. Open Claude Code and run: /speckit-specify $FEATURE_SLUG"
  fi
elif [[ -n "$FEATURE_SLUG" ]]; then
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
