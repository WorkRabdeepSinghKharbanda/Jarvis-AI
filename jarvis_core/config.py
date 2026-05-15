"""Central config — env vars, paths, model name."""
import os
import platform
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

HOME = Path.home()
REPO_ROOT = Path(__file__).resolve().parent.parent

# User-overridable directories
MUSIC_DIR = os.environ.get("JARVIS_MUSIC_DIR", str(HOME / "Music"))
MOVIE_DIR = os.environ.get("JARVIS_MOVIE_DIR", str(HOME / "Movies"))
PROJECTS_DIR = os.environ.get("JARVIS_PROJECTS_DIR", str(REPO_ROOT.parent))

# Email
EMAIL_USER = os.environ.get("JARVIS_EMAIL_USER")
EMAIL_PASS = os.environ.get("JARVIS_EMAIL_PASS")

# Claude
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.environ.get("JARVIS_CLAUDE_MODEL", "claude-haiku-4-5")

# Platform
OS_NAME = platform.system()
IS_MAC = OS_NAME == "Darwin"
IS_WINDOWS = OS_NAME == "Windows"
IS_LINUX = OS_NAME == "Linux"
