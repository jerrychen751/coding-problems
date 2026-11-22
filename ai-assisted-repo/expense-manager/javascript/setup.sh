#!/usr/bin/env bash
set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Setting up JavaScript (Node.js) Environment ==="
NODE_CMD="$(command -v node 2>/dev/null || true)"

if [ -n "$NODE_CMD" ] && "$NODE_CMD" -v >/dev/null 2>&1; then
    echo -e "${GREEN}[OK]${NC} Found Node.js $("$NODE_CMD" -v)"
else
    echo -e "${RED}[!]${NC} Node.js not found. Please install Node.js 14+."
    exit 1
fi

echo -n "Running test suite... "
(cd "$SCRIPT_DIR" && "$NODE_CMD" tests/test_expense_manager.js >/dev/null)
echo -e "${GREEN}[SUCCESS]${NC}"

echo "You can run tests with:"
echo "  make"

