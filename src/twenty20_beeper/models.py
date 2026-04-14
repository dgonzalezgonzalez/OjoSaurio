from dataclasses import dataclass
from enum import Enum


class TimerState(str, Enum):
    FOCUS = "focus"
    BREAK = "break"


class EventType(str, Enum):
    BEEP_1 = "beep_1"
    BEEP_2 = "beep_2"


@dataclass(frozen=True)
class TimerEvent:
    event_type: EventType
    at_monotonic: float
