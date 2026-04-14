from __future__ import annotations

import time
import tkinter as tk
from pathlib import Path

from .audio import AudioPlayer
from .config import Settings
from .models import EventType
from .timer_engine import TimerEngine
from .ui import build_snapshot


class TwentyTwentyApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("OjoSaurio")
        self.root.geometry("280x180")
        self.root.resizable(False, False)

        self.settings = Settings()
        self.engine = TimerEngine(settings=self.settings)

        root_dir = Path(__file__).resolve().parents[2]
        self.audio = AudioPlayer(asset_path=root_dir / "assets" / "beep_soft.wav")

        self.status_var = tk.StringVar(value="Ready")
        self.countdown_var = tk.StringVar(value="20:00")
        self.action_var = tk.StringVar(value="Start")

        self._build_layout()
        self._start_timer_now()
        self.root.after(200, self._bring_to_front)
        self._refresh_ui()
        self._schedule_tick()

    def _build_layout(self) -> None:
        container = tk.Frame(self.root, padx=16, pady=16)
        container.pack(fill=tk.BOTH, expand=True)

        tk.Label(container, text="OjoSaurio 20-20-20", font=("Helvetica", 13, "bold")).pack(pady=(0, 10))
        tk.Label(container, textvariable=self.status_var, font=("Helvetica", 11)).pack()
        tk.Label(container, textvariable=self.countdown_var, font=("Menlo", 24, "bold")).pack(pady=(6, 12))

        controls = tk.Frame(container)
        controls.pack()
        tk.Button(controls, textvariable=self.action_var, width=10, command=self._toggle_start_pause).pack(
            side=tk.LEFT, padx=4
        )
        tk.Button(controls, text="Exit", width=10, command=self.root.destroy).pack(side=tk.LEFT, padx=4)

    def _toggle_start_pause(self) -> None:
        now = time.monotonic()
        if not self.engine.started:
            self.engine.start(now)
        elif self.engine.paused:
            self.engine.resume(now)
        else:
            self.engine.pause(now)
        self._refresh_ui()

    def _start_timer_now(self) -> None:
        self.engine.start(time.monotonic())

    def _bring_to_front(self) -> None:
        try:
            self.root.lift()
            self.root.focus_force()
        except tk.TclError:
            pass

    def _schedule_tick(self) -> None:
        self._tick_once()
        self.root.after(100, self._schedule_tick)

    def _tick_once(self) -> None:
        now = time.monotonic()
        events = self.engine.tick(now)
        for event in events:
            if event.event_type in {EventType.BEEP_1, EventType.BEEP_2}:
                self.audio.play()
        self._refresh_ui(now=now)

    def _refresh_ui(self, now: float | None = None) -> None:
        current = now if now is not None else time.monotonic()
        snap = build_snapshot(self.engine, current)
        self.status_var.set(snap.status_text)
        self.countdown_var.set(snap.countdown_text)
        self.action_var.set(snap.action_button_text)

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    app = TwentyTwentyApp()
    app.run()


if __name__ == "__main__":
    main()
