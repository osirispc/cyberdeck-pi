#!/usr/bin/env python3
import tkinter as tk
import pygame

root = tk.Tk()
root.title("VOIGHT-KAMPFF")
root.configure(bg="black")
root.attributes("-fullscreen", True)

mode = "idle"
subject_id = ""
current_input = ""
question_index = 0
answers = []

questions = [
    "You see a tortoise on its back in the desert. Rate your concern from 1 to 9.",
    "Describe your reaction to a crying child. Rate empathy from 1 to 9.",
    "A wasp lands on your arm. Rate your calm response from 1 to 9.",
    "Your mother gives you a gift. Rate your emotional response from 1 to 9.",
    "You find a wallet full of money. Rate your urge to return it from 1 to 9.",
]

# --- AUDIO SETUP ---
try:
    pygame.mixer.init()

    pygame.mixer.music.load("sounds/startup.ogg")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()

    click_sound = pygame.mixer.Sound("sounds/click.wav")
    click_sound.set_volume(0.45)

    alert_sound = pygame.mixer.Sound("sounds/alert.wav")
    alert_sound.set_volume(0.9)

    AUDIO_OK = True
except Exception as e:
    print("Audio failed:", e)
    AUDIO_OK = False
    click_sound = None
    alert_sound = None


def play_click():
    if AUDIO_OK and click_sound is not None:
        try:
            click_sound.play()
        except Exception:
            pass


def play_alert():
    if AUDIO_OK and alert_sound is not None:
        try:
            alert_sound.play()
        except Exception:
            pass


def start_ambient():
    if AUDIO_OK:
        try:
            pygame.mixer.music.load("sounds/ambient.ogg")
            pygame.mixer.music.set_volume(0.18)
            pygame.mixer.music.play(-1)
        except Exception:
            pass


def update_ui():
    if mode == "idle":
        status_label.config(text="STANDBY")
        question_label.config(text="ENTER SUBJECT ID")
        begin_button.config(text="BEGIN")
        if current_input:
            display_label.config(text=current_input)
        else:
            display_label.config(text="READY")

    elif mode == "question":
        status_label.config(
            text=f"SUBJECT: {subject_id}   QUESTION {question_index + 1}/{len(questions)}"
        )
        question_label.config(text=questions[question_index])
        begin_button.config(text="NEXT")
        if current_input:
            display_label.config(text=current_input)
        else:
            display_label.config(text="ENTER 1-9")

    elif mode == "result":
        begin_button.config(text="RESET")
        question_label.config(text="EVALUATION COMPLETE")
        display_label.config(text=current_input)


def add_digit(digit):
    global current_input

    if mode == "idle":
        current_input += digit
        play_click()
        update_ui()
        return

    if mode == "question":
        if digit in "123456789":
            current_input = digit
            play_click()
            update_ui()


def clear_input(event=None):
    global current_input

    if mode in ("idle", "question"):
        current_input = ""
        play_alert()
        update_ui()


def backspace_input(event=None):
    global current_input

    if mode == "idle" and current_input:
        current_input = current_input[:-1]
        play_click()
        update_ui()
    elif mode == "question" and current_input:
        current_input = ""
        play_click()
        update_ui()


def calculate_result():
    if not answers:
        return "INCONCLUSIVE"

    avg = sum(answers) / len(answers)

    if avg >= 7:
        return "HUMAN"
    if avg >= 4:
        return "INCONCLUSIVE"
    return "REPLICANT SUSPECT"


