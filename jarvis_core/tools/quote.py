"""Quote of the day."""
import requests
from .base import Tool


def _quote_of_day() -> str:
    try:
        r = requests.get("https://quotes.rest/qod?language=en", timeout=10).json()
        q = r["contents"]["quotes"][0]
        return f"{q['quote']} — {q['author']}"
    except Exception as e:
        return f"Could not fetch quote: {e}"


TOOLS = [
    Tool(
        name="quote_of_day",
        description="Fetch the quote of the day.",
        input_schema={"type": "object", "properties": {}},
        handler=_quote_of_day,
    ),
]
