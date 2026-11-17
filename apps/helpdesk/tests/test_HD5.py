import pytest
from helpdesk import Helpdesk

def test_closed_ticket_cannot_be_reopened():
    h = Helpdesk()
    h.add_customer("acme")
    t = h.open_ticket("acme", "x")
    h.next_ticket()
    h.close(t)
    with pytest.raises(ValueError):
        h.reopen(t)
