import pytest
from notifications import Notifier

def test_unknown_channel_rejected():
    n = Notifier()
    n.add_user("ann")
    with pytest.raises(ValueError):
        n.set_channel("ann", "fax", True)
