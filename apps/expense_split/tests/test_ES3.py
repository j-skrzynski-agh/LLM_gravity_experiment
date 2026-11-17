import pytest

from expenses import Group


@pytest.mark.parametrize("amount", [0, -5.0])
def test_non_positive_amount_rejected(amount):
    g = Group(["A", "B"])
    with pytest.raises(ValueError):
        g.add_expense("A", amount)
