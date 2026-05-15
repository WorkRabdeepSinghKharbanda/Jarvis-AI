"""Local media playback."""
import os
import random
import subprocess
from .base import Tool
from ..config import MUSIC_DIR, MOVIE_DIR, IS_MAC, IS_WINDOWS


def _open_path(path: str) -> None:
    if IS_MAC:
        subprocess.Popen(["open", path])
    elif IS_WINDOWS:
        os.startfile(path)
    else:
        subprocess.Popen(["xdg-open", path])


def _play_random(directory: str, label: str) -> str:
    try:
        files = [f for f in os.listdir(directory) if not f.startswith(".")]
    except FileNotFoundError:
        return f"{label} folder not found: {directory}"
    if not files:
        return f"No {label.lower()} found in {directory}"
    choice = random.choice(files)
    _open_path(os.path.join(directory, choice))
    return f"Playing {label.lower()}: {os.path.splitext(choice)[0]}"


def _play_random_music() -> str:
    return _play_random(MUSIC_DIR, "Music")


def _play_random_movie() -> str:
    return _play_random(MOVIE_DIR, "Movie")


TOOLS = [
    Tool(
        name="play_random_music",
        description="Play a random song from the user's local music directory.",
        input_schema={"type": "object", "properties": {}},
        handler=_play_random_music,
    ),
    Tool(
        name="play_random_movie",
        description="Play a random movie from the user's local movie directory.",
        input_schema={"type": "object", "properties": {}},
        handler=_play_random_movie,
    ),
]
