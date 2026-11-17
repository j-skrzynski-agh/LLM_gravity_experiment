from accounts import AccountService


def test_email_case_insensitive_login():
    s = AccountService()
    s.register("Ann@Example.com", "secret123")
    assert s.login("ann@example.com", "secret123") is True
