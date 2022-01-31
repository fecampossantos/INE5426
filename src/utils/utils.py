
EMPTY_SYMBOL = '&'
STACK_BOTTOM = '$'
PROGRAM_START = 'PROGRAM'

def merge(a, b):
    n = len(a)
    a |= b - {EMPTY_SYMBOL}
    return len(a) != n