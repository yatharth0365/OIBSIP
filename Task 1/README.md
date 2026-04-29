# OIBSIP - Task 1: Python Voice Assistant
A desktop voice assistant built with Python and a `tkinter` GUI.
It listens through your microphone, understands voice commands, speaks replies aloud, and can open web searches in your browser.

## Features
- Python GUI using `tkinter`
- Voice command input through the microphone
- Spoken assistant replies
- Handles common commands:
  - Greetings
  - Current time
  - Current date/day/year
  - Joke requests
  - Help/identity prompts
- Web search support:
  - Commands like `search for ...`, `look up ...`, `find ...`, `google ...`
  - Unknown commands prepare a search you can open from the GUI

## Tech Stack
- Python 3
- `tkinter`
- `SpeechRecognition`
- `PyAudio`
- `pyttsx3`
- `webbrowser`

## Project Files
- `app.py` - Python voice assistant GUI and command processing logic
- `.gitignore` - Ignore IDE/cache artifacts

## Setup and Run
1. Install dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```
2. Start the desktop app:
   ```powershell
   py app.py
   ```
3. Click `Listen` and speak a command.

## Example Commands
- `Hello`
- `What time is it?`
- `What's today's date?`
- `Search for machine learning`
- `Tell me a joke`

## Notes
- If `python` is unavailable on Windows, use `py`.
- Voice recognition uses Google's speech recognition service through the `SpeechRecognition` package, so internet access may be required.
- `PyAudio` is required for microphone access.
- Searches open with your system default browser.
