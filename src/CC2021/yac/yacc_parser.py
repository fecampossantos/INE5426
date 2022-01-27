# https://ply.readthedocs.io/en/latest/ply.html#yacc

from CC2021.ply import yacc
from CC2021.lexer.lexer import Lexer
from CC2021.yac.loop_control import LoopControl

# instantiating lex for yacc
lexer = Lexer()
lexer.build()
tokens = lexer.tokens

# loop controller
loop_control = LoopControl()


# temporary vars
TEMP_ALLOC = []
TEMP_DEALLOC = []

# label creator count
LABEL_N = 0


def get_temp_var():
    if len(TEMP_DEALLOC) > 1:
        var = TEMP_DEALLOC.pop()
        TEMP_ALLOC.append(var)

        return var

    else:
        i = 0
        while True:
            var = f't{i}'
            if var not in TEMP_ALLOC:
                TEMP_ALLOC.append(var)
                return var

            i += 1


def free_temp_var(var):
    TEMP_ALLOC.remove(var)
    TEMP_DEALLOC.append(var)


def new_label():
    global LABEL_N
    lbl = f'LABEL{LABEL_N}'
    LABEL_N += 1

    return lbl

# empty (declared to cover for the char '&', referenced as "empty") - necessary by yacc
def p_empty(p: yacc.YaccProduction):
    """empty :"""
    pass

# add loop label for loop control
def p_add_loop_label(p: yacc.YaccProduction):
    """add_loop_label :"""
    loop_control.set_next_label(new_label())

def p_error(p):
    print('___ERROR___')
# begins grammar declaration

def p_prog_statment(p: yacc.YaccProduction):
    """PROGRAM : STATEMENT
               | FUNCLIST
               | empty
    """
    p[0] = p[1]['code']


def p_funclist_funcdef(p: yacc.YaccProduction):
    """FUNCLIST : FUNCDEF FUNCLIST2"""
    p[0] = {
        'code': p[1]['code'] + p[2]['code']
    }


def p_funclist2_funclist(p: yacc.YaccProduction):
    """FUNCLIST2 : FUNCLIST
                   | empty
    """
    if p[1] is None:
        p[0] = {'code': ''}
    else:
        p[0] = {'code': p[1]['code']}


def p_funcdef(p: yacc.YaccProduction):
    """FUNCDEF : DEF IDENT LPARENTHESES PARAMLIST RPARENTHESES LEFTBRACE STATELIST RIGHTBRACE"""
    next_label = new_label()
    if len(p) < 3:
        p[0] = {'code': ''}

    else:
        p[0] = {
            'code': f'goto {next_label}\n{p[2]}:\n{p[4]["code"]}{p[7]["code"]}\n{next_label}:\n'
        }


def p_paralist_param(p: yacc.YaccProduction):
    """PARAMLIST : TYPE IDENT PARAMLIST2
                 | empty
    """
    if len(p) < 3:
        p[0] = {'code': ''}

    else:
        p[0] = {
            'code': 'from_params ' + p[2] + '\n' + p[3]['code']
        }


def p_paramlist2_paramlist(p: yacc.YaccProduction):
    """PARAMLIST2 : COMMA PARAMLIST
                    | empty
    """
    if len(p) < 3:
        p[0] = {'code': ''}

    else:
        p[0] = {'code': p[2]['code']}


def p_type(p: yacc.YaccProduction):
    """TYPE : INT
                | FLOAT
                | STRING
    """
    p[0] = {'code': p[1]}


def p_statement_vardecl(p: yacc.YaccProduction):
    """STATEMENT : VARDECL SEMICOLON"""
    p[0] = {'code': p[1]['code']}


def p_statement_atrib(p: yacc.YaccProduction):
    """STATEMENT : ATRIBSTAT SEMICOLON"""
    p[0] = {'code': p[1]['code']}


def p_statement_print(p: yacc.YaccProduction):
    """STATEMENT : PRINTSTAT SEMICOLON"""
    p[0] = {'code': p[1]['code']}


def p_statement_read(p: yacc.YaccProduction):
    """STATEMENT : READSTAT SEMICOLON"""
    p[0] = {'code': p[1]['code']}


def p_statement_return(p: yacc.YaccProduction):
    """STATEMENT : RETURNSTAT SEMICOLON"""
    p[0] = {'code': p[1]['code']}


