from CC2021.LLC.parser import Parser
from CC2021.strucs import *
from itertools import combinations
from utils.utils import *

## classe que processa uma LLC

class Proc:
    def __init__(self):
        self.llc: LLC = None
        self.empty_symbol = EMPTY_SYMBOL
        self.stack_bottom = STACK_BOTTOM

    def create_llc(self, llc1):
        self.llc: LLC = llc1
        first, follow = self.calculate_firsts_and_follows()
        self.firsts = first
        self.follows = follow

    def read_llc(self, path):
        p = Parser()
        self.create_llc(p.parse(path))

    def calculate_firsts_and_follows(self):
        first = {i: set() for i in self.llc.non_terminals}
        first.update((i, {i}) for i in self.llc.terminals)
        first[self.empty_symbol] = {self.empty_symbol}

        follow = {i: set() for i in self.llc.non_terminals}
        follow[self.empty_symbol] = {self.stack_bottom}
        follow[self.llc.start_s] = {self.stack_bottom}

        epsilon = {self.empty_symbol}

        while True:
            updated = False

            for prod in self.llc.prods:
                # Calculate FIRST
                for symbol in prod.body:
                    updated |= merge(first[prod.head], first[symbol])

                    if symbol not in epsilon:
                        break

                else:
                    first[prod.head] |= {self.empty_symbol}
                    updated |= merge(epsilon, {prod.head})

                # Calculate FOLLOW
                temp = follow[prod.head]
                for symbol in reversed(prod.body):
                    if symbol in follow:
                        updated |= merge(follow[symbol], temp)

                    if symbol in epsilon:
                        temp = temp.union(first[symbol])
                    else:
                        temp = first[symbol]

            if not updated:
                break
        
        return first, follow

    def calculate_first_prod(self, body):
        first = set()
        for s in body:
            first_s = self.firsts[s]

            first |= self.firsts[s] - {self.empty_symbol}

            if self.empty_symbol not in first_s:
                break

        else:
            first |= {self.empty_symbol}

        return first

    

    def is_ll1(self):
        for nt in self.llc.non_terminals:
            if not self.check_conditions_on_productions_of(nt):
                return False
            return True

    def check_conditions_on_productions_of(self, nt):
        productions = list(filter(lambda k: k.head == nt, self.llc.prods))

        for p1, p2 in combinations(productions, 2):
            first_part_of_theorem = self.ll_first_condition(p1, p2)
            second_part_of_theorem = self.ll_second_condition(p1, p2)
            if not (first_part_of_theorem and second_part_of_theorem):
                print('|A gramatica nao e LL(1), provado pelas producoes')
                print('|    | P1: %s' % p1)
                print('|    | P2: %s' % p2)
                return False

        return True
    
    # checa se a LLC é LL(1)
    def ll_first_condition(self, p1: Production, p2: Production):
        # first(p1) <iontersecção> first(p2) == vazio

        p1_first = self.calculate_first_prod(p1.body)
        p2_first = self.calculate_first_prod(p2.body)

        checks = (p1_first.intersection(p2_first) == set())

        if not checks:
            print('A LLC nao e LL(1)! - Falha na primeira parte do teorema')
            print('--> First da primeira producao: %s' % p1_first)
            print('--> First da segunda producao: %s' % p2_first)

        return checks

    def ll_second_condition(self, p1: Production, p2: Production):
        # pra A -> p1 | p2
        # se(p1 -*> &) então (first(p2) <intersecção> follow(A) = vazio)
        # se(p2 -*> &) então (first(p1) <intersecção> follow(A) = vazio)

        check = True
        follow_head = self.follows[p1.head]

        p1_first = self.calculate_first_prod(p1.body)
        p2_first = self.calculate_first_prod(p2.body)

        if EMPTY_SYMBOL in p2_first:
            check &= p1_first.intersection(follow_head) == set()

        if EMPTY_SYMBOL in p1_first:
            check &= p2_first.intersection(follow_head) == set()

        if not check:
            print('A LLC nao e LL(1)! - Falha na segunda parte do teorema')
            print('First da producao 1 %s' % p1_first)
            print('First da producao 2 %s' % p2_first)
            print('Follow do head das producoes %s' % follow_head)

        return check

    def create_table(self):
        if not self.is_ll1():
            print("Essa gramatica nao e LL(1)")
            return False

        table = TableSyntaticAnalyser(self.llc.terminals, self.llc.non_terminals)

        for prod in self.llc.prods:
            first_body = self.calculate_first_prod(prod.body)

            for t in first_body - {self.empty_symbol}:
                table.add_prod(t, prod.head, prod)

            if self.empty_symbol in first_body:
                for t in self.follows[prod.head]:
                    table.add_prod(t, prod.head, prod)

        return table
