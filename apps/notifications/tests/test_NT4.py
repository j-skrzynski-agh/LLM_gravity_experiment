from datetime import datetime, time
from notifications import Notifier

def test_email_delivered_in_quiet_hours():
    n = Notifier(quiet_start=time(22, 0), quiet_end=time(7, 0))
    n.add_user("ann")
    for c in ["email", "sms", "push"]:
        n.set_channel("ann", c, True)
    assert "email" in n.send("ann", "hi", datetime(2026, 1, 5, 23, 0))
