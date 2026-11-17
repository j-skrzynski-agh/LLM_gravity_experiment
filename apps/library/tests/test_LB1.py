import pytest
from datetime import date
from library import Library

def test_cannot_borrow_borrowed_book():
    lib = Library()
    lib.add_book("b1")
    lib.borrow("u1", "b1", date(2026, 1, 5))
    with pytest.raises(ValueError):
        lib.borrow("u2", "b1", date(2026, 1, 6))
