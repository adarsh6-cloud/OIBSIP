import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I could not understand you.")
        return ""

    except sr.RequestError:
        speak("Sorry, the speech service is unavailable.")
        return ""


speak("Hello! I am your Python voice assistant. How can I help you?")

while True:
    command = listen()

    if "hello" in command or "hi" in command:
        speak("Hello! Nice to meet you.")

    elif "your name" in command:
        speak("My name is your Python voice assistant.")

    elif "bye" in command or "exit" in command or "stop" in command:
        speak("Goodbye! Have a nice day.")
        break

    elif command:
        speak("I heard you say " + command)