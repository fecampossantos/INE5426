import sys
# from al import build_lexer, parser
from ply import lex

def build_lexer():
  # Tokens
  tokens = ('INT','FLOAT','STRING','ALLOC','PLUS','MINUS',
  'TIMES','DIVIDE','MOD','EQUAL','DIFFERENT','LT','LE','GT',
  'GE','ASSIGN','COMMA','SEMICOLON','RPARENTHESES',
  'LPARENTHESES','LBRACKET','RBRACKET','RBRACE',
  'LEFTBRACE','DOT','FLOATCONSTANT','INTCONSTANT',
  'STRINGCONSTANT','IDENTATION')

  # Tipos
  t_INT = r'int'
  t_FLOAT = r'float'
  t_STRING = r'string'
  t_ALLOC = r'new'

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

  # float tem que ir antes

  def t_FLOATCONSTANT(t):
    r'[-+]?\d*\.\d+'
    t.value = float(t.value)
    return t

  def t_INTCONSTANT(t):
      # r'[-+]?\d*\.\d+|\d'
      r'\d'
      t.value = int(t.value)
      return t

  def t_STRINGCONSTANT(t):
      r'[a-zA-Z_][a-zA-Z0-9_]*'
      return t

  def t_IDENTATION(t):
    r'\t'
    # pegar dois espaços ou 4 espaços
    return t

  t_ignore = ' \t'

  # ERRO
  def t_error(t):
      print("| Erro léxico em:    '%s'" % t.value[0])
      print("|   -> Linha:        '%s'" % t.lexer.lineno)
      print("|       -> Coluna:   '%s'" % t.lexer.lexpos)
      print()
      t.lexer.skip(1)

  # ------------------------------------------------------------------------------
  # Build the lexer
  lexer = lex.lex()

  return lexer
  # ------------------------------------------------------------------------------


def parser(data, lexer):
  # lexer = build_lexer()
  lexer.input(data)
  while True:
    tok = lexer.token()
    if not tok:
      break
    print(tok)

def main(data):
  lexer = build_lexer()
  parser(data, lexer)


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Por favor, passe o PATH do arquivo como argumento")
  else:
    input_file = open(sys.argv[1])
    data = input_file.read()
    input_file.close()

    main(data)
