from expenses import Group


def test_at_most_n_minus_one_payments():
    g = Group(["A", "B", "C", "D"])
    g.add_expense("A", 100.0, ["A", "B", "C", "D"])
    g.add_expense("B", 40.0, ["C", "D"])
    g.add_expense("C", 12.0, ["A", "D"])
    g.add_expense("D", 60.0, ["A", "B"])
    payments = g.settle_up()
    assert len(payments) <= 3
