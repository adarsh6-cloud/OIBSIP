import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            speak("I did not hear anything. Please try again.")
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand you. Please repeat.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""


def main():
    speak("Hello! I am your voice assistant. How can I help you?")

    while True:
        command = listen()

        if not command:
            continue

        if "hello" in command or "hi" in command:
            speak("Hello! How can I help you?")

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak("The current time is " + current_time)

        elif "date" in command or "today" in command:
            current_date = datetime.datetime.now().strftime("%d %B %Y")
            speak("Today's date is " + current_date)

        elif "search" in command:
            search_query = command.replace("search", "").strip()

            if search_query:
                speak("Searching for " + search_query)
                url = "https://www.google.com/search?q=" + search_query.replace(" ", "+")
                webbrowser.open(url)
            else:
                speak("Please tell me what you want to search.")

        elif "bye" in command or "exit" in command or "stop" in command:
            speak("Goodbye! Have a nice day.")
            break

        else:
            speak("I do not understand that command. Please try again.")


if __name__ == "__main__":
    main()