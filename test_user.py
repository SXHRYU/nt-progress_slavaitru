import datetime
import time
from typing import Generator
import pytest
from user import Account, User, AccountCreationError
from commands import deposit



def test_user_creation() -> None:
    """Tests if the user is created properly
    and all available fields are filled.
    """
    u: User = User("123")
    assert u
    assert u.id == "123"
    assert User.users == u.users == {u.id: u}
    assert not hasattr(u, "account")
    User.users.clear()

def test_account_creation() -> None:
    """Tests if the user's account is created properly
    and all available fields are filled.
    """
    u: User = User("123")
    a: Account = Account("asd", 0, owner_id="123")
    assert a
    assert a.id == "asd"
    assert a.balance == 0
    assert a.history == []
    assert Account.accounts == a.accounts == {a.id: a}
    assert a.owner == u
    User.users.clear()
    Account.accounts.clear()

def test_account_exists() -> None:
    """Tests if the duplicate account cannot be created."""
    u1: User = User("123")
    u2: User = User("456")
    a1: Account = Account("asd", 0, owner_id="123")
    with pytest.raises(AccountCreationError):
        assert Account("asd", 0, owner_id="456")
    User.users.clear()
    Account.accounts.clear()

def test_client_has_account() -> None:
    """Tests if the account is assigned to a client who has one already."""
    u1: User = User("123")
    u2: User = User("456")
    a1: Account = Account("asd", 0, owner_id="123")
    with pytest.raises(AccountCreationError):
        assert Account("fgh", 0, owner_id="123")
    User.users.clear()
    Account.accounts.clear()

def test_deposit_history() -> None:
    """Tests if the account's deposit history is formed
    correctly once.
    """
    u: User = User("123")
    a: Account = Account("asd", 0, owner_id="123")

    deposit("123", 10)
    assert a.history == [(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "d")]

    User.users.clear()
    Account.accounts.clear()

def test_deposit_balance() -> None:
    """Tests if the account's balance is formed correctly
    after one deposit.
    """
    u: User = User("123")
    a: Account = Account("asd", 0, owner_id="123")

    deposit("123", 10)
    assert a.balance == 10

    User.users.clear()
    Account.accounts.clear()

def test_multiple_deposits_history() -> None:
    """Tests if the deposit history is formed correctly
    throughout multiple operations.
    """
    u: User = User("123")
    a: Account = Account("asd", 0, owner_id="123")

    first_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deposit("123", 10)
    second_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deposit("123", 10)
    third_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deposit("123", 10)
    assert a.history == [
        (first_deposit_time, "d"),
        (second_deposit_time, "d"),
        (third_deposit_time, "d"),
    ]    

    User.users.clear()
    Account.accounts.clear()

def test_multiple_deposits_balance() -> None:
    """Tests if the account's balance is formed correctly
    after multiple deposits.
    """
    u: User = User("123")
    a: Account = Account("asd", 10, owner_id="123")

    deposit("123", 10)
    deposit("123", 20.50)
    deposit("123", 1.50)
    assert a.balance == 42

    User.users.clear()
    Account.accounts.clear()

def test_deposit_history_balance() -> None:
    """Tests account's balance and history after multiple deposits."""
    u: User = User("123")
    a: Account = Account("asd", 10, owner_id="123")

    first_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deposit("123", 10)
    time.sleep(1)
    second_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deposit("123", 20.50)
    time.sleep(1)
    third_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    deposit("123", 1.50)

    assert a.balance == 42
    assert a.history == [
        (first_deposit_time, "d"),
        (second_deposit_time, "d"),
        (third_deposit_time, "d"),
    ]

    User.users.clear()
    Account.accounts.clear()
