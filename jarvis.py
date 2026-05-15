"""Jarvis entry point — thin orchestration over jarvis_core."""
import datetime
from jarvis_core.tts import speak
from jarvis_core.stt import takeCommand
from jarvis_core.agent import Agent, available_tools


def greet() -> None:
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    elif 18 <= hour <= 21:
        speak("Good evening!")
    else:
        speak("Good night!")
    speak("I'm Jarvis. How may I help you?")


def main() -> None:
    print(f"[jarvis] Registered tools: {', '.join(available_tools())}")
    agent = Agent()
    greet()
    while True:
        query = takeCommand()
        if query == "none":
            continue
        if any(w in query.lower() for w in ("exit", "quit", "goodbye", "good bye")):
            speak("Goodbye!")
            break
        try:
            reply = agent.handle(query, remember=True)
        except Exception as e:
            reply = f"Sorry, something went wrong: {e}"
        speak(reply)


if __name__ == "__main__":
    main()
