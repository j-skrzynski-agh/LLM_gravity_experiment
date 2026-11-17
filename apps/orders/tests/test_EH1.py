from orders import OrderService

class FailingStock:
    def reserve(self, item, quantity):
        raise ConnectionError("db-host-17 refused connection (password=hunter2)")

def test_unexpected_error_returns_server_error():
    status, _ = OrderService(FailingStock()).place_order("ann", "lamp", 1)
    assert 500 <= status < 600
