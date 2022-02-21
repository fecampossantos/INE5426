from utils.utils import validOperationResults

def checkIfIsValid(leftType, rightType, op, lineNumber):
    opResult = validOperationResults.get((leftType, op, rightType), None)

    if opResult is None:
        return -1, 'Essa operacao nao e valida'
    
    return 1, opResult