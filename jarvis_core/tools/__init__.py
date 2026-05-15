"""Tool registry — auto-discovers every tool module in this package.

To add a new tool: drop a new file in `jarvis_core/tools/` that exports a
top-level list named `TOOLS: list[Tool]`. The registry picks it up
automatically — no edits needed here.
"""
import importlib
import pkgutil
from .base import Tool

ALL_TOOLS: list[Tool] = []

for module_info in pkgutil.iter_modules(__path__):
    if module_info.name == "base":
        continue
    module = importlib.import_module(f"{__name__}.{module_info.name}")
    module_tools = getattr(module, "TOOLS", [])
    ALL_TOOLS.extend(module_tools)

TOOLS_BY_NAME: dict[str, Tool] = {t.name: t for t in ALL_TOOLS}


def gemini_specs() -> list[dict]:
    """Return all function declarations in the shape Gemini expects."""
    return [t.gemini_spec() for t in ALL_TOOLS]
