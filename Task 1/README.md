# OIBSIP - Task 1: Voice Assistant
A browser-based voice assistant built with Flask and the Web Speech API.
It listens to voice commands, sends them to a Python backend, and speaks the response.

## Features
- Voice recognition using browser `SpeechRecognition` (`webkitSpeechRecognition` fallback)
- Spoken responses using browser `SpeechSynthesis`
- Handles common commands:
  - Greetings
  - Current time
  - Current date/day/year
  - Joke requests
  - Help/identity prompts
- Web search support:
  - Commands like `search for ...`, `look up ...`, `find ...`, `google ...`
  - Fallback search for unknown commands

## Tech Stack
- Python 3
- Flask
- Flask-CORS
- HTML, CSS, JavaScript

## Project Files
- `app.py` - Flask backend and command processing logic
- `index.html` - Frontend UI, speech recognition, speech output
- `.gitignore` - Ignore IDE/cache artifacts

## Setup and Run
1. Install dependencies:
   ```powershell
   py -m pip install flask flask-cors
   ```
2. Start the server:
   ```powershell
   py app.py
   ```
3. Open in browser:
   - `http://127.0.0.1:5000`
4. Allow microphone access when prompted.

## Example Voice Commands
- `Hello`
- `What time is it?`
- `What's today's date?`
- `Search for machine learning`
- `Tell me a joke`

## API Endpoint
### `POST /command`
Request body:
```json
{ "text": "search for python tutorials" }
```
Response includes:
- `transcript`
- `reply`
- optional `search_url`
- optional `query`

## Notes
- Best experience on Chrome/Edge (Web Speech API support).
- If `python` is unavailable on Windows, use `py`.
- Default server port is `5000`.
