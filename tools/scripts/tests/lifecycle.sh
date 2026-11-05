#!/usr/bin/env bash
# Run the whole initiative lifecycle on a temporary copy of the repository:
# init -> requirements -> graduate -> archive -> restore -> second initiative with
# delta: modified -> graduate -> third initiative with a stale base_rev is refused.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

(cd "$REPO_ROOT" && git ls-files -co --exclude-standard -z | tar --null -T - -cf -) | tar -xf - -C "$WORK"
cd "$WORK"
git init -q
git config user.name "lifecycle test"
git config user.email "lifecycle@example.invalid"
git add -A
git commit -q -m "base"

FIRST="INIT-2099-001-lifecycle-first"
SECOND="INIT-2099-002-lifecycle-second"
THIRD="INIT-2099-003-lifecycle-third"
REQ="REQ-LIFECYCLE-001"
REGISTRY="products/platform/requirements-registry.yml"

fail() {
  echo "FAILED: $1" >&2
  exit 1
}

add_requirement() {
  # add_requirement <initiative> <description> [yaml fields of the delta]
  python3 - "$1" "$2" "$REQ" "${3:-}" <<'PY'
import sys
from pathlib import Path
import yaml

initiative, description, req_id, extra = sys.argv[1:]
path = Path('initiatives') / initiative / 'requirements.yml'
data = yaml.safe_load(path.read_text())
requirement = {
    'id': req_id,
    'title': 'Lifecycle requirement',
    'type': 'functional',
    'priority': 'P1',
    'status': 'implemented',
    'description': description,
    'acceptance_criteria': ['Given a user When they act Then it works'],
    'trace': {'tests': [f'ext:other/test.ts::{req_id}']},
}
requirement.update(yaml.safe_load(extra) or {})
data['requirements'] = [requirement]
path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
PY
  printf '\n| %s | %s |\n' "$REQ" "$1" >> "initiatives/$1/trace.md"
}

registry_field() {
  python3 - "$REGISTRY" "$REQ" "$1" <<'PY'
import sys
import yaml

path, req_id, expression = sys.argv[1:]
entry = next(item for item in yaml.safe_load(open(path))['entries'] if item['id'] == req_id)
print(eval(expression, {'entry': entry}))
PY
}

expect_field() {
  actual="$(registry_field "$1")"
  [ "$actual" = "$2" ] || fail "$1: expected '$2', got '$actual'"
}

new_initiative() {
  bash tools/init.sh "$1" --profile standard --product platform --owner @platform-team > /dev/null
}

echo "==> First initiative: init, requirements, ADR, graduate"
new_initiative "$FIRST"
add_requirement "$FIRST" "First version of the lifecycle requirement"
cat > "initiatives/$FIRST/decisions/$FIRST-ADR-0001-choice.md" <<ADR
---
status: "accepted"
---

# $FIRST-ADR-0001: A lifecycle decision

Body.
ADR
python3 tools/scripts/check-deltas.py
python3 tools/scripts/graduate.py "$FIRST" --dry-run > /dev/null
git diff --quiet -- "$REGISTRY" || fail "dry run changed the registry"
python3 tools/scripts/graduate.py "$FIRST"
expect_field "entry['rev']" 1
expect_field "len(entry['history'])" 1
ADR_COPY="$(grep -l "original_id: \"$FIRST-ADR-0001-choice\"" products/platform/decisions/*.md)"
grep -q "^# PLAT-[0-9]*: A lifecycle decision$" "$ADR_COPY" || fail "ADR heading not renamed"
grep -q "$FIRST" products/platform/knowledge-log.md || fail "knowledge log not updated"

echo "==> Archive and restore"
python3 - "initiatives/$FIRST/requirements.yml" <<'PY'
import sys
from pathlib import Path
import yaml

path = Path(sys.argv[1])
data = yaml.safe_load(path.read_text())
data['metadata']['initiative_status'] = 'completed'
path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
PY
git add -A
git commit -q -m "first initiative graduated"
bash tools/archive.sh "$FIRST" > /dev/null
[ -d "archive/$FIRST" ] || fail "initiative not archived"
grep -q "$FIRST" archive/INDEX.md || fail "archive index not updated"
ls archive/INDEX.md.bak 2> /dev/null && fail "backup file left by sed"
git add -A
git commit -q -m "archive first initiative"
bash tools/restore.sh "$FIRST" > /dev/null
[ -d "initiatives/$FIRST" ] || fail "initiative not restored"
grep -q "$FIRST" archive/INDEX.md && fail "archive index still names the restored initiative"
git add -A
git commit -q -m "restore first initiative"

echo "==> Running graduate again changes nothing"
python3 tools/scripts/graduate.py "$FIRST" --force > /dev/null
git diff --quiet || fail "repeated graduation changed files"

echo "==> Second initiative: delta modified"
new_initiative "$SECOND"
add_requirement "$SECOND" "Second version of the lifecycle requirement" "{delta: modified, base_rev: 1}"
python3 tools/scripts/check-deltas.py
python3 tools/scripts/graduate.py "$SECOND"
expect_field "entry['rev']" 2
expect_field "entry['description']" "Second version of the lifecycle requirement"
expect_field "[item['initiative'] for item in entry['history']]" "['$FIRST', '$SECOND']"

echo "==> Everything validates"
python3 -m check_jsonschema --schemafile tools/schemas/requirements-registry.schema.json "$REGISTRY" 2> /dev/null
python3 -m yamllint -c .yamllint.yml "$REGISTRY"
for initiative in "$FIRST" "$SECOND"; do
  python3 -m check_jsonschema --schemafile tools/schemas/requirements.schema.json "initiatives/$initiative/requirements.yml" 2> /dev/null
done
python3 tools/scripts/check-trace.py
python3 tools/scripts/check-deltas.py

echo "==> Third initiative: stale base_rev is refused"
git add -A
git commit -q -m "second initiative graduated"
new_initiative "$THIRD"
add_requirement "$THIRD" "Third version that missed the second" "{delta: modified, base_rev: 1}"
python3 tools/scripts/check-deltas.py > /dev/null && fail "check-deltas accepted a stale base_rev"
python3 tools/scripts/graduate.py "$THIRD" > /dev/null && fail "graduate accepted a stale base_rev"
git diff --quiet -- "$REGISTRY" || fail "refused graduation changed the registry"

echo "==> Schema requires base_rev for delta modified"
add_requirement "$THIRD" "Delta without a base revision" "{delta: modified}"
python3 -m check_jsonschema --schemafile tools/schemas/requirements.schema.json "initiatives/$THIRD/requirements.yml" > /dev/null 2>&1 \
  && fail "schema accepted delta: modified without base_rev"

echo "✅ lifecycle: passed"
