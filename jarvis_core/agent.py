"""OpenAI function-calling loop — the brain of Jarvis.

Receives a user transcript, asks GPT which tool to call (if any),
runs it locally, feeds the result back, and loops until GPT produces
a final natural-language reply.
"""
import json
from typing import List, Dict, Any
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .tools import ALL_TOOLS, TOOLS_BY_NAME, openai_specs

_SYSTEM_PROMPT = (
    "You are Jarvis, a concise voice assistant. "
    "Pick the right tool for the user's request and call it. "
    "If the request needs multiple steps, call tools in sequence. "
    "If a required argument is missing or ambiguous, ask one short clarifying question "
    "instead of guessing. "
    "Replies are spoken aloud — keep them under two sentences, "
    "no markdown, no code blocks, no lists."
)


class Agent:
    """Stateless dispatcher: one .handle() per user utterance.

    Pass remember=True to keep multi-turn context across calls (stored in
    self.history). Reset with self.history.clear().
    """

    def __init__(self, model: str = OPENAI_MODEL):
        if not OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY not set. Add it to .env or export it."
            )
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.tools_spec = openai_specs()
        self.history: List[Dict[str, Any]] = []

    def handle(self, user_text: str, *, remember: bool = False) -> str:
        """Send user_text to GPT; execute tool calls; return final reply."""
        if remember:
            self.history.append({"role": "user", "content": user_text})
            messages: List[Dict[str, Any]] = [
                {"role": "system", "content": _SYSTEM_PROMPT},
                *self.history,
            ]
        else:
            messages = [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ]

        final_text = ""
        # Cap loop iterations to prevent runaway tool chains
        for _ in range(8):
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools_spec,
                tool_choice="auto",
            )
            msg = resp.choices[0].message
            final_text = (msg.content or "").strip() or final_text

            if not msg.tool_calls:
                break

            # Append the assistant turn (must include tool_calls)
            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content,
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                }
            )

            # Execute each tool and append a tool result message per call
            for tc in msg.tool_calls:
                tool = TOOLS_BY_NAME.get(tc.function.name)
                try:
                    args = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                if tool is None:
                    result = f"Unknown tool: {tc.function.name}"
                else:
                    result = tool.call(**args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result,
                    }
                )

        if remember:
            self.history.append({"role": "assistant", "content": final_text})
        return final_text or "Done."


def available_tools() -> list[str]:
    """Return names of all registered tools (for debug/inspection)."""
    return [t.name for t in ALL_TOOLS]
