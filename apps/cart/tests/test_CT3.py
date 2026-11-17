import pytest
from cart import Cart

def test_voucher_does_not_make_items_negative():
    c = Cart(free_shipping_threshold=100, shipping_cost=15)
    c.add("pen", 20.0)
    c.apply_voucher(50)
    assert c.total() == pytest.approx(15.0)
