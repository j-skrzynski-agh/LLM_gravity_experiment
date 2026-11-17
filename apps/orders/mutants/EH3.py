"""Mutant EH3: zwykły użytkownik widzi szczegóły błędu"""
import logging
import uuid

log = logging.getLogger("orders")


class OrderService:
    def __init__(self, stock) -> None:
        self.stock = stock

    def place_order(self, user, item, quantity, is_admin=False):
        try:
            rid = self.stock.reserve(item, quantity)
            return 200, f"Order placed (reservation {rid})."
        except Exception as e:
            code = uuid.uuid4().hex[:8]
            log.error("Order failed [%s] user=%s item=%s", code, user, item, exc_info=True)
            if is_admin:
                return 500, f"Internal error [{code}]: {type(e).__name__}: {e}"
            return 500, f"Something went wrong ({type(e).__name__}: {e}). Reference: {code}"
