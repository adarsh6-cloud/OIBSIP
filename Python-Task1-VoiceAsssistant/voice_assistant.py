import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import re
import ast
import operator
import threading
import urllib.parse
import urllib.request
import json


# ---------------- VOICE ENGINE ----------------

engine = pyttsx3.init()
engine.setProperty("rate", 170)


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# ---------------- LISTEN ----------------

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

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
            speak("Sorry, I could not understand you.")
            return ""

        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""

        except Exception as e:
            print("Error:", e)
            speak("Something went wrong while listening.")
            return ""


# ---------------- TIME ----------------

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak("The current time is " + current_time)


# ---------------- DATE ----------------

def tell_date():
    current_date = datetime.datetime.now().strftime("%d %B %Y")
    speak("Today's date is " + current_date)


# ---------------- GOOGLE SEARCH ----------------

def google_search(query):
    if query:
        speak("Searching for " + query)
        url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        webbrowser.open(url)
    else:
        speak("Please tell me what you want to search.")


# ---------------- YOUTUBE ----------------

def youtube_search(query):
    if query:
        speak("Searching YouTube for " + query)
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
        webbrowser.open(url)
    else:
        speak("Please tell me what you want to watch.")


# ---------------- WIKIPEDIA ----------------

def wikipedia_search(query):
    if query:
        speak("Searching Wikipedia for " + query)
        url = "https://en.wikipedia.org/wiki/Special:Search?search=" + urllib.parse.quote(query)
        webbrowser.open(url)
    else:
        speak("Please tell me what you want to know.")


# ---------------- OPEN APPLICATIONS ----------------

def open_application(command):

    if "notepad" in command:
        speak("Opening Notepad.")
        os.system("start notepad")

    elif "calculator" in command:
        speak("Opening Calculator.")
        os.system("start calc")

    elif "chrome" in command:
        speak("Opening Chrome.")
        os.system("start chrome")

    elif "file explorer" in command or "explorer" in command:
        speak("Opening File Explorer.")
        os.system("start explorer")

    else:
        return False

    return True


# ---------------- CALCULATOR ----------------

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def calculate_expression(expression):

    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("multiply", "*")
    expression = expression.replace("times", "*")
    expression = expression.replace("divided by", "/")
    expression = expression.replace("divide", "/")

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError

            if isinstance(node, ast.BinOp):
                left = evaluate(node.left)
                right = evaluate(node.right)
                operation = operators.get(type(node.op))

                if operation is None:
                    raise ValueError

                return operation(left, right)

            raise ValueError

        result = evaluate(tree)

        speak("The answer is " + str(result))

    except Exception:
        speak("Sorry, I could not calculate that.")


# ---------------- NOTES ----------------

def save_note(note):

    if not note:
        speak("Please tell me what I should write.")
        return

    with open("notes.txt", "a", encoding="utf-8") as file:
        time_now = datetime.datetime.now().strftime("%d %B %Y %I:%M %p")
        file.write(f"[{time_now}] {note}\n")

    speak("Your note has been saved.")


# ---------------- READ NOTES ----------------

def read_notes():

    if not os.path.exists("notes.txt"):
        speak("You don't have any saved notes.")
        return

    with open("notes.txt", "r", encoding="utf-8") as file:
        notes = file.readlines()

    if not notes:
        speak("You don't have any saved notes.")
        return

    speak("Here are your saved notes.")

    for note in notes[-5:]:
        print(note.strip())
        speak(note.strip())


# ---------------- WEATHER ----------------

def get_weather(city):

    if not city:
        speak("Please tell me the city name.")
        return

    try:
        url = "https://wttr.in/" + urllib.parse.quote(city) + "?format=j1"

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        description = current["weatherDesc"][0]["value"]

        speak(
            f"The weather in {city} is {description}. "
            f"The temperature is {temperature} degrees Celsius."
        )

    except Exception:
        speak("Sorry, I could not get the weather right now.")


# ---------------- REMINDER ----------------

def reminder_function(message):

    speak("Reminder: " + message)


