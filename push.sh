#!usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
    echo "Usage: ./push.sh <file> <category> [branch]"
    exit 1
fi

FILE="$1"
CATEGORY="$2"
BRANCH="${3:-main}"

if [[ ! -f "$FILE" ]]; then
    echo "File not found: $FILE"
    exit 1
fi

DATE_STR="$(date '+%-m.%-d.%Y')"
MSG="${DATE_STR} - ${CATEGORY}"

git add "$FILE"
git commit -m "$MSG"
git push origin "$BRANCH"
echo "Pushed: $MSG"