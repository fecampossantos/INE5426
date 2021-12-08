###############################################################
#             Construção de Compiladores - INE5426            #  
#               Construção de Analisador Léxico               #
#                           2021.2                            #
#                   Eduardo Gutterres [17200439]              #
#                 Felipe de Campos Santos [17200441]          #
#                   Ricardo Giuliani [17203922]               #
###############################################################


import sys
from ply import lex
from prettytable import PrettyTable


def build_lexer(input):

    

    # =================================================================================
    # Builds the lexer
    lexer = lex.lex()

    return lexer
    # =================================================================================




def parser(data, lexer):
    TYPES_CHECK = ['int', 'float', 'string', 'def']
    # simple list of tokens, consisting of an array
    # of token values
    token_list = []

    # tokens table on the form of
    # {type, value, line, column}
    tokens_table = []

    # symbols table on the form
    # {name, type, declared_line, referenced_lines}
    symbols_table = {}

    lexer.input(data)
    tok = ''

    while True:
        last_tok = tok
        tok = lexer.token()
        if not tok:
            break  # when tok receives NONE, which means end of file
        token_list.append(tok.value)
        tokens_table.append({'token': tok.type, 'value': tok.value,
                            'line': tok.lineno, 'column': find_column(data, tok)})
        if tok.type == 'IDENT':
            # being declared
            if last_tok.value in TYPES_CHECK:
                # already been referenced before
                if tok.value in symbols_table:
                    symbols_table[tok.value]['type'] = last_tok.value
                    symbols_table[tok.value]['declared_line'] = tok.lineno
                else: # hasnt been referenced yet
                    symbols_table[tok.value] = {'name': tok.value, 'type': last_tok.value, 'declared_line': tok.lineno, 'referenced_lines': []}
            else:
                # it is only being referenced
                # already been declared before
                if tok.value in symbols_table:
                    symbols_table[tok.value]['referenced_lines'].append(tok.lineno) 
                else: # hasnt been referenced yet
                    symbols_table[tok.value] = {'name': tok.value, 'type': 'NO_TYPE', 'declared_line': 'NOT_DECLARED', 'referenced_lines': [tok.lineno]}

    return token_list, tokens_table, symbols_table


def print_tokens_table(tokens_table):
    print("========= Tokens Table =========")
    t = PrettyTable(['TOKEN', 'VALUE', 'LINE', 'COLUMN'])
    for entrie in tokens_table:
        t.add_row([entrie['token'], entrie['value'],
                  entrie['line'], entrie['column']])
    print(t)
    print()
    print()


def print_token_list(token_list):
    print("========= Token List =========")
    for tok in token_list:
        print(tok)
    print()
    print()

def print_symbols_table(symbols_table):
    print("========= Symbols Table =========")
    t = PrettyTable(['NAME', 'TYPE', 'DECLARED', 'REFERENCED'])
    for key in symbols_table:
        symbol = symbols_table[key]
        t.add_row([symbol['name'],symbol['type'],symbol['declared_line'],symbol['referenced_lines']])
    print(t)
    print()
    print()

def main(data):
    lexer = build_lexer(data)
    token_list, tokens_table, symbols_table = parser(data, lexer)
    print_tokens_table(tokens_table)
    # print_token_list(token_list)
    print_symbols_table(symbols_table)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No PATH received as argument.")
    else:
        input_file = open(sys.argv[1])
        data = input_file.read()
        input_file.close()

        main(data)
