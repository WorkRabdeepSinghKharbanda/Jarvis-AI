"""Gemini function-calling loop — the brain of Jarvis.

Receives a user transcript, asks Gemini which tool to call (if any),
runs it locally, feeds the result back, and loops until Gemini produces
a final natural-language reply.
"""
from typing import List
from google import genai
from google.genai import types
from .config import GOOGLE_API_KEY, GEMINI_MODEL
from .tools import ALL_TOOLS, TOOLS_BY_NAME, gemini_specs

_SYSTEM_PROMPT = (
    "You are Jarvis, a concise voice assistant. "
    "Pick the right tool for the user's request and call it. "
    "If the request needs multiple steps, call tools in sequence. "
    "If a required argument is missing or ambiguous, ask one short clarifying question "
    "instead of guessing. "
    "Replies are spoken aloud — keep them under two sentences, "
    "no markdown, no code blocks, no lists."
)


def _build_tool_config() -> types.Tool:
    """Wrap all tool declarations into a single Gemini Tool object."""
    return types.Tool(function_declarations=gemini_specs())


class Agent:
    """Stateless dispatcher: one .handle() per user utterance.

    Pass remember=True to keep multi-turn context across calls
    (stored in self.history). Reset with self.history.clear().
    """

    def __init__(self, model: str = GEMINI_MODEL):
        if not GOOGLE_API_KEY:
            raise RuntimeError(
                "GOOGLE_API_KEY not set. Add it to .env or export it."
            )
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model = model
        self.tools = [_build_tool_config()]
        self.config = types.GenerateContentConfig(
            system_instruction=_SYSTEM_PROMPT,
            tools=self.tools,
        )
        self.history: List[types.Content] = []

    def _to_content(self, role: str, parts: list) -> types.Content:
        return types.Content(role=role, parts=parts)

    def handle(self, user_text: str, *, remember: bool = False) -> str:
        """Send user_text to Gemini; execute tool calls; return final reply."""
        user_part = types.Part.from_text(text=user_text)
        if remember:
            self.history.append(self._to_content("user", [user_part]))
            contents: List[types.Content] = list(self.history)
        else:
            contents = [self._to_content("user", [user_part])]

        final_text = ""
        # Cap loop iterations to prevent runaway tool chains
        for _ in range(8):
            resp = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=self.config,
            )

            candidate = resp.candidates[0] if resp.candidates else None
            if not candidate or not candidate.content:
                break

            # Append assistant turn (Gemini calls it "model")
            contents.append(candidate.content)

            # Gather text + function_calls from the model's parts
            tool_calls = []
            text_chunks = []
            for part in candidate.content.parts or []:
                if getattr(part, "function_call", None):
                    tool_calls.append(part.function_call)
                elif getattr(part, "text", None):
                    text_chunks.append(part.text)
            if text_chunks:
                final_text = "".join(text_chunks).strip() or final_text

            if not tool_calls:
                break

            # Execute every requested tool and feed results back
            result_parts = []
            for fc in tool_calls:
                tool = TOOLS_BY_NAME.get(fc.name)
                args = dict(fc.args) if fc.args else {}
                if tool is None:
                    result = f"Unknown tool: {fc.name}"
                else:
                    result = tool.call(**args)
                result_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )
            contents.append(self._to_content("user", result_parts))

        if remember:
            self.history.append(
                self._to_content("model", [types.Part.from_text(text=final_text)])
            )
        return final_text or "Done."


def available_tools() -> list[str]:
    """Return names of all registered tools (for debug/inspection)."""
    return [t.name for t in ALL_TOOLS]
