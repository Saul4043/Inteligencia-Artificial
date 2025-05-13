import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import requests
import os
import webbrowser
import json
import hashlib
import asyncio
from bleak import BleakScanner
import pywifi
from pywifi import const, Profile
from googleapiclient.discovery import build
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from newsapi import NewsApiClient
import openai
import google.generativeai as genai
import whisper
import tkinter as tk
from tkinter import scrolledtext

# Configuración de API Keys
OPENAI_API_KEY = "tu_openai_api_key"
GOOGLE_API_KEY = "tu_google_api_key"

genai.configure(api_key=GOOGLE_API_KEY)
openai.api_key

# Inicializar Whisper
whisper_model = whisper.load_model("base")

# Inicializar el motor de texto a voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Escuchando...")
        try:
            audio = recognizer.listen(source, timeout=5)
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            result = whisper_model.transcribe("temp_audio.wav", language="mex")
            command = result["text"].strip().lower()
            print(f"Dijiste: {command}\n")
            return command
        except sr.UnknownValueError:
            speak("No entendí lo que dijiste.")
        except sr.RequestError:
            speak("No puedo conectarme a Internet.")
        except sr.WaitTimeoutError:
            speak("No detecté ningún sonido.")
        return ""

def authenticate(password):
    """Verifica la contraseña de acceso sin hash."""
    stored_password = "saul"
    return password == stored_password

def get_weather(city):
    """Obtiene el clima de una ciudad."""
    api_key = "tu_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return "No encontré la ciudad."
        temp = data["main"]["temp"]
        desc = data["weather"]["description"]
        return f"El clima en {city} es {temp}°C con {desc}."
    except requests.RequestException:
        return "Error al obtener el clima."

async def scan_bluetooth():
    devices = await BleakScanner.discover()
    if devices:
        speak("Dispositivos Bluetooth encontrados:")
        for device in devices:
            speak(f"{device.name} con dirección {device.address}")
    else:
        speak("No se encontraron dispositivos Bluetooth.")

def connect_wifi(ssid, password):
    """Conecta a una red WiFi específica."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.disconnect()
    profile = Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    iface.remove_all_network_profiles()
    iface.add_network_profile(profile)
    iface.connect(profile)
    speak(f"Intentando conectar a la red {ssid}.")

def scan_wifi():
    """Escanea redes WiFi disponibles."""
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    networks = iface.scan_results()
    if networks:
        speak("Redes WiFi disponibles:")
        for network in networks[:5]:
            speak(network.ssid)
    else:
        speak("No se encontraron redes WiFi.")

def chat_with_gpt(prompt):
    """Interactúa con OpenAI GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def chat_with_gemini(prompt):
    """Interactúa con Google Gemini AI."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

def handle_command(command):
    if "hora" in command:
        speak(f"Son las {datetime.datetime.now().strftime('%H:%M')}.")
        
    elif "clima" in command:
        speak("Dime la ciudad.")
        city = listen()
        
        if city:
            speak(get_weather(city))
    elif "escanea bluetooth" in command:
        asyncio.run(scan_bluetooth())
    elif "escanea wifi" in command:
        scan_wifi()
    elif "conéctate a wifi" in command:
        speak("Dime el nombre de la red WiFi.")
        ssid = listen()
        speak("Dime la contraseña de la red WiFi.")
        password = listen()
        connect_wifi(ssid, password)
    elif "pregunta a gpt" in command:
        speak("¿Qué quieres preguntarle a GPT?")
        prompt = listen()
        response = chat_with_gpt(prompt)
        speak(response)
    elif "pregunta a gemini" in command:
        speak("¿Qué quieres preguntarle a Gemini?")
        prompt = listen()
        response = chat_with_gemini(prompt)
        speak(response)
    elif "salir" in command:
        speak("Hasta luego.")
        return False
    else:
        speak("No entiendo ese comando.")
        speak(response)
        update_textbox(f"Usuario: {command}\nJarvis: {response}\n")
    return True

    
def update_textbox(text):
    text_box.insert(tk.END, text + "\n")
    text_box.see(tk.END)

def on_listen_button():
    command = listen()
    if command:
        handle_command(command)

# Interfaz gráfica
root = tk.Tk()
root.title("Jarvis - Asistente Virtual")
root.geometry("500x400")

text_box = scrolledtext.ScrolledText(root, width=60, height=15, wrap=tk.WORD)
text_box.pack(pady=10)

listen_button = tk.Button(root, text="Escuchar", command=on_listen_button, font=("Arial", 12))
listen_button.pack()

if __name__ == "__main__":
    speak("Hola,  ingrese su contraseña por favor.")
    user_password = input("Contraseña: ")
    if authenticate(user_password):
        speak("Acceso concedido. ¿Cómo puedo ayudarte el dia de hoy?")
        while True:
            command = listen()
            if command and not handle_command(command):
                break
    else:
        speak("Acceso denegado. Cerrando el asistente.")