def set_reminder(command):

    pattern = r"remind me in (\d+) (second|seconds|minute|minutes|hour|hours) (?:to )?(.+)"

    match = re.search(pattern, command)

    if not match:
        speak(
            "Please say something like: "
            "remind me in 10 minutes to drink water."
        )
        return

    amount = int(match.group(1))
    unit = match.group(2)
    message = match.group(3)

    if "hour" in unit:
        seconds = amount * 3600
    elif "minute" in unit:
        seconds = amount * 60
    else:
        seconds = amount

    speak(f"Okay, I will remind you in {amount} {unit}.")

    timer = threading.Timer(
        seconds,
        reminder_function,
        args=[message]
    )

    timer.daemon = True
    timer.start()


# ---------------- DAY INFORMATION ----------------

def day_information():

    today = datetime.datetime.now()

    day = today.strftime("%A")
    date = today.strftime("%d %B %Y")

    speak(f"Today is {day}, {date}.")


# ---------------- MAIN ASSISTANT ----------------

def main():

    speak(
        "Hello! I am your advanced voice assistant. "
        "How can I help you?"
    )

    while True:

        command = listen()

        if not command:
            continue

        # -------- GREETING --------

        if "hello" in command or "hi" in command:
            speak("Hello! Nice to talk to you.")

        # -------- TIME --------

        elif "time" in command:
            tell_time()

        # -------- DATE --------

        elif "date" in command:
            tell_date()

        # -------- TODAY / DAY --------

        elif "today" in command or "day" in command:
            day_information()

        # -------- GOOGLE SEARCH --------

        elif command.startswith("search"):
            search_query = command.replace("search", "", 1).strip()
            google_search(search_query)

        # -------- YOUTUBE --------

        elif "youtube" in command:

            query = command.replace("youtube", "").strip()

            if "play" in query:
                query = query.replace("play", "").strip()

            youtube_search(query)

        elif command.startswith("play"):
            query = command.replace("play", "", 1).strip()
            youtube_search(query)

        # -------- WIKIPEDIA --------

        elif "wikipedia" in command:

            query = command.replace("wikipedia", "").strip()
            wikipedia_search(query)

        elif command.startswith("who is"):
            query = command.replace("who is", "", 1).strip()
            wikipedia_search(query)

        elif command.startswith("what is"):
            query = command.replace("what is", "", 1).strip()
            wikipedia_search(query)

        # -------- WEATHER --------

        elif "weather" in command:

            city = command.replace("weather", "").strip()

            if city.startswith("in "):
                city = city.replace("in ", "", 1).strip()

            get_weather(city)

        # -------- CALCULATOR --------

        elif command.startswith("calculate"):

            expression = command.replace(
                "calculate", "", 1
            ).strip()

            calculate_expression(expression)

        elif "what is" in command and any(
            symbol in command for symbol in ["+", "-", "*", "/"]
        ):

            expression = command.replace("what is", "", 1).strip()
            calculate_expression(expression)

        # -------- NOTES --------

        elif command.startswith("take a note"):
            note = command.replace("take a note", "", 1).strip()
            save_note(note)

        elif command.startswith("note"):
            note = command.replace("note", "", 1).strip()
            save_note(note)

        # -------- READ NOTES --------

        elif "read my notes" in command:
            read_notes()

        # -------- REMINDER --------

        elif "remind me" in command:
            set_reminder(command)

        # -------- OPEN APPLICATION --------

        elif command.startswith("open"):

            opened = open_application(command)

            if not opened:
                app_name = command.replace("open", "", 1).strip()

                if app_name:
                    speak("I will search for " + app_name)
                    google_search(app_name)

                else:
                    speak("Please tell me what you want to open.")

        # -------- CONVERSATION --------

        elif "how are you" in command:
            speak("I am doing great. Thank you for asking!")

        elif "your name" in command:
            speak("My name is your advanced voice assistant.")

        elif "who are you" in command:
            speak(
                "I am a Python based voice assistant "
                "created to help you with different tasks."
            )

        elif "thank you" in command or "thanks" in command:
            speak("You're welcome!")

        # -------- EXIT --------

        elif (
            "bye" in command
            or "exit" in command
            or "stop" in command
            or "quit" in command
        ):
            speak("Goodbye! Have a nice day.")
            break

        # -------- UNKNOWN COMMAND --------

        else:
            speak(
                "I don't understand that command yet. "
                "You can ask me to search Google, search YouTube, "
                "check weather, calculate something, save a note, "
                "set a reminder, or open an application."
            )


# ---------------- START PROGRAM ----------------

if __name__ == "__main__":
    main()