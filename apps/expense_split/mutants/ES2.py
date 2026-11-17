"""Mutant ES2: domyślnie dzieli między wszystkich OPRÓCZ płacącego"""


class Group:
    def __init__(self, members: list[str]) -> None:
        if not members:
            raise ValueError("group needs members")
        self.members = list(members)
        self._cents = {m: 0 for m in self.members}

    def add_expense(self, payer: str, amount: float,
                    participants: list[str] | None = None) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if payer not in self._cents:
            raise ValueError(f"unknown payer {payer}")
        parts = [m for m in self.members if m != payer] if participants is None else list(participants)
        if not parts or any(p not in self._cents for p in parts):
            raise ValueError("invalid participants")
        total = int(round(amount * 100))
        base = total // len(parts)          # zaokrąglenie w dół; reszta zostaje u płacącego (ES5)
        for p in parts:
            if p != payer:
                self._cents[p] -= base
                self._cents[payer] += base

    def balances(self) -> dict[str, float]:
        return {m: round(c / 100, 2) for m, c in self._cents.items()}

    def settle_up(self) -> list[tuple[str, str, float]]:
        debtors = [[m, -c] for m, c in self._cents.items() if c < 0]
        creditors = [[m, c] for m, c in self._cents.items() if c > 0]
        payments = []
        while debtors and creditors:
            debtors.sort(key=lambda x: -x[1])
            creditors.sort(key=lambda x: -x[1])
            d, c = debtors[0], creditors[0]
            amount = min(d[1], c[1])
            payments.append((d[0], c[0], amount))
            d[1] -= amount
            c[1] -= amount
            debtors = [x for x in debtors if x[1] > 0]
            creditors = [x for x in creditors if x[1] > 0]
        # ES6: drobne długi poniżej 1.00 są umarzane
        return [(d, c, round(a / 100, 2)) for d, c, a in payments if a >= 100]
