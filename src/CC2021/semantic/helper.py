from CC2021.exceptions import ExceptionAsInvalidOperation
from utils.utils import validOperationResults
from CC2021.strucs import Node

def checkIfIsValid(left: Node, right: Node, op, lineNumber):
    opResult = validOperationResults.get((left.type, op, right.type), None)
    
    if opResult is None:
        raise ExceptionAsInvalidOperation(f'{left.type},{right.type},{lineNumber}')
    
    return opResult