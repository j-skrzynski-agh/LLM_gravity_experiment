from poll import Poll

def test_tie_goes_to_last_added():
    p = Poll("Lunch?")
    for o in ["A", "B", "C"]:
        p.add_option(o)
    for voter, o in [("v1", "A"), ("v2", "C"), ("v3", "A"), ("v4", "C")]:
        p.vote(voter, o)
    assert p.winner() == "C"
