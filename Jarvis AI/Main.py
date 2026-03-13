import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import pyttsx3
import speech_recognition as sr
import threading
from datetime import datetime
from fuzzywuzzy import fuzz
from decouple import config

from functions.online_ops import (
    find_my_ip,
    get_random_advice,
    get_random_joke,
    play_on_youtube,
    search_on_google,
    search_on_wikipedia,
    send_email,
    send_whatsapp_message,
    get_weather
)

from functions.os_ops import (
    open_calculator,
    open_camera,
    open_cmd,
    open_notepad,
    open_discord
)

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

USERNAME = config("USER")
BOTNAME = config("BOTNAME")

PREDEFINED_CITIES = [
    "Pardubice", "Prague", "London",
    "New York", "Los Angeles", "Tokyo", "Berlin"
]

# ---------------------------------------------------
# Text To Speech
# ---------------------------------------------------

engine = pyttsx3.init()
engine.setProperty("rate", 185)
engine.setProperty("volume", 1)


def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()


# ---------------------------------------------------
# Greeting
# ---------------------------------------------------

def greet_user():
    hour = datetime.now().hour

    if hour < 12:
        speak(f"Good morning {USERNAME}")
    elif hour < 18:
        speak(f"Good afternoon {USERNAME}")
    else:
        speak(f"Good evening {USERNAME}")

    speak(f"I'm {BOTNAME}. How can I help?")


# ---------------------------------------------------
# Voice Recognition
# ---------------------------------------------------

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            query = recognizer.recognize_google(audio).lower()

            print("User:", query)
            return query

        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
        except sr.RequestError:
            speak("Speech service unavailable.")
        except Exception:
            speak("Sorry, I didn't catch that.")

    return ""


# ---------------------------------------------------
# Math
# ---------------------------------------------------

def evaluate_expression(query):
    try:
        query = query.replace("plus", "+")
        query = query.replace("minus", "-")
        query = query.replace("times", "*")
        query = query.replace("divided by", "/")

        result = eval(query)
        speak(f"The result is {result}")
        return result

    except Exception:
        speak("I couldn't calculate that.")
        return None


# ---------------------------------------------------
# City Matching
# ---------------------------------------------------

def closest_city(query):
    best_city = None
    best_score = 0

    for city in PREDEFINED_CITIES:
        score = fuzz.ratio(query.lower(), city.lower())

        if score > best_score:
            best_score = score
            best_city = city

    if best_score > 75:
        return best_city

    return None


# ---------------------------------------------------
# Command Handling
# ---------------------------------------------------

def handle_query(query):

    if "hello" in query:
        speak("Hello!")

    elif "open notepad" in query:
        open_notepad()

    elif "open discord" in query:
        open_discord()

    elif "open command prompt" in query or "open cmd" in query:
        open_cmd()

    elif "open camera" in query:
        open_camera()

    elif "open calculator" in query:
        open_calculator()

    elif "ip address" in query:
        ip = find_my_ip()
        speak(f"Your IP address is {ip}")

    elif "joke" in query:
        speak(get_random_joke())

    elif "advice" in query:
        speak(get_random_advice())

    elif "youtube" in query:
        speak("What should I play?")
        video = listen()
        play_on_youtube(video)

    elif "google" in query:
        speak("What should I search?")
        search = listen()
        search_on_google(search)

    elif "wikipedia" in query:
        speak("What do you want to search?")
        topic = listen()
        result = search_on_wikipedia(topic)
        speak(result)

    elif "weather" in query:
        speak("Which city?")
        city_query = listen()
        city = closest_city(city_query)

        if city:
            weather = get_weather(city)
            speak(weather)
        else:
            speak("I couldn't recognize the city.")

    elif "time" in query:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif any(x in query for x in ["plus", "minus", "times", "divided"]):
        evaluate_expression(query)


# ---------------------------------------------------
# Voice Thread
# ---------------------------------------------------

def voice_loop():
    while True:
        query = listen()
        if query:
            handle_query(query)


# ---------------------------------------------------
# Hand Tracking
# ---------------------------------------------------

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)

previous_x = None
previous_y = None

smooth_factor = 0.6

scale_x = 1.8
scale_y = 0.75


def pinch(hand, w, h):
    index = hand.landmark[8]
    thumb = hand.landmark[4]

    ix, iy = int(index.x * w), int(index.y * h)
    tx, ty = int(thumb.x * w), int(thumb.y * h)

    distance = np.sqrt((ix - tx) ** 2 + (iy - ty) ** 2)

    return distance < 27


def click_gesture(hand, w, h):
    middle = hand.landmark[12]
    thumb = hand.landmark[4]

    mx, my = int(middle.x * w), int(middle.y * h)
    tx, ty = int(thumb.x * w), int(thumb.y * h)

    distance = np.sqrt((mx - tx) ** 2 + (my - ty) ** 2)

    return distance < 24


# ---------------------------------------------------
# Main Loop
# ---------------------------------------------------

def main():

    greet_user()

    voice_thread = threading.Thread(target=voice_loop)
    voice_thread.daemon = True
    voice_thread.start()

    last_click = time.time()

    global previous_x, previous_y

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand,
                    mp_hands.HAND_CONNECTIONS
                )

                wrist = hand.landmark[0]

                wx = wrist.x * w
                wy = wrist.y * h

                if previous_x is None:
                    previous_x, previous_y = wx, wy

                if pinch(hand, w, h):

                    index = hand.landmark[8]

                    x = int(index.x * w)
                    y = int(index.y * h)

                    sx = np.interp(x, [0, w], [0, screen_width * scale_x])
                    sy = np.interp(y, [0, h], [0, screen_height * scale_y])

                    final_x = previous_x * smooth_factor + sx * (1 - smooth_factor)
                    final_y = previous_y * smooth_factor + sy * (1 - smooth_factor)

                    pyautogui.moveTo(final_x, final_y)

                    previous_x, previous_y = final_x, final_y

                elif click_gesture(hand, w, h):

                    now = time.time()

                    if now - last_click > 0.5:

                        button = "right" if wx < w / 2 else "left"
                        pyautogui.click(button=button)

                        last_click = now

        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
