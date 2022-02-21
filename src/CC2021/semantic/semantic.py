# analisador semantico
from CC2021.ply import yacc
from CC2021.lexer.lexer import Lexer
from CC2021.strucs import Scope, ScopeList, Node, ScopeEntry
from utils.utils import validOperationResults

# usado pra controlar os escopos de codigo
scope_list = ScopeList()
numeric_expressions = []

# instanciando yacc
lexer = Lexer()
lexer.build()
tokens = lexer.tokens

def addNewScopeToList(isLoop):
    top_scope = scope_list.getLastScopeOrNoneIfEmpty()
    new_scope = Scope(top_scope, isLoop)

    if top_scope: #if scope is not None
        top_scope.addInnerScope(new_scope)
    
    scope_list.appendScope(new_scope)

def getTypeOfVariable(identificator, lineNumber):
    sp = scope_list.getLastScopeOrNoneIfEmpty()

    while True:
        for l in sp.table:
            if l.label == identificator:
                # found variable we were looking for
                # returns 1 indicating succes and type
                return 1, l.type
        
        # if it has not been found in that scope, check for the parents scope
        sp = sp.previousScope

        if sp is None:
            # parent scope does not exists
            break

    # if has not been found until here, return error
    # that the variable has not been declared
    return -1, 'variavel nao foi declarada'

def checkIfIsValid(leftType, rightType, op, lineNumber):
    opResult = validOperationResults.get((leftType, op, rightType), None)

    if opResult is None:
        return -1, 'Essa operacao nao e valida'
    
    return 1, opResult



###########################################################
#                    yacc declarations                    #
###########################################################


def p_error(p):
    print('error!')

def p_empty(p: yacc.YaccProduction):
    """empty :"""
    pass


# production that will create new scope (not loop)
def p_newScope(p: yacc.YaccProduction):
    """new_scope :"""
    addNewScopeToList(False)

# production that will create new loop scope
def p_newLoopScope(p: yacc.YaccProduction):
    """new_loopScope :"""
    addNewScopeToList(True)

# productions to instantiate the grammar


def p_prog_statment(p: yacc.YaccProduction):
    """PROGRAM : new_scope STATEMENT
               | new_scope FUNCLIST
               | empty
    """
    global_scope = scope_list.getLastScope()
    # p[0] = {
    #     'scopes': global_scope.as_json(),
    #     'numeric_expressions': num_expressions_as_json()
    # }

    # Grants that all all tables where used and popper correctly
    assert len(scope_list) == 0  # nosec


def p_funclist_funcdef(p: yacc.YaccProduction):
    """FUNCLIST : FUNCDEF FUNCLIST2"""
    pass


def p_FUNCLIST2_funclist(p: yacc.YaccProduction):
    """FUNCLIST2 : FUNCLIST
                   | empty
    """
    pass


def p_funcdef(p: yacc.YaccProduction):
    """FUNCDEF : DEF IDENT new_scope LPARENTHESES PARAMLIST RPARENTHESES LEFTBRACE STATELIST RIGHTBRACE"""
    # Go back to upper scope
    scope_list.getLastScope()

    # Add function declaration to current scope
    scope = scope_list.getLastScopeOrNoneIfEmpty()
    scopeEntry = ScopeEntry(p[2], 'function', [], p.lineno(2))
    scope.addToScopeTable(scopeEntry)


def p_paralist_param(p: yacc.YaccProduction):
    """PARAMLIST : TYPE IDENT PARAMLIST2
                 | empty
    """
    if len(p) > 2:
        scope = scope_list.getLastScopeOrNoneIfEmpty()
        scopeEntry = ScopeEntry(p[2], p[1], [], p.lineno(2))
        scope.addToScopeTable(scopeEntry)


def p_paramlistaux_paramlist(p: yacc.YaccProduction):
    """PARAMLIST2 : COMMA PARAMLIST
                    | empty
    """
    pass


def p_datatype(p: yacc.YaccProduction):
    """TYPE : INT
                | FLOAT
                | STRING
    """
    p[0] = p[1]


