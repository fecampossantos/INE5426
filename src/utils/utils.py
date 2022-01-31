
EMPTY_SYMBOL = '&'
STACK_BOTTOM = '$'
PROGRAM_START = 'PROGRAM'

_MAP = {
    'DEF': 'def',
    'FOR': 'for',
    'READ': 'read',
    'PRINT': 'print',
    'RETURN': 'return',
    'IF': 'if',
    'ELSE': 'else',
    'NEW': 'new',
    'INT': 'int',
    'FLOAT': 'float',
    'STRING': 'string',
    'BREAK': 'break',
    'LEFTBRACE': '{',
    'RIGHTBRACE': '}',
    'LPARENTHESES': '(',
    'RPARENTHESES': ')',
    'LBRACKET': '[',
    'RBRACKET': ']',
    'GT': '>',
    'LT': '<',
    'GE': '>=',
    'LE': '<=',
    'EQUALS': '==',
    'DIFFERENT': '!=',
    'PLUS': '+',
    'MINUS': '-',
    'TIMES': '*',
    'DIVIDE': '/',
    'MOD': '%',
    'SEMICOLON': ';',
    'COMMA': ',',
    'NULL': 'null',
    'ASSIGN': '=',
    'IDENT': 'ident',
    'FLOATCONSTANT': 'float_constant',
    'INTCONSTANT': 'int_constant',
    'STRINGCONSTANT': 'string_constant',
    'END_STACK_TOKEN': '$'
}

def merge(a, b):
    n = len(a)
    a |= b - {EMPTY_SYMBOL}
    return len(a) != n