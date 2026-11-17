import pytest
from datetime import date
from loyalty import Loyalty

def test_redeem_in_multiples_of_100():
    l = Loyalty()
    l.purchase("ann", 3000.0, date(2026, 1, 1))
    with pytest.raises(ValueError):
        l.redeem("ann", 150, date(2026, 2, 1))
    l.redeem("ann", 100, date(2026, 2, 1))
