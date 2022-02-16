# analisador semantico
from CC2021.ply import yacc
from CC2021.lexer.lexer import Lexer
from src.CC2021.strucs import Scope, ScopeList

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