def p_statement_vardecl(p: yacc.YaccProduction):
    """STATEMENT : VARDECL SEMICOLON"""
    pass


def p_statement_atrib(p: yacc.YaccProduction):
    """STATEMENT : ATRIBSTAT SEMICOLON"""
    pass


def p_statement_print(p: yacc.YaccProduction):
    """STATEMENT : PRINTSTAT SEMICOLON"""
    pass


def p_statement_read(p: yacc.YaccProduction):
    """STATEMENT : READSTAT SEMICOLON"""
    pass


def p_statement_return(p: yacc.YaccProduction):
    """STATEMENT : RETURNSTAT SEMICOLON"""
    pass


def p_statement_if(p: yacc.YaccProduction):
    """STATEMENT : IFSTAT"""
    pass


def p_statement_for(p: yacc.YaccProduction):
    """STATEMENT : FORSTAT"""
    pass


def p_statement_statelist(p: yacc.YaccProduction):
    """STATEMENT : new_scope LEFTBRACE STATELIST RIGHTBRACE """
    # Return to previous scope
    scope_list.getLastScope()


def p_statement_break(p: yacc.YaccProduction):
    """STATEMENT : BREAK SEMICOLON"""
    # If is not inside loop scope, consider semantic failure
    current_scope = scope_list.getLastScopeOrNoneIfEmpty()

    # Go into upper scopes trying to find a for loop
    while True:
        if current_scope.is_loop:
            break

        current_scope = current_scope.upper_scope

        if current_scope is None:
            raise BreakWithoutLoopError(p.lineno(2))


def p_statement_end(p: yacc.YaccProduction):
    """STATEMENT : SEMICOLON"""
    pass


def p_vardecl(p: yacc.YaccProduction):
    """VARDECL : TYPE IDENT ARRAY_OPT"""
    scopeEntry = ScopeEntry(p[2], p[1], p[3], p.lineno(2))
    scope = scope_list.getLastScopeOrNoneIfEmpty()
    scope.addToScopeTable(scopeEntry)


def p_opt_vector(p: yacc.YaccProduction):
    """ARRAY_OPT : LBRACKET INTCONSTANT RBRACKET ARRAY_OPT
                  | empty
    """
    if len(p) > 2:
        p[0] = [p[2], *p[4]]
    else:
        p[0] = []


def p_atribstat(p: yacc.YaccProduction):
    """ATRIBSTAT : LVALUE ASSIGN RIGHT_ATRIB"""
    pass


def p_atribright_func_or_exp(p: yacc.YaccProduction):
    """RIGHT_ATRIB : EXPR_OR_FCALL"""
    pass


def p_atribright_alloc(p: yacc.YaccProduction):
    """RIGHT_ATRIB : ALLOCEXPRESSION"""
    pass


