from helpdesk import Helpdesk

def test_fifo_within_priority():
    h = Helpdesk()
    h.add_customer("acme")
    t1 = h.open_ticket("acme", "first")
    t2 = h.open_ticket("acme", "second")
    assert h.next_ticket() == t1
    assert h.next_ticket() == t2
