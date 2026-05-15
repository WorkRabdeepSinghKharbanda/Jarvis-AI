"""Wikipedia lookup."""
import wikipedia
from .base import Tool


def _wikipedia_lookup(topic: str, sentences: int = 2) -> str:
    try:
        return wikipedia.summary(topic, sentences=sentences)
    except wikipedia.DisambiguationError as e:
        return f"Multiple matches found. Did you mean: {', '.join(e.options[:5])}?"
    except wikipedia.PageError:
        return f"No Wikipedia page found for '{topic}'."


TOOLS = [
    Tool(
        name="wikipedia_lookup",
        description="Look up a topic on Wikipedia and return a short summary.",
        input_schema={
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "Topic to look up."},
                "sentences": {
                    "type": "integer",
                    "description": "How many sentences to return (default 2).",
                },
            },
            "required": ["topic"],
        },
        handler=_wikipedia_lookup,
    ),
]
