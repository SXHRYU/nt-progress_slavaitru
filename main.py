import inspect
import itertools
from rich import print as rprint
from commands import (
    create_user, create_account,
    delete_user, delete_account,
    display_users, display_accounts,
    deposit, withdraw, show_bank_statement,
    exit
)
from exceptions import (
    MissingArgumentError,
    ExcessArgumentsError,
)

COMMANDS = {
    "create_user": create_user,
    "create_account": create_account,
    "delete_user": delete_user,
    "delete_account": delete_account,
    "display_users": display_users,
    "display_accounts": display_accounts,
    "deposit": deposit,
    "withdraw": withdraw,
    "show_bank_statement": show_bank_statement,
    "exit": exit,
}

def display_available_commands() -> None:
    raw_commands: list[tuple[str, function]] = inspect.getmembers(__import__("commands"), inspect.isfunction)
    commands: list[function] = [i[1] for i in raw_commands if i[0] in COMMANDS]
    docs = [i.__doc__ for i in commands]

    rprint("[bold]Commands:")
    for command, doc in zip(commands, docs):
        rprint(f"\t'{command.__name__}'")
        rprint(f"\t[blue]{doc}")

def display_command_help(command: str) -> None:
    function = COMMANDS[command]
    rprint("[bold]Command:")
    rprint(f"\t'{function.__name__}'")
    rprint(f"\t[blue]{function.__doc__}")

def parse(user_input: str) -> None:
    command = COMMANDS[user_input.split()[0]]
    command_params = inspect.signature(command).parameters.values()
    if len(user_input.split()) == 1 and len(command_params) == 0:
        command()
    elif len(user_input.split()) == 1 and len(command_params) != 0:
        display_command_help(user_input)
    elif user_input.split()[1] in ["help", "-h", "--help"]:
        display_command_help(command)
    else:
        passed_args = user_input.split()[1:]
        function_args = []
        for arg, param in itertools.zip_longest(passed_args, command_params):
            if arg is None and param.default is not inspect.Parameter.empty:
                function_args.append(param.default)
            elif arg is None and param.default is inspect.Parameter.empty:
                rprint(f"Missing [red]{param.name} [white]value!")
                raise MissingArgumentError
            else:
                function_args.append(arg)
        if len(function_args) > len(command_params):
            rprint(f"Too many arguments! Expected: [blue]{len(command_params)}[white]. Got [red]{len(function_args)}.")
            raise ExcessArgumentsError
        command(*function_args)        

if __name__ == "__main__":
    while True:
        raw_input: str = input("> ")
        user_input: str = raw_input.strip()
        if not user_input:
            ...
        elif user_input.split()[0] in COMMANDS:
            try:
                parse(user_input)
            except Exception:
                continue
        else:
            display_available_commands()
            
