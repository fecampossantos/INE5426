
EMPTY_SYMBOL = '&'
STACK_BOTTOM = '$'

def merge(a, b):
    n = len(a)
    a |= b - {EMPTY_SYMBOL}
    return len(a) != n