def p_statement_if(p: yacc.YaccProduction):
    """STATEMENT : IFSTAT"""
    p[0] = {
        'code': p[1]['code']
    }
# def p_statement_if(p: yacc.YaccProduction):
#     """STATEMENT : IFSTAT SEMICOLON"""
#     p[0] = {
#         'code': p[1]['code']
#     }


def p_statement_for(p: yacc.YaccProduction):
    """STATEMENT : FORSTAT"""
    p[0] = {
        'code': p[1]['code']
    }

# def p_statement_for(p: yacc.YaccProduction):
#     """STATEMENT : FORSTAT SEMICOLON"""
#     p[0] = {
#         'code': p[1]['code']
#     }


def p_statement_statelist(p: yacc.YaccProduction):
    """STATEMENT : LEFTBRACE STATELIST RIGHTBRACE """
    p[0] = {
        'code': p[2]['code']
    }


def p_statement_break(p: yacc.YaccProduction):
    """STATEMENT : BREAK SEMICOLON"""
    p[0] = {'code': f'goto {loop_control.get_next_label()}\n'}


def p_statement_end(p: yacc.YaccProduction):
    """STATEMENT : SEMICOLON"""
    p[0] = {'code': ''}


def p_vardecl(p: yacc.YaccProduction):
    """VARDECL : TYPE IDENT ARRAY_OPT"""
    p[0] = {
        'code': f'{p[1]["code"]} {p[2]}{p[3]["code"]}\n'
    }


def p_opt_vector(p: yacc.YaccProduction):
    """ARRAY_OPT : LBRACKET INTCONSTANT RBRACKET ARRAY_OPT
                  | empty
    """
    if len(p) < 3:
        p[0] = {'code': ''}
    else:
        p[0] = {
            'code': '[' + str(p[2]) + ']' + p[4]['code']
        }


def p_atribstat(p: yacc.YaccProduction):
    """ATRIBSTAT : LVALUE ASSIGN RIGHT_ATRIB"""
    p[0] = {
        'code': p[3]['code'] + p[1]['code'] + f'{p[1]["var_name"]} = {p[3]["temp_var"]}\n'
    }


def p_atribright_func_or_exp(p: yacc.YaccProduction):
    """RIGHT_ATRIB : EXPR_OR_FCALL"""
    p[0] = p[1]


def p_atribright_alloc(p: yacc.YaccProduction):
    """RIGHT_ATRIB : ALLOCEXPRESSION"""
    p[0] = p[1]


