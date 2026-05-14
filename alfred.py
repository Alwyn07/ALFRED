import socket
import sys

def single_instance():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("localhost", 65432))
    except:
        print("A.L.F.R.E.D is already running.")
        sys.exit()

single_instance()
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import platform
import threading
import subprocess
import requests
import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

memory = load_memory()
# ==============================
# ⚙️ CONFIG
# ==============================
USE_ONLINE_AI = False   # Set True if using OpenAI
OLLAMA_MODEL = "phi"

if USE_ONLINE_AI:
    from openai import OpenAI
    client = OpenAI(api_key="YOUR_API_KEY")

# ==============================
# 🔊 VOICE
# ==============================
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    print(f"A.L.F.R.E.D: {text}")
    engine.say(text)
    engine.runAndWait()

# ==============================
# 🎤 LISTEN
# ==============================
recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("🎙 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"✅ HEARD: {command}")   # IMPORTANT DEBUG
        return command
    except:
        print("❌ Could not understand")
        return ""

# ==============================
# 🛡 SAFETY
# ==============================
ALLOWED_ACTIONS = ["open", "search", "time", "system", "exit", "play"]

def is_safe(command):
    return any(word in command for word in ALLOWED_ACTIONS)

# ==============================
# 🖥 SYSTEM INFO
# ==============================
def system_info():
    return {
        "OS": platform.system(),
        "Version": platform.version(),
        "Processor": platform.processor(),
    }

# ==============================
# 🌐 WEB
# ==============================
def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

# ==============================
# 🖥 APP CONTROL
# ==============================
import os

def open_app(app_name):
    try:
        # Try direct command
        subprocess.Popen(app_name)
        return
    except:
        pass

    # Search in common paths
    paths = [
        os.environ.get("PROGRAMFILES"),
        os.environ.get("PROGRAMFILES(X86)"),
        os.environ.get("LOCALAPPDATA")
    ]

    for path in paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if app_name.lower() in file.lower() and file.endswith(".exe"):
                    try:
                        subprocess.Popen(os.path.join(root, file))
                        speak(f"Opening {app_name}")
                        return
                    except:
                        pass

    speak("I couldn't find that app")

# ==============================
# 🎯 INTENT DETECTION
# ==============================
def detect_intent(command):
    if any(w in command for w in ["open", "launch", "start"]):
        if any(w in command for w in ["chrome", "browser"]):
            return ("open_app", "chrome")
        if "notepad" in command:
            return ("open_app", "notepad")

    if "youtube" in command or "video" in command:
        return ("open_app", "youtube")

    if any(w in command for w in ["music", "song", "play"]):
        return ("play_music", None)

    if any(w in command for w in ["search", "google"]):
        return ("search", command)

    if "time" in command:
        return ("time", None)

    if "system" in command:
        return ("system", None)

    if "exit" in command:
        return ("exit", None)

    return ("ai", command)

# ==============================
# 🧠 OFFLINE AI (MISTRAL via Ollama)
# ==============================
def offline_ai(command):
    try:
        prompt = f"""
You are A.L.F.R.E.D, a highly intelligent personal AI assistant inspired by Tony Stark.
Be concise, clear, and slightly witty.
Give helpful, direct answers.

User: {command}
A.L.F.R.E.D:
"""

        res = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        return res.json()["response"]

    except:
        return None

# ==============================
# 🌐 ONLINE AI
# ==============================
def online_ai(prompt):
    if not USE_ONLINE_AI:
        return None
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except:
        return None

# ==============================
# 🔀 AI ROUTER
# ==============================
def ai_brain(command):
    # Fast/simple → offline
    if len(command.split()) < 8:
        res = offline_ai(command)
        if res:
            return res

    # Complex → online
    res = online_ai(command)
    if res:
        return res

    return "I couldn't process that."

# ==============================
# 🧠 COMMAND PROCESSOR
# ==============================
def process_command(command):
    if not is_safe(command):
        speak("Blocked by safety protocol")
        return

    intent, data = detect_intent(command)
    print("⚙ Processing:", command)

    if intent == "open_app":
        speak(f"Opening {data}")
        open_app(data)

    elif intent == "play_music":
        speak("Playing music")
        webbrowser.open("https://music.youtube.com")

    elif intent == "search":
        query = command.replace("search", "")
        speak(f"Searching {query}")
        search_web(query)

    elif intent == "time":
        speak(datetime.datetime.now().strftime("%H:%M"))

    elif intent == "system":
        info = system_info()
        for k, v in info.items():
            speak(f"{k} {v}")

    elif intent == "ai":
        speak("Thinking...")
        reply = ai_brain(command)
        speak(reply)

    elif intent == "exit":
        speak("Shutting down")
        exit()

# ==============================
# 🧬 WAKE SYSTEM
# ==============================
WAKE_WORDS = ["alfred", "al fred"]

def wake_listener():
    while True:
        command = listen()

        if any(w in command for w in WAKE_WORDS):
            speak("Yes")

            # 🔥 Extract command after wake word
            for w in WAKE_WORDS:
                command = command.replace(w, "").strip()

            if command:
                process_command(command)
            else:
                command_mode()

# ==============================
# 🔁 COMMAND MODE
# ==============================
def command_mode():
    speak("Command mode activated")

    while True:
        command = listen()

        if not command:
            continue

        if "sleep" in command or "stop" in command:
            speak("Returning to standby")
            break

        process_command(command)

# ==============================
# 🖥 HUD
# ==============================
def hud():
    print("""
    ===============================
        A.L.F.R.E.D ONLINE
    ===============================
    Wake Word: Alfred
    Brain: Phi (Offline) + Optional OpenAI
    ===============================
    """)

def text_input_mode():
    while True:
        cmd = input("\n⌨️ Type Command: ").lower()

        if cmd == "exit":
            break

        if cmd:
            process_command(cmd)

# ==============================
# 🚀 START
# ==============================
if __name__ == "__main__":
    hud()
    speak("A.L.F.R.E.D initialized")

    voice_thread = threading.Thread(target=wake_listener)
    text_thread = threading.Thread(target=text_input_mode)

    voice_thread.start()
    text_thread.start()

    voice_thread.join()
    text_thread.join()
