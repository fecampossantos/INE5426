from CC2021.strucs import LLC, Production
from utils.utils import EMPTY_SYMBOL 

# classe que faz o parsing de uma possivel linguagem, a partir de uma gramatica .grammar

class Parser:
    def __init__(self):

        self.current_symbol = None
        self.empty_symbol = EMPTY_SYMBOL

        self.prods = []
        self.start_symbol = None
        self.non_terminals = set()
        self.terminals = set()

    def parse(self, path):
        with open(path) as _file:
            for line in _file:
                line = line.strip()
                if not line:
                    continue
                self.parse_line(line)
        
        return LLC(symbol_start=self.start_symbol,
                   terminals=self.terminals,
                   non_terminals=self.non_terminals,
                   productions=self.prods)

    def parse_line(self, line):
        if len(line.split(':')) == 2:
            # linha representa a primeira producao
            h, b = line.split(':')
            head = h.strip()
            body_set = b.strip()

            self.current_symbol = head

            if self.start_symbol is None:
                # simbolo inicial ainda nao definido
                self.start_symbol = head
            self.create_production(head, body_set)
        
        else:
          self.create_production(self.current_symbol, line.split('|')[-1])
    
    def create_production(self, head, body_set):
      body = []
      self.non_terminals.add(head)

      for i in body_set.split():
        item = i.strip()
        if item == '':
          continue

        if item == self.empty_symbol:
          body.append(item)
        
        elif (item[0] == '"' and item[-1] == '"'):
          # remove aspas
          symb = item[1:-1]
          body.append(symb)
          self.terminals.add(symb)
        else:
          self.non_terminals.add(item)
          body.append(item)
      
      self.prods.append(Production(head, body))
