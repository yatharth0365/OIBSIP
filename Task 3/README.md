# Advanced Password Generator

## Overview

This project is a desktop password generator built with Python and Tkinter. It lets users create secure, customizable passwords through a graphical interface instead of typing options into the terminal.

## What It Does

The application opens a window where the user can choose password settings, generate a password, and copy it to the clipboard. The generated password changes based on the selected options.

Users can:

- choose the password length
- include lowercase letters, uppercase letters, numbers, and symbols
- select a complexity profile: `Balanced`, `Strong`, or `Maximum`
- require at least one character from each selected character type
- prevent repeated characters
- exclude ambiguous characters such as `O`, `0`, `I`, and `l`
- enter custom characters that should not appear in the password
- copy the password manually
- automatically copy the password after generation

## Expected Behavior

When the program starts, it shows the password generator interface with default strong settings. The user can adjust the options and click **Generate Password**. If the settings are valid, a new password appears in the output field and the app displays a strength label.

If the settings are not valid, the app shows a clear error message. For example, it warns the user when:

- the password length is outside the allowed range
- no character types are selected
- strong rules are enabled but the password is too short
- there are not enough available characters to avoid repeats

## Main Features

- Secure random password generation using Python's `secrets` module
- Tkinter-based graphical user interface
- Password strength feedback
- Custom exclusion support
- Ambiguous-character filtering
- Manual and automatic clipboard copying

## Main File

- `main.py` contains the full application code.

## How to Run

Open a terminal in the project folder and run:

```bash
python main.py
```

This should launch the desktop password generator window.
