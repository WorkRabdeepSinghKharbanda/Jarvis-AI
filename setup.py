"""Setup script for Jarvis-AI.

Install all dependencies:
    python3 setup.py install

Or for editable / dev install:
    python3 -m pip install -e .
"""
from setuptools import setup

setup(
    name="jarvis-ai",
    version="1.0.0",
    description="Voice-activated virtual assistant in Python",
    author="Rabdeep Singh Kharbanda",
    py_modules=["jarvis"],
    python_requires=">=3.8",
    install_requires=[
        "pyttsx3",
        "SpeechRecognition",
        "wikipedia",
        "pywhatkit",
        "pyjokes",
        "plyer",
        "requests",
        "pyaudio",
        "opencv-python",
        "beautifulsoup4",
        "lyricsgenius",
    ],
    extras_require={
        "windows": ["comtypes", "pypiwin32"],
    },
)
