from __future__ import annotations

from dataclasses import dataclass

from .models import TimerState
from .timer_engine import TimerEngine


def format_countdown(seconds_left: int | None) -> str:
    if seconds_left is None:
        return "20:00"
    minutes = seconds_left // 60
    seconds = seconds_left % 60
    return f"{minutes:02d}:{seconds:02d}"


def format_state(engine: TimerEngine) -> str:
    if not engine.started:
        return "Ready"
    if engine.paused:
        return "Paused"
    if engine.state is TimerState.FOCUS:
        return "Focus 20m"
    return "Break 20s"


@dataclass(frozen=True)
class UiSnapshot:
    status_text: str
    countdown_text: str
    action_button_text: str


def build_snapshot(engine: TimerEngine, now: float) -> UiSnapshot:
    status = format_state(engine)
    countdown = format_countdown(engine.seconds_left(now))
    action = "Resume" if engine.paused else ("Pause" if engine.started else "Start")
    return UiSnapshot(status_text=status, countdown_text=countdown, action_button_text=action)
