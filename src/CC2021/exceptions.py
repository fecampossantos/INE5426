class ExceptionAsBreakOutsideLoop(Exception):
    """Thrown when a break is found outside a loop scope"""


class ExceptionAsInvalidIdentifierDeclaration(Exception):
    """Thrown when an identifier can't be declared in the current scope"""