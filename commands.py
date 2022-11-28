import functools
from datetime import datetime
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from user import Account, User
from exceptions import (
    NegativeAmountError,
    ClientNotFoundError,
    AccountNotFoundError,
    WrongAmountFormat,
)

console = Console()


def check_validity(command_func):
    """Decorator to hold all the checks for `withdraw` and `deposit`
    functions.
    """
    @functools.wraps(command_func)
    def wrapper(*args):
        client_id: str = str(args[0])
        amount: float = float(args[1])
        try:
            description: str = str(args[2])
        except IndexError:
            description: str = ""
        
        # Just list all the checks here.
        client: User = User.users.get(client_id)
        if isinstance(amount, int):
            number_of_decimals: int = 2
        else:
            number_of_decimals: int = len(str(amount).split(".")[1])
        if not client:
            rprint(f"[red]Client not found! Try again.")
            raise ClientNotFoundError
        elif amount <= 0:
            rprint(f"[red]amount [white]must be positive number ([red]amount [white]> 0)! Try again.")
            raise NegativeAmountError
        elif number_of_decimals > 2:
            rprint(f"[red]amount [white]must have 2 floating point decimals (e.g. `10.95`) or none (e.g. `500`)! Try again.")
            raise WrongAmountFormat
        else:
            return command_func(client_id, amount, description)
    return wrapper

@check_validity
def deposit(client_id: str, amount: float, description: str = "ATM Deposit"):
    """Description: Deposits money to a given client. Example: `deposit 123-NSiw0-X 15421.22`
        Args:
            *client_id (text): client's ID, on whose account money is to be deposited.
            *amount (float): amount of money to deposit. Minimum: ¢1, Maximum: $1000000 (1 million).
                Format must include pennies after a 'dot', e.g.: 100.12 OR 0.99 OR 2222.00 OR 0.01.
            *description (text, optional): description of a deposit action. [default="ATM Deposit"]
    """
    
    client: User = User.users.get(client_id)
    deposit_time: str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    client.account.history.append((deposit_time, "d"))
    client.account.balance += amount
    print(f"{client_id} depositted ${amount} for '{description}'.")

@check_validity
def withdraw(client_id: str, amount: float, description: str = "ATM Withdrawal"):
    """Description: Withdraws money from a given client. Example: `withdraw 092-VanR0-S 100009.01`
        Args:
            *client_id (text): client's ID, from whose account money is to be withdrawn."
            *amount (float): amount of money to withdraw. Minimum: ¢1, Maximum: $1000000 (1 million),
                but no more than a client has!"
                Format must include pennies after a 'dot', e.g.: `100.12` OR `0.99` OR `2222.00` OR `0.01`."
            *description (text, optional): description of a withdrawal action. [default="ATM Withdrawal"]
    """
    client: User = User.users.get(client_id)
    withdraw_time: str = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    client.account.history.append((withdraw_time, "w"))
    client.account.balance -= amount
    print(f"{client_id} withdrew ${amount} for '{description}'.")

def show_bank_statement(client_id: str, since: datetime = None, till: datetime = None):
    """Description: Show all client's operations.
        Args:
            *client_id (text): client's ID, whose transaction history to display."
            *since (date): from which date to show information. Formats:"
                YYYY-MM-DD; YYYY/MM/DD; YYYY-MM-DD HH:MinMin:SS; YYYY/MM/DD HH:MinMin:SS"
            *till (date): to which date to show information. Formats:"
                YYYY-MM-DD; YYYY/MM/DD; YYYY-MM-DD HH:MinMin:SS; YYYY/MM/DD HH:MinMin:SS"
            (If no `since` or `till` date is provided, shows from the very first transaction or until the very last, respectively.)
    """
    client: User = User.users.get(client_id)
    table = Table("Date", "Description", "Withdrawals", "Deposits", "Balance")
    table.add_row("", "Previous balance", "", "", f"${client.account._initial_balance}", end_section=True)
    table.add_row("yyyy-mm-dd hh:mnmn:ss", "ATM Deposit", "$100.00", "$100.00")
    table.add_row("yyyy-mm-dd hh:mnmn:ss", "ATM Deposit", "$5_000_000.50", "$5_000_100.50")
    table.add_row("yyyy-mm-dd hh:mnmn:ss", "ATM Withdrawal", "$180_000.00", "", "$4_820_100.50", end_section=True)
    table.add_row("", "Totals", "$180_000.00", "$5_000_100.50", "$4_821_000.50")
    console.print(table)

def create_user(client_id: str):
    """Description: Creates a user (client) with given `client_id`.
            Bank account must be created and assigned separately.
        Args:
            *client_id (text): create user with this ID.
    """
    print(f"Created client: {client_id}")
    return User(client_id)

def create_account(account_id: str, client_id: str,
                    balance: float = 0):
    """Description: Creates a bank account assigned to a client.
            Initial balance can be changed.
        Args:
            *account_id (text): create bank account with this ID.
            *client_id (text): ID of this account's owner.
            *balance (float, optional): initial balance of this account. [default=0]
                Format must include pennies after a 'dot', e.g.: 100.12 OR 0.99 OR 2222.00 OR 0.01.
    """
    try:
        a: Account = Account(account_id, balance, owner_id=client_id)
    except (ValueError, TypeError):
        rprint(f"[red]balance [white]must be a number! Try again.")
    else:
        return a

def delete_user(client_id: str):
    """Description: Deletes user from database.
            CAUTION! bank account assigned to user is deleted too.
        Args:
            *client_id (text): delete user with this ID.
    """
    client: User = User.users.get(client_id)
    if client:
        rprint(f"[red]Deleted user {client}")
        User.users.pop(client_id)
    else:
        rprint(f"[red]Client not found! Try again.")
        raise ClientNotFoundError

def delete_account(account_id: str):
    """Description: Deletes bank account from database.
            Owner is not deleted.
        Args:
            *account_id (text): delete bank account with this ID.
    """
    account: Account = Account.accounts.get(account_id)
    if account:
        rprint(f"[red]Deleted account {account}")
        Account.accounts.pop(account_id)
    else:
        rprint(f"[red]Account not found! Try again.")
        raise AccountNotFoundError

def display_users():
    """Description: Displays all registered (created) users.
        Args: None
    """
    rprint(User.users)

def display_accounts():
    """Description: Displays all created accounts.
        Args: None
    """
    rprint(Account.accounts)

def exit():
    """Exit program with code 0. Also possible to exit using 'Ctrl + C.'
        Args: None
    """
    from sys import exit as _exit
    _exit(0)
