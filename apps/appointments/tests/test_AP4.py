from datetime import datetime
from appointments import Scheduler

def test_late_cancellation_keeps_slot_blocked():
    s = Scheduler()
    aid = s.book("P1", "Dr A", datetime(2026, 1, 5, 10), datetime(2026, 1, 5, 11), datetime(2026, 1, 1, 8))
    s.cancel(aid, now=datetime(2026, 1, 5, 7))
    assert s.is_free("Dr A", datetime(2026, 1, 5, 10), datetime(2026, 1, 5, 11)) is False
