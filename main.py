from datetime import datetime
import typer
from rich.console import Console
from rich.table import Table

console = Console()
app = typer.Typer()


@app.command()
def deposit(
    client_id: str = typer.Argument(..., help="client's ID, on whose account money is to be deposited."),
    amount: float = typer.Argument(..., help="amount of money to deposit. Minimum: ¢1, Maximum: $1000000 (1 million). "
            + "Format must include pennies after a 'dot', e.g.: 100.12 OR 0.99 OR 2222.00 OR 0.01."),
    description: str = typer.Option(default="ATM Deposit", help="description of a deposit action.")
    ):
    """Deposits money to a given client. Examle: deposit 123-NSiw0-X 15421.22"""
    print(f"{client_id} depositted ${amount} for '{description}'.")

@app.command()
def withdraw(
    client_id: str = typer.Argument(..., help="client's ID, from whose account money is to be withdrawn."),
    amount: float = typer.Argument(..., help="amount of money to withdraw. Minimum: ¢1, Maximum: $1000000 (1 million), "
            + "but no more than a client has! "
            + "Format must include pennies after a 'dot', e.g.: `100.12` OR `0.99` OR `2222.00` OR `0.01`."),
    description: str = typer.Option(default="ATM Withdrawal", help="description of a withdrawal action.")
    ):
    """Withdraws money from a given client. Examle: withdraw 092-VanR0-S 100009.01"""
    print(f"{client_id} withdrew ${amount} for '{description}'.")

@app.command()
def show_bank_statement(client_id: str, since: datetime = None, till: datetime = None):
    table = Table("Date", "Description", "Withdrawals", "Deposits", "Balance")
    table.add_row("", "Previous balance", "", "", "$900.00", end_section=True)
    table.add_row("yyyy-mm-dd hh:mnmn:ss", "ATM Deposit", "$100.00", "$100.00")
    table.add_row("yyyy-mm-dd hh:mnmn:ss", "ATM Deposit", "$5_000_000.50", "$5_000_100.50")
    table.add_row("yyyy-mm-dd hh:mnmn:ss", "ATM Withdrawal", "$180_000.00", "", "$4_820_100.50", end_section=True)
    table.add_row("", "Totals", "$180_000.00", "$5_000_100.50", "$4_821_000.50")
    console.print(table)

if __name__ == "__main__":
    app()
