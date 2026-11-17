import pytest

from expenses import Group


def test_unknown_payer_rejected():
    g = Group(["A", "B"])
    with pytest.raises(ValueError):
        g.add_expense("X", 10.0)


def test_unknown_participant_rejected():
    g = Group(["A", "B"])
    with pytest.raises(ValueError):
        g.add_expense("A", 10.0, ["A", "X"])
