#!/usr/bin/env bash
# Update the framework files of a repository from a tagged kit version.
# The paths come from tools/kit-paths.txt of that version. The result stays uncommitted:
# local changes to framework files show up in the diff, and nothing else is touched.
# Paths listed in .kit-exclude in the repository root are skipped, a directory covers everything inside it.
# Usage: tools/kit-update.sh <remote-or-path> <tag>
# Example: tools/kit-update.sh upstream kit-v1.1.0
# Example: tools/kit-update.sh /mnt/mirror/Product-base-Spec-Kit kit-v1.1.0
# First update of a repository without this script:
#   git fetch --no-tags <remote-or-path> refs/tags/<tag>
#   git show FETCH_HEAD:tools/kit-update.sh | bash -s -- <remote-or-path> <tag>
set -euo pipefail

SOURCE="${1:-}"
TAG="${2:-}"

if [[ -z "$SOURCE" || -z "$TAG" ]]; then
  echo "Usage: tools/kit-update.sh <remote-or-path> <tag>"
  exit 1
fi

cd "$(git rev-parse --show-toplevel)"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "Error: working tree is not clean. Commit or stash first:"
  git status --short
  exit 1
fi

if ! git fetch --quiet --no-tags "$SOURCE" "refs/tags/$TAG"; then
  echo "Error: cannot fetch tag '$TAG' from '$SOURCE'"
  exit 1
fi
COMMIT="$(git rev-parse 'FETCH_HEAD^{commit}')"

if ! PATHS="$(git show "$COMMIT:tools/kit-paths.txt" 2>/dev/null)"; then
  echo "Error: '$TAG' has no tools/kit-paths.txt, so it cannot be used for an update"
  exit 1
fi

FROM="$(cat VERSION 2>/dev/null || echo unknown)"
TO="$(git show "$COMMIT:VERSION" 2>/dev/null || echo unknown)"
LOCAL_ONLY=""
SKIPPED=""

tag_files() {
  git -c core.quotepath=false ls-tree -r --name-only "$COMMIT" -- "$1"
}

EXCLUDES=""
if [[ -e .kit-exclude ]]; then
  EXCLUDE_LINES="$(cat .kit-exclude)"
  while IFS= read -r entry; do
    entry="${entry%$'\r'}"
    while [[ "$entry" == */ ]]; do
      entry="${entry%/}"
    done
    entry="${entry#./}"
    case "$entry" in
      ''|'#'*) continue ;;
    esac
    EXCLUDES+="$entry"$'\n'
  done <<< "$EXCLUDE_LINES"
fi

while IFS= read -r path; do
  case "$path" in
    ''|'#'*) continue ;;
  esac
  COVERED=false
  PATHSPEC=(":(literal)$path")
  EXCLUDED_FILES=""
  while IFS= read -r entry; do
    if [[ -z "$entry" ]]; then
      continue
    fi
    if [[ "$path" == "$entry" || "$path" == "$entry"/* ]]; then
      COVERED=true
    elif [[ "$entry" == "$path"/* ]]; then
      PATHSPEC+=(":(exclude,literal)$entry")
      FILES="$(tag_files "$entry")"
      if [[ -n "$FILES" ]]; then
        EXCLUDED_FILES+="$FILES"$'\n'
        SKIPPED+="$entry"$'\n'
      fi
    fi
  done <<< "$EXCLUDES"
  if [[ "$COVERED" == true ]]; then
    SKIPPED+="$path"$'\n'
    continue
  fi
  if ! git cat-file -e "$COMMIT:$path" 2>/dev/null; then
    echo "Warning: '$path' is not in $TAG, skipping"
    continue
  fi
  # git checkout fails when the exclusions leave nothing to take.
  if [[ -n "$(comm -23 <(tag_files "$path" | sort) <(printf '%s' "$EXCLUDED_FILES" | sort))" ]]; then
    git checkout --quiet "$COMMIT" -- "${PATHSPEC[@]}"
  fi
  LOCAL_ONLY+="$(comm -23 \
    <(git -c core.quotepath=false ls-files -- "${PATHSPEC[@]}" | sort) \
    <(tag_files "$path" | sort))"$'\n'
done <<< "$PATHS"

while IFS= read -r entry; do
  case $'\n'"$SKIPPED" in
    *$'\n'"$entry"$'\n'*|*$'\n'"$entry"/*) continue ;;
  esac
  if [[ -n "$entry" && ! -e "$entry" ]]; then
    echo "Warning: '$entry' in .kit-exclude matches nothing to update from $TAG"
  fi
done <<< "$EXCLUDES"

echo "Kit version: $FROM -> $TO ($TAG)"
if [[ -n "$SKIPPED" ]]; then
  echo "Skipped, listed in .kit-exclude:"
  printf '%s' "$SKIPPED" | sort -u | sed 's/^/  /'
fi
if git diff --cached --quiet; then
  echo "Already up to date."
  exit 0
fi

git diff --cached --stat

if [[ -n "${LOCAL_ONLY//[$'\n']/}" ]]; then
  echo ""
  echo "Only in this repository, kept as they are (the kit may have removed them):"
  echo "$LOCAL_ONLY" | sed '/^$/d; s/^/  /'
fi

echo ""
echo "Nothing is committed. Next steps:"
echo "  1. Review: git diff --cached"
echo "     Lines shown as removed may be local changes to framework files."
echo "  2. Keep a local version: git restore --source=HEAD --staged --worktree -- <path>"
echo "     or merge the changes back by hand."
echo "     To skip a path on every update, list it in .kit-exclude."
echo "  3. Run: make check-all"
echo "  4. Commit the result."
