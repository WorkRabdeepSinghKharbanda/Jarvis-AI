"""Web browsing + app launching tools."""
import os
import subprocess
import webbrowser
import pywhatkit
from .base import Tool
from ..config import IS_MAC, IS_WINDOWS

_SITE_ALIASES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "stackoverflow": "https://stackoverflow.com",
    "stack overflow": "https://stackoverflow.com",
    "whatsapp": "https://web.whatsapp.com",
    "linkedin": "https://linkedin.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "github": "https://github.com",
    "reddit": "https://reddit.com",
}


def _open_website(url_or_name: str) -> str:
    key = url_or_name.lower().strip()
    url = _SITE_ALIASES.get(key, url_or_name)
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened {url}"


def _open_app(name: str) -> str:
    if IS_MAC:
        subprocess.Popen(["open", "-a", name])
    elif IS_WINDOWS:
        os.startfile(name)
    else:
        subprocess.Popen([name.lower()])
    return f"Launched {name}"


def _play_youtube(query: str) -> str:
    pywhatkit.playonyt(query)
    return f"Playing '{query}' on YouTube"


TOOLS = [
    Tool(
        name="open_website",
        description=(
            "Open a website in the default browser. Accepts a URL or a "
            "common site name like 'youtube', 'google', 'github'."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "url_or_name": {
                    "type": "string",
                    "description": "URL or shorthand site name.",
                }
            },
            "required": ["url_or_name"],
        },
        handler=_open_website,
    ),
    Tool(
        name="open_app",
        description=(
            "Launch a desktop application by its display name. "
            "Examples: 'Visual Studio Code', 'Google Chrome', 'Firefox', 'Arduino'."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Application name."}
            },
            "required": ["name"],
        },
        handler=_open_app,
    ),
    Tool(
        name="play_youtube",
        description="Search YouTube for the given query and start playing the first result.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query."}
            },
            "required": ["query"],
        },
        handler=_play_youtube,
    ),
]
