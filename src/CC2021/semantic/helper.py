from CC2021.exceptions import ExceptionAsInvalidOperation
from utils.utils import validOperationResults

def checkIfIsValid(leftType, rightType, op, lineNumber):
    opResult = validOperationResults.get((leftType, op, rightType), None)

    if opResult is None:
        raise ExceptionAsInvalidOperation(f'{leftType},{rightType},{lineNumber}')
    
    return 1, opResult