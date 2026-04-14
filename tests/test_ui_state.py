from twenty20_beeper.config import Settings
from twenty20_beeper.timer_engine import TimerEngine
from twenty20_beeper.ui import build_snapshot


def test_snapshot_ready_before_start() -> None:
    eng = TimerEngine(settings=Settings())
    snap = build_snapshot(eng, now=0.0)
    assert snap.status_text == "Ready"
    assert snap.countdown_text == "20:00"
    assert snap.action_button_text == "Start"


def test_snapshot_paused_has_resume() -> None:
    eng = TimerEngine(settings=Settings())
    eng.start(now=0.0)
    eng.pause(now=10.0)
    snap = build_snapshot(eng, now=10.0)
    assert snap.status_text == "Paused"
    assert snap.action_button_text == "Resume"
