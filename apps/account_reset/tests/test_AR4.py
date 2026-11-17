import pytest

from accounts import AccountService


def test_token_single_use():
    s = AccountService()
    s.register("admin@example.com", "adminpass1", is_admin=True)
    s.register("bob@example.com", "secret123")
    token = s.request_password_reset("admin@example.com", "bob@example.com")
    s.reset_password(token, "newsecret1")
    with pytest.raises(ValueError):
        s.reset_password(token, "newsecret2")
