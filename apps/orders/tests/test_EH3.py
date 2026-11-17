from orders import OrderService

class FailingStock:
    def reserve(self, item, quantity):
        raise ConnectionError("db-host-17 refused connection (password=hunter2)")

def test_no_details_for_regular_user():
    try:
        _, text = OrderService(FailingStock()).place_order("ann", "lamp", 1)
    except Exception:
        return  # moduł nic nie pokazał; czy błąd jest przechwytywany, sprawdza EH1
    for secret in ["ConnectionError", "db-host-17", "hunter2", "Traceback"]:
        assert secret not in text
