#!/usr/bin/env python3
"""
Voight-Kampff Prop Console
- Fullscreen Tkinter UI
- Offline voice via pyttsx3
- Ollama integration via local HTTP API
- Keyboard-driven interrogation flow

Keys:
  SPACE   = ask next built-in question
  O       = send current question to Ollama for a live response
  R       = random result
  C       = clear transcript
  ESC     = quit fullscreen
  Q       = quit
"""

import json
import queue
import random
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

import requests

try:
    import pyttsx3
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False


# =========================
# CONFIG
# =========================
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL = "llama3.1:8b"   # change this to your installed model
WINDOW_TITLE = "VOIGHT-KAMPFF UNIT"
ENABLE_VOICE = True
VOICE_RATE = 155
VOICE_VOLUME = 1.0

QUESTIONS = [
    "You see a tortoise on its back in the desert. What do you do?",
    "A wasp lands on your wrist while you are holding a child's photograph. Describe your feeling.",
    "You find a wallet full of cash in a hallway with no cameras. What happens next?",
    "Someone laughs while describing a tragedy. What do you notice first?",
    "Your dog is old, sick, and in pain. The vet asks for a decision. Speak.",
    "A friend betrays you and then asks for forgiveness. What changes inside you?",
    "You are given a perfect memory that never happened. Do you keep it?",
    "A child asks if machines can dream. Answer carefully.",
    "You hear crying through a locked door. There is risk in opening it. What do you do?",
    "Tell me about your mother.",
]

SYSTEM_PROMPT = """You are the dialogue engine for a fictional Voight-Kampff interrogation prop inspired by retro-futuristic cinema.
Respond in 1 to 3 sentences.
Tone: clinical, eerie, intelligent.
Do not mention being an AI.
Occasionally refer to pupil response, autonomic stress, empathic drift, or baseline deviation.
"""

RESULTS = [
    "RESULT: HUMAN RESPONSE WITH ELEVATED STRESS MARKERS",
    "RESULT: INCONCLUSIVE — BASELINE DRIFT DETECTED",
    "RESULT: EMPATHIC LATENCY OUTSIDE HUMAN NORM",
    "RESULT: POSSIBLE REPLICANT PROFILE",
    "RESULT: BASELINE ACCEPTED",
]


