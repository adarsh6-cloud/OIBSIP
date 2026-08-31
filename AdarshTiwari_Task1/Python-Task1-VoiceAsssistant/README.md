# 🎙️ Advanced Python Voice Assistant

An advanced Python-based voice assistant that listens to spoken commands, understands different types of requests, and responds using text-to-speech.

This project was developed as **OIBSIP Python Programming – Task 1: Voice Assistant**.

---

## 📌 Project Overview

This Voice Assistant uses **Speech Recognition** to capture commands through a microphone and **Text-to-Speech** to respond verbally.

It can perform several useful tasks such as:

* 🕐 Tell the current time and date
* 🌦️ Provide live weather information
* 🔎 Search Google
* ▶️ Search YouTube
* 📖 Search Wikipedia
* 🧮 Perform mathematical calculations
* 📝 Save and read notes
* ⏰ Set timed reminders
* 📧 Send emails using voice commands
* 💡 Answer general knowledge questions
* 💻 Open applications such as Chrome, Notepad and Calculator
* ⚙️ Execute custom commands
* 🗣️ Understand different natural-language phrases
* ❌ Handle speech recognition and microphone errors gracefully

---

## ✨ Features

### 🗣️ Voice Recognition

The assistant captures the user's voice through the microphone and converts it into text using `SpeechRecognition`.

### 🔊 Text-to-Speech

Every assistant response is spoken aloud using `pyttsx3`.

### 🕐 Time & Date

The assistant can tell:

* Current time
* Current date
* Current day

### 🌐 Web Search

The assistant can open searches directly in the browser:

* Google
* YouTube
* Wikipedia

Example commands:

```text
Search for Python programming
Search YouTube for Python tutorials
Search Wikipedia for Artificial Intelligence
```

### 🌦️ Live Weather

The assistant fetches current weather information using the **wttr.in JSON endpoint**.

It provides:

* Weather condition
* Temperature in Celsius
* Feels-like temperature
* Humidity

Example:

```text
What is the weather in Lucknow?
```

### ⏰ Timed Reminders

Users can set reminders using voice commands.

Example:

```text
Remind me in 10 seconds to drink water.
```

The assistant gives an audible reminder when the timer finishes.

### 📧 Email Sending

The assistant can send emails through voice commands using SMTP.

It can ask for:

1. Recipient email
2. Email subject
3. Email message

Email credentials are loaded from **environment variables** instead of being written directly into the source code.

### 📝 Notes

The assistant can save notes to `notes.txt` and read previously saved notes.

Examples:

```text
Take a note complete my Python project
```

```text
Read my notes
```

### 🧮 Safe Calculator

The assistant can perform mathematical calculations such as:

```text
What is 25 plus 15?
```

```text
Calculate 100 divided by 4
```

The calculator validates the expression before evaluating it for safer execution.

### 💡 General Knowledge

A local knowledge base is included for common questions about:

* Python
* Artificial Intelligence
* Machine Learning
* APIs
* REST APIs
* GitHub
* NLP

If an answer is not available in the local knowledge base, the assistant can perform a Google search.

### 💻 Application Control

The assistant can open supported applications:

```text
Open Notepad
Open Calculator
Open Chrome
Open File Explorer
```

### ⚙️ Custom Commands

Custom web commands can be stored in:

```text
custom_commands.ini
```

Default examples include:

```text
open github
open linkedin
open google
```

These commands can open the corresponding websites.

### 🧠 Natural Language Understanding

Instead of requiring only one exact command, the assistant uses a lightweight intent parser that recognizes different phrases and extracts useful information such as:

* Weather location
* Search query
* Reminder duration and message
* Notes
* Calculation expressions

---

## 🛠️ Technologies Used

* **Python**
* `SpeechRecognition`
* `pyttsx3`
* `datetime`
* `webbrowser`
* `urllib`
* `json`
* `smtplib`
* `ssl`
* `configparser`
* `threading`
* `ast`
* `operator`
* `re`

---

## 📂 Project Structure

```text
Advanced-Voice-Assistant/
│
├── voice_assistant.py
├── custom_commands.ini
├── notes.txt
├── README.md
└── screenshots/
    ├── screenshot1.png
    ├── screenshot2.png
    └── screenshot3.png
```

> `notes.txt` is created automatically when the assistant saves a note.

---

## ⚙️ Installation

### 1. Install Python

Make sure Python is installed on your computer.

Check the installation:

```bash
python --version
```

### 2. Install Required Libraries

Run:

```bash
pip install SpeechRecognition pyttsx3 PyAudio
```

If `PyAudio` is already installed, you can simply install the remaining libraries:

```bash
pip install SpeechRecognition pyttsx3
```

### 3. Run the Assistant

Open the project folder in CMD/Terminal and run:

```bash
python voice_assistant.py
```

The assistant will start listening through the microphone.

---

## 🎤 Example Commands

| Command                               | Action                            |
| ------------------------------------- | --------------------------------- |
| `Hello`                               | Gives a greeting                  |
| `What is the time?`                   | Tells current time                |
| `What is today's date?`               | Tells current date                |
| `What is the weather in Lucknow?`     | Gives current weather             |
| `Search for Python`                   | Opens Google search               |
| `Search YouTube for Python tutorials` | Opens YouTube search              |
| `Search Wikipedia for Python`         | Opens Wikipedia search            |
| `What is Python?`                     | Answers from local knowledge base |
| `What is 25 plus 15?`                 | Calculates the answer             |
| `Take a note ...`                     | Saves a note                      |
| `Read my notes`                       | Reads saved notes                 |
| `Remind me in 10 seconds to ...`      | Sets a reminder                   |
| `Open Notepad`                        | Opens Notepad                     |
| `Open Calculator`                     | Opens Calculator                  |
| `Open Chrome`                         | Opens Chrome                      |
| `Open GitHub`                         | Opens GitHub using custom command |
| `Bye`                                 | Closes the assistant              |

---

## 🔐 Security & Privacy

* Email credentials are **not hard-coded** in the Python source code.
* Email settings are read from environment variables.
* Custom commands are restricted to web links instead of executing arbitrary shell commands.
* Calculator expressions are validated before evaluation.
* The project processes microphone input for speech recognition.

Users should avoid storing sensitive personal information in `notes.txt`.

---

## ⚠️ Error Handling

The assistant handles several common errors, including:

* Microphone access problems
* Speech recognition failures
* Unclear speech
* Internet connection problems
* Weather service errors
* Invalid calculations
* Email configuration errors
* Missing saved notes

Instead of crashing, the assistant provides a suitable response whenever possible.

---

## 🎯 OIBSIP Task

**Internship:** Oasis Infobyte Internship Program (OIBSIP)

**Track:** Python Programming

**Task:** Task 1 – Voice Assistant

**Tier:** Advanced

---

## 🎥 Demo

A screen-recorded demonstration of the project shows the Voice Assistant running and performing its implemented features.

**Demo Video:**
https://drive.google.com/file/d/1jc42ynstF35tjcRGNrJEb7dcAjya6Vfi/view?usp=sharing

---

## 📸 Screenshots

Project screenshots are available in the `screenshots` folder.

They demonstrate the Voice Assistant interface, commands, responses and working features.

---

## 👨‍💻 Author

**Adarsh Tiwari**

Python Programming Intern
Oasis Infobyte Internship Program

---

## 📄 License

This project was created for educational and internship purposes.
