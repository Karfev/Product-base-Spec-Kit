#!/usr/bin/env bash
# Upgrade an initiative to a higher profile.
# Usage: ./tools/upgrade.sh INIT-YYYY-NNN-slug --profile standard|extended|enterprise [--force] [--preset archkom]
# Example: ./tools/upgrade.sh INIT-2026-042-user-auth --profile standard
# Example: ./tools/upgrade.sh INIT-2026-042-user-auth --profile extended --preset archkom
set -euo pipefail

INITIATIVE_ID="${1:-}"
TARGET_PROFILE=""
FORCE=false
PRESET=""

# Parse arguments
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --profile)
      TARGET_PROFILE="${2:-}"
      shift 2
      ;;
    --profile=*)
      TARGET_PROFILE="${1#--profile=}"
      shift
      ;;
    --force)
      FORCE=true
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
      shift
      ;;
  esac
done

VALID_PROFILES="minimal standard extended enterprise"
if ! echo "$VALID_PROFILES" | grep -qw "$TARGET_PROFILE"; then
  echo "Error: --profile must be one of: $VALID_PROFILES"
  exit 1
fi

if [[ -z "$INITIATIVE_ID" ]]; then
  echo "Usage: $0 INIT-YYYY-NNN-slug --profile standard|extended|enterprise [--force] [--preset archkom]"
  echo "Example: $0 INIT-2026-042-user-auth --profile standard"
  exit 1
fi

if ! echo "$INITIATIVE_ID" | grep -qE '^INIT-[0-9]{4}-[0-9]{3}-[a-z0-9-]+$'; then
  echo "Error: initiative ID must match INIT-YYYY-NNN-slug (e.g., INIT-2026-042-user-auth)"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_INIT="$REPO_ROOT/initiatives/$INITIATIVE_ID"
TEMPLATE_INIT="$REPO_ROOT/initiatives/{INIT-YYYY-NNN-slug}"
REQ_FILE="$TARGET_INIT/requirements.yml"

if [[ ! -d "$TARGET_INIT" ]]; then
  echo "Error: initiative not found at $TARGET_INIT"
  exit 1
fi

if [[ ! -f "$REQ_FILE" ]]; then
  echo "Error: requirements.yml not found at $REQ_FILE"
  exit 1
fi

# Profile ranking
profile_rank() {
  case "$1" in
    minimal)    echo 0 ;;
    standard)   echo 1 ;;
    extended)   echo 2 ;;
    enterprise) echo 3 ;;
    *)          echo -1 ;;
  esac
}

# Read current profile from requirements.yml
CURRENT_PROFILE=$(python3 -c "
import yaml, sys
with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)
print(data.get('metadata', {}).get('profile', 'unknown'))
" "$REQ_FILE")

CURRENT_RANK=$(profile_rank "$CURRENT_PROFILE")
TARGET_RANK=$(profile_rank "$TARGET_PROFILE")

if [[ "$CURRENT_RANK" -eq "$TARGET_RANK" ]]; then
  echo "Initiative $INITIATIVE_ID is already at profile '$CURRENT_PROFILE'. Nothing to do."
  exit 0
fi

if [[ "$TARGET_RANK" -lt "$CURRENT_RANK" ]]; then
  if [[ "$FORCE" == true ]]; then
    echo "Warning: downgrading from $CURRENT_PROFILE to $TARGET_PROFILE (--force). Files will NOT be removed."
  else
    echo "Error: cannot downgrade from $CURRENT_PROFILE to $TARGET_PROFILE."
    echo "Downgrade requires --force flag and Tech Lead sign-off."
    echo "Note: --force will update the profile metadata but will NOT remove existing files."
    exit 1
  fi
fi

if [[ "$PRESET" == "archkom" && "$TARGET_PROFILE" == "minimal" ]]; then
  echo "Error: --preset archkom requires at least --profile standard (needs design.md and decisions/)"
  exit 1
fi

# Read metadata for placeholder substitution
PRODUCT=$(python3 -c "
import yaml, sys
with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)
print(data.get('metadata', {}).get('product', ''))
" "$REQ_FILE")

