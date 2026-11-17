from datetime import datetime
from appointments import Scheduler

NOW = datetime(2026, 1, 1, 8)

def test_touching_appointments_allowed():
    s = Scheduler()
    s.book("P1", "Dr A", datetime(2026, 1, 5, 9), datetime(2026, 1, 5, 10), NOW)
    s.book("P2", "Dr A", datetime(2026, 1, 5, 10), datetime(2026, 1, 5, 11), NOW)
