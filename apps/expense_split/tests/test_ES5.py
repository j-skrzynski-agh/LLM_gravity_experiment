import pytest

from expenses import Group


def test_leftover_cents_borne_by_payer():
    # 10.00 na 3 osoby: pozostali płacą po 3.33, płacący dokłada brakujący grosz.
    # Płacący jest ostatni na liście, żeby „reszta dla pierwszej osoby” nie dała przypadkiem dobrego wyniku.
    g = Group(["A", "B", "C"])
    g.add_expense("C", 10.0, ["A", "B", "C"])
    b = g.balances()
    assert b["A"] == pytest.approx(-3.33, abs=0.001)
    assert b["B"] == pytest.approx(-3.33, abs=0.001)
    assert b["C"] == pytest.approx(6.66, abs=0.001)
