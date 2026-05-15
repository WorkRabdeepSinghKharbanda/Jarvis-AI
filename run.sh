#!/usr/bin/env bash
# Run Jarvis-AI.
# Usage:  ./run.sh

set -euo pipefail

cd "$(dirname "$0")"

# Warn if email credentials missing (not fatal — only email feature breaks)
if [[ -z "${JARVIS_EMAIL_USER:-}" || -z "${JARVIS_EMAIL_PASS:-}" ]]; then
    echo "WARN: JARVIS_EMAIL_USER / JARVIS_EMAIL_PASS not set."
    echo "      Email feature will fail. All other commands work."
    echo
fi

exec python3 jarvis.py
