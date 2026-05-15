"""Jokes."""
import pyjokes
from .base import Tool


def _tell_joke() -> str:
    return pyjokes.get_joke()


TOOLS = [
    Tool(
        name="tell_joke",
        description="Tell a programming joke.",
        input_schema={"type": "object", "properties": {}},
        handler=_tell_joke,
    ),
]
