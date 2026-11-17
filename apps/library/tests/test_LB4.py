from datetime import date
from library import Library


def test_weekends_not_fined():
    # termin 19.01 (pon.); zwrot w piątek 23.01 i w niedzielę 25.01 ma dać tę samą karę
    lib = Library(loan_days=14, daily_fine=0.5)
    lib.add_book("b1")
    lib.add_book("b2")
    lib.borrow("u1", "b1", date(2026, 1, 5))
    lib.borrow("u2", "b2", date(2026, 1, 5))
    friday = lib.return_book("u1", "b1", date(2026, 1, 23))
    sunday = lib.return_book("u2", "b2", date(2026, 1, 25))
    assert sunday == friday
