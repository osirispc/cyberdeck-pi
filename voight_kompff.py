#!/usr/bin/env python3
import json
import random
import tkinter as tk
from pathlib import Path
from datetime import datetime
from tkinter import scrolledtext

APP_DIR = Path(__file__).resolve().parent
REPORT_DIR = APP_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

QUESTIONS = [
    "You are reading a magazine. You come across a full-page photo of a nude model. Is this testing whether I am a replicant or whether I am a lesbian, Mr. Deckard?",
    "You're in a desert, walking in the sand, when all of a sudden you look down and see a tortoise. It's crawling toward you. You reach down and flip the tortoise over on its back.",
    "Describe in single words only the good things that come into your mind about your mother.",
    "A child shows you a butterfly collection. One specimen is still alive, pinned through the abdomen. What do you do?",
    "You find a wallet on the sidewalk. There is money inside and a family photo. What is the first thing you notice?",
    "You see a wasp land on a stranger's cheek. The stranger does not notice. What do you do?",
    "Someone gives you a calfskin wallet for your birthday. How do you respond?",
    "A friend laughs while telling you their dog died. What do you think is happening?",
    "You are watching an old home movie and realize one person in the frame was never really there. How do you feel?",
    "A power failure knocks out the city. A child nearby begins to cry. What do you do first?",
]

SUBJECTS = [
    "LEON-09", "RACHAEL-07", "PRIS-14", "ZHORA-03", "K-21", "LUV-02", "DECKARD-01"
]


class VKApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Voight-Kampff")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)

        self.session_active = False
        self.session_started_at = None
        self.session_id = self.new_session_id()
        self.subject_id = random.choice(SUBJECTS)
        self.operator = "DECKARD"
        self.question_index = 0
        self.response_level = 50
        self.pulse = 72
        self.respiration = 12
        self.baseline = 1.02
        self.pupil = 3.3
        self.verdict = "AWAITING BASELINE"
        self.history = []

        self.title_var = tk.StringVar(value="VOIGHT-KAMPFF EMPATHY RESPONSE ANALYZER")
        self.status_var = tk.StringVar(value="SYSTEM READY")
        self.session_var = tk.StringVar(value=self.session_id)
        self.subject_var = tk.StringVar(value=self.subject_id)
        self.clock_var = tk.StringVar(value="")
        self.pulse_var = tk.StringVar(value="")
        self.resp_var = tk.StringVar(value="")
        self.base_var = tk.StringVar(value="")
        self.pupil_var = tk.StringVar(value="")
        self.verdict_var = tk.StringVar(value=self.verdict)
        self.question_var = tk.StringVar(value="Press START TEST to begin.")
        self.scale_var = tk.StringVar(value="NEUTRAL RESPONSE")

        self.build_ui()
        self.bind_keys()
        self.refresh_metrics()
        self.log("Voight-Kampff console online.")
        self.log("Press START TEST to initialize a subject session.")
        self.tick()

    def new_session_id(self) -> str:
        return datetime.now().strftime("VK-%Y%m%d-%H%M%S")

    def build_ui(self) -> None:
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        header = tk.Frame(self.root, bg="black", highlightbackground="#7a0000", highlightthickness=1)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=18, pady=(18, 10))
        header.grid_columnconfigure(1, weight=1)

        tk.Label(
            header,
            textvariable=self.title_var,
            bg="black",
            fg="#ff4040",
            font=("Courier", 22, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))

        tk.Label(
            header,
            textvariable=self.status_var,
            bg="black",
            fg="#ffd166",
            font=("Courier", 12),
            anchor="w",
        ).grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        tk.Label(
            header,
            textvariable=self.clock_var,
            bg="black",
            fg="#9ad1ff",
            font=("Courier", 12),
            anchor="e",
        ).grid(row=0, column=1, rowspan=2, sticky="e", padx=14)

        side = tk.Frame(self.root, bg="black", highlightbackground="#333333", highlightthickness=1, width=320)
        side.grid(row=1, column=0, sticky="nsw", padx=(18, 10), pady=(0, 18))
        side.grid_propagate(False)

        self.side_value(side, "SESSION", self.session_var, 0)
        self.side_value(side, "SUBJECT", self.subject_var, 1)
        self.side_value(side, "OPERATOR", tk.StringVar(value=self.operator), 2)
        self.side_value(side, "PULSE", self.pulse_var, 3)
        self.side_value(side, "RESPIRATION", self.resp_var, 4)
        self.side_value(side, "BASELINE SHIFT", self.base_var, 5)
        self.side_value(side, "PUPIL SCALE", self.pupil_var, 6)
        self.side_value(side, "VERDICT", self.verdict_var, 7)

        controls = tk.Frame(side, bg="black")
        controls.grid(row=8, column=0, sticky="ew", padx=12, pady=(18, 8))
        controls.grid_columnconfigure((0, 1), weight=1)

        self.make_btn(controls, "START TEST", self.start_test).grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "NEXT QUESTION", self.next_question).grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "CALM", lambda: self.record_response(20, "CALM")).grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "NEUTRAL", lambda: self.record_response(50, "NEUTRAL")).grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "AGITATED", lambda: self.record_response(80, "AGITATED")).grid(row=2, column=0, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "HOSTILE", lambda: self.record_response(95, "HOSTILE")).grid(row=2, column=1, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "SAVE REPORT", self.save_report).grid(row=3, column=0, sticky="ew", padx=4, pady=4)
        self.make_btn(controls, "RESET", self.reset_session).grid(row=3, column=1, sticky="ew", padx=4, pady=4)

        main = tk.Frame(self.root, bg="black", highlightbackground="#333333", highlightthickness=1)
        main.grid(row=1, column=1, sticky="nsew", padx=(10, 18), pady=(0, 18))
        main.grid_rowconfigure(4, weight=1)
        main.grid_columnconfigure(0, weight=1)

        tk.Label(
            main,
            text="CURRENT PROMPT",
            bg="black",
            fg="#ffd166",
            font=("Courier", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 8))

        tk.Label(
            main,
            textvariable=self.question_var,
            bg="black",
            fg="#f5f5f5",
            font=("Courier", 20),
            justify="left",
            wraplength=860,
            anchor="w",
        ).grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))

        meter_frame = tk.Frame(main, bg="black")
        meter_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 8))
        meter_frame.grid_columnconfigure(0, weight=1)

        tk.Label(
            meter_frame,
            text="EMPATHY RESPONSE SCALE",
            bg="black",
            fg="#ffd166",
            font=("Courier", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.meter = tk.Canvas(
            meter_frame,
            width=880,
            height=36,
            bg="#111111",
            highlightbackground="#7a0000",
            highlightthickness=1,
        )
        self.meter.grid(row=1, column=0, sticky="ew")
        self.meter_fill = self.meter.create_rectangle(0, 0, 0, 36, fill="#ff4040", width=0)

        tk.Label(
            meter_frame,
            textvariable=self.scale_var,
            bg="black",
            fg="#9ad1ff",
            font=("Courier", 12),
            anchor="w",
        ).grid(row=2, column=0, sticky="ew", pady=(8, 0))

        tk.Label(
            main,
            text="CONSOLE",
            bg="black",
            fg="#ffd166",
            font=("Courier", 13, "bold"),
            anchor="w",
        ).grid(row=3, column=0, sticky="ew", padx=18, pady=(12, 8))

        self.console = scrolledtext.ScrolledText(
            main,
            bg="#050505",
            fg="#90ee90",
            insertbackground="#90ee90",
            font=("Courier", 11),
            relief="flat",
            height=12,
            wrap="word",
        )
        self.console.grid(row=4, column=0, sticky="nsew", padx=18, pady=(0, 18))

        footer = tk.Label(
            self.root,
            text="SPACE/ENTER: NEXT   LEFT/RIGHT: ADJUST RESPONSE   S: START   R: RESET   F5: SAVE REPORT   ESC: EXIT",
            bg="black",
            fg="#666666",
            font=("Courier", 10),
        )
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 12))

    def side_value(self, parent: tk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        box = tk.Frame(parent, bg="black", highlightbackground="#1d1d1d", highlightthickness=1)
        box.grid(row=row, column=0, sticky="ew", padx=12, pady=7)
        tk.Label(
            box,
            text=label,
            bg="black",
            fg="#888888",
            font=("Courier", 10, "bold"),
            anchor="w",
        ).pack(anchor="w", padx=10, pady=(8, 2))
        tk.Label(
            box,
            textvariable=variable,
            bg="black",
            fg="#f5f5f5",
            font=("Courier", 13),
            anchor="w",
        ).pack(anchor="w", padx=10, pady=(0, 8))

    def make_btn(self, parent: tk.Frame, text: str, command) -> tk.Button:
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#130000",
            fg="#ff6b6b",
            activebackground="#2b0000",
            activeforeground="#ffd166",
            relief="ridge",
            bd=2,
            font=("Courier", 11, "bold"),
            padx=8,
            pady=8,
            highlightthickness=0,
        )

    def bind_keys(self) -> None:
        self.root.bind("<Escape>", lambda event: self.root.destroy())
        self.root.bind("<Return>", lambda event: self.next_question())
        self.root.bind("<space>", lambda event: self.next_question())
        self.root.bind("<Left>", lambda event: self.bump_response(-5))
        self.root.bind("<Right>", lambda event: self.bump_response(5))
        self.root.bind("<s>", lambda event: self.start_test())
        self.root.bind("<S>", lambda event: self.start_test())
        self.root.bind("<r>", lambda event: self.reset_session())
        self.root.bind("<R>", lambda event: self.reset_session())
        self.root.bind("<F5>", lambda event: self.save_report())

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")

    def refresh_metrics(self) -> None:
        self.pulse_var.set(f"{self.pulse} BPM")
        self.resp_var.set(f"{self.respiration} RPM")
        self.base_var.set(f"{self.baseline:.2f}x")
        self.pupil_var.set(f"{self.pupil:.1f} mm")
        self.verdict_var.set(self.verdict)

        width = int(self.meter.winfo_width() or 880)
        fill = int(width * (self.response_level / 100))
        self.meter.coords(self.meter_fill, 0, 0, fill, 36)

        if self.response_level < 30:
            scale = "CONTROLLED / LOW REACTIVITY"
        elif self.response_level < 60:
            scale = "NEUTRAL / BASELINE DRIFT"
        elif self.response_level < 80:
            scale = "ELEVATED / EMPATHIC STRAIN"
        else:
            scale = "CRITICAL / POSSIBLE REPLICANT RESPONSE"
        self.scale_var.set(f"{scale}   [{self.response_level:03d}]")

    def start_test(self) -> None:
        self.session_active = True
        self.session_started_at = datetime.now()
        self.session_id = self.new_session_id()
        self.subject_id = random.choice(SUBJECTS)
        self.session_var.set(self.session_id)
        self.subject_var.set(self.subject_id)
        self.question_index = 0
        self.history = []
        self.status_var.set("SESSION ACTIVE")
        self.question_var.set(QUESTIONS[self.question_index])
        self.record_response(50, "BASELINE", autosave=False)
        self.log(f"Session {self.session_id} started for subject {self.subject_id}.")
        self.log("Baseline calibrated. Proceed with question one.")

    def next_question(self) -> None:
        if not self.session_active:
            self.start_test()
            return
        self.question_index = (self.question_index + 1) % len(QUESTIONS)
        self.question_var.set(QUESTIONS[self.question_index])
        self.log(f"Prompt advanced to item {self.question_index + 1}/{len(QUESTIONS)}.")

    def bump_response(self, delta: int) -> None:
        self.record_response(max(0, min(100, self.response_level + delta)), "MANUAL ADJUST")

    def record_response(self, level: int, label: str, autosave: bool = True) -> None:
        self.response_level = max(0, min(100, level))
        intensity = self.response_level / 100.0

        self.pulse = int(68 + intensity * 56 + random.randint(-3, 4))
        self.respiration = int(11 + intensity * 11 + random.randint(0, 2))
        self.baseline = round(0.92 + intensity * 0.62 + random.uniform(-0.03, 0.03), 2)
        self.pupil = round(3.0 + intensity * 2.6 + random.uniform(-0.2, 0.2), 1)

        if self.response_level >= 85 or self.baseline >= 1.45:
            self.verdict = "REVIEW: REPLICANT RISK"
        elif self.response_level >= 65:
            self.verdict = "INCONCLUSIVE: ELEVATED STRESS"
        else:
            self.verdict = "HUMAN RANGE / BASELINE HOLDING"

        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "question_index": self.question_index,
            "question": QUESTIONS[self.question_index] if self.session_active else "N/A",
            "response_label": label,
            "response_level": self.response_level,
            "pulse": self.pulse,
            "respiration": self.respiration,
            "baseline": self.baseline,
            "pupil": self.pupil,
            "verdict": self.verdict,
        }

        if autosave and self.session_active:
            self.history.append(entry)

        self.refresh_metrics()
        self.log(
            f"{label}: level={self.response_level:03d} pulse={self.pulse} "
            f"baseline={self.baseline:.2f} verdict={self.verdict}"
        )

    def reset_session(self) -> None:
        self.session_active = False
        self.session_started_at = None
        self.session_id = self.new_session_id()
        self.subject_id = random.choice(SUBJECTS)
        self.session_var.set(self.session_id)
        self.subject_var.set(self.subject_id)
        self.question_index = 0
        self.response_level = 50
        self.pulse = 72
        self.respiration = 12
        self.baseline = 1.02
        self.pupil = 3.3
        self.verdict = "AWAITING BASELINE"
        self.question_var.set("Press START TEST to begin.")
        self.status_var.set("SYSTEM READY")
        self.history = []
        self.refresh_metrics()
        self.log("Session reset. Ready for next subject.")

    def save_report(self) -> None:
        payload = {
            "session_id": self.session_var.get(),
            "subject_id": self.subject_var.get(),
            "operator": self.operator,
            "started_at": self.session_started_at.isoformat(timespec="seconds") if self.session_started_at else None,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
            "verdict": self.verdict,
            "history": self.history,
        }

        filename = REPORT_DIR / f"{self.session_var.get()}.json"
        with filename.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)

        self.log(f"Report saved: {filename}")
        self.status_var.set(f"REPORT SAVED -> {filename.name}")

    def tick(self) -> None:
        self.clock_var.set(datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        if self.session_active:
            drift = random.choice([-1, 0, 0, 1])
            nudged = max(0, min(100, self.response_level + drift))
            if nudged != self.response_level:
                self.response_level = nudged
                self.refresh_metrics()
        self.root.after(350, self.tick)


def main() -> None:
    root = tk.Tk()
    VKApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
