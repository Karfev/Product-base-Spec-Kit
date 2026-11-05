#!/usr/bin/env bash
# Update the framework files of a repository from a tagged kit version.
# The paths come from tools/kit-paths.txt of that version. The result stays uncommitted:
# local changes to framework files show up in the diff, and nothing else is touched.
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

while IFS= read -r path; do
  case "$path" in
    ''|'#'*) continue ;;
  esac
  if ! git cat-file -e "$COMMIT:$path" 2>/dev/null; then
    echo "Warning: '$path' is not in $TAG, skipping"
    continue
  fi
  git --literal-pathspecs checkout --quiet "$COMMIT" -- "$path"
  LOCAL_ONLY+="$(comm -23 \
    <(git -c core.quotepath=false --literal-pathspecs ls-files -- "$path" | sort) \
    <(git -c core.quotepath=false ls-tree -r --name-only "$COMMIT" -- "$path" | sort))"$'\n'
done <<< "$PATHS"

echo "Kit version: $FROM -> $TO ($TAG)"
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
echo "  3. Run: make check-all"
echo "  4. Commit the result."
