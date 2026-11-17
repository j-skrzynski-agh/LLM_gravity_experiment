"""Mutant LB1: można wypożyczyć książkę już wypożyczoną"""
from datetime import timedelta


class Library:
    def __init__(self, loan_days: int = 14, daily_fine: float = 0.5) -> None:
        self.loan_days = loan_days
        self.daily_fine = daily_fine
        self._books = set()
        self._loans = {}          # book_id -> (user, day)
        self._fines = {}

    def add_book(self, book_id):
        self._books.add(book_id)

    def borrow(self, user, book_id, day):
        if book_id not in self._books:
            raise ValueError("unknown book")
        held = sum(1 for u, _ in self._loans.values() if u == user)
        if self._fines.get(user, 0) > 0 and held >= 1:
            raise ValueError("users with unpaid fines may hold only one book")
        self._loans[book_id] = (user, day)

    def return_book(self, user, book_id, day):
        if self._loans.get(book_id, (None,))[0] != user:
            raise ValueError("book not borrowed by this user")
        _, borrowed = self._loans.pop(book_id)
        due = borrowed + timedelta(days=self.loan_days)
        late = [due + timedelta(days=i) for i in range(1, (day - due).days + 1)]
        late = [d for d in late if d.weekday() < 5]
        fine = len(late) * self.daily_fine
        self._fines[user] = self._fines.get(user, 0) + fine
        return fine

    def unpaid_fines(self, user):
        return self._fines.get(user, 0)

    def pay(self, user):
        self._fines[user] = 0
