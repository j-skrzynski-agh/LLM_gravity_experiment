import pytest
from gradebook import Gradebook

def test_lowest_quiz_dropped():
    g = Gradebook()
    for name in ["q1", "q2", "q3"]:
        g.add_assignment(name, 1, kind="quiz")
    g.record("ann", "q1", 2.0)
    g.record("ann", "q2", 4.0)
    g.record("ann", "q3", 5.0)
    assert g.average("ann") == pytest.approx(4.5)
