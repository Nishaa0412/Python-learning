import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import openai
from gtts import gTTS
import pygame
import os
import tempfile
from dotenv import load_dotenv
import musicLibrary  # Make sure this file exists and contains your music dictionary

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
newsapi = os.getenv("NEWSAPI_KEY")

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
            tts.save(temp_filename)

        pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(temp_filename)
    except Exception as e:
        print(f"Speaking error: {e}")


def aiProcess(command):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
                {"role": "user", "content": command}
            ]
        )
        return completion['choices'][0]['message']['content']
    except Exception as e:
        return f"Sorry, I encountered an error with OpenAI: {e}"


def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")

    elif c.startswith("play "):
        song = c.split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find {song} in your music library.")

    elif "news" in c:
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                for article in articles[:5]:  # Read only top 5 headlines
                    speak(article.get('title', 'No title'))
            else:
                speak("Sorry, I couldn't fetch the news.")
        except Exception as e:
            speak(f"Failed to get news: {e}")

    elif "stop" in c or "exit" in c:
        speak("Goodbye!")
        exit()

    else:
        output = aiProcess(c)
        speak(output)


# Main program
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            print("Listening for wake word 'Jarvis'...")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
            wake_word = recognizer.recognize_google(audio).lower()

            if wake_word == "jarvis":
                speak("Yes?")
                print("Jarvis activated, waiting for command...")

                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                command = recognizer.recognize_google(audio)
                print(f"Command received: {command}")
                processCommand(command)

        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as err:
            print(f"Unexpected error: {err}")
