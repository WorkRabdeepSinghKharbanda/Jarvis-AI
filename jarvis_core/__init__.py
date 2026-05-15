"""Jarvis core package: modular voice assistant runtime.

Layout:
    config.py        — env vars, paths
    tts.py           — speak()
    stt.py           — takeCommand()
    agent.py         — Claude tool-use loop
    tools/           — one tool per file; auto-registered
"""