def p_funccall_or_exp_plus(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : PLUS FACTOR OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR
                              | MINUS FACTOR OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    right_node = p[2]['node']
    if p[1] == '-':
        right_node.value *= -1

    if p[3]:
        result_type = checkIfIsValid(p[3]['node'],
                                 right_node,
                                 p[3]['operation'],
                                 p.lineno(1))
        right_node = Node(p[3]['node'],
                          right_node,
                          p[3]['operation'],
                          result_type)

    if p[4]:
        result_type = checkIfIsValid(p[4]['node'],
                                 right_node,
                                 p[4]['operation'],
                                 p.lineno(1))
        right_node = Node(p[4]['node'],
                          right_node,
                          p[4]['operation'],
                          result_type)

    numeric_expressions.append(right_node)


def p_funccal_or_exp_int_const(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : INTCONSTANT OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    node = Node(None, None, p[1], 'int')

    if p[2]:
        result_type = checkIfIsValid(node,
                                 p[2]['node'],
                                 p[2]['operation'],
                                 p.lineno(2))
        node = Node(node, p[2]['node'], p[2]['operation'], result_type)

    if p[3]:
        result_type = checkIfIsValid(node,
                                 p[3]['node'],
                                 p[3]['operation'],
                                 p.lineno(2))
        node = Node(node, p[3]['node'], p[3]['operation'], result_type)

    p[0] = {
        'node': node
    }

    numeric_expressions.append((node, p.lineno(2)))


def p_funccal_or_exp_float_const(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : FLOATCONSTANT OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    node = Node(None, None, p[1], 'float')

    if p[2]:
        result_type = checkIfIsValid(node,
                                 p[2]['node'],
                                 p[2]['operation'],
                                 p.lineno(2))
        node = Node(node, p[2]['node'], p[2]['operation'], result_type)

    if p[3]:
        result_type = checkIfIsValid(node,
                                 p[3]['node'],
                                 p[3]['operation'],
                                 p.lineno(2))
        node = Node(node, p[3]['node'], p[3]['operation'], result_type)

    p[0] = {
        'node': node
    }

    numeric_expressions.append((node, p.lineno(2)))


def p_funccal_or_exp_string_const(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : STRINGCONSTANT OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    node = Node(None, None, p[1], 'string')

    if p[2]:
        result_type = checkIfIsValid(node,
                                 p[2]['node'],
                                 p[2]['operation'],
                                 p.lineno(1))
        node = Node(node, p[2]['node'], p[2]['operation'], result_type)

    if p[3]:
        result_type = checkIfIsValid(node,
                                 p[3]['node'],
                                 p[3]['operation'],
                                 p.lineno(1))
        node = Node(node, p[3]['node'], p[3]['operation'], result_type)

    p[0] = {
        'node': node
    }

    numeric_expressions.append((node, p.lineno(1)))


def p_funccall_or_exp_null(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : NULL OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    pass


def p_funccall_or_exp_parentesis(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : LPARENTHESES NUMEXPRESSION RPARENTHESES OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    node = p[2]['node']

    if p[4]:
        result_type = checkIfIsValid(node,
                                 p[4]['node'],
                                 p[4]['operation'],
                                 p.lineno(1))
        node = Node(node, p[4]['node'], p[4]['operation'], result_type)

    if p[5]:
        result_type = checkIfIsValid(node,
                                 p[5]['node'],
                                 p[5]['operation'],
                                 p.lineno(1))
        node = Node(node, p[5]['node'], p[5]['operation'], result_type)

    p[0] = {
        'node': node
    }

    numeric_expressions.append((node, p.lineno(1)))


def p_funccall_or_exp_ident(p: yacc.YaccProduction):
    """EXPR_OR_FCALL : IDENT AFTER_IDENT"""
    node = Node(None, None, p[1], getTypeOfVariable(p[1], p.lineno(1)))

    if p[2] is None or p[2]['node'] == None:
        return

    if p[2]:
        node.value += p[2]['vec_access']
        result_type = checkIfIsValid(node,
                                 p[2]['node'],
                                 p[2]['operation'],
                                 p.lineno(1))
        node = Node(node, p[2]['node'], p[2]['operation'], result_type)

        numeric_expressions.append((node, p.lineno(1)))


def p_follow_ident_alloc(p: yacc.YaccProduction):
    """AFTER_IDENT : OPT_ALLOC_EXPR OPT_UNARY_TERM OPT_ARITHM OPT_CMP_EXPR"""
    node = None
    operation = ''

    if p[2]:
        node = p[2]['node']
        operation = p[2]['operation']

    if p[3]:
        if node is None:
            node = p[3]['node']
            operation = p[3]['operation']

        else:
            result_type = checkIfIsValid(node,
                                     p[3]['node'],
                                     p[3]['operation'],
                                     p.lineno(0))
            node = Node(node, p[3]['node'], p[3]['operation'], result_type)

    p[0] = {
        'vec_access': p[1],
        'node': node,
        'operation': operation
    }


def p_follow_ident_parentesis(p: yacc.YaccProduction):
    """AFTER_IDENT : LPARENTHESES PARAMLISTCALL RPARENTHESES """
    pass


def p_paramlistcall_ident(p: yacc.YaccProduction):
    """PARAMLISTCALL : IDENT PARAMLISTCALL2
                     | empty
    """
    pass


def p_paramlistcallaux(p: yacc.YaccProduction):
    """PARAMLISTCALL2 : COMMA PARAMLISTCALL
                        | empty
    """
    pass


def p_printstat(p: yacc.YaccProduction):
    """PRINTSTAT : PRINT EXPRESSION"""
    pass


def p_readstat(p: yacc.YaccProduction):
    """READSTAT : READ LVALUE"""
    pass


def p_returnstat(p: yacc.YaccProduction):
    """RETURNSTAT : RETURN OPT_LVALUE"""
    pass

def p_opt_lvalue(p: yacc.YaccProduction):
    """OPT_LVALUE : LVALUE
                    | empty"""
    # p[0] = p[1]
    pass


def p_ifstat(p: yacc.YaccProduction):
    """IFSTAT : IF LPARENTHESES EXPRESSION RPARENTHESES new_scope LEFTBRACE STATELIST RIGHTBRACE ELSESTAT"""
    # Go back to previous scope
    scope_list.getLastScope()


def p_elsestat(p: yacc.YaccProduction):
    """ELSESTAT : ELSE new_scope LEFTBRACE STATELIST RIGHTBRACE
                | empty
    """
    if len(p) > 2:
        # Go back to previous scope
        scope_list.getLastScope()


def p_forstat(p: yacc.YaccProduction):
    """FORSTAT : FOR LPARENTHESES ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RPARENTHESES new_loop_scope LEFTBRACE STATELIST RIGHTBRACE"""
    scope_list.getLastScope()


def p_statelist(p: yacc.YaccProduction):
    """STATELIST : STATEMENT OPT_STATELIST"""
    pass


def p_opt_statelist(p: yacc.YaccProduction):
    """OPT_STATELIST : STATELIST
                     | empty
    """
    pass


def p_allocexp(p: yacc.YaccProduction):
    """ALLOCEXPRESSION : NEW TYPE LBRACKET NUMEXPRESSION RBRACKET OPT_ALLOC_EXPR"""
    numeric_expressions.append((p[4]['node'], p.lineno(1)))


def p_opt_allocexp(p: yacc.YaccProduction):
    """OPT_ALLOC_EXPR : LBRACKET NUMEXPRESSION RBRACKET OPT_ALLOC_EXPR
                        | empty
    """
    if len(p) < 3:
        p[0] = ''
    else:
        p[0] = '[' + str(p[2]) + ']' + p[4]

        numeric_expressions.append((p[2]['node'], p.lineno(1)))


def p_expression(p: yacc.YaccProduction):
    """EXPRESSION : NUMEXPRESSION OPT_CMP_EXPR"""
    numeric_expressions.append((p[1]['node'], p.lineno(1)))


def p_opt_rel_op_num_expr(p: yacc.YaccProduction):
    """OPT_CMP_EXPR : CMP NUMEXPRESSION
                    | empty
    """
    if len(p) < 3:
        pass

    else:
        numeric_expressions.append((p[2]['node'], p.lineno(1)))


def p_relop_lt(p: yacc.YaccProduction):
    """CMP : LT"""
    pass


def p_relop_gt(p: yacc.YaccProduction):
    """CMP : GT"""
    pass


def p_relop_lte(p: yacc.YaccProduction):
    """CMP : LE"""
    pass


def p_relop_gte(p: yacc.YaccProduction):
    """CMP : GE"""


def p_relop_eq(p: yacc.YaccProduction):
    """CMP : EQUALS"""
    pass


def p_relop_neq(p: yacc.YaccProduction):
    """CMP : DIFFERENT"""
    pass


def p_numexp(p: yacc.YaccProduction):
    """NUMEXPRESSION : TERM OPT_ARITHM"""
    if p[2] is None:
        p[0] = p[1]

    else:
        result_type = checkIfIsValid(p[1]['node'],
                                 p[2]['node'],
                                 p[2]['operation'],
                                 p.lineno(1))
        p[0] = {
            'node': Node(p[1]['node'],
                         p[2]['node'],
                         p[2]['operation'],
                         result_type)
        }


def p_rec_plus_minus(p: yacc.YaccProduction):
    """OPT_ARITHM : ARITHM TERM OPT_ARITHM
                    | empty
    """
    if len(p) < 3:
        # Case empty
        p[0] = None

    elif p[3]:
        # Case there's another recursive operation being made
        result_type = checkIfIsValid(p[2]['node'],
                                 p[3]['node'],
                                 p[3]['operation'],
                                 p.lineno(1))
        p[0] = {
            'node': Node(p[2]['node'], p[3]['node'],
                         p[3]['operation'], result_type),
            'operation': p[1]['operation']
        }
    else:
        # Case there's no more operattions to the right
        p[0] = {
            'node': p[2]['node'],
            'operation': p[1]['operation']
        }


def p_plus(p: yacc.YaccProduction):
    """ARITHM : PLUS
                     | MINUS"""
    p[0] = {'operation': p[1]}


def p_term_unary_exp(p: yacc.YaccProduction):
    """TERM : UNARYEXPR OPT_UNARY_TERM"""
    if p[2]:
        # If there's another operation being made
        result_type = checkIfIsValid(p[1]['node'],
                                 p[2]['node'],
                                 p[2]['operation'],
                                 p.lineno(1))
        p[0] = {
            'node': Node(p[1]['node'], p[2]['node'], p[2]['operation'], result_type),
            'operation': p[2]['operation']
        }

    else:
        # Pass the UNARYEXPR node upwards
        p[0] = {
            'node': p[1]['node']
        }


def p_rec_unaryexp_op(p: yacc.YaccProduction):
    """OPT_UNARY_TERM : OPT_UNARY TERM
                     | empty
    """
    if len(p) < 3:
        # Case empty
        p[0] = None

    else:
        p[0] = {
            'node': p[2]['node'],
            'operation': p[1]['operation']
        }


def p_rec_unaryexp_times(p: yacc.YaccProduction):
    """OPT_UNARY : TIMES
                    | DIVIDE
                    | MOD """
    p[0] = {'operation': p[1]}


def p_rec_unaryexp_plusminus(p: yacc.YaccProduction):
    """UNARYEXPR : ARITHM FACTOR"""
    if p[1]['operation'] == '-':
        p[2]['node'].value *= -1

    p[0] = p[2]


def p_rec_unaryexp_factor(p: yacc.YaccProduction):
    """UNARYEXPR : FACTOR"""
    p[0] = p[1]


def p_factor_int_cte(p: yacc.YaccProduction):
    """FACTOR : INTCONSTANT"""
    p[0] = {'node': Node(None, None, p[1], 'int')}


def p_factor_float_cte(p: yacc.YaccProduction):
    """FACTOR : FLOATCONSTANT"""
    p[0] = {'node': Node(None, None, p[1], 'float')}


def p_factor_string_cte(p: yacc.YaccProduction):
    """FACTOR : STRINGCONSTANT"""
    p[0] = {'node': Node(None, None, p[1], 'string')}


def p_factor_null(p: yacc.YaccProduction):
    """FACTOR : NULL"""
    p[0] = {'node': Node(None, None, None, 'null')}


def p_factor_lvalue(p: yacc.YaccProduction):
    """FACTOR : LVALUE"""
    p[0] = p[1]


def p_factor_expr(p: yacc.YaccProduction):
    """FACTOR : LPARENTHESES NUMEXPRESSION RPARENTHESES"""
    p[0] = p[2]

    numeric_expressions.append((p[2]['node'], p.lineno(1)))


def p_lvalue_ident(p: yacc.YaccProduction):
    """LVALUE : IDENT OPT_ALLOC_EXPR"""
    p[0] = {
        'node': Node(None, None, p[1] + p[2],
                     result_type=getTypeOfVariable(p[1], p.lineno(1)))
    }


_parser = yacc.yacc(start='PROGRAM', check_recursion=False)


def semanticParse(text: str):
    return _parser.parse(text, lexer=lexer)