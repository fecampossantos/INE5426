import uuid
from typing import List, Set, Dict, Optional, Union
from CC2021.exceptions import InvalidIdentifierDeclarationException

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

# structures for semantic analysis

class Scope:
  def __init__(self, previousScope = None, isLoop = False):
    self.table = []
    self.innerScopes = []

    self.previousScope = previousScope
    self.isLoop = isLoop
  
  def addInnerScope(self, scopeToAdd):
    self.innerScopes.append(scopeToAdd)
  
  def doesVarAlreadyExists(self, identificator):
    for l in self.table:
      if l.label == identificator:
        return True, l.line
    
    return False, -1
  
  def addToScopeTable(self, entryToAdd):
    exists, line = self.doesVarAlreadyExists(entryToAdd.label)

    if exists:
      raise InvalidIdentifierDeclarationException(line)
    
    self.table.append(entryToAdd)
    # return 1 indicating succes, and empty string
    return 1, ''
  
  def getAsJSON(self):
    return {
      'table': [item.getAsJSON() for item in self.table],
      'innerScopes':[scope.getAsJSON() for scope in self.innerScopes]
    }

class ScopeList:
  def __init__(self):
    self.list = []
  def __len__(self):
    return len(self.list)

  def getLastScope(self):
    return self.list.pop()

  def appendScope(self, scope):
    self.list.append(scope)
  
  def getLastScopeOrNoneIfEmpty(self):
    if self.list:
      return self.list[-1]
    else:
      return None
  
  
class Node:
  def __init__(self, value = None, type = None, left = None, right = None):
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
  
  def set_left(self, left):
    self.left = left

  def set_right(self, right):
    self.right = right
  
  def getAsJSON(self):
    left = None
    right = None

    if self.left is not None:
      left = self.left.getAsJSON()
    if self.right is not None:
      right = self.right.getAsJSON()
    
    return {
      'vaue': self.value,
      'left': left,
      'right': right
    }

class ScopeEntry:
  def __init__(self, label, type, size, line):
      # nome da var, func, etc
      self.label: str = label
      # tipo (function, list, ...)
      self.type: str = type
      # se for lista, qual o tamanho dela
      self.size: List[int] = size
      self.line: int = line
    
  def get_label(self):
    return self.label
  def get_type(self):
    return self.type
  def get_size(self):
    return self.size
  def get_line(self):
    return self.line
  def set_label(self, newLabel):
    self.label = newLabel
  def set_type(self, newType):
    self.type = newType
  def set_size(self, newSize):
    self.size = newSize
  def set_line(self, newLine):
    self.line = newLine

  def getAsJSON(self):
    return {
      'label' : self.label,
      'type' : self.type,
      'size' : self.size,
      'line' : self.line
    }
