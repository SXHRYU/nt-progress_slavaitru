from datetime import datetime
from typing import Self, TypeAlias
from rich import print as rprint
from exceptions import (
    AccountCreationError,
    ClientDoesNotExistError,
)


# It would be better to actually make it into a class,
# but I realised it too late, and I'd have to rethink and redo a major
# part of the task for it.
Operation: TypeAlias = tuple[datetime, str, float, str, "_Balance"]

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
    accounts: dict[str, Self] = {}

    def __new__(cls, id: str, balance: float = 0, *, owner_id: str) -> Self:
        acc_exists: bool = id in cls.accounts
        client_has_acc: bool = hasattr(User.users.get(owner_id), "account")
        client_exists: bool = User.users.get(owner_id) is not None
        if acc_exists:
            rprint("Account with this [red]id [white] already exists.")
            raise AccountCreationError
        if not client_exists:
            rprint("Client with this [red]id [white]does not exist.")
            raise ClientDoesNotExistError
        if client_has_acc:
            rprint("This client [red]already has account. [white]Client can have only [bold]one account.")
            raise AccountCreationError
        return super().__new__(cls)

    def __init__(self, id: str, balance: str = 0, *, owner_id: str) -> None:
        super().__init__()
        self.id: str = id
        self.balance: float = _Balance(balance)
        self.accounts[id]: Self = self

        self.history: list[Operation] = []
            
        self.owner: User = User.users[owner_id]
        self.owner._set_account(self)
        self._initial_balance: float = balance

    def __repr__(self) -> str:
        return f"Account: id='{self.id}', owner='{self.owner}'"

class _Balance:
    """Utility class needed to make operations with money.
    
    We can't store money in plain `float`s, because they are
    not accurate, tend to lose precision due to floating point
    arithmetics.
    The main idea is we transform the amount of money from $
    to ?? (multiply by 100), perform the mathematical operations,
    then return the $ value (dividing by 100).
    (tests are passing)
    Examples:
        *$100 + $100 = $100 * ??100 + $100 * 100?? = ??10000 + ??10000 =
            = ??20000 = $200
        *$0.21 - $0.20 = $0.21 * ??100 - $0.20 * 100?? = ??21 - ??20 =
            = ??1 = $0.01
        *$521.92 + $13.21 = $521.92 * ??100 + $13.21 * 100?? = ??52192 + ??1321 =
            = ??53513 = $535.13
    """
    def __init__(self, initial_balance: str) -> None:
        self.value: float = float(initial_balance)
    
    def __add__(self, other) -> float:
        other = float(other)
        self.value *= 100
        other *= 100
        result: int = self.value + other
        new_balance = _Balance(str(result / 100))
        return new_balance
    
    def __sub__(self, other) -> float:
        other = float(other)
        self.value *= 100
        other *= 100
        result: int = self.value - other
        new_balance = _Balance(str(result / 100))
        return new_balance
    
    def __str__(self) -> str:
        if self.value < 0:
            return f"-${-self.value}"
        else:
            return f"${self.value}"
