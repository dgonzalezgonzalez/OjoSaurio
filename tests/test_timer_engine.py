from twenty20_beeper.config import Settings
from twenty20_beeper.models import EventType, TimerState
from twenty20_beeper.timer_engine import TimerEngine


def test_full_cycle_beep1_then_beep2_then_next_focus() -> None:
    eng = TimerEngine(settings=Settings(focus_seconds=1200, break_seconds=20))
    eng.start(now=0.0)

    ev1 = eng.tick(now=1200.0)
    assert [x.event_type for x in ev1] == [EventType.BEEP_1]
    assert eng.state is TimerState.BREAK

    ev2 = eng.tick(now=1220.0)
    assert [x.event_type for x in ev2] == [EventType.BEEP_2]
    assert eng.state is TimerState.FOCUS


def test_pause_resume_preserves_remaining_time() -> None:
    eng = TimerEngine(settings=Settings(focus_seconds=1200, break_seconds=20))
    eng.start(now=0.0)
    eng.pause(now=100.0)
    assert eng.paused is True
    assert eng.seconds_left(now=100.0) == 1100

    eng.resume(now=200.0)
    assert eng.paused is False
    assert eng.seconds_left(now=200.0) == 1100


def test_pause_resume_inside_break_window() -> None:
    eng = TimerEngine(settings=Settings(focus_seconds=1200, break_seconds=20))
    eng.start(now=0.0)
    eng.tick(now=1200.0)
    eng.pause(now=1205.0)
    assert eng.seconds_left(now=1205.0) == 15

    eng.resume(now=1300.0)
    ev = eng.tick(now=1315.0)
    assert [x.event_type for x in ev] == [EventType.BEEP_2]
    assert eng.state is TimerState.FOCUS


def test_large_sleep_jump_no_beep_burst() -> None:
    eng = TimerEngine(settings=Settings(focus_seconds=1200, break_seconds=20))
    eng.start(now=0.0)
    ev = eng.tick(now=1800.0)
    assert [x.event_type for x in ev] == [EventType.BEEP_1]
    # Immediate second tick at same timestamp should not create second beep.
    assert eng.tick(now=1800.0) == []


def test_negative_now_ignored() -> None:
    eng = TimerEngine(settings=Settings())
    eng.start(now=1.0)
    assert eng.tick(now=-5.0) == []
