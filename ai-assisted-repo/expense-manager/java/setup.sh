#!/usr/bin/env bash
set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Setting up Java Environment ==="

CORRETTO_HOME=$(find "$HOME/.corretto" -maxdepth 3 -type d -name "Home" 2>/dev/null | head -n 1 || true)
if [ -n "$CORRETTO_HOME" ]; then
    export PATH="$CORRETTO_HOME/bin:$PATH"
fi

if command -v java >/dev/null 2>&1 && command -v javac >/dev/null 2>&1; then
    echo -e "${GREEN}[OK]${NC} Found Java: $(javac -version 2>&1)"
else
    echo -e "${YELLOW}[!]${NC} Java JDK not found in PATH."
    OS="$(uname -s)"
    ARCH="$(uname -m)"
    if [ "$OS" = "Darwin" ]; then
        CORRETTO_ARCH="aarch64"
        if [ "$ARCH" = "x86_64" ]; then CORRETTO_ARCH="x64"; fi
        INSTALL_DIR="$HOME/.corretto"
        mkdir -p "$INSTALL_DIR"
        echo "Downloading Amazon Corretto 21 JDK for macOS ($CORRETTO_ARCH)..."
        curl -sL "https://corretto.aws/downloads/latest/amazon-corretto-21-${CORRETTO_ARCH}-macos-jdk.tar.gz" | tar -xz -C "$INSTALL_DIR"
        JDK_HOME=$(find "$INSTALL_DIR" -maxdepth 3 -type d -name "Home" | head -n 1)
        export PATH="$JDK_HOME/bin:$PATH"
        echo -e "${GREEN}[OK]${NC} Amazon Corretto installed without sudo"
    elif [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y default-jdk
    fi
fi

mkdir -p "$SCRIPT_DIR/lib"
JUNIT_JAR="$SCRIPT_DIR/lib/junit-platform-console-standalone-1.10.2.jar"
if [ ! -f "$JUNIT_JAR" ]; then
    echo "Downloading JUnit 5 console standalone..."
    curl -sSL "https://repo1.maven.org/maven2/org/junit/platform/junit-platform-console-standalone/1.10.2/junit-platform-console-standalone-1.10.2.jar" -o "$JUNIT_JAR"
fi

echo -n "Running test suite... "
(cd "$SCRIPT_DIR" && make >/dev/null)
echo -e "${GREEN}[SUCCESS]${NC}"

echo "You can run tests with:"
echo "  make"

