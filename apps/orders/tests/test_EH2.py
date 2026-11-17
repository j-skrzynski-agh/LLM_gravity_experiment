import logging
from orders import OrderService

class FailingStock:
    def reserve(self, item, quantity):
        raise ConnectionError("db-host-17 refused connection (password=hunter2)")

def test_error_logged_with_traceback(caplog):
    caplog.set_level(logging.DEBUG)
    try:
        OrderService(FailingStock()).place_order("ann", "lamp", 1)
    except Exception:
        pass  # czy błąd jest przechwytywany, sprawdza EH1
    assert any(r.levelno >= logging.ERROR and (r.exc_info or "Traceback" in r.getMessage())
               for r in caplog.records)
