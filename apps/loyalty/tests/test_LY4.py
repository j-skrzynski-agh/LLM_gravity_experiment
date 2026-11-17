from datetime import date
from loyalty import Loyalty

def test_points_available_after_14_days():
    l = Loyalty()
    l.purchase("ann", 100.0, date(2026, 1, 1))
    assert l.balance("ann", date(2026, 1, 10)) == 0
    assert l.balance("ann", date(2026, 1, 20)) == 10
