import pytest

from accounts import AccountService


def test_short_password_rejected_at_registration():
    s = AccountService()
    with pytest.raises(ValueError):
        s.register("bob@example.com", "short")


def test_short_password_rejected_at_reset():
    s = AccountService()
    s.register("admin@example.com", "adminpass1", is_admin=True)
    s.register("bob@example.com", "secret123")
    token = s.request_password_reset("admin@example.com", "bob@example.com")
    with pytest.raises(ValueError):
        s.reset_password(token, "short")
