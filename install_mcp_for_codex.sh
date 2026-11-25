#!/bin/bash
# FL Studio MCP - Codex CLI Registration
# Registers the MCP server with OpenAI Codex CLI

set -e

SCRIPT_DIR="$(cd -- "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
SERVER_SCRIPT="$SCRIPT_DIR/fl_studio_mcp_server.py"

if ! command -v codex >/dev/null 2>&1; then
    echo "Install the Codex CLI and make sure codex is on PATH before registering the server." >&2
    exit 1
fi

# Git Bash needs native Windows paths when registering a Windows virtual environment.
if [[ -f "$SCRIPT_DIR/.venv/Scripts/python.exe" ]] && command -v cygpath >/dev/null 2>&1; then
    VENV_PYTHON="$(cygpath -aw "$SCRIPT_DIR/.venv/Scripts/python.exe")"
    SERVER_SCRIPT="$(cygpath -aw "$SERVER_SCRIPT")"
elif [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Python virtual environment not found. Run ./install_prerequisites.sh first." >&2
    exit 1
fi

exec codex mcp add fl-studio-mcp -- "$VENV_PYTHON" "$SERVER_SCRIPT"
