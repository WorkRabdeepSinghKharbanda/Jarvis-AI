"""Claude tool-use loop — the brain of Jarvis.

Receives a user transcript, asks Claude which tool to call (if any),
runs it locally, feeds the result back, and loops until Claude produces
a final natural-language reply.
"""
from typing import List, Dict, Any
import anthropic
from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL
from .tools import ALL_TOOLS, TOOLS_BY_NAME, anthropic_specs

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

    Conversation memory is NOT persisted across utterances by default; each
    call starts a fresh message thread. To enable multi-turn memory, instantiate
    once and keep `self.history` across calls (see `handle_with_memory`).
    """

    def __init__(self, model: str = CLAUDE_MODEL):
        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. Add it to .env or export it."
            )
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = model
        self.tools_spec = self._build_tool_spec_with_caching()
        self.history: List[Dict[str, Any]] = []

    def _build_tool_spec_with_caching(self) -> List[dict]:
        """Mark the last tool with cache_control so the whole tool block is cached."""
        specs = anthropic_specs()
        if specs:
            specs[-1] = {**specs[-1], "cache_control": {"type": "ephemeral"}}
        return specs

    def handle(self, user_text: str, *, remember: bool = False) -> str:
        """Send `user_text` to Claude; execute tool calls; return final reply."""
        if remember:
            self.history.append({"role": "user", "content": user_text})
            messages = list(self.history)
        else:
            messages = [{"role": "user", "content": user_text}]

        final_text = ""
        while True:
            resp = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=_SYSTEM_PROMPT,
                tools=self.tools_spec,
                messages=messages,
            )

            # Capture any text the model emitted in this turn
            final_text = "".join(
                b.text for b in resp.content if getattr(b, "type", None) == "text"
            ).strip() or final_text

            if resp.stop_reason == "end_turn":
                break
            if resp.stop_reason != "tool_use":
                # Unknown stop reason — bail safely
                break

            # Append assistant turn and execute every requested tool
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if getattr(block, "type", None) != "tool_use":
                    continue
                tool = TOOLS_BY_NAME.get(block.name)
                if tool is None:
                    result = f"Unknown tool: {block.name}"
                else:
                    result = tool.call(**(block.input or {}))
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )
            messages.append({"role": "user", "content": tool_results})

        if remember:
            self.history.append({"role": "assistant", "content": final_text})
        return final_text or "Done."


def available_tools() -> list[str]:
    """Return names of all registered tools (for debug/inspection)."""
    return [t.name for t in ALL_TOOLS]
