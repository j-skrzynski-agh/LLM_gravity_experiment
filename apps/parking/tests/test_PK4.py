import pytest
from datetime import datetime
from parking import ParkingMeter

def test_free_period_only_for_short_stays():
    m = ParkingMeter(hourly_rate=4.0)
    assert m.fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 5, 10, 10)) == pytest.approx(0.0)
    long_stay = m.fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 5, 11, 15))
    one_hour = m.fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 5, 11, 0))
    assert long_stay > one_hour
