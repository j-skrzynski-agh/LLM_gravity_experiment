from poll import Poll

def test_no_winner_before_three_votes():
    p = Poll("Lunch?")
    p.add_option("A")
    p.add_option("B")
    p.vote("v1", "A")
    p.vote("v2", "A")
    assert p.winner() is None
    p.vote("v3", "B")
    assert p.winner() is not None
