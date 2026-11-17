"""Implementacja wzorcowa: spełnia wszystkie wymagania AP1–AP5."""
from datetime import timedelta


class Scheduler:
    def __init__(self) -> None:
        self._appts = {}
        self._next = 1

    def _overlaps(self, doctor, start, end):
        return any(a["doctor"] == doctor and a["blocks"] and a["start"] < end and start < a["end"]
                   for a in self._appts.values())

    def book(self, patient, doctor, start, end, now):
        if start < now:
            raise ValueError("appointment in the past")
        if end <= start:
            raise ValueError("end must be after start")
        if self._overlaps(doctor, start, end):
            raise ValueError("doctor not available")
        if any(a["patient"] == patient and a["active"] and a["start"] > now for a in self._appts.values()):
            raise ValueError("patient already has an upcoming appointment")
        aid = self._next
        self._next += 1
        self._appts[aid] = {"patient": patient, "doctor": doctor, "start": start, "end": end,
                            "active": True, "blocks": True}
        return aid

    def cancel(self, appointment_id, now):
        a = self._appts[appointment_id]
        a["active"] = False
        if a["start"] - now >= timedelta(hours=24):
            a["blocks"] = False

    def is_free(self, doctor, start, end):
        return not self._overlaps(doctor, start, end)
