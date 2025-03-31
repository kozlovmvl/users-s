from string import ascii_letters, digits

from .exceptions import UsernameInvalidLength, UsernameInvalidSymbol, EmailInvalidStruct


def validate_username_length(value: str) -> str:
    if len(value) < 3:
        raise UsernameInvalidLength
    return value


def validate_username_symbols(value: str) -> str:
    valid_symbols = ascii_letters + digits + "-_"
    if any([s not in valid_symbols for s in value]):
        raise UsernameInvalidSymbol
    return value


def validate_email_struct(value: str) -> str:
    parts = value.split("@")
    if len(parts) != 2 or parts[0] == "" or parts[1] == "":
        raise EmailInvalidStruct
    return value
