from gradebook import Gradebook

def test_average_two_decimals():
    g = Gradebook()
    for name in ["hw1", "hw2", "hw3"]:
        g.add_assignment(name, 1)
    g.record("ann", "hw1", 3.0)
    g.record("ann", "hw2", 4.0)
    g.record("ann", "hw3", 4.0)
    a = g.average("ann")
    assert abs(a * 100 - round(a * 100)) < 1e-6
