#!/usr/bin/env python3
import tkinter as tk
import pygame

root = tk.Tk()
root.title("VOIGHT-KAMPFF")
root.configure(bg="black")
root.attributes("-fullscreen", True)

current_input = ""

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


def update_display():
    if current_input:
        display_label.config(text=current_input)
    else:
        display_label.config(text="READY")


def add_digit(digit):
    global current_input
    current_input += digit
    play_click()
    update_display()


def clear_input(event=None):
    global current_input
    current_input = ""
    play_alert()
    update_display()
    status_label.config(text="INPUT CLEARED")


def backspace_input(event=None):
    global current_input
    if current_input:
        current_input = current_input[:-1]
        play_click()
        update_display()


def begin_test(event=None):
    play_click()
    if current_input:
        status_label.config(text=f"TEST IN PROGRESS : {current_input}")
    else:
        status_label.config(text="TEST IN PROGRESS")


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
        begin_test()


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
status_label.pack(pady=(0, 20))

display_label = tk.Label(
    root,
    text="READY",
    fg="red",
    bg="black",
    font=("Courier", 36, "bold"),
    width=12,
    height=2,
    relief="solid",
    bd=2
)
display_label.pack(pady=10)

help_label = tk.Label(
    root,
    text="KEYBOARD: 0-9 | BACKSPACE = DELETE | C = CLEAR | ENTER = BEGIN | ESC = EXIT",
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
    command=begin_test,
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

audio_started = False

def kick_off_audio():
    global audio_started
    if not audio_started:
        audio_started = True
        start_ambient()

root.after(2400, kick_off_audio)
root.mainloop()
