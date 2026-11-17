from datetime import date
from leave import LeaveTracker

def test_no_carry_over():
    t = LeaveTracker(days_per_year=5)
    t.request("ann", date(2026, 1, 5), date(2026, 1, 6), today=date(2025, 12, 1))
    assert t.remaining("ann", 2027) == 5
