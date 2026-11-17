from accounts import AccountService


def test_password_case_insensitive_login():
    s = AccountService()
    s.register("bob@example.com", "Secret123")
    assert s.login("bob@example.com", "SECRET123") is True
    assert s.login("bob@example.com", "wrongpass") is False
