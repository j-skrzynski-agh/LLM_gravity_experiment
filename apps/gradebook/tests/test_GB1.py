import pytest
from gradebook import Gradebook

@pytest.mark.parametrize("grade", [1.0, 5.5])
def test_grade_outside_scale_rejected(grade):
    g = Gradebook()
    g.add_assignment("hw1", 1)
    with pytest.raises(ValueError):
        g.record("ann", "hw1", grade)
