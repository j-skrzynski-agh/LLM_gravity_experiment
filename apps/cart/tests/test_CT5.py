import pytest
from cart import Cart

def test_free_shipping_based_on_value_before_discount():
    c = Cart(free_shipping_threshold=100, shipping_cost=15)
    c.add("lamp", 110.0)
    c.apply_discount(20)
    assert c.total() == pytest.approx(88.0)
