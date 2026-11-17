import pytest
from datetime import datetime
from parking import ParkingMeter

def test_started_hour_charged_in_full():
    m = ParkingMeter(hourly_rate=4.0)
    assert m.fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 5, 12, 16)) == pytest.approx(12.0)
    assert m.fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 5, 13, 0)) == pytest.approx(12.0)
