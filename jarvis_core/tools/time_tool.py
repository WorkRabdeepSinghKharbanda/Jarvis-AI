"""Time + sleep timer."""
import datetime
import time
from .base import Tool


def _get_time() -> str:
    return datetime.datetime.now().strftime("%H:%M:%S")


def _sleep_timer(seconds: int) -> str:
    if seconds <= 0 or seconds > 3 * 60 * 60:
        return "Sleep duration must be between 1 second and 3 hours."
    time.sleep(seconds)
    return f"Done waiting {seconds} seconds."


TOOLS = [
    Tool(
        name="get_time",
        description="Return the current local time as HH:MM:SS.",
        input_schema={"type": "object", "properties": {}},
        handler=_get_time,
    ),
    Tool(
        name="sleep_timer",
        description="Wait for the specified number of seconds. Use for 'wait N seconds/minutes/hours'.",
        input_schema={
            "type": "object",
            "properties": {
                "seconds": {"type": "integer", "description": "Number of seconds to wait."}
            },
            "required": ["seconds"],
        },
        handler=_sleep_timer,
    ),
]
