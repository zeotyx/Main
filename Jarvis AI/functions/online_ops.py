import requests
import wikipedia
import pywhatkit as kit
import smtplib

from email.message import EmailMessage
from decouple import config


# -------------------------------------------------
# Configuration
# -------------------------------------------------

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

NEWS_API_KEY = config("NEWS_API_KEY")
TMDB_API_KEY = config("TMDB_API_KEY")
WEATHER_API_KEY = config("OPENWEATHER_API_KEY")


# -------------------------------------------------
# Network Helpers
# -------------------------------------------------

def get_json(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Request failed:", e)
        return None


# -------------------------------------------------
# General Utilities
# -------------------------------------------------

def find_my_ip():
    data = get_json("https://api64.ipify.org?format=json")
    return data["ip"] if data else None


def search_on_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        return "I couldn't find anything on Wikipedia."


def play_on_youtube(video):
    kit.playonyt(video)


def search_on_google(query):
    kit.search(query)


# -------------------------------------------------
# Messaging
# -------------------------------------------------

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+420{number}", message)


def send_email(receiver, subject, message):

    try:
        email = EmailMessage()
        email["From"] = EMAIL
        email["To"] = receiver
        email["Subject"] = subject
        email.set_content(message)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(email)

        return True

    except Exception as e:
        print("Email error:", e)
        return False


# -------------------------------------------------
# Information APIs
# -------------------------------------------------

def get_latest_news():

    url = f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={NEWS_API_KEY}"

    data = get_json(url)

    if not data:
        return []

    articles = data.get("articles", [])
    return [article["title"] for article in articles[:5]]


def get_trending_movies():

    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"

    data = get_json(url)

    if not data:
        return []

    results = data.get("results", [])
    return [movie["original_title"] for movie in results[:5]]


# -------------------------------------------------
# Fun APIs
# -------------------------------------------------

def get_random_joke():

    headers = {"Accept": "application/json"}

    data = get_json("https://icanhazdadjoke.com/", headers=headers)

    return data["joke"] if data else "I couldn't find a joke."


def get_random_advice():

    data = get_json("https://api.adviceslip.com/advice")

    if not data:
        return "No advice available right now."

    return data["slip"]["advice"]


# -------------------------------------------------
# Weather
# -------------------------------------------------

def get_weather(city):

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    data = get_json(url)

    if not data:
        return None

    weather = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]

    return weather, temperature, feels_like
