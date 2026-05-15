#!/usr/bin/env bash
# One-shot setup for Jarvis-AI.
# Installs system + Python dependencies. Safe to re-run.

set -euo pipefail

echo "==> Jarvis-AI setup"
echo

OS="$(uname -s)"

# 1. System-level deps (portaudio for pyaudio)
case "$OS" in
    Darwin)
        if ! command -v brew >/dev/null 2>&1; then
            echo "Homebrew not found. Install from https://brew.sh and re-run." >&2
            exit 1
        fi
        if ! brew list portaudio >/dev/null 2>&1; then
            echo "==> Installing portaudio via Homebrew"
            brew install portaudio
        else
            echo "==> portaudio already installed"
        fi
        ;;
    Linux)
        if command -v apt-get >/dev/null 2>&1; then
            echo "==> Installing portaudio19-dev via apt"
            sudo apt-get update
            sudo apt-get install -y portaudio19-dev python3-pyaudio
        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y portaudio-devel
        else
            echo "Install portaudio manually for your distro." >&2
        fi
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "==> Windows detected — relying on pip wheels for pyaudio"
        ;;
esac

# 2. Python deps (editable install via setup.py)
echo
echo "==> Upgrading pip"
python3 -m pip install --upgrade pip

echo
echo "==> Installing Jarvis-AI Python dependencies"
python3 -m pip install -e .

# Windows extras
if [[ "$OS" =~ ^(MINGW|MSYS|CYGWIN) ]]; then
    echo "==> Installing Windows-only extras"
    python3 -m pip install -e ".[windows]"
fi

# 3. Env-var hint
echo
echo "==> Setup complete."
echo
if [[ -z "${JARVIS_EMAIL_USER:-}" || -z "${JARVIS_EMAIL_PASS:-}" ]]; then
    cat <<'EOF'
NOTE: email sending requires these environment variables:
    export JARVIS_EMAIL_USER="you@gmail.com"
    export JARVIS_EMAIL_PASS="<gmail-app-password>"

Generate a Gmail App Password at: https://myaccount.google.com/apppasswords
(2FA must be enabled on the Google account.)

Add the two exports to ~/.zshrc (macOS) or ~/.bashrc (Linux) to persist.
EOF
fi

echo
echo "Run with:  ./run.sh"
