import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
from config import apikey
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)


def say(text):
    engine.say(text)
    engine.runAndWait()


chatStr = ""


def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reply = response["choices"][0]["text"].strip()
    say(reply)
    chatStr += f"{reply}\n"
    return reply


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    filename = f"Openai/{random.randint(1, 100000)}.txt"
    with open(filename, "w") as f:
        f.write(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print("Error: Could not recognize speech.")
            return ""


if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        query = takeCommand().lower()
        if query == "":
            continue

        sites = {"youtube": "https://www.youtube.com", "wikipedia": "https://www.wikipedia.com",
                 "google": "https://www.google.com"}
        for site, url in sites.items():
            if f"open {site}" in query:
                say(f"Opening {site} maam...")
                webbrowser.open(url)
                continue

        if "open music" in query:
            musicPath = "C:\\Users\\YourUsername\\Music\\song.mp3"  # Update path
            os.system(f'start "" "{musicPath}"')

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes")

        elif "using artificial intelligence" in query:
            ai(prompt=query)

        elif "jarvis quit" in query:
            say("Goodbye, maam)
            exit()

        elif "reset chat" in query:
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)

        # say(query)