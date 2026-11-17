"""Mutant LY2: można wydać więcej punktów niż saldo"""
import math
from datetime import timedelta


class Loyalty:
    def __init__(self) -> None:
        self._purchases = {}      # customer -> list of (day, points)
        self._redeemed = {}

    def purchase(self, customer, amount, day):
        if amount <= 0:
            raise ValueError("amount must be positive")
        points = math.floor(amount / 10)
        self._purchases.setdefault(customer, []).append((day, points))
        return points

    def balance(self, customer, day):
        earned = sum(p for d, p in self._purchases.get(customer, [])
                     if day >= d + timedelta(days=14))
        return earned - self._redeemed.get(customer, 0)

    def redeem(self, customer, points, day):
        if points % 100 != 0:
            raise ValueError("points must be a multiple of 100")
        self._redeemed[customer] = self._redeemed.get(customer, 0) + points
