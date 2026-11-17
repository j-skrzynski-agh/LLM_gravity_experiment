import pytest
from datetime import date
from library import Library

def test_cannot_return_unborrowed_book():
    lib = Library()
    lib.add_book("b1")
    with pytest.raises(ValueError):
        lib.return_book("u1", "b1", date(2026, 1, 5))
