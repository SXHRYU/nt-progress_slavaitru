import typer
from datetime import datetime

app = typer.Typer()


@app.command()
def deposit(client: str, amount: float, description: str = "ATM Deposit"):
    print(f"{client} depositted ${amount} for '{description}'.")

@app.command()
def withdraw(client: str, amount: float, description: str = "ATM Withdrawal"):
    print(f"{client} withdrew ${amount} for '{description}'.")

@app.command()
def show_bank_statement(client: str, since: datetime = None, till: datetime = None):
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
