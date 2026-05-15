# Jarvis-AI

A Python-based voice-activated virtual assistant inspired by Iron Man's J.A.R.V.I.S. Executes a wide range of desktop and web tasks via natural-language voice commands.

## Features

- Search any topic on Wikipedia
- Open popular websites (YouTube, LinkedIn, etc.) by voice
- Play random music / movies from local storage
- Launch installed programs (VS Code, Notepad, etc.)
- Play YouTube videos on demand
- Compose and send emails
- Tell jokes, current day, and time
- Live COVID-19 statistics for any Indian state
- Daily quote of the day
- Real-time weather for any city
- Launch sibling projects: Secure-Vision, Customer-Browser, Face-Detector

## Tech Stack

- **Language:** Python 3
- **Voice I/O:** `pyttsx3`, `speech_recognition`
- **Web / APIs:** `wikipedia`, `requests`, weather + quote APIs
- **Automation:** `pywhatkit`, `webbrowser`, `os`, `smtplib`
- **ML / CV:** OpenCV (for vision sub-modules)

## Project Structure

```
Jarvis-AI/
├── jarvis.py     # Main assistant script
└── weather.ico   # App icon
```

## Setup

```bash
git clone https://github.com/WorkRabdeepSinghKharbanda/Jarvis-AI.git
cd Jarvis-AI
pip install pyttsx3 SpeechRecognition wikipedia pywhatkit requests pyaudio opencv-python
python jarvis.py
```

> **macOS / Linux note:** `pyaudio` may require `portaudio` (e.g. `brew install portaudio`).

## Usage

Run the script and speak commands such as:
- *"Open YouTube"*
- *"Play a song"*
- *"Tell me a joke"*
- *"What's the weather in Delhi"*
- *"Search Wikipedia for Albert Einstein"*

## License

MIT
