# OIBSIP - Task 2: BMI Calculator GUI
This task contains a desktop GUI application built in Python to calculate Body Mass Index (BMI) from user input and display the BMI category.

## Objective
Build a simple, user-friendly BMI calculator with a graphical interface where users can:
- Enter height and weight
- Calculate BMI instantly
- See health category feedback based on BMI value

## Features
- Clean GUI-based input form
- Input validation for empty/non-numeric values
- Instant BMI calculation
- BMI category interpretation (Underweight, Normal, Overweight, Obese)
- Easy reset/recalculation workflow

## Tech Stack
- Python 3
- Tkinter (GUI)

## Project Files
- `bmi_calculator_gui.py` - Main Python GUI application for BMI calculation
- `README.md` - Task documentation and usage instructions

## BMI Formula
BMI is calculated as:

`BMI = weight (kg) / [height (m)]^2`

If height is entered in centimeters, it is converted to meters before calculation.

## How to Run
1. Open terminal in this folder (`Task 2`).
2. Run:
   ```powershell
   py bmi_calculator_gui.py
   ```
   (Use `python bmi_calculator_gui.py` if `py` is unavailable.)

## Usage
1. Enter height and weight in the GUI fields.
2. Click the calculate button.
3. View:
   - BMI value
   - Corresponding BMI category

## BMI Categories Used
- Below 18.5 -> Underweight
- 18.5 to 24.9 -> Normal weight
- 25.0 to 29.9 -> Overweight
- 30.0 and above -> Obese

## Notes
- Enter numeric values only.
- Height must be greater than zero.
- This tool provides general fitness guidance and is not a medical diagnosis.
