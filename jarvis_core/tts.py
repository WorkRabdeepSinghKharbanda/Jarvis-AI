"""Text-to-speech — platform-aware.

macOS: native `say` (pyttsx3 nsss hangs on runAndWait).
Windows/Linux: pyttsx3 with sapi5/espeak driver.
"""
import subprocess
from .config import IS_MAC, IS_WINDOWS

_engine = None


def _init_engine():
    global _engine
    if _engine is not None:
        return _engine
    import pyttsx3
    driver = "sapi5" if IS_WINDOWS else "espeak"
    _engine = pyttsx3.init(driver)
    _engine.setProperty("rate", 175)
    voices = _engine.getProperty("voices")
    if voices:
        _engine.setProperty("voice", voices[0].id)
    return _engine


def speak(text: str) -> None:
    """Speak text aloud. Blocks until done."""
    text = str(text).strip()
    if not text:
        return
    print(f"[jarvis] {text}")
    if IS_MAC:
        subprocess.run(["say", text])
        return
    engine = _init_engine()
    engine.say(text)
    engine.runAndWait()
