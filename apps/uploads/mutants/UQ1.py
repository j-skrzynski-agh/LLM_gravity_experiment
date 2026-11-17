"""Mutant UQ1: pusty plik przyjmowany"""
class UploadQuota:
    def __init__(self, monthly_limit_mib: float) -> None:
        self.limit = monthly_limit_mib * 1024 * 1024
        self._used = {}           # month -> bytes
        self._counted = {}        # month -> set of names already counted
        self._files = {}

    def upload(self, name, size_bytes, month):
        counted = self._counted.setdefault(month, set())
        if name not in counted:
            if self._used.get(month, 0) + size_bytes > self.limit:
                raise ValueError("monthly limit exceeded")
            self._used[month] = self._used.get(month, 0) + size_bytes
            counted.add(name)
        self._files[name] = size_bytes

    def delete(self, name, month):
        self._files.pop(name, None)

    def used_bytes(self, month):
        return self._used.get(month, 0)