OWNER=$(python3 -c "
import yaml, sys
with open(sys.argv[1]) as f:
    data = yaml.safe_load(f)
print(data.get('metadata', {}).get('owner', ''))
" "$REQ_FILE")
OWNER_BARE="${OWNER#@}"

echo "Upgrading $INITIATIVE_ID: $CURRENT_PROFILE → $TARGET_PROFILE"

# Create backup
BACKUP_DIR="$TARGET_INIT/.backup/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
# Copy all files except .backup itself
find "$TARGET_INIT" -maxdepth 1 -not -name '.backup' -not -path "$TARGET_INIT" -exec cp -r {} "$BACKUP_DIR/" \;
echo "  Backup created: .backup/$(basename "$BACKUP_DIR")"

# Add .backup/ to initiative .gitignore if needed
INIT_GITIGNORE="$TARGET_INIT/.gitignore"
if [[ ! -f "$INIT_GITIGNORE" ]] || ! grep -q '.backup/' "$INIT_GITIGNORE" 2>/dev/null; then
  echo ".backup/" >> "$INIT_GITIGNORE"
fi

# Define artifact matrix per profile level
# Each level adds files on top of the previous
STANDARD_ADDS=(
  "design.md"
  "trace.md"
  "contracts/openapi.yaml"
  "contracts/asyncapi.yaml"
  "contracts/README.md"
  "contracts/schemas/.gitkeep"
  "decisions/ADR-template.md"
  "decisions/README.md"
  "delivery/rollout.md"
  "ops/slo.yaml"
  "ops/prr-checklist.md"
)

EXTENDED_ADDS=(
  "compliance/regulatory-review.md"
  "ops/threat-model.md"
  "ops/nfr-validation.md"
  "delivery/migration.md"
)

ARCHKOM_ADDS=("brd.md" "hld.md")

# Collect files to add based on upgrade path
FILES_TO_ADD=()

if [[ "$CURRENT_RANK" -lt 1 && "$TARGET_RANK" -ge 1 ]]; then
  FILES_TO_ADD+=("${STANDARD_ADDS[@]}")
fi

if [[ "$CURRENT_RANK" -lt 2 && "$TARGET_RANK" -ge 2 ]]; then
  FILES_TO_ADD+=("${EXTENDED_ADDS[@]}")
fi

# Function to copy a template file with placeholder substitution
copy_template_file() {
  local rel_path="$1"
  local target_file="$TARGET_INIT/$rel_path"
  local template_file="$TEMPLATE_INIT/$rel_path"

  # Never overwrite existing files
  if [[ -f "$target_file" ]]; then
    return
  fi

  # Handle .gitkeep separately
  if [[ "$(basename "$rel_path")" == ".gitkeep" ]]; then
    mkdir -p "$(dirname "$target_file")"
    touch "$target_file"
    return
  fi

  if [[ ! -f "$template_file" ]]; then
    echo "  Warning: template file not found: $rel_path (skipping)"
    return
  fi

  mkdir -p "$(dirname "$target_file")"
  cp "$template_file" "$target_file"

  # Placeholder substitution
  sed -i.bak "s|{INIT-YYYY-NNN-slug}|$INITIATIVE_ID|g" "$target_file"
  sed -i.bak "s|{YYYY-MM-DD}|$(date +%Y-%m-%d)|g" "$target_file"
  if [[ -n "$PRODUCT" ]]; then
    sed -i.bak "s|{product}|$PRODUCT|g" "$target_file"
  fi
  if [[ -n "$OWNER_BARE" ]]; then
    sed -i.bak "s|{team}|$OWNER_BARE|g" "$target_file"
    sed -i.bak "s|{team-or-person}|$OWNER|g" "$target_file"
  fi
  rm -f "${target_file}.bak"
}

# Copy missing files
ADDED_COUNT=0
for f in "${FILES_TO_ADD[@]}"; do
  if [[ ! -f "$TARGET_INIT/$f" ]]; then
    copy_template_file "$f"
    ADDED_COUNT=$((ADDED_COUNT + 1))
    echo "  + $f"
  fi
done

# Standard profile: filter PRR checklist (remove Extended-only sections)
if [[ "$TARGET_PROFILE" == "standard" ]]; then
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
    echo "  PRR checklist filtered for Standard profile"
  fi
fi

# Enterprise-specific artifacts
if [[ "$CURRENT_RANK" -lt 3 && "$TARGET_RANK" -ge 3 ]]; then
  if [[ ! -d "$TARGET_INIT/architecture-views" ]]; then
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
    ADDED_COUNT=$((ADDED_COUNT + 1))
    echo "  + architecture-views/README.md"
  fi

  if [[ ! -f "$TARGET_INIT/subsystem-classification.yaml" ]]; then
    cat > "$TARGET_INIT/subsystem-classification.yaml" <<YAML
# Классификация подсистемы по онтологии АИС
# Валидация: make validate (при profile=enterprise)
# Схема: tools/schemas/subsystem-classification.schema.json
initiative: "$INITIATIVE_ID"
classification:
  system_scale: "С.М.М"          # С.М.М | С.М.С | С.М.Б
  subsystem_type: "ПС.Т.П"       # ПС.Т.И | ПС.Т.ПТ | ПС.Т.П
  subsystem_owner: "$OWNER"
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
    ADDED_COUNT=$((ADDED_COUNT + 1))
    echo "  + subsystem-classification.yaml"
  fi
fi

# Archkom preset (optional)
if [[ "$PRESET" == "archkom" ]]; then
  echo ""
  echo "  ==> Applying archkom preset..."

  for f in "${ARCHKOM_ADDS[@]}"; do
    copy_template_file "$f"
    if [[ -f "$TARGET_INIT/$f" ]]; then
      echo "  + $f (archkom)"
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
fi

# Remove placeholder-named files that may have been copied
rm -f "$TARGET_INIT/contracts/schemas/{entity}.schema.json" 2>/dev/null || true
mkdir -p "$TARGET_INIT/contracts/schemas" 2>/dev/null || true
touch "$TARGET_INIT/contracts/schemas/.gitkeep" 2>/dev/null || true

# Replace placeholder requirements with empty array in new requirements
# (only for files that were just copied from template)
for yml_file in "$TARGET_INIT/contracts/openapi.yaml" "$TARGET_INIT/contracts/asyncapi.yaml"; do
  if [[ -f "$yml_file" ]]; then
    # No-op: contract files don't need requirements cleanup
    true
  fi
done

# Update metadata.profile via sed (preserves formatting)
sed -i.bak "s|profile: \"$CURRENT_PROFILE\"|profile: \"$TARGET_PROFILE\"|" "$REQ_FILE"
# Handle unquoted profile values too
sed -i.bak "s|profile: '$CURRENT_PROFILE'|profile: '$TARGET_PROFILE'|" "$REQ_FILE"
sed -i.bak "s|profile: $CURRENT_PROFILE$|profile: \"$TARGET_PROFILE\"|" "$REQ_FILE"
# Update last_updated
sed -i.bak "s|last_updated: ['\"].*['\"]|last_updated: \"$(date +%Y-%m-%d)\"|" "$REQ_FILE"
rm -f "${REQ_FILE}.bak"

echo ""
echo "✅ Upgraded $INITIATIVE_ID: $CURRENT_PROFILE → $TARGET_PROFILE ($ADDED_COUNT files added)"
echo ""
echo "Next steps:"
echo "  1. Review new stub files and fill placeholders"
echo "  2. Run: make validate"
if [[ "$TARGET_PROFILE" == "enterprise" ]]; then
  echo "  3. Fill subsystem-classification.yaml"
  echo "  4. Run: /speckit-architecture $INITIATIVE_ID"
fi
if [[ "$PRESET" == "archkom" ]]; then
  echo "  Archkom artifact chain: brd.md → prd.md → hld.md → decisions/ADR → design.md"
fi
