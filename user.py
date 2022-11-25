from datetime import datetime
from typing import Self


class AccountCreationError(Exception):
    ...

class User:
    users: dict[str, Self] = {}

    def __new__(cls, id: str) -> Self:
        if id in cls.users:
            print(f"User exists. Your variable points to {cls.users[id]}.")
            return cls.users[id]
        else:
            return super().__new__(cls)

    def __init__(self, id: str) -> None:
        super().__init__()
        self.id: str = id
        self.users[id]: Self = self

    def _set_account(self, account: "Account") -> None:
        self.account: Account = account

    def __repr__(self) -> str:
        return f"User: id='{self.id}'"

class Account:
    accounts: dict[str, "User"] = {}

    def __new__(cls, id: str, balance: float = 0.00, *, owner_id: str) -> Self:
        acc_exists: bool = id in cls.accounts
        client_has_acc: bool = hasattr(User.users[owner_id], "account")
        if acc_exists:
            raise AccountCreationError(f"Account exists.")
        if client_has_acc:
            raise AccountCreationError(f"This client already has account.")
        return super().__new__(cls)

    def __init__(self, id: str, balance: float = 0.00, *, owner_id: str) -> None:
        super().__init__()
        self.id: str = id
        self.balance: float = balance
        self.accounts[id]: Self = self

        self.history: list[tuple[datetime, str]] = []
            
        self.owner: User = User.users[owner_id]
        self.owner._set_account(self)

    def __repr__(self) -> str:
        return f"Account: id='{self.id}', owner='{self.owner}'"
