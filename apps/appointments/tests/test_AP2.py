import pytest
from datetime import datetime
from appointments import Scheduler

NOW = datetime(2026, 1, 1, 8)

def test_overlap_rejected():
    s = Scheduler()
    s.book("P1", "Dr A", datetime(2026, 1, 5, 10), datetime(2026, 1, 5, 11), NOW)
    with pytest.raises(ValueError):
        s.book("P2", "Dr A", datetime(2026, 1, 5, 10, 30), datetime(2026, 1, 5, 11, 30), NOW)
