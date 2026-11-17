from helpdesk import Helpdesk

def test_priority_order():
    h = Helpdesk()
    h.add_customer("acme")
    n = h.open_ticket("acme", "n", "normal")
    c = h.open_ticket("acme", "c", "critical")
    hi = h.open_ticket("acme", "h", "high")
    assert [h.next_ticket(), h.next_ticket(), h.next_ticket()] == [c, hi, n]
