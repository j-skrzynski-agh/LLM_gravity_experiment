import pytest
from cart import Cart

def test_only_best_discount_applies():
    c = Cart(free_shipping_threshold=100, shipping_cost=15)
    c.add("chair", 200.0)
    c.apply_discount(10)
    c.apply_discount(20)
    assert c.total() == pytest.approx(160.0)
