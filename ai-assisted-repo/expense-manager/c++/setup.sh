#!/usr/bin/env bash
set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Setting up C++ Environment ==="
CXX_CMD=""
if command -v clang++ >/dev/null 2>&1; then
    CXX_CMD="clang++"
elif command -v g++ >/dev/null 2>&1; then
    CXX_CMD="g++"
else
    echo -e "${RED}[!]${NC} No C++ compiler found. Please install Xcode CLT (macOS) or build-essential (Linux)."
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Found $($CXX_CMD --version | head -n 1)"

# Check Google Test
HAS_GTEST=0
if [ -f "/opt/homebrew/include/gtest/gtest.h" ] || [ -f "/usr/local/include/gtest/gtest.h" ] || [ -f "/usr/include/gtest/gtest.h" ]; then
    HAS_GTEST=1
fi

if [ "$HAS_GTEST" -eq 0 ]; then
    echo -e "${YELLOW}[!]${NC} Google Test not found. Installing..."
    OS="$(uname -s)"
    if [ "$OS" = "Darwin" ]; then
        if command -v brew >/dev/null 2>&1; then
            brew install googletest
        fi
    elif [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y libgtest-dev cmake
    fi
fi

echo -n "Running test suite... "
(cd "$SCRIPT_DIR" && make >/dev/null && make clean >/dev/null)
echo -e "${GREEN}[SUCCESS]${NC}"

echo "You can run tests with:"
echo "  make"

