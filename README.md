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
python3 -m pip install pyttsx3 SpeechRecognition wikipedia pywhatkit pyjokes plyer requests pyaudio opencv-python beautifulsoup4
python3 jarvis.py
```

> **Platform notes:**
> - **macOS / Linux:** `pyaudio` requires `portaudio` (`brew install portaudio` on macOS; `sudo apt install portaudio19-dev` on Debian/Ubuntu).
> - **Text-to-speech driver:** `pyttsx3.init('sapi5')` (line 23 in `jarvis.py`) only works on Windows. On macOS use `nsss`, on Linux use `espeak`. Cross-platform fix:
>   ```python
>   import platform
>   driver = {'Windows': 'sapi5', 'Darwin': 'nsss', 'Linux': 'espeak'}[platform.system()]
>   engine = pyttsx3.init(driver)
>   ```
> - **Notification icons:** `jarvis.py` lines 110 and 195 hardcode `C:\project\jarvisAI\*.ico`. Replace with relative paths (e.g. `weather.ico`) for non-Windows use.
> - **Windows only:** `pyttsx3` on Windows additionally needs `python3 -m pip install comtypes pypiwin32`.

## Usage

Run the script and speak commands such as:
- *"Open YouTube"*
- *"Play a song"*
- *"Tell me a joke"*
- *"What's the weather in Delhi"*
- *"Search Wikipedia for Albert Einstein"*

## License

MIT
