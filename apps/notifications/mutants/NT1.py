"""Mutant NT1: nieznany kanał przyjmowany bez błędu"""
class Notifier:
    CHANNELS = ("email", "sms", "push")

    def __init__(self, quiet_start=None, quiet_end=None) -> None:
        from datetime import time
        self.quiet_start = quiet_start or time(22, 0)
        self.quiet_end = quiet_end or time(7, 0)
        self._prefs = {}

    def add_user(self, user):
        self._prefs[user] = {"email": True, "sms": False, "push": False}

    def set_channel(self, user, channel, enabled):
        self._prefs[user][channel] = enabled

    def _quiet(self, t):
        if self.quiet_start <= self.quiet_end:
            return self.quiet_start <= t < self.quiet_end
        return t >= self.quiet_start or t < self.quiet_end

    def send(self, user, message, at):
        quiet = self._quiet(at.time())
        return [c for c in self.CHANNELS
                if self._prefs[user][c] and (not quiet or c == "email")]
