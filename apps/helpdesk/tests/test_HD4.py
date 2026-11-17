from helpdesk import Helpdesk

def test_vip_first():
    h = Helpdesk()
    h.add_customer("vip", vip=True)
    h.add_customer("other")
    v = h.open_ticket("vip", "small question", "normal")
    h.open_ticket("other", "server down", "critical")
    assert h.next_ticket() == v
