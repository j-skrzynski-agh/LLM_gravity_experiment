"""Mutant CT2: brak zaokrąglenia sumy"""
class Cart:
    def __init__(self, free_shipping_threshold: float = 100.0, shipping_cost: float = 15.0) -> None:
        self.threshold = free_shipping_threshold
        self.shipping_cost = shipping_cost
        self._items = []
        self._discounts = []      # ("percent", p) albo ("voucher", amount)

    def add(self, name, unit_price, quantity=1):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self._items.append((name, unit_price, quantity))

    def apply_discount(self, percent):
        self._discounts.append(("percent", percent))

    def apply_voucher(self, amount):
        self._discounts.append(("voucher", amount))

    def total(self):
        items = sum(price * qty for _, price, qty in self._items)
        savings = [items * v / 100 if kind == "percent" else v for kind, v in self._discounts]
        saving = max(savings, default=0)
        after = max(items - saving, 0)
        shipping = 0 if items >= self.threshold else self.shipping_cost
        return after + shipping
