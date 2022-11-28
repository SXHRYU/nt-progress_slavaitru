import functools
from datetime import datetime
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from user import Account, User, _Balance
from exceptions import (
    NegativeAmountError,
    ClientNotFoundError,
    AccountNotFoundError,
    AccountDoesNotExistError,
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
        try:
            amount: float = float(args[1])
        except ValueError:
            rprint(f"[red]amount [white]must be a numerical value.")
            raise ValueError
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
            rprint("[red]Client not found! Try again.")
            raise ClientNotFoundError
        elif not hasattr(client, "account"):
            rprint("[red]Client doesn't have a bank account! Try again.")
            raise AccountDoesNotExistError
        elif amount <= 0:
            rprint("[red]amount [white]must be positive number ([red]amount [white]> 0)! Try again.")
            raise NegativeAmountError
        elif number_of_decimals > 2:
            rprint("[red]amount [white]must have 2 floating point decimals (e.g. `10.95`) or none (e.g. `500`)! Try again.")
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
    client.account.balance += amount
    client.account.history.append((deposit_time, "d", amount, description, str(client.account.balance)))
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
    client.account.balance -= amount
    client.account.history.append((withdraw_time, "w", amount, description, str(client.account.balance)))
    print(f"{client_id} withdrew ${amount} for '{description}'.")

def show_bank_statement(client_id: str, since: datetime = None, till: datetime = None):
    """Description: Show all client's operations.
        Args:
            *client_id (text): client's ID, whose transaction history to display."
            *since (date): from which date to show information. Formats (no quotes):"
                YYYY-MM-DD; YYYY/MM/DD; YYYY-MM-DD HH:MinMin:SS; YYYY/MM/DD HH:MinMin:SS"
                To skip this parameter, enter any symbol.
            *till (date): to which date to show information. Formats (no quotes):"
                YYYY-MM-DD; YYYY/MM/DD; YYYY-MM-DD HH:MinMin:SS; YYYY/MM/DD HH:MinMin:SS"
            (If no `since` or `till` date is provided, shows from the very first transaction or until the very last, respectively.)
            Examples:
                `show_bank_statement STYB227`
                `show_bank_statement STYB227 1999-09-30 2022/10/10 20:15:14`
                (skip `since`) `show_bank_statement STYB227 - 2022/10/10 20:15:14`
                (skip `till`) `show_bank_statement STYB227 1999-09-30`
                (skip `till`) `show_bank_statement STYB227 1999-09-30 -`
    """
    def _transform_to_datetime(date_string: str) -> datetime:
        # Needed because of different possible date fields.
        formats = [
            "%Y-%m-%d %H:%M:%S",     # -> YYYY-MM-DD HH:MinMin:SS
            "%Y/%m/%d %H:%M:%S",     # -> YYYY/MM/DD HH:MinMin:SS
            "%Y-%m-%d",              # -> YYYY-MM-DD
            "%Y/%m/%d",              # -> YYYY/MM/DD
        ]
        for format in formats:
            try:
                datetime_obj = datetime.strptime(date_string, format)
            except ValueError:
                continue
            else:
                break
        else:
            raise ValueError
        return datetime_obj

    try:
        if not since:
            since = datetime.min
        else:
            since = _transform_to_datetime(since)
    except ValueError:
        rprint("[blue][bold]since is skipped")
        since = datetime.min
    try:
        if not till:
            till = datetime.max
        else:
            till = _transform_to_datetime(till)
    except ValueError:
        rprint("[red]till [white]format should be of following:\n"
                + "\t*YYYY-MM-DD\n\t*YYYY/MM/DD\n\t*YYYY-MM-DD HH:MinMin:SS\n\t*YYYY/MM/DD HH:MinMin:SS")
    
    client: User = User.users.get(client_id)
    if not hasattr(client, "account"):
        rprint(f"Client '[bold]{client_id}' [red]doesn't have an account yet!")
    else:
        total_deposit: float = _Balance('0')
        total_withdraw: float = _Balance('0')
        final_balance: float = _Balance(client.account._initial_balance)

        table = Table("Date", "Description", "Withdrawals", "Deposits", "Balance")
        table.add_row("", "Previous balance", "", "", f"${client.account._initial_balance}", end_section=True)

        for operation in client.account.history:
            if since < datetime.strptime(operation[0], "%Y-%m-%d %H:%M:%S") < till:
                if operation[1] == "d":
                    table.add_row(operation[0], operation[3], "", f"${operation[2]}", str(operation[4]))
                    total_deposit += float(operation[2])
                    final_balance += float(operation[2])
                elif operation[1] == "w":
                    table.add_row(operation[0], operation[3], f"${operation[2]}", "", str(operation[4]))
                    total_withdraw += float(operation[2])
                    final_balance -= float(operation[2])
        table.add_row("", "Totals", str(total_withdraw), str(total_deposit), str(final_balance))
        console.print(table)

def create_user(client_id: str):
    """Description: Creates a user (client) with given `client_id`.
            Bank account must be created and assigned separately.
        Args:
            *client_id (text): create user with this ID.
    """
    u: User = User(client_id)
    rprint(f"Created client: [bold]{u}")
    return u

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
        rprint(f"Created account: [bold]{a}")
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
        if hasattr(client, "account"):
            # technically it'd be better architecture-wise to implement
            # observer class to detect changes in `Users.user` to delete
            # the corresponding account on user deletion but I don't
            # have neither knowledge nor time to do it
            Account.accounts.pop(client.account.id)
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
