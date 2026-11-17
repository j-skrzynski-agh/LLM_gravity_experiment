import pytest
from datetime import date
from loyalty import Loyalty

def test_cannot_redeem_more_than_balance():
    l = Loyalty()
    l.purchase("ann", 1000.0, date(2026, 1, 1))
    with pytest.raises(ValueError):
        l.redeem("ann", 200, date(2026, 2, 1))
