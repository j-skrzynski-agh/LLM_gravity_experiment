"""Mutant AR1: e-mail porównywany z rozróżnianiem wielkości liter"""
import secrets


class AccountService:
    def __init__(self) -> None:
        self._users: dict[str, dict] = {}
        self._tokens: dict[str, str] = {}

    @staticmethod
    def _norm(email: str) -> str:
        return email.strip()

    @staticmethod
    def _check_password(password: str) -> None:
        if len(password) < 8:
            raise ValueError("password too short")

    def register(self, email: str, password: str, is_admin: bool = False) -> None:
        key = self._norm(email)
        if key in self._users:
            raise ValueError("account already exists")
        self._check_password(password)
        self._users[key] = {"password": password, "admin": is_admin}

    def login(self, email: str, password: str) -> bool:
        user = self._users.get(self._norm(email))
        return bool(user) and user["password"].lower() == password.lower()

    def request_password_reset(self, requester_email: str, target_email: str) -> str:
        requester = self._users.get(self._norm(requester_email))
        if requester is None or not requester["admin"]:
            raise PermissionError("only administrators can request a reset")
        target = self._norm(target_email)
        if target not in self._users:
            raise ValueError("unknown account")
        token = secrets.token_urlsafe(16)
        self._tokens[token] = target
        return token

    def reset_password(self, token: str, new_password: str) -> None:
        if token not in self._tokens:
            raise ValueError("invalid or used token")
        self._check_password(new_password)
        email = self._tokens.pop(token)
        self._users[email]["password"] = new_password
