import pytest
from datetime import date
from leave import LeaveTracker

def test_not_enough_days():
    t = LeaveTracker(days_per_year=5)
    t.request("ann", date(2026, 1, 5), date(2026, 1, 9), today=date(2025, 12, 1))
    with pytest.raises(ValueError):
        t.request("ann", date(2026, 1, 12), date(2026, 1, 12), today=date(2025, 12, 1))
