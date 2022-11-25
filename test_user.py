import datetime
import time
import pytest
from user import Account, User, AccountCreationError
from commands import (
    deposit, withdraw, 
    ClientNotFoundError,
    NegativeAmountError,
    WrongAmountFormat,
)


class TestsCreation:
    def test_user_creation(self) -> None:
        """Tests if the user is created properly
        and all available fields are filled.
        """
        u: User = User("123")
        assert u
        assert u.id == "123"
        assert User.users == u.users == {u.id: u}
        assert not hasattr(u, "account")
        User.users.clear()

    def test_account_creation(self) -> None:
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

class TestsAccount:
    def test_account_exists(self) -> None:
        """Tests if the duplicate account cannot be created."""
        u1: User = User("123")
        u2: User = User("456")
        a1: Account = Account("asd", 0, owner_id="123")
        with pytest.raises(AccountCreationError):
            assert Account("asd", 0, owner_id="456")
        User.users.clear()
        Account.accounts.clear()

    def test_client_has_account(self) -> None:
        """Tests if the account is assigned to a client who has one already."""
        u1: User = User("123")
        u2: User = User("456")
        a1: Account = Account("asd", 0, owner_id="123")
        with pytest.raises(AccountCreationError):
            assert Account("fgh", 0, owner_id="123")
        User.users.clear()
        Account.accounts.clear()

class TestsDeposit:
    def test_deposit_history(self) -> None:
        """Tests if the account's deposit history is formed
        correctly once.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        deposit(client_id="123", amount=10)
        assert a.history == [(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "d")]

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after one deposit.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        deposit(client_id="123", amount=10)
        assert a.balance == 10

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_deposits_history(self) -> None:
        """Tests if the deposit history is formed correctly
        throughout multiple operations.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        first_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deposit(client_id="123", amount=10)
        second_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deposit(client_id="123", amount=10)
        third_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deposit(client_id="123", amount=10)
        assert a.history == [
            (first_deposit_time, "d"),
            (second_deposit_time, "d"),
            (third_deposit_time, "d"),
        ]    

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_deposits_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after multiple deposits.
        """
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        deposit(client_id="123", amount=10)
        deposit(client_id="123", amount=20.50)
        deposit(client_id="123", amount=1.50)
        assert a.balance == 42

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_history_balance(self) -> None:
        """Tests account's balance and history after multiple deposits."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        first_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deposit(client_id="123", amount=10)
        time.sleep(1)
        second_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deposit(client_id="123", amount=20.50)
        time.sleep(1)
        third_deposit_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        deposit(client_id="123", amount=1.50)

        assert a.balance == 42
        assert a.history == [
            (first_deposit_time, "d"),
            (second_deposit_time, "d"),
            (third_deposit_time, "d"),
        ]

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_negative_money(self) -> None:
        """Tests if negative amount of money was deposited."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(NegativeAmountError):
            assert deposit(client_id="123", amount=-10)

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_client_not_found(self) -> None:
        """Tests if client is found."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(ClientNotFoundError):
            assert deposit(client_id="456", amount=10)

        User.users.clear()
        Account.accounts.clear()

class TestsWithdrawal:
    def test_withdraw_history(self) -> None:
        """Tests if the account's withdraw history is formed
        correctly once.
        """
        u: User = User("123")
        a: Account = Account("asd", 100, owner_id="123")

        withdraw(client_id="123", amount=10)
        assert a.history == [(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "w")]

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after one withdrawal.
        """
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        withdraw(client_id="123", amount=10)
        assert a.balance == 0

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_withdraws_history(self) -> None:
        """Tests if the withdrawal history is formed correctly
        throughout multiple operations.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        first_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw(client_id="123", amount=10)
        second_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw(client_id="123", amount=10)
        third_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw(client_id="123", amount=10)
        assert a.history == [
            (first_withdraw_time, "w"),
            (second_withdraw_time, "w"),
            (third_withdraw_time, "w"),
        ]    

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_withdraws_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after multiple withdrawals.
        """
        u: User = User("123")
        a: Account = Account("asd", 1000, owner_id="123")

        withdraw(client_id="123", amount=10)
        withdraw(client_id="123", amount=200)
        withdraw(client_id="123", amount=0.01)
        assert a.balance == 789.99

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_history_balance(self) -> None:
        """Tests account's balance and history after multiple withdrawals."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        first_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw(client_id="123", amount=10)
        time.sleep(1)
        second_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw(client_id="123", amount=20)
        time.sleep(1)
        third_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw(client_id="123", amount=1)

        assert a.balance == -21
        assert a.history == [
            (first_withdraw_time, "w"),
            (second_withdraw_time, "w"),
            (third_withdraw_time, "w"),
        ]

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_negative_money(self) -> None:
        """Tests if negative amount of money was withdrawn."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(NegativeAmountError):
            assert withdraw(client_id="123", amount=-10)

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_client_not_found(self) -> None:
        """Tests if client is found."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(ClientNotFoundError):
            assert withdraw(client_id="456", amount=10)

        User.users.clear()
        Account.accounts.clear()

class TestsIntegrity:
    def test_number_of_decimals(self) -> None:
        """Tests if amount of money entered contains 2 decimals."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        try:
            withdraw(client_id="123", amount=10.11)
            withdraw(client_id="123", amount=0.1)
            deposit(client_id="123", amount=0.10)
            withdraw(client_id="123", amount=0.01)
            deposit(client_id="123", amount=10000.01)
        except:
            assert False
        else:
            assert True
        finally:
            with pytest.raises(WrongAmountFormat):
                assert withdraw(client_id="123", amount=10.00111)

        User.users.clear()
        Account.accounts.clear()

