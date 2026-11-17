import pytest
from datetime import date
from leave import LeaveTracker


def test_short_notice_rejected():
    t = LeaveTracker()
    with pytest.raises(ValueError):
        t.request("ann", date(2026, 1, 5), date(2026, 1, 5), today=date(2026, 1, 4))   # 1 dzień przed
    t.request("ann", date(2026, 1, 5), date(2026, 1, 5), today=date(2025, 12, 29))     # tydzień przed
