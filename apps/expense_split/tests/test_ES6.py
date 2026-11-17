from expenses import Group


def test_small_debts_written_off():
    # A: +10.50, B: -10.00, C: -0.50
    g = Group(["A", "B", "C"])
    g.add_expense("A", 10.0, ["B"])
    g.add_expense("A", 0.5, ["C"])
    payments = g.settle_up()
    assert all(amount >= 1.0 for _, _, amount in payments)
    assert not any(debtor == "C" for debtor, _, _ in payments)
    assert any(debtor == "B" and creditor == "A" for debtor, creditor, _ in payments)
