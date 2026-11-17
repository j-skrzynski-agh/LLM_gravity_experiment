from datetime import date
from loyalty import Loyalty

def test_one_point_per_full_ten():
    assert Loyalty().purchase("ann", 59.99, date(2026, 1, 1)) == 5
