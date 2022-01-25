import os
from collections import deque
from typing import List, Tuple, Optional

from CC2021.ply.lex import LexToken
from CC2021.LLC.proc import Proc


_START_SYMBOL = 'A'
_EMPTY_SYMBOL = '&'
_END_SYMBOL = '$'

_MAP = {
    'DEF': 'def',
    'IF': 'if',
    'FOR': 'for',
    'ELSE': 'else',
    'NEW': 'new',
    'INT': 'int',
    'FLOAT': 'float',
    'STRING': 'string',
    'BREAK': 'break',
    'READ': 'read',
    'PRINT': 'print',
    'RETURN': 'return',
    'LEFTBRACE': '{',
    'RIGHTBRACE': '}',
    'LPARENTHESES': '(',
    'RPARENTHESES': ')',
    'LBRACKET': '[',
    'RBRACKET': ']',
    'GT': '>',
    'LT': '<',
    'GE': '>=',
    'LE': '<=',
    'EQUALS': '==',
    'DIFFERENT': '!=',
    'PLUS': '+',
    'MINUS': '-',
    'TIMES': '*',
    'DIVIDE': '/',
    'MOD': '%',
    'SEMICOLON': ';',
    'COMMA': ',',
    'NULL': 'null',
    'ASSIGN': '=',
    'IDENT': 'ident',
    'FLOATCONSTANT': 'float_constant',
    'INTCONSTANT': 'int_constant',
    'STRINGCONSTANT': 'string_constant',
    'STACK_TOK': '$'
}

STACK_TOKEN = LexToken()
STACK_TOKEN.type = 'STACK_TOK'

class Parser:
  def __init__(self):
    path = os.path.join(os.path.dirname(__file__), '..','..','utils','grammar','cc2021.grammar')
    proc = Proc()

    proc.read_llc(path)

    self.llc = proc.llc
    self.start_symbol = proc.llc.start_s
    self.empty_symbol = _EMPTY_SYMBOL
    self.table = proc.create_table()

  def parse(self, tokens):
    stack = deque()

    stack.append(_END_SYMBOL)     # stack begins with end stack symbol
    stack.append(self.start_symbol)   # and then the starting symbol

    for tk in tokens  + [STACK_TOKEN]:
      mapped_token = _MAP[tk.type]

      while True:
        # if the mapped token is the same as the last entrie (top) on the stack, pop
        if mapped_token == stack[-1]:
          stack.pop()
          break

        # if not, applies production
        prod = self.table.get_prod(stack[-1], mapped_token)
        # if returns None, then it is a syntatic error
        if prod is None:
          return(False, tk)

        # if it got here, production was applied
        # removes the top symbol
        stack.pop()
        # and adds those that the production creates
        for symbol in reversed(prod.body):
          if symbol != self.empty_symbol:
            stack.append(symbol)
    
    # if the stack is not empty, it is not correct
    if len(stack) > 1:
      return (False, tk)
    # else, everything is correct

    return (True, None)

parser = Parser()