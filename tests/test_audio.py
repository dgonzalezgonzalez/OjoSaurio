import threading
from pathlib import Path

from twenty20_beeper.audio import AudioPlayer


def test_audio_player_calls_backend_once() -> None:
    calls: list[Path] = []

    def fake_backend(path: Path) -> None:
        calls.append(path)

    player = AudioPlayer(asset_path=Path("assets/beep_soft.wav"), backend=fake_backend)
    player.play()
    assert calls == [Path("assets/beep_soft.wav")]


def test_audio_player_nonblocking_calls_backend() -> None:
    calls: list[Path] = []
    called = threading.Event()

    def fake_backend(path: Path) -> None:
        calls.append(path)
        called.set()

    player = AudioPlayer(asset_path=Path("assets/beep_soft.wav"), backend=fake_backend)
    player.play_nonblocking()
    assert called.wait(timeout=1.0)
    assert calls == [Path("assets/beep_soft.wav")]


def test_audio_player_nonblocking_swallows_backend_errors() -> None:
    called = threading.Event()

    def bad_backend(_: Path) -> None:
        called.set()
        raise RuntimeError("boom")

    player = AudioPlayer(asset_path=Path("assets/beep_soft.wav"), backend=bad_backend)
    player.play_nonblocking()
    assert called.wait(timeout=1.0)
