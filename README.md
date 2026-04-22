# Voice Assistant (Beginner Internship Task)
A basic browser-based voice assistant that listens to your voice, understands simple commands, and speaks responses.
## Project Description
This project is a beginner-friendly voice assistant with these core capabilities:
- Greeting responses for commands like `Hello`, `Hi`, `Good morning`
- Tells current local time (`What time is it?`)
- Tells today’s date (`What's today's date?`, `What day is it?`)
- Web search for commands like `Search for ...`, `Look up ...`, `Find ...`
- Fallback web search for unknown commands
- Extra commands such as identity/help/jokes

How it works:
- Uses browser **SpeechRecognition** (Web Speech API) to convert voice to text
- Sends recognized text to a Flask backend endpoint (`/command`)
- Backend parses command and returns a reply (+ optional Google search URL)
- Uses browser **SpeechSynthesis** to speak the assistant response
- UI animation glows while listening and turns blue while speaking

## Tech Stack
- Python
- Flask + Flask-CORS
- HTML/CSS/JavaScript (Web Speech API)

## Setup Instructions
### 1) Install Python
Install Python 3.10+ from the official Python website.

On Windows, if `pip` is not recognized, use:
- `py -m pip ...`

### 2) Install dependencies
Open terminal in this project folder and run:

```powershell
py -m pip install flask flask-cors
```

### 3) Run the app
From the project folder:

```powershell
py app.py
```

You should see:
- `Starting server at http://localhost:5000`

### 4) Open in browser
Go to:
- `http://127.0.0.1:5000`

Allow microphone permission when prompted.

## Usage
Click the mic button and speak commands like:
- `Hello`
- `What time is it?`
- `What's today's date?`
- `Search for black holes`
- `Tell me a joke`

## Notes
- This app requires a browser that supports `SpeechRecognition` (Chrome/Edge recommended).
- If `python` command does not work on your system, use `py`.
- If port `5000` is busy, update the port in `app.py` and open that port in your browser.
- If port `5000` is busy, update the port in `app.py` and open that port in your browser.
