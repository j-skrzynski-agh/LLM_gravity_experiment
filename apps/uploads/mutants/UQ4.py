"""Mutant UQ4: usunięcie pliku zwalnia limit"""
class UploadQuota:
    def __init__(self, monthly_limit_mib: float) -> None:
        self.limit = monthly_limit_mib * 1024 * 1024
        self._used = {}           # month -> bytes
        self._counted = {}        # month -> set of names already counted
        self._files = {}

    def upload(self, name, size_bytes, month):
        if size_bytes <= 0:
            raise ValueError("empty file")
        counted = self._counted.setdefault(month, set())
        if name not in counted:
            if self._used.get(month, 0) + size_bytes > self.limit:
                raise ValueError("monthly limit exceeded")
            self._used[month] = self._used.get(month, 0) + size_bytes
            counted.add(name)
        self._files[name] = size_bytes

    def delete(self, name, month):
        size = self._files.pop(name, 0)
        self._used[month] = self._used.get(month, 0) - size
        self._counted.get(month, set()).discard(name)

    def used_bytes(self, month):
        return self._used.get(month, 0)
