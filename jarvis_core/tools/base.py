"""Tool primitive — every tool conforms to this shape."""
from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class Tool:
    """One executable capability exposed to the LLM.

    name         — snake_case identifier (used by Claude to call).
    description  — natural-language description for Claude's tool router.
    input_schema — JSON Schema describing the args.
    handler      — Python callable, receives kwargs from Claude's tool_use.input
                   and returns a string (passed back to Claude as tool_result).
    """
    name: str
    description: str
    input_schema: dict
    handler: Callable[..., Any]

    def gemini_spec(self) -> dict:
        """Function declaration in Gemini's tool format."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.input_schema,
        }

    def call(self, **kwargs) -> str:
        try:
            result = self.handler(**kwargs)
            return str(result) if result is not None else "Done."
        except Exception as e:
            return f"Error executing {self.name}: {e}"
