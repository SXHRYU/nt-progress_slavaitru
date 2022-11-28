import datetime
import time
import pytest
from user import Account, User, AccountCreationError
from commands import (
    create_user, create_account,
    delete_user, delete_account,
    display_users, display_accounts,
    deposit, withdraw,
)
from exceptions import (
    ClientNotFoundError,
    AccountNotFoundError,
    NegativeAmountError,
    WrongAmountFormat,
    AccountCreationError,
    ClientDoesNotExistError,
    AccountDoesNotExistError,
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
        assert a.balance.value == 0
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
    
    def test_client_not_exists(self) -> None:
        """Tests if the account is assigned to a non-existent user."""
        u: User = User("123")
        with pytest.raises(ClientDoesNotExistError):
            assert Account("asd", 0, owner_id="456")
        User.users.clear()
        Account.accounts.clear()
    
    def test_balance_not_string(self) -> None:
        """Tests if the balance being passed into the account
        is a numerical value.
        """
        u: User = User("123")
        with pytest.raises(ValueError):
            assert Account("asd", "lkjhg", owner_id="123")
        User.users.clear()
        Account.accounts.clear()
        
    def test_balance_not_sequence(self) -> None:
        """Tests if the balance being passed into the account
        is a numerical value.
        """
        u: User = User("123")
        with pytest.raises(TypeError):
            assert Account("asd", [1000], owner_id="123")
            assert Account("asd", (1000), owner_id="123")
            assert Account("asd", set(1000), owner_id="123")
            assert Account("asd", {1000: None}, owner_id="123")
        User.users.clear()
        Account.accounts.clear()

class TestsDeposit:
    def test_deposit_client_not_found(self) -> None:
        """Tests if client is found."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(ClientNotFoundError):
            assert deposit("456", 10)

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_client_no_account(self) -> None:
        """Tests if client is found but he has no account."""
        u: User = User("123")

        with pytest.raises(AccountDoesNotExistError):
            assert deposit("123", 10)

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_history(self) -> None:
        """Tests if the account's deposit history is formed
        correctly once.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        deposit("123", 10, "test1")
        assert a.history == [
            (str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "d", 10, "test1", "$10.0")
        ]

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after one deposit.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        deposit("123", 10)
        assert a.balance.value == 10

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_deposits_history(self) -> None:
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
        deposit("123", 10, "test3")
        assert a.history == [
            (first_deposit_time, "d", 10, "", "$10.0"),
            (second_deposit_time, "d", 10, "", "$20.0"),
            (third_deposit_time, "d", 10, "test3", "$30.0"),
        ]    

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_deposits_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after multiple deposits.
        """
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        deposit("123", 10)
        deposit("123", 20.50)
        deposit("123", 1.50)
        assert a.balance.value == 42

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_history_balance(self) -> None:
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

        assert a.balance.value == 42
        assert a.history == [
            (first_deposit_time, "d", 10.0, "", "$20.0"),
            (second_deposit_time, "d", 20.50, "", "$40.5"),
            (third_deposit_time, "d", 1.50, "", "$42.0"),
        ]

        User.users.clear()
        Account.accounts.clear()

    def test_deposit_negative_money(self) -> None:
        """Tests if negative amount of money was deposited."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(NegativeAmountError):
            assert deposit("123", -10)

        User.users.clear()
        Account.accounts.clear()

class TestsWithdrawal:
    def test_withdraw_client_not_found(self) -> None:
        """Tests if client is found."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(ClientNotFoundError):
            assert withdraw("456", 10)

        User.users.clear()
        Account.accounts.clear()


    def test_withdraw_client_no_account(self) -> None:
        """Tests if client is found but he has no account."""
        u: User = User("123")

        with pytest.raises(AccountDoesNotExistError):
            assert withdraw("123", 10)

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_history(self) -> None:
        """Tests if the account's withdraw history is formed
        correctly once.
        """
        u: User = User("123")
        a: Account = Account("asd", 100, owner_id="123")

        withdraw("123", 10, "test")
        assert a.history == [
            (str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "w", 10, "test", "$90.0")
            ]

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after one withdrawal.
        """
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        withdraw("123", 10)
        assert a.balance.value == 0

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_withdraws_history(self) -> None:
        """Tests if the withdrawal history is formed correctly
        throughout multiple operations.
        """
        u: User = User("123")
        a: Account = Account("asd", 0, owner_id="123")

        first_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw("123", 10)
        second_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw("123", 10)
        third_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw("123", 10)
        assert a.history == [
            (first_withdraw_time, "w", 10, "", "-$10.0"),
            (second_withdraw_time, "w", 10, "", "-$20.0"),
            (third_withdraw_time, "w", 10, "", "-$30.0"),
        ]    

        User.users.clear()
        Account.accounts.clear()

    def test_multiple_withdraws_balance(self) -> None:
        """Tests if the account's balance is formed correctly
        after multiple withdrawals.
        """
        u: User = User("123")
        a: Account = Account("asd", 1000, owner_id="123")

        withdraw("123", 10)
        withdraw("123", 200)
        withdraw("123", 0.01)
        assert a.balance.value == 789.99

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_history_balance(self) -> None:
        """Tests account's balance and history after multiple withdrawals."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        first_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw("123", 10, "test1")
        time.sleep(1)
        second_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw("123", 20, "test2")
        time.sleep(1)
        third_withdraw_time: str = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        withdraw("123", 1, "test1")

        assert a.balance.value == -21
        assert a.history == [
            (first_withdraw_time, "w", 10, "test1", "$0.0"),
            (second_withdraw_time, "w", 20, "test2", "-$20.0"),
            (third_withdraw_time, "w", 1, "test1", "-$21.0"),
        ]

        User.users.clear()
        Account.accounts.clear()

    def test_withdraw_negative_money(self) -> None:
        """Tests if negative amount of money was withdrawn."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(NegativeAmountError):
            assert withdraw("123", -10)

        User.users.clear()
        Account.accounts.clear()

class TestsIntegrity:
    def test_number_of_decimals(self) -> None:
        """Tests if amount of money entered contains 2 decimals."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        try:
            withdraw("123", 10.11)
            withdraw("123", 0.1)
            deposit("123", 0.10)
            withdraw("123", 0.01)
            deposit("123", 10000.01)
        except:
            assert False
        else:
            assert True
        finally:
            with pytest.raises(WrongAmountFormat):
                assert withdraw("123", 10.00111)

        User.users.clear()
        Account.accounts.clear()

    def test_if_number(self) -> None:
        """Tests if number was actually passed into operations."""
        u: User = User("123")
        a: Account = Account("asd", 10, owner_id="123")

        with pytest.raises(ValueError):
            assert deposit(123, "dd")
        
        User.users.clear()
        Account.accounts.clear()

class TestsUtility:
    """Tests given utility functions from `commands.py`."""
    def test_create_user(self) -> None:
        create_user("asd")
        create_user("qwe")
        create_user("zxc")
        assert User.users == {
            "asd": User.users["asd"],
            "qwe": User.users["qwe"],
            "zxc": User.users["zxc"],
        }

        User.users.clear()
        Account.accounts.clear()
        
    def test_create_account(self) -> None:
        u1: User = User("qwe")
        u2: User = User("asd")
        u3: User = User("zxc")
        create_account("123", "qwe")
        create_account("456", "asd", 100.0)
        create_account("789", "zxc", 123456.23)
        assert Account.accounts == {
            "123": Account.accounts["123"],
            "456": Account.accounts["456"],
            "789": Account.accounts["789"],
        }
        User.users.clear()
        Account.accounts.clear()

    def test_delete_user(self) -> None:
        u1: User = User("qwe")
        u2: User = User("asd")
        u3: User = User("zxc")
        delete_user("qwe")
        delete_user("zxc")
        assert User.users == {
            "asd": User.users["asd"],
        }
        User.users.clear()
        Account.accounts.clear()
        
    def test_delete_account(self) -> None:
        u1: User = User("qwe")
        u2: User = User("asd")
        u3: User = User("zxc")
        a1: Account = Account("123", owner_id="qwe")
        a2: Account = Account("456", owner_id="asd")
        a3: Account = Account("789", owner_id="zxc")
        
        delete_account("123")
        delete_account("789")
        assert Account.accounts == {
            "456": Account.accounts["456"],
        }
        User.users.clear()
        Account.accounts.clear()

    def test_complex_utility(self) -> None:
        create_user("qwe")
        delete_user("qwe")
        create_user("qwe")

        create_user("asd")
        create_account("123", "asd")

        create_user("zxc")
        create_account("456", "zxc")
        delete_user("zxc")

        delete_account("123")
        create_account("123", "qwe")
        
        assert User.users == {
            "qwe": User.users["qwe"],
            "asd": User.users["asd"],
        }
        assert Account.accounts == {
            "123": Account.accounts["123"],
        }

        User.users.clear()
        Account.accounts.clear()
