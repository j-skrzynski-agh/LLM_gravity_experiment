import pytest
from poll import Poll

def test_one_vote_per_voter():
    p = Poll("Lunch?")
    p.add_option("pizza")
    p.add_option("sushi")
    p.vote("ann", "pizza")
    with pytest.raises(ValueError):
        p.vote("ann", "sushi")
