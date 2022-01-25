import sys
from prettytable import PrettyTable
from CC2021.ply.lex import lex


class Lexer:
    # Reserved words
    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'string': 'STRING',
        'new': 'NEW',
        'def': 'DEF',
        'break': 'BREAK',
        'print': 'PRINT',
        'return': 'RETURN',
        'read': 'READ',
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        # added later
        'true': 'TRUE',
        'false': 'FALSE',
        'null': 'NULL'
    }

    #============ OP ============#
    # Arithmetics
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_ASSIGN = r'='
    # Relationals
    t_EQUALS = r'=='
    t_DIFFERENT = r'!='
    t_LT = r'<'
    t_LE = r'<='
    t_GT = r'>'
    t_GE = r'>='
    # Other
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_RPARENTHESES = r'\)'
    t_LPARENTHESES = r'\('
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_RIGHTBRACE = r'}'
    t_LEFTBRACE = r'{'
    t_DOT = r'\.'

    # Linebreak
    # - Doesn't return token
    # - Count as a new line for the lexer
    def t_LINEBREAK(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        pass

    # Float
    # - Has to come before Int
    def t_FLOATCONSTANT(self, t):
        r'\d+\.\d+'
        # t.value = float(t.value)
        return t

    # Int
    # - Get's all Integer numbers (decimal, octal, hexadecimal and binary)
    def t_INTCONSTANT(self, t):
        r'[0-9A-F]+[hH]|[0-7]+[oO]|[01]+[bB]|[0-9]+'
        # t.value = int(t.value)
        return t

    # String
    # - Any characters inside double quotes ("")
    def t_STRINGCONSTANT(self, t):
        r'"[^\n"\r]*"'
        return t

    # Identification
    # - Has to come after the string constant, or else the rule "<ident>" would be true
    # - Before returning, checks if the string perceived as Id is not a reserved word.
    # --> If it is, returns the token type as the reserved word instead of 'IDENT'
    def t_IDENT(self, t):
        r'[A-Za-z][A-Za-z0-9]*'
        t.type = self.reserved.get(t.value, 'IDENT')    # Check for reserved words
        return t

    # Comment
    # Get's anything between /* ... */, for multiline comments,
    # or after // for single line comments
    # - Doesn't return anything, the "token" is discarded
    def t_COMMENT(self, t):
        r'(\/\*([^*]|[\r\n]|(\*+([^*\/]|[\r\n])))*\*+\/)|(\/\/.*)'
        pass

    # Ignores spaces
    t_ignore = ' \t'
    
    # Error
    # - Called when a token is not recognized by any of the rules
    # - Calls find_column to get the column in the line of the error
    # - Prints the character, line and column of the lexical error
    def t_error(self, t):
        column = self.find_column(input, t)
        print()
        print('\x1b[7;31;47m' +
              "|        ERRO LÉXICO ENCONTRADO        |" + '\x1b[0m')
        print("|      -> Caracter:  '%s'" % t.value[0])
        print("|      -> Linha:      %s" % t.lexer.lineno)
        print("|      -> Coluna:     %s" % column)
        print()
        t.lexer.skip(1)

    # Tokens
    tokens = list(reserved.values()) + ['PLUS', 'MINUS',
                                        'TIMES', 'DIVIDE', 'MOD', 'EQUALS', 'DIFFERENT', 'LT', 'LE', 'GT',
                                        'GE', 'ASSIGN', 'COMMA', 'SEMICOLON', 'RPARENTHESES',
                                        'LPARENTHESES', 'LBRACKET', 'RBRACKET', 'RIGHTBRACE',
                                        'LEFTBRACE', 'DOT', 'FLOATCONSTANT', 'INTCONSTANT',
                                        'STRINGCONSTANT', 'LINEBREAK', 'IDENT']
    # https://www.dabeaz.com/ply/ply.html#ply_nn9
    # Compute column.
    #     input is the input text string
    #     token is a token instance

    def find_column(self, input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, code: str, **kwargs):
        self._input = code
        self.lexer.input(code, **kwargs)

    def token(self):
        return self.lexer.token()
