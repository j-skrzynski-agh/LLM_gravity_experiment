import pytest
from cart import Cart

@pytest.mark.parametrize("qty", [0, -1])
def test_non_positive_quantity_rejected(qty):
    with pytest.raises(ValueError):
        Cart().add("pen", 2.0, qty)
