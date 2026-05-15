#!/usr/bin/env bash
# Run Jarvis-AI.
# Usage:  ./run.sh

set -euo pipefail

cd "$(dirname "$0")"

# Warn if .env missing (jarvis.py loads it via python-dotenv at startup)
if [[ ! -f .env && -z "${JARVIS_EMAIL_USER:-}" ]]; then
    echo "WARN: no .env file and JARVIS_EMAIL_USER not exported."
    echo "      Email feature will fail. All other commands work."
    echo "      Run ./setup.sh or copy .env.example to .env."
    echo
fi

exec python3 jarvis.py
