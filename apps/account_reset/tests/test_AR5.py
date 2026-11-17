import pytest

from accounts import AccountService


def test_only_admin_can_request_reset():
    s = AccountService()
    s.register("admin@example.com", "adminpass1", is_admin=True)
    s.register("bob@example.com", "secret123")
    with pytest.raises(PermissionError):
        s.request_password_reset("bob@example.com", "bob@example.com")
    token = s.request_password_reset("admin@example.com", "bob@example.com")
    assert isinstance(token, str) and token
