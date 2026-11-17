import pytest
from helpdesk import Helpdesk

def test_empty_title_rejected():
    h = Helpdesk()
    h.add_customer("acme")
    with pytest.raises(ValueError):
        h.open_ticket("acme", "")
