from dataclasses import dataclass
from typing import Any, List, Set, Dict, Optional, Union
import time

@dataclass
class Production:
  head: str
  body: List[str]

  def __eq__(self, p2):
      h_eq = self.head == p2.head
      b_eq = self.body == p2.body
      return h_eq and b_eq
  
  def __str__(self):
    return self.__repr__()
  
  def __repr__(self):
    return f'{self.head} -> ' + ' '.join(self.body)

@dataclass
class LLC:
  start_s: str
  terminals: Set[str]
  non_terminals: Set[str]
  prods: List[Production]

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
    print('adding production to table')
    print('non terminal: %s' % non_terminal)
    print('terminal: %s' % terminal)
    print('production: %s' % prod)
    print('elemtn: %s' % el)

    if el is not None and el != prod:
      print('Error: the cell in the Syntatic Analyser table cannot be created twice')
    
    self.table[non_terminal][terminal] = prod
  
  def get_prod(self, non_terminal, terminal):
    return self.table[non_terminal][terminal]
  
  def get_table(self):
    return self.table
  

@dataclass
class SymbolRow:
  name: str
  index_token: int
  type: str
  line_declared: int
  lines_referenced: List[int]

@dataclass
class TableEntry:
    identifier_label: str
    datatype: str
    dimension: List[int]
    line: int

    def as_json(self):
        return {
            'identifier_label': self.identifier_label,
            'datatype': self.datatype,
            'dimension': self.dimension,
            'line': self.line
        }


class Scope:
    def __init__(self, upper_scope=None, is_loop: bool = False):
        self.table: List[TableEntry] = []

        self.upper_scope = upper_scope

        self.inner_scopes = []

        self.is_loop = is_loop

    def add_entry(self, entry: TableEntry):
        is_present, line_declared = self.var_already_present(entry.identifier_label)
        if is_present:
          print('This variable has already been declared before on line %s' % line_declared)
        self.table.append(entry)

    def var_already_present(self, ident):
        for entry in self.table:
            if entry.identifier_label == ident:
                return True, entry.line

        return False, 0

    def add_inner(self, scope):
        self.inner_scopes.append(scope)

    def __str__(self):
        return '\n'.join([
            str(entry)
            for entry in self.table
        ]) + '\n'

    def as_json(self) -> Dict:
        return {
            'table': [
                entry.as_json() for entry in self.table
            ],
            'inner_scopes': [scope.as_json() for scope in self.inner_scopes]
        }


class ScopeStack:
    def __init__(self):
        self.stack = []

    def pop(self):
        return self.stack.pop()

    def push(self, scope: Scope):
        self.stack.append(scope)

    def seek(self) -> Scope:
        if self.stack:
            return self.stack[-1]
        else:
            return None

    def __len__(self):
        return len(self.stack)


@dataclass
class Node:
    def __init__(self, left: Optional['Node'], right: Optional['Node'],
                 value: Optional[Union[str, int, float]], result_type: str):
        self.left = left
        self.right = right
        self.value = value

        self.result_type = result_type

        self.id = int(time.time())

    def as_json(self) -> Dict:
        left = None
        if self.left is not None:
            left = self.left.as_json()

        right = None
        if self.right is not None:
            right = self.right.as_json()

        return {
            'value': self.value,
            'left': left,
            'right': right
        }

    def __str__(self):
        return f'<NodeId: {self.id}>'
