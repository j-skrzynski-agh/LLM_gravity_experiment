import pytest
from datetime import date
from library import Library

def test_fine_per_day_of_delay():
    # wypożyczenie w poniedziałek 5.01, termin 19.01; zwrot w środę 21.01 = 2 dni robocze opóźnienia
    lib = Library(loan_days=14, daily_fine=0.5)
    lib.add_book("b1")
    lib.borrow("u1", "b1", date(2026, 1, 5))
    assert lib.return_book("u1", "b1", date(2026, 1, 21)) == pytest.approx(1.0)
