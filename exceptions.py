class ClientNotFoundError(Exception): 
    """Raises if operation on non-existent user."""
    ...

class AccountNotFoundError(Exception):
    """"Raises if operation on non-existent account
    (e.g. `delete_account`).
    """
    ...

class ClientDoesNotExistError(Exception): 
    """Raises if account assigned to non-existent user."""
    ...

class AccountDoesNotExistError(Exception): 
    """Raises if operation on user with not account."""
    ...

class NegativeAmountError(Exception): 
    """Raises if operation with `amount` < 0"""
    ...

class WrongAmountFormat(Exception): 
    """Raises if `amount` has > 2 decimals"""
    ...

class AccountCreationError(Exception): 
    """Raises if error is raised during account creation
    (that are caused directly by account creation process,
    not by, for example, assigning account to non-existent user).
    """
    ...

class MissingArgumentError(Exception): 
    """Raises if not all arguments are passed in CLI."""
    ...

class ExcessArgumentsError(Exception): 
    """Raises if excess arguments are passed in CLI."""
    ...
