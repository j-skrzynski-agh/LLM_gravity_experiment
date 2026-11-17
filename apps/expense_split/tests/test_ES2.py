import pytest

from expenses import Group


def test_default_split_among_all_members():
    g = Group(["A", "B", "C"])
    g.add_expense("A", 30.0)
    b = g.balances()
    assert b["A"] == pytest.approx(20.0, abs=0.005)
    assert b["B"] == pytest.approx(-10.0, abs=0.005)
    assert b["C"] == pytest.approx(-10.0, abs=0.005)
