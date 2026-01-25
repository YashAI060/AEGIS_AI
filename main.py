import speech_recognition as sr
import pygame
import requests
import os
import sys
import time
import datetime
import pywhatkit
import pyautogui
from google import genai 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QMovie, QColor, QFont
from PyQt5.QtCore import QThread, pyqtSignal, Qt

CONTACTS = {
    "jami": "+923063250169",  
    "vishal": "+923423633554",
    "add contact": "+92"
}


GENAI_API_KEY = ""
ELEVENLABS_API_KEY = ""
WEATHER_API_KEY = ""

#'pNInz6obpgDQGcFmaJgB' (Adam) 
VOICE_ID = "pNInz6obpgDQGcFmaJgB" 


pygame.mixer.init()

def speak(text):
    """Speaks using ElevenLabs API"""
    print(f"AEGIS: {text}") 
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2", 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            with open("output.mp3", "wb") as f:
                f.write(response.content)
            
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            os.remove("output.mp3") 
        else:
            print(f"11Labs Error: {response.text}")

    except Exception as e:
        print(f"Audio Error: {e}")

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res["cod"] != "404":
            return f"{res['main']['temp']}°C with {res['weather'][0]['description']}."
        return "City not found."
    except: return "Connection Error."

client = None
try:
    if "PASTE" not in GENAI_API_KEY:
        client = genai.Client(api_key=GENAI_API_KEY)
except:
    pass


try:
    import face_unlock
except ImportError:
    pass

def ask_ai(query):
    if client is None:
        return "API Key check karo."
    try:
        sys_instruction = (
            "You are AEGIS. Detect language. "
            "1. If Hindi/Hinglish -> Reply in Hinglish. "
            "2. If English -> Reply in English. "
            "Short answer (1 sentence). Tone: Heavy & Professional."
        )
        
        
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=sys_instruction + "\nUser: " + query
        )
        return response.text.replace("*", "").replace("#", "")

    except Exception as e:
        print(f"\n[DEBUG ERROR]: {e}")
        
        if "429" in str(e):
            return "Sir, aaj ka free quota khatam ho gaya hai. New API Key chahiye."
        return "Server error."

def take_command():
    r = sr.Recognizer()
    with sr.Microphone(device_index=3) as source:
        print("\rListening...", end="", flush=True)
        try:
            r.pause_threshold = 1.0
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return "None"

    try:
        print("\rProcessing... ", end="", flush=True)
        query = r.recognize_google(audio, language='en-in') 
        print(f"\nUser: {query}")
    except:
        return "None"
    return query.lower()


if __name__ == "__main__":
    speak("Systems initialized.")
    
    verified = True
    if 'face_unlock' in sys.modules:
        speak("Scanning biometric ID...")
        if not face_unlock.recognize_user():
            verified = False

    if verified:
        speak("Welcome back, Sir. Ready for commands.")
        
        while True:
            query = take_command()
            if query == "None": continue

            
            if 'weather' in query or 'mausam' in query:
                speak("Checking satellite data...")
                
                report = get_weather("Karachi") 
                speak(report)

            
            elif 'news' in query or 'khabrein' in query:
                speak("Fetching latest headlines...")
                pywhatkit.search("Latest News Pakistan") 
                speak("Here are the top stories.")

            elif 'whatsapp' in query:
                speak("Kisko message bhejna hai?")
                
                name = take_command()
                
                if name in CONTACTS:
                    speak(f"Okay, {name} ko kya message likhna hai?")
                    
                    msg = take_command()
                    
                    speak(f"Sending message to {name}...")
                    
                    pywhatkit.sendwhatmsg_instantly(CONTACTS[name], msg, 15, True, 4)
                    
                    
                    pyautogui.press('enter')
                    speak("Message sent successfully.")
                else:
                    speak("Sorry, ye naam meri contact list mein nahi hai.")

            elif 'volume up' in query or 'awaaz badhao' in query:
                speak("Volume increased.")
                pyautogui.press("volumeup")
                pyautogui.press("volumeup") 
                
            elif 'volume down' in query or 'awaaz kam' in query:
                speak("Volume decreased.")
                pyautogui.press("volumedown")
                pyautogui.press("volumedown")

            elif 'mute' in query or 'chup' in query:
                speak("System Muted.")
                pyautogui.press("volumemute")

            elif 'screenshot' in query:
                speak("Taking screenshot.")
                
                name = f"screenshot_{int(time.time())}.png"
                pyautogui.screenshot(name)
                speak("Screenshot saved.")

            elif 'minimize' in query or 'chupa do' in query:
                speak("Minimizing windows.")
                pyautogui.hotkey('win', 'd') 
            
            elif 'switch window' in query or 'badlo' in query:
                pyautogui.hotkey('alt', 'tab')
                
            elif 'shutdown system' in query: 
                speak("Shutting down the computer in 5 seconds.")
                os.system("shutdown /s /t 5") 
                break

            elif 'restart system' in query:
                speak("Restarting system.")
                os.system("shutdown /r /t 5")
                break

            elif 'stop' in query or 'exit' in query or 'band ho ja' in query:
                speak("Powering down. Goodbye.")
                break 

            elif 'time' in query or 'waqt' in query:
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"Current time is {strTime}")
            
            elif 'open vs code' in query:
                speak("Opening Visual Studio Code.")
                os.system("code .")

            elif 'play' in query:
                song = query.replace('play', '')
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)

            else:
                response = ask_ai(query)
                speak(response)
    else:
        speak("Access Denied.")
