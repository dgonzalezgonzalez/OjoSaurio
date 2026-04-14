import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    focus_seconds: int = 20 * 60
    break_seconds: int = 20

    def __post_init__(self) -> None:
        if self.focus_seconds <= 0:
            raise ValueError("focus_seconds must be > 0")
        if self.break_seconds <= 0:
            raise ValueError("break_seconds must be > 0")

    @classmethod
    def from_env(cls) -> "Settings":
        focus_raw = os.getenv("TWENTY20_FOCUS_SECONDS", "1200")
        break_raw = os.getenv("TWENTY20_BREAK_SECONDS", "20")
        return cls(focus_seconds=int(focus_raw), break_seconds=int(break_raw))
