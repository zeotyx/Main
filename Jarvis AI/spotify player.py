import pyautogui
import time
import subprocess
import psutil
import pygetwindow as gw


SPOTIFY_PATH = r"C:\Users\lolik\AppData\Roaming\Spotify\Spotify.exe"


def is_spotify_running():
    for process in psutil.process_iter(["name"]):
        name = process.info.get("name", "")
        if name and "spotify" in name.lower():
            return True
    return False


def open_spotify():
    if is_spotify_running():
        print("Spotify already running.")
        return True

    try:
        subprocess.Popen(SPOTIFY_PATH)
        print("Starting Spotify...")
        time.sleep(5)
        return True
    except Exception as e:
        print("Failed to start Spotify:", e)
        return False


def focus_spotify():
    try:
        windows = gw.getWindowsWithTitle("Spotify")

        if not windows:
            print("Spotify window not found.")
            return False

        window = windows[0]
        window.activate()

        print("Spotify focused.")
        time.sleep(1)
        return True

    except Exception as e:
        print("Couldn't focus Spotify:", e)
        return False


def search_playlist(name):
    pyautogui.hotkey("ctrl", "l")
    time.sleep(0.5)

    pyautogui.typewrite(name)
    pyautogui.press("enter")

    time.sleep(3)


def select_playlist():
    pyautogui.press("down")
    time.sleep(0.8)

    pyautogui.press("down")
    time.sleep(0.5)

    pyautogui.press("enter")

    time.sleep(2)


def start_playback():
    pyautogui.press("space")


def play_saved_playlist(playlist_name):

    if not open_spotify():
        return

    if not focus_spotify():
        return

    search_playlist(playlist_name)

    select_playlist()

    start_playback()

    print(f"Playing playlist: {playlist_name}")


if __name__ == "__main__":
    play_saved_playlist("Therian Playlist")
