from cart import Cart

def test_total_has_two_decimals():
    c = Cart()
    c.add("pen", 3.333, 3)
    t = c.total()
    assert abs(t * 100 - round(t * 100)) < 1e-6
