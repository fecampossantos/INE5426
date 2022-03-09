###############################################################
#             Construção de Compiladores - INE5426            #
#               Construção de Analisador Léxico               #
#                           2021.2                            #
#                   Eduardo Gutterres [17200439]              #
#                 Felipe de Campos Santos [17200441]          #
#                   Ricardo Giuliani [17203922]               #
###############################################################


import json
import sys
import os
from prettytable import PrettyTable

from CC2021.lexer.lexer import Lexer
from CC2021.parser.parser import parser
from CC2021.semantic.semantic import semantic_parse
from CC2021.semantic.gci import code
from src.CC2021.exceptions import BreakOutsideLoopException, InvalidIdentifierDeclarationException

from utils.printer import print_symbols_table, print_token_list, print_tokens_table


def get_info(lexer):
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

    # lexer.input(data)
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

    token_list, tokens_values, tokens_table, symbols_table = get_info(lexer)
    # print_tokens_table(tokens_table)
    # print_token_list(tokens_values)
    # print_symbols_table(symbols_table)

    passed_parsing, wrong_token = parser.parse(tokens=token_list)

    if not passed_parsing:
        print('Syntatic error on line %s' % wrong_token.lineno)
        print('Token: %s' % wrong_token)
        print('\n')
        print('\n')
    else:
      print('Syntatic Analysis succesfull! \n')
    
    print('Starting semantic analysis -->')

    try:
        semantic_rslt = semantic_parse(data)
        # print(semantic_rslt['scope_list'])
        with open('semantic_analysis.json', 'w') as f:
            json.dump(semantic_rslt['scope_list'], f, indent=2, sort_keys=False)

    except BreakOutsideLoopException as e:
        print("Caught break ouside loop at line " + e)
    except InvalidIdentifierDeclarationException as e:
        print("Caught invalid identifier declaration inside scope at line " + e)

    print('Análise Semântica exportada para o arquivo semantic_analysis.json')

    intermediary_code = code(data)

   
    with open('intermediary_code.txt', 'w') as f:
        f.write(intermediary_code)

    print('Código Intermediário exportado para o arquivo intermediary_code.txt')

    return


if __name__ == '__main__':
    args = sys.argv[1]

    if(args == 'all'):
      paths = [
        'src/examples/exemplo1.lcc',
        'src/examples/exemplo2.lcc',
        # 'src/examples/exemplo1-professor.lcc',
        'src/examples/exemplo2-professor.lcc',
        'src/examples/prog1.lcc',
        'src/examples/utils3.lcc',
        'src/examples/utils.lcc',
        'src/examples/utils2.lcc',
        'src/examples/math.lcc',
        ## generates error
        'src/examples/utils_withError_noSemicolon_line10.lcc',
        'src/examples/utils_withError_valueAtribuiton_line2.lcc'
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
