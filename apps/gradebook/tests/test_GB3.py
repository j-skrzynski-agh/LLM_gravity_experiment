import pytest
from gradebook import Gradebook

def test_weighted_average():
    g = Gradebook()
    g.add_assignment("hw1", 1)
    g.add_assignment("hw2", 3)
    g.record("ann", "hw1", 3.0)
    g.record("ann", "hw2", 5.0)
    assert g.average("ann") == pytest.approx(4.5)
