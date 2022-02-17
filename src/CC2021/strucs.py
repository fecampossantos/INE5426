import uuid
from asyncio.windows_events import NULL
from typing import List, Set, Dict, Optional, Union

class Production:
  head: str
  body: List[str]

  def __init__(self, head, body):
      self.head = head
      self.body = body

  def __eq__(self, p2):
      h_eq = self.head == p2.head
      b_eq = self.body == p2.body
      return h_eq and b_eq
  
  def __str__(self):
    return self.__repr__()
  
  def __repr__(self):
    return f'{self.head} -> ' + ' '.join(self.body)


class LLC:
  start_s: str
  terminals: Set[str]
  non_terminals: Set[str]
  prods: List[Production]

  def __init__(self, symbol_start, terminals, non_terminals, productions):
      self.start_s = symbol_start
      self.terminals = terminals
      self.non_terminals = non_terminals
      self.prods = productions

class TableSyntaticAnalyser:
  def __init__(self, terminals, non_terminals, stack_bottom='$' ):
      columns = terminals | {stack_bottom}
      rows = non_terminals

      self.table = {}

      # initializating table
      for r in rows:
        self.table[r] = {}      
        for c in columns:
          self.table [r][c] = None
  
  def add_prod(self,terminal, non_terminal, prod):
    el = self.table[non_terminal][terminal]

    if el is not None and el != prod:
      print('Error: the cell in the Syntatic Analyser table cannot be created twice')
    
    self.table[non_terminal][terminal] = prod
  
  def get_prod(self, non_terminal, terminal):
    return self.table[non_terminal][terminal]
  
  def get_table(self):
    return self.table

class Node:
  def __init__(self, value = NULL, left = NULL, right = NULL):
      self.value = value
      self.right = right
      self.left = left
      self.id = uuid.uuid4()

  def get_id(self):
    return self.id

  def get_value(self):
    return self.value
  
  def get_left(self):
    return self.left

  def get_right(self):
    return self.right

  def set_value(self, value):
    self.value = value
  
  def gset_left(self, left):
    self.left = left

  def set_right(self, right):
    self.right = right
