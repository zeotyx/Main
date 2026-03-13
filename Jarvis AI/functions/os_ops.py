import os
import subprocess
import random
import time
import webbrowser
import requests
import pyttsx3

from datetime import datetime


# -------------------------------------------------
# TexttoSpeech
# -------------------------------------------------

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


# -------------------------------------------------
# Application Paths
# -------------------------------------------------

APP_PATHS = {
    "notepad": r"C:\Program Files\Notepad++\notepad++.exe",
    "discord": r"C:\Users\lolik\AppData\Local\Discord\app-1.0.9173\Discord.exe",
    "calculator": r"C:\Windows\System32\calc.exe",
}


# -------------------------------------------------
# Utilities
# -------------------------------------------------

def get_current_time():
    return datetime.now().strftime("%H:%M:%S")


def open_browser(url="https://www.google.com"):
    webbrowser.open(url)


def shutdown_system():
    os.system("shutdown /s /f /t 1")


# -------------------------------------------------
# weather
# -------------------------------------------------

def get_weather(city):

    API_KEY = "YOUR_OPENWEATHER_API_KEY"

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 404:

            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]

            return f"{weather} with a temperature of {temperature}°C"

        return "City not found"

    except Exception as e:
        print("Weather error:", e)
        return "Unable to retrieve weather."


# -------------------------------------------------
# Alarm
# -------------------------------------------------

def set_alarm(alarm_time):

    hour, minute = map(int, alarm_time.split(":"))

    now = datetime.now()
    alarm = datetime(now.year, now.month, now.day, hour, minute)

    while datetime.now() < alarm:
        time.sleep(10)

    speak(f"Alarm! It's {alarm_time}.")


# -------------------------------------------------
# Media
# -------------------------------------------------

def play_music(song_name):

    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    webbrowser.open(search_url)


# -------------------------------------------------
# Notes & Reminders
# -------------------------------------------------

def take_note(content, filename="notes.txt"):

    with open(filename, "a") as file:
        file.write(content + "\n")


def set_reminder(task, reminder_time, filename="reminders.txt"):

    with open(filename, "a") as file:
        file.write(f"Reminder: {task} at {reminder_time}\n")

    speak(f"I'll remind you about {task} at {reminder_time}")


# -------------------------------------------------
# Translation
# -------------------------------------------------

def translate_text(sentence, language):

    from googletrans import Translator

    translator = Translator()

    try:
        result = translator.translate(sentence, dest=language)
        return result.text
    except Exception:
        return "Translation failed."


# -------------------------------------------------
# Dictionary
# -------------------------------------------------

def get_word_definition(word):

    API_KEY = "YOUR_MERRIAM_WEBSTER_KEY"

    url = (
        f"https://www.dictionaryapi.com/api/v3/references/"
        f"collegiate/json/{word}?key={API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if data and "shortdef" in data[0]:
            return data[0]["shortdef"][0]

        return "Definition not found"

    except Exception:
        return "Error retrieving definition."


# -------------------------------------------------
# Applications
# -------------------------------------------------

def open_camera():
    subprocess.run("start microsoft.windows.camera:", shell=True)


def open_notepad():
    os.startfile(APP_PATHS["notepad"])


def open_discord():
    os.startfile(APP_PATHS["discord"])


def open_cmd():
    os.system("start cmd")


def open_calculator():
    subprocess.Popen(APP_PATHS["calculator"])


# -------------------------------------------------
# Responses
# -------------------------------------------------

def get_random_joke():

    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]

    return random.choice(jokes)


def get_random_advice():

    advices = [
        "Don't take life too seriously, nobody gets out alive anyway.",
        "Believe in yourself and all that you are.",
        "If you want something you've never had, you must be willing to do something you've never done."
    ]

    return random.choice(advices)