def p_funccall_or_exp_minus(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : MINUS FACTOR OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR
                              | PLUS FACTOR OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    previous_code = ''
    curr_left_value = f'{p[1]} {p[2]["temp_var"]}'
    for i in range(3, 6):
        if p[i]['code']:
            temp_var = get_temp_var()
            previous_code += p[i]['code']
            previous_code += f'{temp_var} = {curr_left_value} {p[i]["operation"]} {p[i]["temp_var"]}\n'

            curr_left_value = temp_var

    p[0] = {
        'temp_var': curr_left_value,
        'code': previous_code
    }


def p_funccall_or_exp_string(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : INTCONSTANT OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR
                              | STRINGCONSTANT OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR
                              | FLOATCONSTANT OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""

    curr_left_value = get_temp_var()
    previous_code = f'{curr_left_value} = {p[1]}\n'
    for i in range(2, 5):
        if p[i]['code']:
            temp_var = get_temp_var()
            previous_code += p[i]['code']
            previous_code += f'{temp_var} = {curr_left_value} {p[i]["operation"]} {p[i]["temp_var"]}\n'

            curr_left_value = temp_var

    p[0] = {
        'temp_var': curr_left_value,
        'code': previous_code
    }


def p_funccall_or_exp_null(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : NULL OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    previous_code = ''
    curr_left_value = p[1]
    for i in range(2, 5):
        if p[i]['code']:
            temp_var = get_temp_var()
            previous_code += p[i]['code']
            previous_code += f'{temp_var} = {curr_left_value} {p[i]["operation"]} {p[i]["temp_var"]}\n'

            curr_left_value = temp_var

    p[0] = {
        'temp_var': curr_left_value,
        'code': previous_code
    }


def p_funccall_or_exp_parentesis(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : LPARENTHESES NUMEXPRESSION RPARENTHESES OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    previous_code = p[2]['code']
    curr_left_value = p[2]['temp_var']
    for i in range(4, 7):
        if p[i]['code']:
            temp_var = get_temp_var()
            previous_code += p[i]['code']
            previous_code += f'{temp_var} = {curr_left_value} {p[i]["operation"]} {p[i]["temp_var"]}\n'

            curr_left_value = temp_var

    p[0] = {
        'temp_var': curr_left_value,
        'code': previous_code
    }


def p_funccall_or_exp_ident(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : IDENT AFTER_IDENT"""
    if p[2]['funcall']:
        p[0] = {
            'code': p[2]['code'],
            'temp_var': p[2]['temp_var'],
        }

    elif p[2].get('operation', False):
        temp_var = get_temp_var()
        op = p[2]['operation']
        right_temp = p[2]['temp_var']
        code = f'{temp_var} = {p[1]} {op} {right_temp}\n'
        p[0] = {
            'code': p[2]['code'] + code,
            'temp_var': temp_var
        }
    else:
        p[0] = {
            'code': '',
            'temp_var': p[1]
        }


def p_follow_ident_alloc(p: yacc.YaccProduction):
    """AFTER_IDENT : OPT_ALLOC_EXPR OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    index_access = ''

    if p[1]['code']:
        index_access = p[1]['code']

    for i in range(2, 5):
        if p[i]['code']:
            p[0] = {
                'code': p[i]['code'],
                'temp_var': p[i]['temp_var'],
                'operation': p[i]['operation'],
                'index_access': index_access,
                'funcall': False
            }
            break

    else:
        p[0] = {
            'code': '',
            'funcall': False
        }


def p_follow_ident_parentesis(p: yacc.YaccProduction):
    """AFTER_IDENT : LPARENTHESES PARAMLISTCALL RPARENTHESES"""
    func_ident = p[-1]
    num_params = p[2]['num_params']
    temp_var = get_temp_var()
    code = f'{temp_var} = call {func_ident}, {num_params}\n'
    p[0] = {
        'code': p[2]['code'] + code,
        'temp_var': temp_var,
        'funcall': True
    }


def p_paramlistcall_ident(p: yacc.YaccProduction):
    """PARAMLISTCALL : IDENT PARAMLISTCALL2
                     | empty
    """
    if len(p) < 3:
        p[0] = {'code': '', 'num_params': 0}
    else:
        p[0] = {
            'code': 'param ' + p[1] + '\n' + p[2]['code'],
            'num_params': p[2]['num_params']
        }


def p_paramlistcallaux(p: yacc.YaccProduction):
    """PARAMLISTCALL2 : COMMA PARAMLISTCALL
                        | empty
    """
    if len(p) < 3:
        p[0] = {'code': '', 'num_params': 0}
    else:
        p[0] = {
            'code': p[2]['code'],
            'num_params': p[2]['num_params'] + 1
        }


def p_printstat(p: yacc.YaccProduction):
    """PRINTSTAT : PRINT EXPRESSION"""
    p[0] = {'code': p[2]['code'] + f'print {p[2]["temp_var"]}\n'}


def p_readstat(p: yacc.YaccProduction):
    """READSTAT : READ LVALUE"""
    p[0] = {'code': 'read ' + p[2]['var_name']}


# def p_returnstat(p: yacc.YaccProduction):
#     """RETURNSTAT : RETURN"""
#     p[0] = {'code': f'{p[1]}\n'}

def p_returnstat(p: yacc.YaccProduction):
    """RETURNSTAT : RETURN OPT_LVALUE"""
    p[0] = {'code': 'return ' + p[2]['var_name']}

def p_opt_lvalue(p: yacc.YaccProduction):
    """OPT_LVALUE   : LVALUE
                    | empty"""
    if p[1]:
        p[0] = {'code': p[1]['code']}
    else:
        p[0] = {'code': ''}

def p_ifstat(p: yacc.YaccProduction):
    """IFSTAT : IF LPARENTHESES EXPRESSION RPARENTHESES LEFTBRACE STATELIST RIGHTBRACE ELSESTAT"""
    cond_temp_var = p[3]['temp_var']
    next_label = new_label()

    else_start_label = p[8].get('start_label', None)
    cond_false_next_label = else_start_label if else_start_label else next_label

    jump_over_else = f'goto {next_label}\n' if else_start_label is not None else ''

    code = p[3]['code'] + f"if False {cond_temp_var} goto {cond_false_next_label}\n" + \
        p[6]['code'] + jump_over_else + p[8]['code'] + next_label + ':\n'

    p[0] = {
        'code': code
    }


def p_opt_else(p: yacc.YaccProduction):
    """ELSESTAT : ELSE LEFTBRACE STATELIST RIGHTBRACE
                | empty
    """
    if len(p) < 3:
        p[0] = {
            'code': "",
        }
    else:
        start_label = new_label()
        p[0] = {
            'code': start_label + ':\n' + p[3]['code'],
            'start_label': start_label
        }


def p_forstat(p: yacc.YaccProduction):
    """FORSTAT : add_loop_label FOR LPARENTHESES ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RPARENTHESES LEFTBRACE STATELIST RIGHTBRACE"""
    start_label = new_label()
    next_label = loop_control.get_next_label()
    cond_code_body = p[6]['code']
    cond_temp_var = p[6]['temp_var']

    first_atrib_code = p[4]['code'] + '\n'
    cond_code = f'if False {cond_temp_var} goto {next_label}\n'
    body_code = p[11]['code']
    increment_code = p[8]['code']
    go_to_start_code = f'goto {start_label}\n'

    code = first_atrib_code +\
        start_label + ':\n' +\
        cond_code_body +\
        cond_code +\
        body_code +\
        increment_code +\
        go_to_start_code +\
        next_label + ':\n'

    p[0] = {
        'code': code
    }


def p_statelist(p: yacc.YaccProduction):
    """STATELIST : STATEMENT OPT_STATELIST"""
    p[0] = {
        'code': p[1]['code'] + p[2]['code']
    }


def p_opt_statelist(p: yacc.YaccProduction):
    """OPT_STATELIST : STATELIST
                     | empty
    """
    if p[1]:
        p[0] = {'code': p[1]['code']}
    else:
        p[0] = {'code': ''}


def p_allocexp(p: yacc.YaccProduction):
    """ALLOCEXPRESSION : NEW TYPE LBRACKET NUMEXPRESSION RBRACKET OPT_ALLOC_EXPR"""
    temp_var = get_temp_var()

    p[0] = {
        'temp_var': temp_var,
        'code': p[6]['code'] + f'{temp_var} = new {p[2]["code"]}{p[6]["alloc_brackets"]}\n',
    }


def p_opt_allocexp(p: yacc.YaccProduction):
    """OPT_ALLOC_EXPR : LBRACKET NUMEXPRESSION RBRACKET OPT_ALLOC_EXPR
                        | empty
    """
    if len(p) < 3:
        p[0] = {
            'code': '',
            'alloc_brackets': ''
        }
    else:
        p[0] = {
            'code': p[2]['code'] + p[4]['code'],
            'alloc_brackets': f'[{p[2]["temp_var"]}]' + p[4]['alloc_brackets']
        }


def p_expression(p: yacc.YaccProduction):
    """EXPRESSION : NUMEXPRESSION OPT_CMP_EXPR"""
    opt_code = p[2]['code']
    result_temp_var = get_temp_var()

    code = f'{result_temp_var} = {p[1]["temp_var"]}'

    if opt_code:
        operator = p[2]['operation']
        code += f' {operator} {p[2]["temp_var"]}\n'
    else:
        code += '\n'

    p[0] = {
        'temp_var': result_temp_var,
        'code': p[2]['code'] + p[1]['code'] + code
    }


def p_opt_rel_op_num_expr(p: yacc.YaccProduction):
    """OPT_CMP_EXPR : CMP NUMEXPRESSION
                           | empty
    """
    if len(p) < 3:
        p[0] = {'code': ''}

    else:
        p[0] = {
            'temp_var': p[2]['temp_var'],
            'operation': p[1]['code'],
            'code': p[2]['code'],
        }


def p_relop_lt(p: yacc.YaccProduction):
    """CMP : LT"""
    p[0] = {'code': '<'}


def p_relop_gt(p: yacc.YaccProduction):
    """CMP : GT"""
    p[0] = {'code': '>'}


def p_relop_lte(p: yacc.YaccProduction):
    """CMP : LE"""
    p[0] = {'code': '<='}


def p_relop_gte(p: yacc.YaccProduction):
    """CMP : GE"""
    p[0] = {'code': '>='}


def p_relop_eq(p: yacc.YaccProduction):
    """CMP : EQUALS"""
    p[0] = {'code': '=='}


def p_relop_neq(p: yacc.YaccProduction):
    """CMP : DIFFERENT"""
    p[0] = {'code': '!='}


def p_numexp(p: yacc.YaccProduction):
    """NUMEXPRESSION : TERM OPT_ARITHM"""
    if not p[2]['code']:
        p[0] = p[1]

    else:
        temp_var = get_temp_var()
        left_temp = p[1]['temp_var']
        op = p[2]['operation']
        right_temp = p[2]['temp_var']
        p[0] = {
            'code': p[2]['code'] + p[1]['code'] + f'{temp_var} = {left_temp} {op} {right_temp}\n',
            'temp_var': temp_var
        }


def p_rec_plus_minus(p: yacc.YaccProduction):
    """OPT_ARITHM : ARITHM TERM OPT_ARITHM
                           | empty
    """
    if len(p) < 3:
        p[0] = {'code': ''}

    elif p[3]['code']:
        temp_var = get_temp_var()
        left_temp = p[2]['temp_var']
        op = p[3]['operation']
        right_temp = p[3]['temp_var']

        p[0] = {
            'code': p[3]['code'] + p[2]['code'] + f'{temp_var} = {left_temp} {op} {right_temp}\n',
            'temp_var': temp_var,
            'operation': p[1]['code']
        }

    else:
        p[0] = {
            'code': p[2]['code'],
            'temp_var': p[2]['temp_var'],
            'operation': p[1]['code']
        }


def p_arithm_operators(p: yacc.YaccProduction):
    """ARITHM : PLUS
                     | MINUS
    """
    p[0] = {'code': p[1]}


def p_unary_operators(p: yacc.YaccProduction):
    """OPT_UNARY : TIMES
                    | MOD
                    | DIVIDE """
    p[0] = {'code': p[1]}


def p_term_unary_exp(p: yacc.YaccProduction):
    """TERM : UNARYEXPR OPT_UNARY_TERM"""
    if p[2]['code']:
        temp_var = get_temp_var()
        left_temp = p[1]['temp_var']
        op = p[2]['operation']
        right_temp = p[2]['temp_var']
        p[0] = {
            'code': p[1]['code'] + f'{temp_var} = {left_temp} {op} {right_temp}\n',
            'temp_var': temp_var
        }

    else:
        p[0] = p[1]


def p_rec_unaryexp_op(p: yacc.YaccProduction):
    """OPT_UNARY_TERM : OPT_UNARY TERM
                     | empty
    """
    if len(p) < 3:
        p[0] = {'code': ''}

    else:
        p[0] = {
            'code': p[2]['code'],
            'temp_var': p[2]['temp_var'],
            'operation': p[1]['code']
        }


def p_rec_unaryexp_plusminus(p: yacc.YaccProduction):
    """UNARYEXPR : ARITHM FACTOR"""
    p[0] = {
        'code': p[2]['code'] + f'{p[1]["code"]}{p[2]["code"]}\n',
        'temp_var': p[2]['temp_var']
    }


def p_rec_unaryexp_factor(p: yacc.YaccProduction):
    """UNARYEXPR : FACTOR"""
    p[0] = p[1]


def p_factor_const(p: yacc.YaccProduction):
    """FACTOR : INTCONSTANT
              | FLOATCONSTANT
              | STRINGCONSTANT
              | NULL"""
    temp_var = get_temp_var()
    p[0] = {
        'code': f'{temp_var} = {p[1]}\n',
        'temp_var': temp_var
    }


def p_factor_lvalue(p: yacc.YaccProduction):
    """FACTOR : LVALUE"""
    p[0] = {
        'code': f'{p[1]["temp_var"]} = {p[1]["var_name"]}\n',
        'temp_var': p[1]['temp_var']
    }


def p_factor_expr(p: yacc.YaccProduction):
    """FACTOR : LPARENTHESES NUMEXPRESSION RPARENTHESES"""
    p[0] = p[2]


def p_lvalue_ident(p: yacc.YaccProduction):
    """LVALUE : IDENT OPT_ALLOC_EXPR"""
    temp_var = get_temp_var()
    p[0] = {
        'code': p[2]['code'],
        'temp_var': temp_var,
        'var_name': f'{p[1]}{p[2]["alloc_brackets"]}'
    }


yac_parser = yacc.yacc(start='PROGRAM', check_recursion=False)


def generate_code_from_source(text: str):
    # return _parser.parse(text, lexer=lexer, debug=True)
    return yac_parser.parse(text, lexer=lexer)
