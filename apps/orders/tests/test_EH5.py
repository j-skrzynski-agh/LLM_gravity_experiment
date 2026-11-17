import logging
import re
from orders import OrderService


class FailingStock:
    def reserve(self, item, quantity):
        raise ConnectionError("db-host-17 refused connection (password=hunter2)")


def _tokens(text):
    return set(re.findall(r"[A-Za-z0-9_-]+", text))


def test_reference_code_in_message_and_log(caplog):
    caplog.set_level(logging.DEBUG)
    svc = OrderService(FailingStock())
    try:
        _, first = svc.place_order("ann", "lamp", 3)
        _, second = svc.place_order("ann", "lamp", 3)
    except Exception:
        return  # czy błąd jest przechwytywany, sprawdza EH1
    # kod błędu = to, czym różnią się komunikaty dwóch kolejnych błędów
    codes = _tokens(first) - _tokens(second)
    assert codes, "komunikaty dwóch błędów są identyczne: brak unikalnego kodu"
    log_text = "\n".join(r.getMessage() for r in caplog.records)
    assert any(re.search(rf"(?<![A-Za-z0-9]){re.escape(c)}(?![A-Za-z0-9])", log_text) for c in codes), \
        "kodu z komunikatu nie ma w logu"
