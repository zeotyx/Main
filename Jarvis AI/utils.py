import pyttsx3
from decouple import config
from datetime import datetime


USERNAME = config("USER")
BOTNAME = config("BOTNAME")


def init_tts():
    engine = pyttsx3.init("sapi5")

    engine.setProperty("rate", 185)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)

    return engine


engine = init_tts()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_user():
    hour = datetime.now().hour

    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    speak(f"{greeting} {USERNAME}")
    speak(f"I'm {BOTNAME}. How can I help?")
