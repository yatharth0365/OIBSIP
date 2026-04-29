import string
import tkinter as tk
from secrets import choice
from tkinter import messagebox, ttk


MIN_LENGTH = 4
MAX_LENGTH = 128
AMBIGUOUS_CHARACTERS = "O0oIl1|`'\",.;:()[]{}"


def build_charset(use_lower, use_upper, use_digits, use_symbols, excluded_characters):
    charsets = []

    if use_lower:
        charsets.append("".join(ch for ch in string.ascii_lowercase if ch not in excluded_characters))
    if use_upper:
        charsets.append("".join(ch for ch in string.ascii_uppercase if ch not in excluded_characters))
    if use_digits:
        charsets.append("".join(ch for ch in string.digits if ch not in excluded_characters))
    if use_symbols:
        charsets.append("".join(ch for ch in string.punctuation if ch not in excluded_characters))

    return [charset for charset in charsets if charset]


def secure_shuffle(characters):
    pool = list(characters)
    shuffled = []
    while pool:
        index = choice(range(len(pool)))
        shuffled.append(pool.pop(index))
    return "".join(shuffled)


def evaluate_strength(password, selected_sets, strong_rules_enabled):
    length = len(password)
    unique_chars = len(set(password))
    symbol_count = sum(char in string.punctuation for char in password)
    digit_count = sum(char.isdigit() for char in password)

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if selected_sets >= 3:
        score += 1
    if selected_sets == 4:
        score += 1
    if unique_chars >= max(8, length - 2):
        score += 1
    if symbol_count > 0:
        score += 1
    if digit_count > 0:
        score += 1
    if strong_rules_enabled:
        score += 1

    if score <= 3:
        return "Moderate"
    if score <= 6:
        return "Strong"
    return "Very strong"


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Generator")
        self.root.geometry("760x620")
        self.root.minsize(700, 560)
        self.root.configure(bg="#f4f6f8")

        self.password_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Choose your settings and generate a password.")
        self.strength_var = tk.StringVar(value="Strength: waiting")
        self.length_var = tk.StringVar(value="16")
        self.custom_exclude_var = tk.StringVar()

        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.avoid_ambiguous_var = tk.BooleanVar(value=True)
        self.require_all_selected_var = tk.BooleanVar(value=True)
        self.no_repeat_var = tk.BooleanVar(value=False)
        self.strong_rules_var = tk.BooleanVar(value=True)
        self.auto_copy_var = tk.BooleanVar(value=False)

        self.profile_var = tk.StringVar(value="Strong")

        self._configure_style()
        self._build_layout()
        self.apply_profile("Strong")

    def _configure_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("App.TFrame", background="#f4f6f8")
        style.configure("Panel.TFrame", background="#ffffff")
        style.configure("Title.TLabel", background="#f4f6f8", foreground="#18212b", font=("Segoe UI", 18, "bold"))
        style.configure("Body.TLabel", background="#f4f6f8", foreground="#4b5563", font=("Segoe UI", 10))
        style.configure("PanelTitle.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 11, "bold"))
        style.configure("PanelBody.TLabel", background="#ffffff", foreground="#374151", font=("Segoe UI", 10))
        style.configure("Status.TLabel", background="#ffffff", foreground="#1f2937", font=("Segoe UI", 10))
        style.configure("Output.TEntry", fieldbackground="#f9fafb", foreground="#111827", padding=10)
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 10))
        style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=(12, 10))
        style.configure("TLabelframe", background="#ffffff", borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background="#ffffff", foreground="#111827", font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", background="#ffffff", foreground="#1f2937", font=("Segoe UI", 10))
        style.configure("TRadiobutton", background="#ffffff", foreground="#1f2937", font=("Segoe UI", 10))
        style.configure("TCombobox", padding=6)
        style.map("Primary.TButton", background=[("active", "#2563eb"), ("!disabled", "#1d4ed8")], foreground=[("!disabled", "#ffffff")])

    def _build_layout(self):
        container = ttk.Frame(self.root, padding=18, style="App.TFrame")
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="Advanced Password Generator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Create secure passwords with rules, exclusions, and one-click clipboard copy.",
            style="Body.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        output_panel = ttk.Frame(container, padding=16, style="Panel.TFrame")
        output_panel.pack(fill="x", pady=(0, 14))

        ttk.Label(output_panel, text="Generated Password", style="PanelTitle.TLabel").pack(anchor="w")

        entry_row = ttk.Frame(output_panel, style="Panel.TFrame")
        entry_row.pack(fill="x", pady=(10, 8))
        self.password_entry = ttk.Entry(entry_row, textvariable=self.password_var, font=("Consolas", 14), style="Output.TEntry")
        self.password_entry.pack(side="left", fill="x", expand=True)
        ttk.Button(entry_row, text="Copy", command=self.copy_password, style="Secondary.TButton").pack(side="left", padx=(10, 0))

        action_row = ttk.Frame(output_panel, style="Panel.TFrame")
        action_row.pack(fill="x")
        ttk.Button(action_row, text="Generate Password", command=self.generate_password, style="Primary.TButton").pack(side="left")
        ttk.Label(action_row, textvariable=self.strength_var, style="PanelBody.TLabel").pack(side="right")

        content = ttk.Frame(container, style="App.TFrame")
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)

        left_panel = ttk.Frame(content, padding=14, style="Panel.TFrame")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 7))

        right_panel = ttk.Frame(content, padding=14, style="Panel.TFrame")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(7, 0))

        self._build_left_panel(left_panel)
        self._build_right_panel(right_panel)

        footer = ttk.Frame(container, padding=12, style="Panel.TFrame")
        footer.pack(fill="x", pady=(14, 0))
        ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel", wraplength=680, justify="left").pack(anchor="w")

    def _build_left_panel(self, parent):
        ttk.Label(parent, text="Basic Settings", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 12))

        profile_frame = ttk.LabelFrame(parent, text="Complexity Profile", padding=12)
        profile_frame.pack(fill="x", pady=(0, 12))

        for profile in ("Balanced", "Strong", "Maximum"):
            ttk.Radiobutton(
                profile_frame,
                text=profile,
                value=profile,
                variable=self.profile_var,
                command=lambda current=profile: self.apply_profile(current),
            ).pack(anchor="w", pady=2)

        length_frame = ttk.LabelFrame(parent, text="Password Length", padding=12)
        length_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(
            length_frame,
            text=f"Use a value between {MIN_LENGTH} and {MAX_LENGTH}.",
            style="PanelBody.TLabel",
        ).pack(anchor="w", pady=(0, 6))

        length_row = ttk.Frame(length_frame, style="Panel.TFrame")
        length_row.pack(fill="x")
        ttk.Entry(length_row, textvariable=self.length_var, width=10, font=("Segoe UI", 11)).pack(side="left")
        ttk.Button(length_row, text="Apply Profile", command=lambda: self.apply_profile(self.profile_var.get()), style="Secondary.TButton").pack(side="left", padx=(10, 0))

        types_frame = ttk.LabelFrame(parent, text="Character Types", padding=12)
        types_frame.pack(fill="x")
        ttk.Checkbutton(types_frame, text="Lowercase letters (a-z)", variable=self.lower_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(types_frame, text="Uppercase letters (A-Z)", variable=self.upper_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(types_frame, text="Numbers (0-9)", variable=self.digits_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(types_frame, text="Symbols (!, @, #, ...)", variable=self.symbols_var).pack(anchor="w", pady=2)

    def _build_right_panel(self, parent):
        ttk.Label(parent, text="Security and Copy Options", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 12))

        rules_frame = ttk.LabelFrame(parent, text="Security Rules", padding=12)
        rules_frame.pack(fill="x", pady=(0, 12))
        ttk.Checkbutton(rules_frame, text="Require at least one character from each selected type", variable=self.require_all_selected_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(rules_frame, text="Apply strong password rules", variable=self.strong_rules_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(rules_frame, text="Prevent repeated characters", variable=self.no_repeat_var).pack(anchor="w", pady=2)
        ttk.Checkbutton(rules_frame, text="Exclude ambiguous characters", variable=self.avoid_ambiguous_var).pack(anchor="w", pady=2)

        exclude_frame = ttk.LabelFrame(parent, text="Custom Exclusions", padding=12)
        exclude_frame.pack(fill="x", pady=(0, 12))
        ttk.Label(
            exclude_frame,
            text="Characters entered here will never appear in the password.",
            style="PanelBody.TLabel",
            wraplength=280,
            justify="left",
        ).pack(anchor="w", pady=(0, 6))
        ttk.Entry(exclude_frame, textvariable=self.custom_exclude_var, font=("Consolas", 11)).pack(fill="x")

        clipboard_frame = ttk.LabelFrame(parent, text="Clipboard", padding=12)
        clipboard_frame.pack(fill="x")
        ttk.Checkbutton(clipboard_frame, text="Copy password automatically after generation", variable=self.auto_copy_var).pack(anchor="w", pady=2)
        ttk.Label(
            clipboard_frame,
            text="Copying uses the system clipboard through Tkinter.",
            style="PanelBody.TLabel",
            wraplength=280,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def apply_profile(self, profile):
        presets = {
            "Balanced": {"length": "12", "symbols": False, "strong": False, "no_repeat": False},
            "Strong": {"length": "16", "symbols": True, "strong": True, "no_repeat": False},
            "Maximum": {"length": "24", "symbols": True, "strong": True, "no_repeat": True},
        }

        preset = presets.get(profile, presets["Strong"])
        self.length_var.set(preset["length"])
        self.symbols_var.set(preset["symbols"])
        self.strong_rules_var.set(preset["strong"])
        self.no_repeat_var.set(preset["no_repeat"])
        self.status_var.set(f"{profile} profile applied. Generate when you are ready.")

    def generate_password(self):
        try:
            length = int(self.length_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid length", "Password length must be a whole number.")
            self.status_var.set("Please enter a numeric password length.")
            return

        if not MIN_LENGTH <= length <= MAX_LENGTH:
            messagebox.showerror("Invalid length", f"Password length must be between {MIN_LENGTH} and {MAX_LENGTH}.")
            self.status_var.set(f"Length must stay between {MIN_LENGTH} and {MAX_LENGTH}.")
            return

        excluded = self.custom_exclude_var.get()
        if self.avoid_ambiguous_var.get():
            excluded += AMBIGUOUS_CHARACTERS
        excluded_characters = set(excluded)

        charsets = build_charset(
            self.lower_var.get(),
            self.upper_var.get(),
            self.digits_var.get(),
            self.symbols_var.get(),
            excluded_characters,
        )

        if not charsets:
            messagebox.showerror("No characters available", "Select at least one character type with available characters.")
            self.status_var.set("No usable characters remain after applying your filters.")
            return

        selected_types = len(charsets)

        if self.strong_rules_var.get():
            if length < 12:
                messagebox.showerror("Security rules", "Strong password rules require a length of at least 12.")
                self.status_var.set("Increase the length to at least 12 for strong password mode.")
                return
            if selected_types < 3:
                messagebox.showerror("Security rules", "Strong password rules require at least three character types.")
                self.status_var.set("Enable at least three character types for strong password mode.")
                return

        if self.require_all_selected_var.get() and selected_types > length:
            messagebox.showerror("Length too short", "Length must be at least the number of required character types.")
            self.status_var.set("Increase the length or reduce the required character types.")
            return

        total_available = len(set("".join(charsets)))
        if self.no_repeat_var.get() and length > total_available:
            messagebox.showerror("Not enough unique characters", "There are not enough unique characters to avoid repeats with the current settings.")
            self.status_var.set("Relax the exclusions or allow repeated characters.")
            return

        required_characters = []
        if self.require_all_selected_var.get():
            for charset in charsets:
                required_characters.append(choice(charset))

        all_characters = "".join(charsets)
        password_characters = list(required_characters)

        while len(password_characters) < length:
            candidate = choice(all_characters)
            if self.no_repeat_var.get() and candidate in password_characters:
                continue
            password_characters.append(candidate)

        password = secure_shuffle(password_characters)
        self.password_var.set(password)
        self.strength_var.set(f"Strength: {evaluate_strength(password, selected_types, self.strong_rules_var.get())}")
        self.status_var.set("Password generated successfully.")
        self.password_entry.selection_range(0, tk.END)
        self.password_entry.focus_set()

        if self.auto_copy_var.get():
            self.copy_password(show_message=False)
            self.status_var.set("Password generated and copied to the clipboard.")

    def copy_password(self, show_message=True):
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            self.status_var.set("Generate a password before copying it.")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        if show_message:
            self.status_var.set("Password copied to the clipboard.")


def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
