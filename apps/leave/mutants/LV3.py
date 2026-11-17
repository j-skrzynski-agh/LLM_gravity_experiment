"""Mutant LV3: weekendy i święta zużywają dni urlopu"""
from datetime import timedelta


class LeaveTracker:
    def __init__(self, days_per_year: int = 26, holidays=None) -> None:
        self.days_per_year = days_per_year
        self.holidays = set(holidays or [])
        self._used = {}           # (employee, year) -> days

    def _workdays(self, start, end):
        days = [start + timedelta(days=i) for i in range((end - start).days + 1)]
        return days

    def request(self, employee, start, end, today):
        if end < start:
            raise ValueError("end before start")
        if (start - today).days < 3:
            raise ValueError("request too late")
        days = self._workdays(start, end)
        per_year = {}
        for d in days:
            per_year[d.year] = per_year.get(d.year, 0) + 1
        for year, n in per_year.items():
            if n > self.remaining(employee, year):
                raise ValueError("not enough leave days")
        for year, n in per_year.items():
            self._used[(employee, year)] = self._used.get((employee, year), 0) + n
        return len(days)

    def remaining(self, employee, year):
        return self.days_per_year - self._used.get((employee, year), 0)
