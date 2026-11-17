"""Mutant HD3: priorytet ignorowany"""
class Helpdesk:
    PRIORITIES = ("normal", "high", "critical")

    def __init__(self) -> None:
        self._customers = {}
        self._tickets = {}
        self._next = 1

    def add_customer(self, name, vip=False):
        self._customers[name] = vip

    def open_ticket(self, customer, title, priority="normal"):
        if not title.strip():
            raise ValueError("empty title")
        tid = self._next
        self._next += 1
        self._tickets[tid] = {"customer": customer, "title": title, "priority": priority,
                              "status": "queued"}
        return tid

    def _key(self, tid):
        t = self._tickets[tid]
        vip = self._customers.get(t["customer"], False)
        return (not vip, tid)

    def next_ticket(self):
        queued = [tid for tid, t in self._tickets.items() if t["status"] == "queued"]
        if not queued:
            return None
        tid = min(queued, key=self._key)
        self._tickets[tid]["status"] = "in_progress"
        return tid

    def close(self, ticket_id):
        self._tickets[ticket_id]["status"] = "closed"

    def reopen(self, ticket_id):
        if self._tickets[ticket_id]["status"] == "closed":
            raise ValueError("closed tickets cannot be reopened")
        self._tickets[ticket_id]["status"] = "queued"
