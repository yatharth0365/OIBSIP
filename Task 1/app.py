import datetime as dt
import random
import threading
import tkinter as tk
from tkinter import ttk
from urllib.parse import quote_plus
import webbrowser

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None


APP_TITLE = "Python Voice Assistant"


def process_command(text: str) -> dict:
    """Return the assistant response for a spoken command."""
    original = text.strip()
    command = original.lower()

    if not command:
        return {"reply": "I did not hear a command. Please try again."}

    greetings = (
        "hello",
        "hi",
        "hey",
        "howdy",
        "good morning",
        "good afternoon",
        "good evening",
    )
    if any(command.startswith(word) for word in greetings):
        hour = dt.datetime.now().hour
        greeting = (
            "Good morning"
            if hour < 12
            else "Good afternoon"
            if hour < 17
            else "Good evening"
        )
        return {
            "reply": f"{greeting}! I am listening. Ask me the time, date, a joke, or a web search."
        }

    if "time" in command or "clock" in command:
        now = dt.datetime.now().strftime("%I:%M %p")
        return {"reply": f"The current time is {now}."}

    if "year" in command:
        return {"reply": f"The current year is {dt.datetime.now().year}."}

    if "date" in command or "today" in command or "day" in command:
        today = dt.datetime.now().strftime("%A, %B %d, %Y")
        return {"reply": f"Today is {today}."}

    search_prefixes = ("search for ", "search ", "look up ", "find ", "google ")
    for prefix in search_prefixes:
        if command.startswith(prefix):
            query = original[len(prefix) :].strip()
            return make_search_response(query)

    if "your name" in command or "who are you" in command or "what are you" in command:
        return {
            "reply": "I am a Python voice assistant. I listen through your microphone and answer with speech."
        }

    if "help" in command or "what can you do" in command:
        return {
            "reply": "You can say hello, ask for the time or date, ask for a joke, or say search for followed by a topic."
        }

    if "thank" in command:
        return {"reply": "You're welcome!"}

    if "joke" in command:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything.",
            "I told my computer I needed a break, and now it keeps suggesting vacation photos.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
        ]
        return {"reply": random.choice(jokes)}

    return make_search_response(original, fallback=True)


def make_search_response(query: str, fallback: bool = False) -> dict:
    clean_query = query.strip()
    if not clean_query:
        return {"reply": "Please tell me what you want to search for."}

    url = f"https://www.google.com/search?q={quote_plus(clean_query)}"
    if fallback:
        reply = f'I did not recognize that command, so I searched the web for "{clean_query}".'
    else:
        reply = f'Searching the web for "{clean_query}".'

    return {"reply": reply, "search_url": url, "query": clean_query}


class VoiceAssistantGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("760x560")
        self.root.minsize(600, 460)

        self.recognizer = sr.Recognizer() if sr else None
        self.tts_engine = self.create_tts_engine()

        self.is_listening = False
        self.search_url = ""
        self.status = tk.StringVar(value="Ready")
        self.transcript = tk.StringVar(value="-")

        self.configure_style()
        self.build_layout()
        self.report_missing_dependencies()

    def configure_style(self) -> None:
        self.root.configure(bg="#101418")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#101418")
        style.configure("Card.TFrame", background="#182028", relief="flat")
        style.configure(
            "TLabel",
            background="#101418",
            foreground="#e9edf0",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Muted.TLabel",
            background="#101418",
            foreground="#9aa6ad",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Card.TLabel",
            background="#182028",
            foreground="#e9edf0",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Title.TLabel",
            background="#101418",
            foreground="#f5f7f8",
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "TButton",
            background="#2775c7",
            foreground="#ffffff",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=(14, 9),
        )
        style.map("TButton", background=[("active", "#3288df"), ("disabled", "#43505a")])
        style.configure(
            "Secondary.TButton",
            background="#24313b",
            foreground="#e9edf0",
        )
        style.map("Secondary.TButton", background=[("active", "#30414d")])

    def create_tts_engine(self):
        if pyttsx3 is None:
            return None

        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            return engine
        except Exception:
            return None

    def build_layout(self) -> None:
        shell = ttk.Frame(self.root, padding=24)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(4, weight=1)

        ttk.Label(shell, text=APP_TITLE, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            shell,
            text="Click Listen, speak a command, and the assistant will reply aloud.",
            style="Muted.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 22))

        controls = ttk.Frame(shell, style="Card.TFrame", padding=16)
        controls.grid(row=2, column=0, sticky="ew")
        controls.columnconfigure(1, weight=1)

        self.listen_button = ttk.Button(controls, text="Listen", command=self.start_listening)
        self.listen_button.grid(row=0, column=0, padx=(0, 12))

        ttk.Label(controls, textvariable=self.status, style="Card.TLabel").grid(
            row=0, column=1, sticky="w"
        )

        transcript_card = ttk.Frame(shell, style="Card.TFrame", padding=16)
        transcript_card.grid(row=3, column=0, sticky="ew", pady=(16, 0))
        transcript_card.columnconfigure(0, weight=1)

        ttk.Label(transcript_card, text="Heard Command", style="Card.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(transcript_card, textvariable=self.transcript, style="Card.TLabel").grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )

        content = ttk.Frame(shell)
        content.grid(row=4, column=0, sticky="nsew", pady=18)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        reply_card = ttk.Frame(content, style="Card.TFrame", padding=16)
        reply_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        reply_card.columnconfigure(0, weight=1)
        reply_card.rowconfigure(1, weight=1)

        ttk.Label(reply_card, text="Assistant Reply", style="Card.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.reply_box = tk.Text(
            reply_card,
            height=10,
            wrap="word",
            borderwidth=0,
            bg="#182028",
            fg="#e9edf0",
            insertbackground="#e9edf0",
            font=("Segoe UI", 12),
        )
        self.reply_box.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.update_reply("Hello! Click Listen and speak a command.")

        actions = ttk.Frame(reply_card, style="Card.TFrame")
        actions.grid(row=2, column=0, sticky="ew", pady=(14, 0))
        ttk.Button(
            actions,
            text="Open Search",
            style="Secondary.TButton",
            command=self.open_search,
        ).pack(side="left")
        ttk.Button(
            actions,
            text="Repeat Reply",
            style="Secondary.TButton",
            command=self.repeat_reply,
        ).pack(side="left", padx=(8, 0))

        examples_card = ttk.Frame(content, style="Card.TFrame", padding=16)
        examples_card.grid(row=0, column=1, sticky="nsew")

        ttk.Label(examples_card, text="Say These", style="Card.TLabel").pack(anchor="w")
        examples = [
            "Hello",
            "What time is it?",
            "What's today's date?",
            "Tell me a joke",
            "Search for machine learning",
        ]
        for example in examples:
            ttk.Label(examples_card, text=example, style="Card.TLabel").pack(
                anchor="w", pady=(12, 0)
            )

    def report_missing_dependencies(self) -> None:
        missing = []
        if sr is None:
            missing.append("SpeechRecognition")
        if pyttsx3 is None or self.tts_engine is None:
            missing.append("pyttsx3")

        if missing:
            message = (
                "Missing voice package: "
                + ", ".join(missing)
                + ". Install the requirements listed in README.md."
            )
            self.status.set(message)
            self.update_reply(message)

    def start_listening(self) -> None:
        if self.is_listening:
            return

        if sr is None:
            self.update_reply("SpeechRecognition is not installed. Please install it first.")
            return

        self.is_listening = True
        self.listen_button.configure(state="disabled")
        self.status.set("Listening... speak now")
        thread = threading.Thread(target=self.listen_for_command, daemon=True)
        thread.start()

    def listen_for_command(self) -> None:
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=8)

            self.root.after(0, self.status.set, "Recognizing speech...")
            command = self.recognizer.recognize_google(audio)
            self.root.after(0, self.handle_command, command)
        except sr.WaitTimeoutError:
            self.root.after(0, self.show_error, "I did not hear anything. Please try again.")
        except sr.UnknownValueError:
            self.root.after(0, self.show_error, "I could not understand that. Please try again.")
        except sr.RequestError:
            self.root.after(
                0,
                self.show_error,
                "Speech recognition service is unavailable. Check your internet connection.",
            )
        except OSError:
            self.root.after(
                0,
                self.show_error,
                "No microphone was found. Connect a microphone and try again.",
            )
        except AttributeError:
            self.root.after(
                0,
                self.show_error,
                "Microphone support is missing. Install PyAudio and try again.",
            )
        finally:
            self.root.after(0, self.finish_listening)

    def finish_listening(self) -> None:
        self.is_listening = False
        self.listen_button.configure(state="normal")
        if self.status.get().startswith(("Listening", "Recognizing")):
            self.status.set("Ready")

    def handle_command(self, command: str) -> None:
        self.transcript.set(command)
        result = process_command(command)
        self.search_url = result.get("search_url", "")
        self.update_reply(result["reply"])
        self.status.set(f'Processed: "{command}"')

        if self.search_url:
            webbrowser.open(self.search_url)

        self.speak(result["reply"])

    def update_reply(self, text: str) -> None:
        self.reply_box.configure(state="normal")
        self.reply_box.delete("1.0", "end")
        self.reply_box.insert("1.0", text)
        self.reply_box.configure(state="disabled")

    def speak(self, text: str) -> None:
        if not text or self.tts_engine is None:
            return

        thread = threading.Thread(target=self.speak_in_background, args=(text,), daemon=True)
        thread.start()

    def speak_in_background(self, text: str) -> None:
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def repeat_reply(self) -> None:
        reply = self.reply_box.get("1.0", "end").strip()
        self.speak(reply)

    def open_search(self) -> None:
        if self.search_url:
            webbrowser.open(self.search_url)
            self.status.set("Opened search results in your browser.")
        else:
            self.status.set("No search is ready yet.")

    def show_error(self, message: str) -> None:
        self.status.set(message)
        self.update_reply(message)
        self.speak(message)


def main() -> None:
    root = tk.Tk()
    VoiceAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
