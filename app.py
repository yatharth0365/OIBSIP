import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def process_command(text: str) -> dict:
    """Parse transcribed text and return a reply + optional search query."""
    t = text.lower().strip()

    # Greetings
    if any(t.startswith(w) for w in ["hello", "hi", "hey", "howdy", "good morning", "good afternoon", "good evening"]):
        hour = datetime.datetime.now().hour
        greet = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
        return {"reply": f"{greet}! I'm your voice assistant. Ask me the time, date, or to search the web."}

    # Time
    if "time" in t or "clock" in t:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return {"reply": f"The current time is {now}."}

    # Year
    if "year" in t:
        return {"reply": f"The current year is {datetime.datetime.now().year}."}

    # Date
    if "date" in t or "today" in t or "day" in t:
        d = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return {"reply": f"Today is {d}."}

    # Web search patterns
    for prefix in ["search for ", "search ", "look up ", "find ", "google "]:
        if t.startswith(prefix):
            query = text[len(prefix):].strip()
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            return {"reply": f'Searching the web for "{query}".', "search_url": url, "query": query}

    # Identity
    if "your name" in t or "who are you" in t or "what are you" in t:
        return {"reply": "I'm a voice assistant that can greet you, tell time and date, crack jokes, and search the web."}

    # Help
    if "help" in t or "what can you do" in t:
        return {"reply": "I can tell you the time, date, or search the web. Try: What time is it? Or: Search for Python tutorials."}

    # Thanks
    if "thank" in t:
        return {"reply": "You're welcome! Let me know if I can help with anything else."}

    # Joke
    if "joke" in t:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything.",
            "I told my computer I needed a break and now it won't stop sending me Kit-Kat ads.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
        ]
        import random
        return {"reply": random.choice(jokes)}

    # Fallback: search whatever was said
    query = text.strip()
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    return {"reply": f'I didn\'t catch that command — searching the web for "{query}".', "search_url": url, "query": query}


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    transcript = str(data.get("text", "")).strip()
    if not transcript:
        return jsonify({"error": "No text provided"}), 400

    command_result = process_command(transcript)
    return jsonify({"transcript": transcript, **command_result})


@app.route("/")
def index():
    return send_from_directory(app.root_path, "index.html")


if __name__ == "__main__":
    print("Starting server at http://localhost:5000")
    app.run(debug=True, port=5000)
