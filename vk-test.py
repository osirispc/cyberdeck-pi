#!/usr/bin/env python3
import tkinter as tk
import pygame

root = tk.Tk()
root.title("VK TEST")
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
        label.config(text=current_input)
    else:
        label.config(text="VK TEST WINDOW")

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

def backspace_input(event=None):
    global current_input
    if current_input:
        current_input = current_input[:-1]
        play_click()
        update_display()

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

root.bind("<Escape>", close_app)
root.bind("<Key>", on_key)

label = tk.Label(
    root,
    text="VK TEST WINDOW",
    fg="red",
    bg="black",
    font=("Courier", 24)
)
label.pack(expand=True)

help_label = tk.Label(
    root,
    text="0-9 = input   BACKSPACE = delete   C = clear   ESC = exit",
    fg="red",
    bg="black",
    font=("Courier", 14)
)
help_label.pack(pady=20)

root.after(2400, start_ambient)
root.after(5000, lambda: None)

root.mainloop()
