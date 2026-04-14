from __future__ import annotations

import math
import platform
import shutil
import struct
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

AudioBackend = Callable[[Path], None]


def _build_tone_wav_bytes(
    *,
    frequency_hz: float = 880.0,
    duration_s: float = 0.14,
    volume: float = 0.18,
    sample_rate: int = 44100,
) -> bytes:
    frames_count = int(sample_rate * duration_s)
    pcm = bytearray()
    for i in range(frames_count):
        sample = math.sin(2.0 * math.pi * frequency_hz * (i / sample_rate))
        value = int(32767 * volume * sample)
        pcm.extend(struct.pack("<h", value))

    data_size = len(pcm)
    channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * channels * (bits_per_sample // 8)
    block_align = channels * (bits_per_sample // 8)

    header = bytearray()
    header.extend(b"RIFF")
    header.extend(struct.pack("<I", 36 + data_size))
    header.extend(b"WAVE")
    header.extend(b"fmt ")
    header.extend(struct.pack("<IHHIIHH", 16, 1, channels, sample_rate, byte_rate, block_align, bits_per_sample))
    header.extend(b"data")
    header.extend(struct.pack("<I", data_size))
    return bytes(header + pcm)


_WINDOWS_TONE_WAV = _build_tone_wav_bytes()


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

        try:
            winsound.PlaySound(_WINDOWS_TONE_WAV, winsound.SND_MEMORY | winsound.SND_ASYNC)
        except RuntimeError:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        return

    print("\a", end="", flush=True)


@dataclass
class AudioPlayer:
    asset_path: Path
    backend: AudioBackend = default_audio_backend

    def play(self) -> None:
        self.backend(self.asset_path)
