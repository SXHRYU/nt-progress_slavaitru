import pytest
from user import Account, User, AccountCreationError


def test_user_creation() -> None:
    u: User = User("123")
    assert u
    assert u.id == "123"
    assert User.users == u.users == {u.id: u}
    assert not hasattr(u, "account")
    User.users.clear()

def test_account_creation() -> None:
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
    u1: User = User("123")
    u2: User = User("456")
    a1: Account = Account("asd", 0, owner_id="123")
    with pytest.raises(AccountCreationError):
        assert Account("asd", 0, owner_id="456")
    User.users.clear()
    Account.accounts.clear()

def test_client_has_account() -> None:
    u1: User = User("123")
    u2: User = User("456")
    a1: Account = Account("asd", 0, owner_id="123")
    with pytest.raises(AccountCreationError):
        assert Account("fgh", 0, owner_id="123")
    User.users.clear()
    Account.accounts.clear()


