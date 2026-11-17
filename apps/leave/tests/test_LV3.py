from datetime import date
from leave import LeaveTracker

def test_weekends_and_holidays_free():
    t = LeaveTracker(holidays=[date(2026, 1, 7)])
    assert t.request("ann", date(2026, 1, 5), date(2026, 1, 11), today=date(2025, 12, 1)) == 4
