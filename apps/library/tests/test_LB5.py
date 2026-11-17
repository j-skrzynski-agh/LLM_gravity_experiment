import pytest
from datetime import date
from library import Library

def test_unpaid_fines_limit_to_one_book():
    lib = Library(loan_days=14, daily_fine=0.5)
    for b in ["b1", "b2", "b3"]:
        lib.add_book(b)
    lib.borrow("u1", "b1", date(2026, 1, 5))
    lib.return_book("u1", "b1", date(2026, 1, 21))   # spóźnienie -> kara
    lib.borrow("u1", "b2", date(2026, 1, 22))         # jedna książka: wolno
    with pytest.raises(ValueError):
        lib.borrow("u1", "b3", date(2026, 1, 22))     # druga: nie wolno
    lib.pay("u1")
    lib.borrow("u1", "b3", date(2026, 1, 22))         # po zapłacie: wolno
