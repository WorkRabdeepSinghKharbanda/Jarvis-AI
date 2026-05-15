"""COVID-19 case lookup for Indian states."""
import requests
from .base import Tool

_DATA_URL = (
    "https://api.apify.com/v2/key-value-stores/"
    "toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true"
)


def _covid_cases(region: str) -> str:
    try:
        data = requests.get(_DATA_URL, timeout=10).json()["regionData"]
    except Exception as e:
        return f"Could not fetch COVID data: {e}"
    needle = region.lower().strip()
    for row in data:
        if needle in row.get("region", "").lower():
            return (
                f"COVID-19 in {row['region']}: "
                f"Active {row['activeCases']}, "
                f"Deaths {row['newDeceased']}, "
                f"Recovered {row['newRecovered']}, "
                f"Total {row['totalInfected']}"
            )
    return f"No COVID data found for '{region}'."


TOOLS = [
    Tool(
        name="covid_cases",
        description="Get COVID-19 case statistics for an Indian state or region.",
        input_schema={
            "type": "object",
            "properties": {
                "region": {"type": "string", "description": "Indian state/region name."}
            },
            "required": ["region"],
        },
        handler=_covid_cases,
    ),
]
