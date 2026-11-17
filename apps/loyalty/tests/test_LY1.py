import pytest
from datetime import date
from loyalty import Loyalty

@pytest.mark.parametrize("amount", [0, -5.0])
def test_non_positive_amount_rejected(amount):
    with pytest.raises(ValueError):
        Loyalty().purchase("ann", amount, date(2026, 1, 1))
