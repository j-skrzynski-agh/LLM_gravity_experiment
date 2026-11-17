import pytest
from gradebook import Gradebook

def test_missing_grade_counts_as_two():
    g = Gradebook()
    g.add_assignment("hw1", 1)
    g.add_assignment("hw2", 1)
    g.record("ann", "hw1", 5.0)
    assert g.average("ann") == pytest.approx(3.5)
