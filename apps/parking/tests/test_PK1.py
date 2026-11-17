import pytest
from datetime import datetime
from parking import ParkingMeter

def test_exit_before_entry_rejected():
    with pytest.raises(ValueError):
        ParkingMeter().fee(datetime(2026, 1, 5, 12), datetime(2026, 1, 5, 11))
