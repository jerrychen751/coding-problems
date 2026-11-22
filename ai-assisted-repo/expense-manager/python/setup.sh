#!/usr/bin/env bash
set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Setting up Python Environment ==="
if command -v python3 >/dev/null 2>&1; then
    echo -e "${GREEN}[OK]${NC} Found $(python3 --version)"
else
    echo -e "${RED}[!]${NC} Python 3 not found. Please install Python 3.8+."
    exit 1
fi

if ! python3 -m pytest --version >/dev/null 2>&1 && [ ! -f "$SCRIPT_DIR/.venv/bin/pytest" ]; then
    echo "Installing pytest in local virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
    "$SCRIPT_DIR/.venv/bin/pip" install --quiet pytest
fi

echo -e "${GREEN}[OK]${NC} Pytest is ready."
echo "You can run tests with:"
echo "  make"
