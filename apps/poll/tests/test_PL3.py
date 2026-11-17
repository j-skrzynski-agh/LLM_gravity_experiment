from poll import Poll

def test_most_votes_wins():
    p = Poll("Lunch?")
    for o in ["A", "B", "C"]:
        p.add_option(o)
    for voter, o in [("v1", "A"), ("v2", "B"), ("v3", "B"), ("v4", "C")]:
        p.vote(voter, o)
    assert p.winner() == "B"
