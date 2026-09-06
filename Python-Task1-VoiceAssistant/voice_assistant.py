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
import smtplib
import ssl
import configparser
import time


# ============================================================
# ADVANCED PYTHON VOICE ASSISTANT - OIBSIP TASK 1
# ============================================================

APP_NAME = "Advanced Voice Assistant"

# ---------------- VOICE ENGINE ----------------

def speak(text):
    """Print and speak every assistant response."""
    print(f"Assistant: {text}")

    try:
        voice_engine = pyttsx3.init()
        voice_engine.setProperty("rate", 150)
        voice_engine.setProperty("volume", 1.0)

        voice_engine.say(str(text))
        voice_engine.runAndWait()
        voice_engine.stop()

    except Exception as error:
        print("Speech error:", error)
# ---------------- SPEECH RECOGNITION ----------------

def listen():
    """Capture speech from microphone and convert it to text."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.5

    try:
        with sr.Microphone() as source:
            print("\nListening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        command = recognizer.recognize_google(audio, language="en-IN")
        command = command.lower().strip()
        print("You:", command)
        return command

    except sr.WaitTimeoutError:
        speak("I did not hear anything. Please try again.")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand you. Please repeat.")
    except sr.RequestError:
        speak("Speech recognition is unavailable. Please check your internet connection.")
    except OSError:
        speak("I could not access the microphone. Please check your microphone settings.")
    except Exception as error:
        print("Listening error:", error)
        speak("Something went wrong while listening.")

    return ""


# ============================================================
# BASIC FEATURES
# ============================================================

def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")


def tell_date():
    current_date = datetime.datetime.now().strftime("%d %B %Y")
    speak(f"Today's date is {current_date}.")


def day_information():
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%A')}, {now.strftime('%d %B %Y')}.")


def google_search(query):
    if not query:
        speak("Please tell me what you want to search.")
        return

    speak(f"Searching Google for {query}.")
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)


def youtube_search(query):
    if not query:
        speak("Please tell me what you want to watch.")
        return

    speak(f"Searching YouTube for {query}.")
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    webbrowser.open(url)


def wikipedia_search(query):
    if not query:
        speak("Please tell me what you want to know.")
        return

    speak(f"Searching Wikipedia for {query}.")
    url = "https://en.wikipedia.org/wiki/Special:Search?search=" + urllib.parse.quote(query)
    webbrowser.open(url)


# ============================================================
# APPLICATION CONTROL
# ============================================================

def open_application(command):
    apps = {
        "notepad": "start notepad",
        "calculator": "start calc",
        "chrome": "start chrome",
        "file explorer": "start explorer",
        "explorer": "start explorer"
    }

    for app_name, command_to_run in apps.items():
        if app_name in command:
            speak(f"Opening {app_name}.")
            os.system(command_to_run)
            return True

    return False


# ============================================================
# SAFE CALCULATOR
# ============================================================

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def calculate_expression(expression):
    expression = expression.lower()

    replacements = {
        "plus": "+",
        "minus": "-",
        "multiplied by": "*",
        "multiply by": "*",
        "multiply": "*",
        "times": "*",
        "divided by": "/",
        "divide by": "/",
        "divide": "/"
    }

    for word, symbol in replacements.items():
        expression = expression.replace(word, symbol)

    expression = expression.replace("what is", "").strip()

    # Only allow calculator characters.
    if not re.fullmatch(r"[0-9+\-*/().%\s]+", expression):
        speak("Sorry, I could not calculate that safely.")
        return

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value

            if isinstance(node, ast.BinOp):
                left = evaluate(node.left)
                right = evaluate(node.right)
                operation = OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError

                return operation(left, right)

            if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                return -evaluate(node.operand)

            raise ValueError

        result = evaluate(tree)
        speak(f"The answer is {result}.")

    except Exception:
        speak("Sorry, I could not calculate that.")


# ============================================================
# NOTES
# ============================================================

NOTES_FILE = "notes.txt"


def save_note(note):
    if not note:
        speak("Please tell me what I should write.")
        return

    timestamp = datetime.datetime.now().strftime("%d %B %Y %I:%M %p")

    with open(NOTES_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {note}\n")

    speak("Your note has been saved.")


def read_notes():
    if not os.path.exists(NOTES_FILE):
        speak("You don't have any saved notes.")
        return

    with open(NOTES_FILE, "r", encoding="utf-8") as file:
        notes = [line.strip() for line in file.readlines() if line.strip()]

    if not notes:
        speak("You don't have any saved notes.")
        return

    speak(f"You have {len(notes)} saved notes.")

    for note in notes[-5:]:
        print(note)
        speak(note)


# ============================================================
# WEATHER API
# Uses wttr.in's JSON endpoint, so no API key is required.
# ============================================================

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
            data = json.loads(response.read().decode("utf-8"))

        current = data["current_condition"][0]
        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]

        speak(
            f"The current weather in {city} is {description}. "
            f"The temperature is {temperature} degrees Celsius, "
            f"it feels like {feels_like} degrees, "
            f"and the humidity is {humidity} percent."
        )

    except Exception as error:
        print("Weather error:", error)
        speak("Sorry, I could not get the weather right now.")


# ============================================================
# TIMED REMINDERS
# ============================================================

active_timers = []


def reminder_function(message):
    speak(f"Reminder: {message}")


def set_reminder(command):
    pattern = (
        r"remind me in (\d+)\s*"
        r"(second|seconds|minute|minutes|hour|hours)"
        r"(?:\s+to)?\s+(.+)"
    )

    match = re.search(pattern, command.lower())

    if not match:
        speak(
            "Please say something like: "
            "remind me in 10 minutes to drink water."
        )
        return

    amount = int(match.group(1))
    unit = match.group(2)
    message = match.group(3).strip()

    if "hour" in unit:
        seconds = amount * 3600
    elif "minute" in unit:
        seconds = amount * 60
    else:
        seconds = amount

    speak(f"Okay. I will remind you in {amount} {unit}.")

    timer = threading.Timer(seconds, reminder_function, args=[message])
    timer.daemon = True
    active_timers.append(timer)
    timer.start()


# ============================================================
# GENERAL KNOWLEDGE - LOCAL KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = {
    "what is python": "Python is a high level, interpreted programming language known for its simple syntax and wide use in automation, data science, web development and artificial intelligence.",
    "who created python": "Python was created by Guido van Rossum.",
    "what is artificial intelligence": "Artificial intelligence is the field of computer science focused on creating systems that can perform tasks that normally require human intelligence.",
    "what is machine learning": "Machine learning is a branch of artificial intelligence where computers learn patterns from data to make predictions or decisions.",
    "what is api": "An API is an application programming interface that allows different software systems to communicate with each other.",
    "what is rest api": "A REST API is a web API that follows REST principles and commonly uses HTTP methods such as GET, POST, PUT and DELETE.",
    "what is github": "GitHub is a platform for hosting and collaborating on software projects using Git version control.",
    "what is nlp": "Natural language processing is a field of artificial intelligence that helps computers understand and work with human language."
}


def answer_general_question(command):
    normalized = re.sub(r"\s+", " ", command.lower()).strip()

    # Exact and close phrase matching.
    for question, answer in KNOWLEDGE_BASE.items():
        if question in normalized or normalized in question:
            speak(answer)
            return True

    return False


# ============================================================
# CUSTOM COMMANDS
# ============================================================

CONFIG_FILE = "custom_commands.ini"


def create_default_config():
    if os.path.exists(CONFIG_FILE):
        return

    config = configparser.ConfigParser()
    config["commands"] = {
        "open github": "https://github.com",
        "open linkedin": "https://www.linkedin.com",
        "open google": "https://www.google.com"
    }

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        config.write(file)


def load_custom_commands():
    create_default_config()

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")

    return dict(config["commands"]) if "commands" in config else {}


def execute_custom_command(command):
    commands = load_custom_commands()

    for trigger, action in commands.items():
        if command.strip() == trigger.strip().lower():
            if action.startswith(("http://", "https://")):
                speak(f"Opening {trigger}.")
                webbrowser.open(action)
                return True

            # For safety, config commands are not executed as shell commands.
            speak(f"Custom command found, but this action is not a web link: {action}")
            return True

    return False


# ============================================================
# EMAIL
# ============================================================

def load_email_config():
    """
    Reads email settings from environment variables.

    Required:
      VOICE_EMAIL_ADDRESS
      VOICE_EMAIL_PASSWORD
      VOICE_SMTP_SERVER
      VOICE_SMTP_PORT

    Example for Gmail:
      VOICE_SMTP_SERVER=smtp.gmail.com
      VOICE_SMTP_PORT=465

    Use an app password where the email provider requires it.
    Never put your real password directly in this source code.
    """
    return {
        "address": os.getenv("VOICE_EMAIL_ADDRESS"),
        "password": os.getenv("VOICE_EMAIL_PASSWORD"),
        "server": os.getenv("VOICE_SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("VOICE_SMTP_PORT", "465"))
    }


def send_email(recipient, subject, body):
    settings = load_email_config()

    if not settings["address"] or not settings["password"]:
        speak(
            "Email is not configured yet. "
            "Please set the required email environment variables."
        )
        return False

    try:
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(
            settings["server"],
            settings["port"],
            context=context,
            timeout=15
        ) as server:
            server.login(settings["address"], settings["password"])
            message = (
                f"From: {settings['address']}\n"
                f"To: {recipient}\n"
                f"Subject: {subject}\n\n"
                f"{body}"
            )
            server.sendmail(settings["address"], recipient, message)

        speak("The email has been sent successfully.")
        return True

    except Exception as error:
        print("Email error:", error)
        speak("I could not send the email. Please check your email settings.")
        return False


def send_email_by_voice():
    speak("Who should receive the email?")
    recipient = listen()

    if not recipient:
        return

    # Speech recognition often hears "at" and "dot" instead of email symbols.
    recipient = recipient.replace(" at ", "@")
    recipient = recipient.replace(" dot ", ".")
    recipient = recipient.replace(" ", "")

    if "@" not in recipient or "." not in recipient:
        speak(
            "I could not recognize a valid email address. "
            "You can type the address in the terminal."
        )
        recipient = input("Recipient email: ").strip()

    speak("What should be the subject?")
    subject = listen()

    if not subject:
        subject = "Message from Voice Assistant"

    speak("What should I say in the email?")
    body = listen()

    if not body:
        speak("I could not hear the email message.")
        return

    send_email(recipient, subject, body)


# ============================================================
# NATURAL LANGUAGE INTENT PARSER
# ============================================================

def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s@.+*/%()-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def parse_intent(command):
    """
    Lightweight NLU-style intent parser.
    It uses phrases/synonyms and extracts useful entities from
    free-form sentences instead of requiring one exact command.
    """

    command = normalize_text(command)

    # Exit
    if any(phrase in command for phrase in [
        "goodbye", "bye", "exit", "quit", "stop the assistant",
        "close yourself", "shutdown"
    ]):
        return "exit", None

    # Greeting
    if any(phrase in command for phrase in [
        "hello", "hi", "hey assistant", "good morning",
        "good afternoon", "good evening"
    ]):
        return "greeting", None

    # Time
    if any(phrase in command for phrase in [
        "what time", "current time", "tell me the time",
        "time is it", "time right now"
    ]) or command == "time":
        return "time", None

    # Date/day
    if any(phrase in command for phrase in [
        "today's date", "todays date", "what date",
        "current date", "what day is it", "which day"
    ]):
        return "date", None

    # Weather
    if "weather" in command or "temperature" in command:
        city = ""

        match = re.search(r"(?:weather|temperature)\s+(?:in|at|of)\s+(.+)", command)
        if match:
            city = match.group(1).strip()
        else:
            match = re.search(r"(?:weather|temperature)\s+(.+)", command)
            if match:
                city = match.group(1).strip()

        return "weather", city

    # Reminder
    if "remind me" in command or "set a reminder" in command:
        return "reminder", command

    # Email
    if any(phrase in command for phrase in [
        "send an email", "send email", "write an email",
        "email someone", "send a mail", "send mail"
    ]):
        return "email", None

    # Notes
    if any(phrase in command for phrase in [
        "read my notes", "read my note", "show my notes"
    ]):
        return "read_notes", None

    if any(phrase in command for phrase in [
        "take a note", "save a note", "write a note", "remember this"
    ]):
        note = re.sub(
            r"^(take a note|save a note|write a note|remember this)\s*",
            "",
            command
        ).strip()
        return "save_note", note

    # YouTube
    if "youtube" in command or command.startswith("play "):
        query = command.replace("youtube", "").strip()
        query = re.sub(r"^play\s+", "", query).strip()
        return "youtube", query

    # Wikipedia
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        return "wikipedia", query

    # Google search
    if any(phrase in command for phrase in [
        "search for", "search google for", "google search",
        "look up", "find information about", "search"
    ]):
        query = re.sub(
            r"^(search google for|search for|google search|look up|find information about|search)\s*",
            "",
            command
        ).strip()
        return "google", query

    # Applications
    if command.startswith("open "):
        return "open_application", command

    # Calculator
    if (
        command.startswith("calculate")
        or any(word in command for word in [
            "plus", "minus", "multiply", "times", "divided by"
        ])
        or re.search(r"\d+\s*[\+\-\*/%]\s*\d+", command)
    ):
        return "calculate", command

    # General knowledge
    if any(command.startswith(prefix) for prefix in [
        "what is", "what are", "who is", "who was",
        "where is", "why is", "how does", "define"
    ]):
        return "knowledge", command

    # Conversation
    if any(phrase in command for phrase in [
        "how are you", "how r u", "how are u"
    ]):
        return "how_are_you", None

    if "your name" in command or "who are you" in command:
        return "name", None

    if "thank you" in command or "thanks" in command:
        return "thanks", None

    # Custom commands are checked last.
    if execute_custom_command(command):
        return "custom", None

    return "unknown", command


# ============================================================
# COMMAND ROUTER
# ============================================================

def handle_command(command):
    intent, data = parse_intent(command)

    if intent == "greeting":
        speak("Hello! Nice to talk to you.")

    elif intent == "time":
        tell_time()

    elif intent == "date":
        tell_date()

    elif intent == "weather":
        if not data:
            speak("Which city should I check?")
            data = listen()

        get_weather(data)

    elif intent == "reminder":
        set_reminder(data)

    elif intent == "email":
        send_email_by_voice()

    elif intent == "read_notes":
        read_notes()

    elif intent == "save_note":
        if not data:
            speak("What should I write?")
            data = listen()
        save_note(data)

    elif intent == "youtube":
        youtube_search(data)

    elif intent == "wikipedia":
        wikipedia_search(data)

    elif intent == "google":
        google_search(data)

    elif intent == "open_application":
        if not open_application(data):
            app_name = data.replace("open", "", 1).strip()
            speak(f"I don't have a direct application handler for {app_name}.")
            google_search(app_name)

    elif intent == "calculate":
        calculate_expression(data)

    elif intent == "knowledge":
        if not answer_general_question(data):
            speak("I don't have that answer in my local knowledge base. I can search the web for you.")
            google_search(data)

    elif intent == "how_are_you":
        speak("I am doing great. Thank you for asking!")

    elif intent == "name":
        speak(
            "My name is your advanced Python voice assistant. "
            "I can understand several natural language commands."
        )

    elif intent == "thanks":
        speak("You're welcome!")

    elif intent == "custom":
        pass

    elif intent == "exit":
        speak("Goodbye! Have a nice day.")
        return False

    else:
        speak(
            "I don't understand that yet. You can ask me about the time, "
            "date, weather, reminders, email, notes, calculations, "
            "web search, YouTube, Wikipedia, or applications."
        )

    return True


# ============================================================
# MAIN
# ============================================================

def main():
    create_default_config()

    speak(
        "Hello! I am your advanced Python voice assistant. "
        "I can help with time, date, weather, reminders, email, "
        "notes, calculations, web searches and more."
    )

    while True:
        command = listen()

        if not command:
            continue

        if not handle_command(command):
            break


if __name__ == "__main__":
    main()
