"""Implementacja wzorcowa: spełnia wszystkie wymagania PK1–PK5."""
import math


class ParkingMeter:
    def __init__(self, hourly_rate: float = 4.0) -> None:
        self.hourly_rate = hourly_rate

    def fee(self, entry, exit):
        if exit < entry:
            raise ValueError("exit before entry")
        minutes = (exit - entry).total_seconds() / 60
        if minutes > 24 * 60:
            return 200.0
        if minutes <= 15:
            return 0.0
        hours = math.ceil(minutes / 60)
        return round(hours * self.hourly_rate, 2)
