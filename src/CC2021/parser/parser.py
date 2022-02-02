import os
from collections import deque

from CC2021.ply.lex import LexToken
from CC2021.LLC.proc import Proc
from utils.utils import STACK_BOTTOM, EMPTY_SYMBOL, _MAP

class Parser:
  def __init__(self):
    llc_path = os.path.join(os.path.dirname(__file__), '..','..','utils','grammar','cc2021.grammar')
    # cria o processador da gramatica
    proc = Proc()
    #cria a gramatica llc a partir do .grammar
    proc.read_llc(llc_path)

    self.llc = proc.llc
    self.start_symbol = proc.llc.start_s
    self.table = proc.create_table()
    self.empty_symbol = EMPTY_SYMBOL

  def parse(self, tokens):
    stack = deque()

    stack.append(STACK_BOTTOM)        # o stack sempre comeca com o simbolo de fundo
    stack.append(self.start_symbol)

    for tk in tokens  + [STACK_TOKEN]:
      mapped_token = _MAP[tk.type]

      while True:
        # se o token mapeado eh o mesmo do topo da stack, remove ele
        if mapped_token == stack[-1]:
          stack.pop()
          break

        # se nao, aplica a producao definida na tabela
        prod = self.table.get_prod(stack[-1], mapped_token)

        # caso um None seja retornado, indicando que nao existe uma
        # producao, significa um erro
        if prod is None:
          print('Erro!')
          print('Token -> %s' % mapped_token)
          print('Topo da stack -> %s' % stack[-1])
          return(False, tk)

        # producao foi aplicada, remove o topo
        stack.pop()
        # e adiciona simbolos gerados pela producao
        for symbol in reversed(prod.body):
          if symbol != self.empty_symbol:
            stack.append(symbol)
    
    # se chega no final com o stack nao-vazio, ocorreu algum erro
    if len(stack) > 1:
      return (False, tk)
    # se nao, tudo certo

    return (True, None)

STACK_TOKEN = LexToken()
STACK_TOKEN.type = 'END_STACK_TOKEN'

parser = Parser()