import pytest
from datetime import date
from leave import LeaveTracker

def test_end_before_start_rejected():
    with pytest.raises(ValueError):
        LeaveTracker().request("ann", date(2026, 2, 10), date(2026, 2, 6), today=date(2026, 1, 1))
