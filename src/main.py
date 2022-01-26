###############################################################
#             Construção de Compiladores - INE5426            #
#               Construção de Analisador Léxico               #
#                           2021.2                            #
#                   Eduardo Gutterres [17200439]              #
#                 Felipe de Campos Santos [17200441]          #
#                   Ricardo Giuliani [17203922]               #
###############################################################


import sys
import os
from prettytable import PrettyTable

from CC2021.lexer.lexer import Lexer
from CC2021.parser.parser import parser
# from parser.parser import Parser
from utils.printer import print_symbols_table, print_token_list, print_tokens_table
from CC2021.semantic.semantic import parse
from CC2021.yac.yacc_parser import generate_code_from_source


def get_info(data, lexer):
    TYPES_CHECK = ['int', 'float', 'string', 'def']
    # simple list of tokens, consisting of an array
    # of token values
    token_list = []
    tokens_values = []

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
        token_list.append(tok)
        tokens_values.append(tok.value)
        tokens_table.append({'token': tok.type, 'value': tok.value,
                            'line': tok.lineno, 'column': lexer.find_column(data, tok)})
        if tok.type == 'IDENT':
            # being declared
            if last_tok.value in TYPES_CHECK:
                # already been referenced before
                if tok.value in symbols_table:
                    symbols_table[tok.value]['type'] = last_tok.value
                    symbols_table[tok.value]['declared_line'] = tok.lineno
                else:  # hasnt been referenced yet
                    symbols_table[tok.value] = {
                        'name': tok.value, 'type': last_tok.value, 'declared_line': tok.lineno, 'referenced_lines': []}
            else:
                # it is only being referenced
                # already been declared before
                if tok.value in symbols_table:
                    symbols_table[tok.value]['referenced_lines'].append(
                        tok.lineno)
                else:  # hasnt been referenced yet
                    symbols_table[tok.value] = {'name': tok.value, 'type': 'NO_TYPE',
                                                'declared_line': 'NOT_DECLARED', 'referenced_lines': [tok.lineno]}

    return token_list, tokens_values, tokens_table, symbols_table


def main(data):
    lexer = Lexer()
    lexer.build()
    lexer.input(data)

    token_list, tokens_values, tokens_table, symbols_table = get_info(
        data, lexer)
    # print_tokens_table(tokens_table)
    # print_token_list(tokens_values)
    # print_symbols_table(symbols_table)


    check, wrong_token = parser.parse(tokens=token_list)

    if not check:
        print('Syntatic error on line %s' % wrong_token.lineno)
        print('Token: %s' % wrong_token)
        sys.exit(1)

    print('Syntatic Analysis succesfull! \n')

    return
    #need to do semantic analysis later


if __name__ == '__main__':
    args = sys.argv[1]

    if(args == 'all'):
      paths = [
        # 'src/examples/exemplo1.lcc', #passes
        # 'src/examples/exemplo2.lcc', #passes
        # 'src/examples/prog1.lcc', #error
        # 'src/examples/tdee.lcc', #error
        # 'src/examples/utils.lcc', #error
        'src/examples/utils2.lcc',
        'src/examples/bhaskara.lcc',
        'src/examples/example_error_break.lcc',
        'src/examples/example_error_var_scope.lcc',
        'src/examples/example_error_var_type.lcc',
        'src/examples/exemplo3.lcc',
        'src/examples/geometry.lcc',
        'src/examples/math.lcc',
        'src/examples/vinho.lcc',
        ]
      for path in paths:
        print('running for %s' %path)
        inp = open(path)
        data = inp.read()
        inp.close()
        main(data)
    else:
      input_file = open(sys.argv[1])
      data = input_file.read()
      input_file.close()
      main(data)
