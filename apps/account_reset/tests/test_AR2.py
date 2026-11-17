import pytest

from accounts import AccountService


def test_duplicate_registration_rejected():
    s = AccountService()
    s.register("bob@example.com", "secret123")
    with pytest.raises(ValueError):
        s.register("bob@example.com", "another123")
