from pathlib import Path

from twenty20_beeper.audio import AudioPlayer


def test_audio_player_calls_backend_once() -> None:
    calls: list[Path] = []

    def fake_backend(path: Path) -> None:
        calls.append(path)

    player = AudioPlayer(asset_path=Path("assets/beep_soft.wav"), backend=fake_backend)
    player.play()
    assert calls == [Path("assets/beep_soft.wav")]
