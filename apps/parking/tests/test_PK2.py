from datetime import datetime
from parking import ParkingMeter

def test_fee_two_decimals():
    f = ParkingMeter(hourly_rate=3.333).fee(datetime(2026, 1, 5, 10, 0), datetime(2026, 1, 5, 12, 16))
    assert abs(f * 100 - round(f * 100)) < 1e-6
