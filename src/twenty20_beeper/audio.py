from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

AudioBackend = Callable[[Path], None]


def default_audio_backend(asset_path: Path) -> None:
    system = platform.system()
    if system == "Darwin" and shutil.which("afplay"):
        subprocess.Popen(  # noqa: S603
            ["afplay", str(asset_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return

    if system == "Windows":
        import winsound

        winsound.PlaySound(str(asset_path), winsound.SND_FILENAME | winsound.SND_ASYNC)
        return

    print("\a", end="", flush=True)


@dataclass
class AudioPlayer:
    asset_path: Path
    backend: AudioBackend = default_audio_backend

    def play(self) -> None:
        self.backend(self.asset_path)