def begin_or_next(event=None):
    global mode, subject_id, question_index, current_input, answers

    if mode == "idle":
        if not current_input:
            status_label.config(text="ENTER SUBJECT ID FIRST")
            play_alert()
            return

        subject_id = current_input
        current_input = ""
        question_index = 0
        answers = []
        mode = "question"
        play_click()
        update_ui()
        return

    if mode == "question":
        if not current_input:
            status_label.config(text="ENTER RESPONSE 1-9")
            play_alert()
            return

        answers.append(int(current_input))
        current_input = ""
        play_click()

        if question_index < len(questions) - 1:
            question_index += 1
            update_ui()
        else:
            result = calculate_result()
            mode = "result"
            status_label.config(text=f"SUBJECT: {subject_id}")
            current_input = result
            play_alert()
            update_ui()
        return

    if mode == "result":
        mode = "idle"
        subject_id = ""
        question_index = 0
        answers = []
        current_input = ""
        play_click()
        update_ui()


def close_app(event=None):
    play_alert()
    root.after(200, root.destroy)


def on_key(event):
    key = event.keysym

    if key in [str(n) for n in range(10)]:
        add_digit(key)
    elif key == "BackSpace":
        backspace_input()
    elif key.lower() == "c":
        clear_input()
    elif key in ("Return", "KP_Enter"):
        begin_or_next()


root.bind("<Escape>", close_app)
root.bind("<Key>", on_key)
root.protocol("WM_DELETE_WINDOW", close_app)

title_label = tk.Label(
    root,
    text="VOIGHT-KAMPFF TEST CONSOLE",
    fg="red",
    bg="black",
    font=("Courier", 24, "bold")
)
title_label.pack(pady=(30, 10))

status_label = tk.Label(
    root,
    text="STANDBY",
    fg="red",
    bg="black",
    font=("Courier", 16)
)
status_label.pack(pady=(0, 15))

question_label = tk.Label(
    root,
    text="ENTER SUBJECT ID",
    fg="red",
    bg="black",
    font=("Courier", 18),
    wraplength=1000,
    justify="center"
)
question_label.pack(pady=(0, 20))

display_label = tk.Label(
    root,
    text="READY",
    fg="red",
    bg="black",
    font=("Courier", 36, "bold"),
    width=18,
    height=2,
    relief="solid",
    bd=2
)
display_label.pack(pady=10)

help_label = tk.Label(
    root,
    text="KEYBOARD: 0-9 | BACKSPACE = DELETE | C = CLEAR | ENTER = BEGIN/NEXT | ESC = EXIT",
    fg="red",
    bg="black",
    font=("Courier", 12)
)
help_label.pack(pady=(0, 20))

keypad_frame = tk.Frame(root, bg="black")
keypad_frame.pack(pady=10)

button_style = {
    "font": ("Courier", 20, "bold"),
    "bg": "black",
    "fg": "red",
    "activebackground": "black",
    "activeforeground": "red",
    "width": 6,
    "height": 2,
    "bd": 2,
    "highlightbackground": "red",
    "highlightcolor": "red",
}

buttons = [
    ("1", lambda: add_digit("1")),
    ("2", lambda: add_digit("2")),
    ("3", lambda: add_digit("3")),
    ("4", lambda: add_digit("4")),
    ("5", lambda: add_digit("5")),
    ("6", lambda: add_digit("6")),
    ("7", lambda: add_digit("7")),
    ("8", lambda: add_digit("8")),
    ("9", lambda: add_digit("9")),
    ("CLEAR", clear_input),
    ("0", lambda: add_digit("0")),
    ("BACK", backspace_input),
]

for index, (text, command) in enumerate(buttons):
    row = index // 3
    col = index % 3
    btn = tk.Button(
        keypad_frame,
        text=text,
        command=command,
        **button_style
    )
    btn.grid(row=row, column=col, padx=10, pady=10)

begin_button = tk.Button(
    root,
    text="BEGIN",
    command=begin_or_next,
    font=("Courier", 20, "bold"),
    bg="black",
    fg="red",
    activebackground="black",
    activeforeground="red",
    width=20,
    height=2,
    bd=2,
    highlightbackground="red",
    highlightcolor="red",
)
begin_button.pack(pady=25)

update_ui()
root.after(2400, start_ambient)
root.mainloop()