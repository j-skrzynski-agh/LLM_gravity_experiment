import pytest
from datetime import datetime
from appointments import Scheduler

def test_past_appointment_rejected():
    s = Scheduler()
    with pytest.raises(ValueError):
        s.book("P1", "Dr A", datetime(2026, 1, 5, 10), datetime(2026, 1, 5, 11), now=datetime(2026, 1, 6, 8))
