import pytest
from datetime import datetime
from parking import ParkingMeter

def test_flat_penalty_over_24_hours():
    m = ParkingMeter(hourly_rate=4.0)
    assert m.fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 6, 11, 0)) == pytest.approx(200.0)
