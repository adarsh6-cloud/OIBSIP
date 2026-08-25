🎙️ Advanced Voice Assistant — Python

A Python-based Advanced Voice Assistant that listens to voice commands, converts speech into text, processes the command, and responds using text-to-speech.

This project was developed as part of the Oasis Infobyte (OIBSIP) Python Internship – Task 1 and has been enhanced with multiple useful features beyond the basic requirements.

 Features

-  Voice command recognition
-  Text-to-speech responses
-  Current time
-  Current date and day
-  Google search
-  YouTube search
-  Wikipedia search
-  Open applications
  - Notepad
  - Calculator
  - Chrome
  - File Explorer
-  Voice-based calculator
-  Save notes
-  Read saved notes
-  Set voice-based reminders
-  Weather information
-  Basic conversational responses
-  Error handling for microphone and speech-recognition problems
-  Voice-controlled exit

 Technologies Used

- Python
- SpeechRecognition
- PyAudio
- pyttsx3
- Web Browser
- Datetime
- OS
- Threading
- urllib
- JSON
- AST / Operator

 Project Structure

Python-Task1-VoiceAssistant/
│
├── voice_assistant.py
├── README.md
├── Screenshot.png
└── notes.txt

«"notes.txt" is created automatically when the assistant saves a note.»

 Installation

1. Install Python

Make sure Python is installed on your computer.

Check the installation using:

python --version

2. Install Required Libraries

Open the terminal in the project folder and run:

pip install SpeechRecognition pyttsx3 PyAudio

If PyAudio installation causes an error on Windows, install a compatible PyAudio package for your Python version.

 How to Run

Open the terminal in the project folder and run:

python voice_assistant.py

The assistant will greet you and start listening for voice commands.

 Example Voice Commands

Command| Action
"What is the time?"| Tells the current time
"What is today's date?"| Tells today's date
"Search Python programming"| Searches Google
"Play music on YouTube"| Searches YouTube
"Who is Albert Einstein?"| Searches Wikipedia
"Weather in Lucknow"| Gives weather information
"Calculate 25 plus 15"| Calculates the answer
"Take a note buy a notebook"| Saves a note
"Read my notes"| Reads saved notes
"Remind me in 1 minute to drink water"| Creates a reminder
"Open calculator"| Opens Calculator
"Open notepad"| Opens Notepad
"How are you?"| Gives a conversational response
"Bye"| Stops the assistant

 Project Screenshot

"Voice Assistant Screenshot" (Screenshot.png)

🎥 Project Demo

A video demonstration of the Voice Assistant is available as part of the project submission.

 How It Works

The assistant follows a simple voice-processing pipeline:

User Voice
    ↓
Microphone
    ↓
Speech Recognition
    ↓
Command Processing
    ↓
Selected Action
    ↓
Text-to-Speech
    ↓
Assistant Voice Response

The microphone captures the user's speech, "SpeechRecognition" converts it into text, Python processes the command, and "pyttsx3" converts the response back into speech.

 Error Handling

The assistant handles several common situations:

- No voice input
- Unclear speech
- Speech recognition service unavailable
- Invalid calculator expressions
- Weather service unavailable
- Missing notes
- Unknown commands

 Future Improvements

Future versions can include:

-  AI-powered conversations
-  Email automation
-  WhatsApp automation
-  Smart-home control
-  Voice authentication
-  More natural language understanding
-  System monitoring
-  Advanced file management

 Internship

Program: Oasis Infobyte (OIBSIP)
Track: Python Programming
Task: Task 1 — Voice Assistant

 Author

Adarsh Tiwari

BCA Student | Python & Technology Enthusiast

---

 If you find this project useful, feel free to explore the repository and give it a star!