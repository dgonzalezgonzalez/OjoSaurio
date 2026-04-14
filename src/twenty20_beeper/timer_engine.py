from dataclasses import dataclass

from .config import Settings
from .models import EventType, TimerEvent, TimerState


@dataclass
class TimerEngine:
    settings: Settings
    state: TimerState = TimerState.FOCUS
    started: bool = False
    paused: bool = False
    _deadline: float | None = None
    _remaining: float | None = None

    def start(self, now: float) -> None:
        self.state = TimerState.FOCUS
        self.started = True
        self.paused = False
        self._remaining = None
        self._deadline = now + self.settings.focus_seconds

    def pause(self, now: float) -> None:
        if not self.started or self.paused or self._deadline is None:
            return
        self._remaining = max(0.0, self._deadline - now)
        self.paused = True

    def resume(self, now: float) -> None:
        if not self.started or not self.paused:
            return
        remaining = self._remaining if self._remaining is not None else self._default_duration()
        self._deadline = now + remaining
        self._remaining = None
        self.paused = False

    def tick(self, now: float) -> list[TimerEvent]:
        if not self.started or self.paused or self._deadline is None:
            return []
        if now < 0:
            return []

        if self.state is TimerState.FOCUS and now >= self._deadline:
            self.state = TimerState.BREAK
            self._deadline = now + self.settings.break_seconds
            return [TimerEvent(event_type=EventType.BEEP_1, at_monotonic=now)]

        if self.state is TimerState.BREAK and now >= self._deadline:
            self.state = TimerState.FOCUS
            self._deadline = now + self.settings.focus_seconds
            return [TimerEvent(event_type=EventType.BEEP_2, at_monotonic=now)]

        return []

    def seconds_left(self, now: float) -> int | None:
        if not self.started:
            return None
        if self.paused:
            remaining = self._remaining if self._remaining is not None else self._default_duration()
            return int(round(max(0.0, remaining)))
        if self._deadline is None:
            return None
        return int(round(max(0.0, self._deadline - now)))

    def _default_duration(self) -> float:
        if self.state is TimerState.FOCUS:
            return float(self.settings.focus_seconds)
        return float(self.settings.break_seconds)
