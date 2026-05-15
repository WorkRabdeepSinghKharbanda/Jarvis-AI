"""Weather lookup via Google search scraping."""
import requests
import bs4
from .base import Tool


def _get_weather(city: str) -> str:
    url = f"https://www.google.com/search?q=weather+{city}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        data = requests.get(url, headers=headers, timeout=10).text
        soup = bs4.BeautifulSoup(data, "html.parser")
        temp = soup.find("div", attrs={"class": "BNeawe iBp4i AP7Wnd"})
        meta = soup.find("div", attrs={"class": "BNeawe tAd8D AP7Wnd"})
        if not temp or not meta:
            return f"Could not parse weather for {city}."
        parts = meta.text.split("\n")
        when = parts[0] if parts else ""
        sky = parts[1] if len(parts) > 1 else ""
        return f"{city.title()}: {temp.text}, {sky} ({when})"
    except Exception as e:
        return f"Weather lookup failed: {e}"


TOOLS = [
    Tool(
        name="get_weather",
        description="Get current weather for a city.",
        input_schema={
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name."}
            },
            "required": ["city"],
        },
        handler=_get_weather,
    ),
]
