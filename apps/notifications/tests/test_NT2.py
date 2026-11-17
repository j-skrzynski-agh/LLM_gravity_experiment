from datetime import datetime
from notifications import Notifier


def test_disabled_channel_not_used():
    n = Notifier()
    n.add_user("ann")
    n.set_channel("ann", "push", True)
    n.set_channel("ann", "sms", True)
    n.set_channel("ann", "sms", False)
    sent = n.send("ann", "hi", datetime(2026, 1, 5, 12, 0))
    assert "sms" not in sent and "push" in sent
