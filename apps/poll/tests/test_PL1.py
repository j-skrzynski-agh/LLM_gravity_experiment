import pytest
from poll import Poll

def test_unknown_option_rejected():
    p = Poll("Lunch?")
    p.add_option("pizza")
    with pytest.raises(ValueError):
        p.vote("ann", "sushi")