# =========================
# APP
# =========================
class VKApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)

        self.tts_engine = None
        self.voice_queue = queue.Queue()
        self.current_question_index = -1
        self.current_question = ""
        self.is_analyzing = False

        self._build_ui()
        self._bind_keys()
        self._init_tts()
        self._start_voice_worker()
        self._boot_sequence()

    def _build_ui(self):
        self.header = tk.Label(
            self.root,
            text="VOIGHT-KAMPFF INTERROGATION CONSOLE",
            font=("Courier", 28, "bold"),
            fg="#ff3b3b",
            bg="black",
            pady=18
        )
        self.header.pack(fill="x")

        self.status_var = tk.StringVar(value="STATUS: IDLE")
        self.status = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Courier", 18, "bold"),
            fg="#f5f5f5",
            bg="black",
            anchor="w",
            padx=30
        )
        self.status.pack(fill="x")

        self.scan_var = tk.StringVar(value="PUPIL RESPONSE: --")
        self.scan = tk.Label(
            self.root,
            textvariable=self.scan_var,
            font=("Courier", 16),
            fg="#bdbdbd",
            bg="black",
            anchor="w",
            padx=30,
            pady=10
        )
        self.scan.pack(fill="x")

        self.question_frame = tk.Frame(self.root, bg="black", highlightbackground="#660000", highlightthickness=2)
        self.question_frame.pack(fill="x", padx=30, pady=12)

        self.question_label = tk.Label(
            self.question_frame,
            text="PRESS SPACE TO BEGIN",
            font=("Courier", 24, "bold"),
            fg="#ffcccc",
            bg="black",
            wraplength=1200,
            justify="left",
            padx=20,
            pady=20
        )
        self.question_label.pack(fill="x")

        self.transcript = scrolledtext.ScrolledText(
            self.root,
            font=("Courier", 14),
            bg="#050505",
            fg="#d9d9d9",
            insertbackground="white",
            wrap=tk.WORD,
            height=18,
            bd=2,
            relief="flat"
        )
        self.transcript.pack(fill="both", expand=True, padx=30, pady=18)

        self.footer = tk.Label(
            self.root,
            text="SPACE next question   |   O ollama response   |   R random result   |   C clear   |   ESC exit fullscreen   |   Q quit",
            font=("Courier", 12),
            fg="#888888",
            bg="black",
            pady=12
        )
        self.footer.pack(fill="x")

    def _bind_keys(self):
        self.root.bind("<space>", lambda e: self.ask_next_question())
        self.root.bind("<o>", lambda e: self.ask_ollama())
        self.root.bind("<O>", lambda e: self.ask_ollama())
        self.root.bind("<r>", lambda e: self.random_result())
        self.root.bind("<R>", lambda e: self.random_result())
        self.root.bind("<c>", lambda e: self.clear_transcript())
        self.root.bind("<C>", lambda e: self.clear_transcript())
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.bind("<q>", lambda e: self.root.destroy())
        self.root.bind("<Q>", lambda e: self.root.destroy())

    def _init_tts(self):
        if not ENABLE_VOICE or not TTS_AVAILABLE:
            return
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty("rate", VOICE_RATE)
            self.tts_engine.setProperty("volume", VOICE_VOLUME)
        except Exception:
            self.tts_engine = None

    def _start_voice_worker(self):
        def worker():
            while True:
                text = self.voice_queue.get()
                if text is None:
                    break
                if self.tts_engine:
                    try:
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    except Exception:
                        pass
                self.voice_queue.task_done()

        threading.Thread(target=worker, daemon=True).start()

    def speak(self, text: str):
        if ENABLE_VOICE and self.tts_engine:
            self.voice_queue.put(text)

    def write_transcript(self, speaker: str, text: str):
        timestamp = time.strftime("%H:%M:%S")
        self.transcript.insert(tk.END, f"[{timestamp}] {speaker}: {text}\n\n")
        self.transcript.see(tk.END)

    def _boot_sequence(self):
        boot_lines = [
            "BOOTING UNIT...",
            "LOADING EMPATHIC RESPONSE MATRICES...",
            "CALIBRATING PUPIL TRACKER...",
            "READY."
        ]

        def run():
            for line in boot_lines:
                self.write_transcript("SYSTEM", line)
                self.status_var.set(f"STATUS: {line}")
                time.sleep(0.6)
            self.status_var.set("STATUS: READY")
            self.scan_var.set("PUPIL RESPONSE: STABLE")
            self.question_label.config(text="PRESS SPACE TO BEGIN")
            self.speak("Voight Kampff unit ready.")

        threading.Thread(target=run, daemon=True).start()

    def ask_next_question(self):
        self.current_question_index = (self.current_question_index + 1) % len(QUESTIONS)
        self.current_question = QUESTIONS[self.current_question_index]
        self.question_label.config(text=self.current_question)
        self.status_var.set("STATUS: INTERROGATION ACTIVE")
        self.scan_var.set(f"PUPIL RESPONSE: {random.randint(12, 42)} ms")
        self.write_transcript("UNIT", self.current_question)
        self.speak(self.current_question)

    def ask_ollama(self):
        if not self.current_question:
            self.ask_next_question()
            return

        if self.is_analyzing:
            return

        self.is_analyzing = True
        self.status_var.set("STATUS: ANALYZING")
        self.scan_var.set("PUPIL RESPONSE: SAMPLING AUTONOMIC VARIANCE...")
        self.write_transcript("SYSTEM", "Submitting interrogation vector to local cognitive engine...")

        def worker():
            try:
                payload = {
                    "model": OLLAMA_MODEL,
                    "prompt": f"{SYSTEM_PROMPT}\n\nQuestion: {self.current_question}\nResponse:",
                    "stream": False
                }
                response = requests.post(OLLAMA_URL, json=payload, timeout=90)
                response.raise_for_status()
                data = response.json()
                text = data.get("response", "").strip()

                if not text:
                    text = "No usable response returned from local model."

                self.root.after(0, lambda: self._handle_ollama_response(text))
            except Exception as exc:
                self.root.after(0, lambda: self._handle_ollama_response(f"OLLAMA ERROR: {exc}"))
            finally:
                self.is_analyzing = False

        threading.Thread(target=worker, daemon=True).start()

    def _handle_ollama_response(self, text: str):
        self.write_transcript("SUBJECT", text)
        self.speak(text)
        self.status_var.set("STATUS: RESPONSE CAPTURED")
        self.scan_var.set(
            f"PUPIL RESPONSE: {random.randint(18, 67)} ms | BLUSH INDEX: {random.randint(1, 9)}"
        )

    def random_result(self):
        result = random.choice(RESULTS)
        self.write_transcript("SYSTEM", result)
        self.status_var.set("STATUS: EVALUATION COMPLETE")
        self.scan_var.set("PUPIL RESPONSE: FINALIZED")
        self.question_label.config(text=result)
        self.speak(result)

    def clear_transcript(self):
        self.transcript.delete("1.0", tk.END)
        self.write_transcript("SYSTEM", "Transcript cleared.")
        self.status_var.set("STATUS: READY")
        self.scan_var.set("PUPIL RESPONSE: STABLE")
        self.question_label.config(text="PRESS SPACE TO BEGIN")


def main():
    root = tk.Tk()
    app = VKApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
