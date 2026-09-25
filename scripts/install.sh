#!/usr/bin/env bash
# BC Design System - Universal Multi-Runtime Installer for Linux / macOS / WSL
# Supports Claude Code, Codex, Antigravity, and Kiro

AI_TOOL="${1:-all}"
TARGET_DIR="${2:-.}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/install.py"

if command -v python3 &>/dev/null; then
    python3 "${PYTHON_SCRIPT}" --ai "${AI_TOOL}" --target-dir "${TARGET_DIR}"
elif command -v python &>/dev/null; then
    python "${PYTHON_SCRIPT}" --ai "${AI_TOOL}" --target-dir "${TARGET_DIR}"
elif command -v py &>/dev/null; then
    py -3 "${PYTHON_SCRIPT}" --ai "${AI_TOOL}" --target-dir "${TARGET_DIR}"
else
    echo "Error: Python 3.x is required to run the installer."
    exit 1
fi
