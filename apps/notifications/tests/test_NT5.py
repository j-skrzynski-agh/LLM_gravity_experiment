from datetime import datetime
from notifications import Notifier

def test_new_user_has_only_email():
    n = Notifier()
    n.add_user("ann")
    assert n.send("ann", "hi", datetime(2026, 1, 5, 12, 0)) == ["email"]
