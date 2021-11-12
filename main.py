import sys
# from al import build_lexer, parser
from ply import lex


def build_lexer(input):

    #============ OPERADORES ============#

    # Aritméticos
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'

    # Relacionais
    t_EQUAL = r'=='
    t_DIFFERENT = r'!='
    t_LT = r'<'
    t_LE = r'<='
    t_GT = r'>'
    t_GE = r'>='
    t_ASSIGN = r'='

    # Outros
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_RPARENTHESES = r'\)'
    t_LPARENTHESES = r'\('
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_RBRACE = '}'
    t_LEFTBRACE = r'{'
    t_DOT = r'\.'

    # t_LINEBREAK = r'\n'

    def t_LINEBREAK(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    # float tem que ir antes
    def t_FLOATCONSTANT(t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTCONSTANT(t):
        r'[0-9A-F]+[hH]|[0-7]+[oO]|[01]+[bB]|[0-9]+'
        # t.value = int(t.value)
        return t

    def t_STRINGCONSTANT(t):
        r'"[^\n"\r]*"'
        return t

    # ident has to come after the string constant, or else the
    # rule "<ident>" would be true
    def t_IDENT(t):
        r'[A-Za-z][A-Za-z0-9]*'
        t.type = reserved.get(t.value,'IDENT')    # Check for reserved words
        return t

    t_ignore = ' \t'

    # ERRO
    def t_error(t):
        column = find_column(input, t)
        print()
        print("| Erro léxico em:    '%s'" % t.value[0])
        print("|   -> Linha:        '%s'" % t.lexer.lineno)
        print("|       -> Coluna:   '%s'" % column)
        print()
        t.lexer.skip(1)

    # palavras reservadas
    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'string': 'STRING',
        'new': 'ALLOC',
        'def': 'DEF',
        'break': 'BREAK',
        'print': 'PRINT',
        'return': 'RETURN',
        'read': 'READ',
        'if': 'IF',
        'for': 'FOR',
    }

    # Tokens
    tokens = list(reserved.values()) + ['PLUS', 'MINUS',
              'TIMES', 'DIVIDE', 'MOD', 'EQUAL', 'DIFFERENT', 'LT', 'LE', 'GT',
              'GE', 'ASSIGN', 'COMMA', 'SEMICOLON', 'RPARENTHESES',
              'LPARENTHESES', 'LBRACKET', 'RBRACKET', 'RBRACE',
              'LEFTBRACE', 'DOT', 'FLOATCONSTANT', 'INTCONSTANT',
              'STRINGCONSTANT', 'LINEBREAK', 'IDENT']

    # ------------------------------------------------------------------------------
    # Build the lexer
    lexer = lex.lex()

    return lexer
    # ------------------------------------------------------------------------------

# https://www.dabeaz.com/ply/ply.html#ply_nn9
# Compute column.
#     input is the input text string
#     token is a token instance


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def parser(data, lexer):
    # lexer = build_lexer()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break  # when tok receives NONE, which means end of file
        print(tok)


def main(data):
    lexer = build_lexer(data)
    parser(data, lexer)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Por favor, passe o PATH do arquivo como argumento")
    else:
        input_file = open(sys.argv[1])
        data = input_file.read()
        input_file.close()

        main(data)
