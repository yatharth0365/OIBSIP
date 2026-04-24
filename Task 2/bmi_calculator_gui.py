"""
BMI Calculator - GUI Version (Advanced)
A modern graphical interface for BMI calculation with real-time updates.
Built with tkinter for cross-platform compatibility.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple


class BMICalculator:
    """
    GUI-based BMI Calculator application using tkinter.
    """
    
    # Color scheme
    COLORS = {
        "bg_primary": "#f0f4f8",
        "bg_secondary": "#ffffff",
        "text_dark": "#1a1a1a",
        "text_light": "#666666",
        "accent_blue": "#3498db",
        "accent_green": "#27ae60",
        "accent_orange": "#f39c12",
        "accent_red": "#e74c3c",
        "border": "#ecf0f1",
        "underweight": "#3498db",
        "normal": "#27ae60",
        "overweight": "#f39c12",
        "obese": "#e74c3c"
    }
    
    # BMI Categories
    BMI_CATEGORIES = {
        "Underweight": {
            "range": (0, 18.5),
            "color": "underweight",
            "description": "BMI less than 18.5 - Consider consulting a healthcare provider",
            "emoji": "🔵"
        },
        "Normal Weight": {
            "range": (18.5, 25),
            "color": "normal",
            "description": "BMI between 18.5 and 24.9 - Healthy weight range",
            "emoji": "🟢"
        },
        "Overweight": {
            "range": (25, 30),
            "color": "overweight",
            "description": "BMI between 25 and 29.9 - Consider lifestyle changes",
            "emoji": "🟡"
        },
        "Obese": {
            "range": (30, float('inf')),
            "color": "obese",
            "description": "BMI 30 or higher - Consult with a healthcare provider",
            "emoji": "🔴"
        }
    }
    
    def __init__(self, root):
        """Initialize the BMI Calculator application."""
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Set window icon and styling
        self.root.configure(bg=self.COLORS["bg_primary"])
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Configure ttk styles for modern appearance."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure(
            'TButton',
            font=('Segoe UI', 10, 'bold'),
            padding=10,
            background=self.COLORS["accent_blue"],
            foreground="white"
        )
        
        # Configure label style
        style.configure(
            'TLabel',
            background=self.COLORS["bg_primary"],
            foreground=self.COLORS["text_dark"],
            font=('Segoe UI', 10)
        )
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.COLORS["bg_primary"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🏥 BMI Calculator",
            font=('Segoe UI', 24, 'bold'),
            bg=self.COLORS["bg_primary"],
            fg=self.COLORS["accent_blue"]
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Calculate your Body Mass Index",
            font=('Segoe UI', 11),
            bg=self.COLORS["bg_primary"],
            fg=self.COLORS["text_light"]
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Input section frame
        input_frame = tk.Frame(main_frame, bg=self.COLORS["bg_secondary"], relief=tk.FLAT)
        input_frame.pack(fill=tk.BOTH, padx=0, pady=10)
        input_frame.configure(highlightthickness=1, highlightbackground=self.COLORS["border"])
        
        # Input boxes container - side by side
        inputs_container = tk.Frame(input_frame, bg=self.COLORS["bg_secondary"])
        inputs_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Weight input box
        weight_box = tk.Frame(inputs_container, bg=self.COLORS["bg_secondary"])
        weight_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        weight_label = tk.Label(
            weight_box,
            text="Weight (kg)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.COLORS["bg_secondary"],
            fg=self.COLORS["accent_blue"]
        )
        weight_label.pack(anchor=tk.W, pady=(0, 8))

        self.weight_var = tk.StringVar()
        weight_entry = tk.Entry(
            weight_box,
            textvariable=self.weight_var,
            font=('Segoe UI', 16, 'bold'),
            width=15,
            relief=tk.SOLID,
            bd=2,
            bg="#ffffff",
            fg=self.COLORS["text_dark"],
            justify=tk.CENTER
        )
        weight_entry.pack(fill=tk.BOTH, ipady=12)
        weight_entry.bind('<KeyRelease>', lambda e: self.calculate_bmi_live())

        # Height input box
        height_box = tk.Frame(inputs_container, bg=self.COLORS["bg_secondary"])
        height_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        height_label = tk.Label(
            height_box,
            text="Height (cm)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.COLORS["bg_secondary"],
            fg=self.COLORS["accent_blue"]
        )
        height_label.pack(anchor=tk.W, pady=(0, 8))

        self.height_var = tk.StringVar()
        height_entry = tk.Entry(
            height_box,
            textvariable=self.height_var,
            font=('Segoe UI', 16, 'bold'),
            width=15,
            relief=tk.SOLID,
            bd=2,
            bg="#ffffff",
            fg=self.COLORS["text_dark"],
            justify=tk.CENTER
        )
        height_entry.pack(fill=tk.BOTH, ipady=12)
        height_entry.bind('<KeyRelease>', lambda e: self.calculate_bmi_live())

        # Results section
        results_frame = tk.Frame(main_frame, bg=self.COLORS["bg_secondary"], relief=tk.FLAT)
        results_frame.pack(fill=tk.BOTH, padx=0, pady=10)
        results_frame.configure(highlightthickness=1, highlightbackground=self.COLORS["border"])

        # BMI Value display
        self.bmi_label = tk.Label(
            results_frame,
            text="BMI: --",
            font=('Segoe UI', 28, 'bold'),
            bg=self.COLORS["bg_secondary"],
            fg=self.COLORS["accent_blue"]
        )
        self.bmi_label.pack(pady=(20, 10))

        # Category display
        self.category_label = tk.Label(
            results_frame,
            text="Category: --",
            font=('Segoe UI', 14, 'bold'),
            bg=self.COLORS["bg_secondary"],
            fg=self.COLORS["text_dark"]
        )
        self.category_label.pack(pady=(0, 10))

        # Description display
        self.description_label = tk.Label(
            results_frame,
            text="",
            font=('Segoe UI', 10),
            bg=self.COLORS["bg_secondary"],
            fg=self.COLORS["text_light"],
            wraplength=400,
            justify=tk.CENTER
        )
        self.description_label.pack(pady=(0, 20))

        # BMI Range reference
        reference_frame = tk.Frame(main_frame, bg=self.COLORS["bg_secondary"], relief=tk.FLAT)
        reference_frame.pack(fill=tk.BOTH, padx=0, pady=10)
        reference_frame.configure(highlightthickness=1, highlightbackground=self.COLORS["border"])

        reference_title = tk.Label(
            reference_frame,
            text="BMI Categories Reference",
            font=('Segoe UI', 11, 'bold'),
            bg=self.COLORS["bg_secondary"],
            fg=self.COLORS["text_dark"]
        )
        reference_title.pack(pady=(10, 10))

        reference_data = [
            ("Underweight", "< 18.5", self.COLORS["underweight"]),
            ("Normal", "18.5 - 24.9", self.COLORS["normal"]),
            ("Overweight", "25 - 29.9", self.COLORS["overweight"]),
            ("Obese", "≥ 30", self.COLORS["obese"])
        ]

        for category, range_text, color in reference_data:
            ref_item = tk.Frame(reference_frame, bg=self.COLORS["bg_secondary"])
            ref_item.pack(fill=tk.X, padx=15, pady=5)

            color_dot = tk.Label(
                ref_item,
                text="●",
                font=('Segoe UI', 14),
                bg=self.COLORS["bg_secondary"],
                fg=color
            )
            color_dot.pack(side=tk.LEFT, padx=(0, 10))

            cat_text = tk.Label(
                ref_item,
                text=f"{category}: {range_text}",
                font=('Segoe UI', 10),
                bg=self.COLORS["bg_secondary"],
                fg=self.COLORS["text_dark"],
                justify=tk.LEFT
            )
            cat_text.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.COLORS["bg_primary"])
        button_frame.pack(fill=tk.X, pady=20)

        # Calculate button
        calc_button = tk.Button(
            button_frame,
            text="📊 Calculate BMI",
            command=self.calculate_bmi,
            font=('Segoe UI', 11, 'bold'),
            bg=self.COLORS["accent_green"],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        calc_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Reset button
        reset_button = tk.Button(
            button_frame,
            text="🔄 Reset",
            command=self.reset_calculator,
            font=('Segoe UI', 11, 'bold'),
            bg=self.COLORS["accent_blue"],
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        reset_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def calculate_bmi(self):
        """Calculate BMI from user inputs."""
        try:
            weight = float(self.weight_var.get())
            height_cm = float(self.height_var.get())

            # Convert height from cm to meters
            height_m = height_cm / 100

            # Validate inputs
            if weight <= 0 or height_cm <= 0:
                messagebox.showerror("Invalid Input", "Weight and height must be greater than 0.")
                return

            if weight > 500 or height_cm > 300:
                messagebox.showwarning("Warning", "Values seem unrealistic. Please check your inputs.")
                return

            # Calculate BMI
            bmi = weight / (height_m ** 2)

            # Classify BMI
            category, color, description, emoji = self.classify_bmi(bmi)

            # Update display
            self.bmi_label.config(text=f"BMI: {bmi:.1f}", fg=self.COLORS[color])
            self.category_label.config(text=f"{emoji} {category}")
            self.description_label.config(text=description)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")

    def calculate_bmi_live(self):
        """Calculate BMI in real-time as user types."""
        try:
            if self.weight_var.get() and self.height_var.get():
                weight = float(self.weight_var.get())
                height_cm = float(self.height_var.get())

                # Convert height from cm to meters
                height_m = height_cm / 100

                if weight > 0 and height_cm > 0 and weight <= 500 and height_cm <= 300:
                    bmi = weight / (height_m ** 2)
                    category, color, description, emoji = self.classify_bmi(bmi)
                    self.bmi_label.config(text=f"BMI: {bmi:.1f}", fg=self.COLORS[color])
                    self.category_label.config(text=f"{emoji} {category}")
                    self.description_label.config(text=description)

        except ValueError:
            pass

    def classify_bmi(self, bmi: float) -> Tuple[str, str, str, str]:
        """
        Classify BMI into categories.

        Args:
            bmi (float): BMI value

        Returns:
            Tuple: (category, color_code, description, emoji)
        """
        for category, data in self.BMI_CATEGORIES.items():
            min_range, max_range = data["range"]
            if min_range <= bmi < max_range:
                return category, data["color"], data["description"], data["emoji"]

        return "Unknown", "text_dark", "Unable to classify BMI", "❓"

    def reset_calculator(self):
        """Reset the calculator to initial state."""
        self.weight_var.set("")
        self.height_var.set("")
        self.bmi_label.config(text="BMI: --", fg=self.COLORS["accent_blue"])
        self.category_label.config(text="Category: --")
        self.description_label.config(text="")


def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()