from datetime import datetime, time
from notifications import Notifier

def test_quiet_hours_span_midnight():
    n = Notifier(quiet_start=time(22, 0), quiet_end=time(7, 0))
    n.add_user("ann")
    for c in ["email", "sms", "push"]:
        n.set_channel("ann", c, True)
    night = n.send("ann", "hi", datetime(2026, 1, 5, 2, 0))
    assert "sms" not in night and "push" not in night
    day = n.send("ann", "hi", datetime(2026, 1, 5, 12, 0))
    assert "sms" in day and "push" in day
