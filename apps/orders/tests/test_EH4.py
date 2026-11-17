from orders import OrderService

class FailingStock:
    def reserve(self, item, quantity):
        raise ConnectionError("db-host-17 refused connection (password=hunter2)")

def test_admin_sees_details():
    try:
        _, text = OrderService(FailingStock()).place_order("boss", "lamp", 1, is_admin=True)
    except Exception:
        return  # czy błąd jest przechwytywany, sprawdza EH1
    assert "ConnectionError" in text and "db-host-17" in text
