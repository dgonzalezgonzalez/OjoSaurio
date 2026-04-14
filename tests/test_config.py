import pytest

from twenty20_beeper.config import Settings


def test_defaults_match_rule_20_20_20() -> None:
    cfg = Settings()
    assert cfg.focus_seconds == 1200
    assert cfg.break_seconds == 20


def test_invalid_focus_rejected() -> None:
    with pytest.raises(ValueError, match="focus_seconds"):
        Settings(focus_seconds=0)


def test_invalid_break_rejected() -> None:
    with pytest.raises(ValueError, match="break_seconds"):
        Settings(break_seconds=-1)


def test_from_env_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TWENTY20_FOCUS_SECONDS", "30")
    monkeypatch.setenv("TWENTY20_BREAK_SECONDS", "20")
    cfg = Settings.from_env()
    assert cfg.focus_seconds == 30
    assert cfg.break_seconds == 20
