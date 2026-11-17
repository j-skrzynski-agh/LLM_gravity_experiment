import pytest
from datetime import datetime
from appointments import Scheduler

NOW = datetime(2026, 1, 1, 8)

def test_one_upcoming_appointment_per_patient():
    s = Scheduler()
    s.book("P1", "Dr A", datetime(2026, 1, 5, 10), datetime(2026, 1, 5, 11), NOW)
    with pytest.raises(ValueError):
        s.book("P1", "Dr B", datetime(2026, 1, 8, 10), datetime(2026, 1, 8, 11), NOW)
