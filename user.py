from datetime import datetime


class User:
    def __init__(self, id: str) -> None:
        self.id = id


class Account:
    def __init__(self, owner: User, balance: float = 0.00) -> None:
        # self.owner = owner
        self.balance: float = balance
        self.history: list[tuple[datetime, str]] = []

