from typing import Set, Union, List
from CC2021.strucs import LLC, Production

_EMPTY_SYMBOL = '&'


class Parser:
    def __init__(self):
        # self.current_symbol: Union[None, str] = None
        self.current_symbol = None
        self.empty_symbol = _EMPTY_SYMBOL

        # self.prods: List[Production] = []
        # self.start_symbol: Union[None, str] = None
        # self.non_terminals: Set[str] = set()
        # self.terminals: Set[str] = set()
        self.prods = []
        self.start_symbol = None
        self.non_terminals = set()
        self.terminals = set()

    def parse(self, path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.parse_line(line)

        return LLC(start_s=self.start_symbol,
                   terminals=self.terminals,
                   non_terminals=self.non_terminals,
                   prods=self.prods)

    def parse_line(self, line):
        if len(line.split(':')) == 2:
            # if this line represents the first prod
            h, b = line.split(':')
            head = h.strip()
            body_set = b.strip()

            self.current_symbol = head

            if self.start_symbol is None:
                # start symbol not set yet
                self.start_symbol = head

            body = []

            self.non_terminals.add(head)
            items = body_set.split()
            for i in items:
                i = i.strip()
                if i == '':
                    continue

                if i == self.empty_symbol:
                    body.append(i)
                elif (i[0] == '"' and i[-1] == '"'):
                    # if item begins and ends with double quotes, remove them
                    s = i[1:-1]
                    body.append(s)
                    self.terminals.add(s)
                else:
                    self.non_terminals.add(i)
                    body.append(i)

            self.prods.append(Production(head, body))
