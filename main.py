import typer
from datetime import datetime

app = typer.Typer()


@app.command()
def deposit(
    client_id: str = typer.Argument(..., help="client's ID, on whose account money is to be deposited."),
    amount: float = typer.Argument(..., help="amount of money to deposit. Minimum: ¢1, Maximum: $1000000 (1 million). "
            + "Format must include pennies after a 'dot', e.g.: 100.12 OR 0.99 OR 2222.00 OR 0.01."),
    description: str = typer.Option(default="ATM Deposit", help="description of a deposit action.")
    ):
    """Deposits money to a given client."""
    print(f"{client_id} depositted ${amount} for '{description}'.")

@app.command()
def withdraw(
    client_id: str = typer.Argument(..., help="client's ID, from whose account money is to be withdrawn."),
    amount: float = typer.Argument(..., help="amount of money to withdraw. Minimum: ¢1, Maximum: $1000000 (1 million), "
            + "but no more than a client has! "
            + "Format must include pennies after a 'dot', e.g.: `100.12` OR `0.99` OR `2222.00` OR `0.01`."),
    description: str = typer.Option(default="ATM Withdrawal", help="description of a withdrawal action.")
    ):
    """Withdraws money from a given client."""
    print(f"{client_id} withdrew ${amount} for '{description}'.")

@app.command()
def show_bank_statement(client_id: str, since: datetime = None, till: datetime = None):
    print(
            "----------------------------------------------------------------------------------------------------\n"
        +   "| Date                | Description      | Withdrawals     | Deposits          | Balance           |\n"
        +   "|---------------------|------------------|-----------------|-------------------|-------------------|\n"
        +   "|                     | Previous balance |                 |                   |            $900.00|\n"
        +   "|---------------------|------------------|-----------------|-------------------|-------------------|\n"
        +   "|yyyy-mm-dd hh:mnmn:ss| ATM Deposit      |                 |            $100.00|            $100.00|\n"
        +   "|yyyy-mm-dd hh:mnmn:ss| ATM Deposit      |                 |      $5_000_000.50|      $5_000_100.50|\n"
        +   "|yyyy-mm-dd hh:mnmn:ss| ATM Withdrawal   |      $180_000.00|                   |      $4_820_100.50|\n"
        +   "|---------------------|------------------|-----------------|-------------------|-------------------|\n"
        +   "|                     | Totals           |      $180_000.00|      $5_000_100.50|      $4_821_000.50|\n"
        +   "----------------------------------------------------------------------------------------------------\n"
    )


if __name__ == "__main__":
    app()
