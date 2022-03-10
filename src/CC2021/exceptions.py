class BreakOutsideLoopException(Exception):
    """Thrown when a break is found outside a loop scope"""


class InvalidIdentifierDeclarationException(Exception):
    """Thrown when an identifier can't be declared in the current scope"""
