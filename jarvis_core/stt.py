"""Speech-to-text via Google Web Speech API (free, online)."""
import speech_recognition as sr


def takeCommand() -> str:
    """Capture audio from default microphone and transcribe to text.

    Returns 'none' on failure (caller decides whether to retry).
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query
    except Exception:
        return "none"
