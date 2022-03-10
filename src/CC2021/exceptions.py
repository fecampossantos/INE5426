class ExceptionAsBreakOutsideLoop(Exception):
    """Thrown when a break is found outside a loop scope"""


class ExceptionAsInvalidIdentifierDeclaration(Exception):
    """Thrown when an identifier can't be declared in the current scope"""

class ExceptionAsInvalidOperation(Exception):
    """Thrown when there is an invalid operation between two variable types"""

class ExceptionAsVariableNotDeclared(Exception):
    """Thrown when there is access to a not declared variable"""