from CC2021.LLC.parser import Parser
from itertools import combinations
from CC2021.strucs import TableSyntaticAnalyser
from CC2021.strucs import LLC
from CC2021.strucs import Production


_EMPTY_SYMBOL = '&'
_STACK_BOTTOM = '$'


def unite(a, b):
    n = len(a)
    a |= b - {_EMPTY_SYMBOL}
    return len(a) != n


class Proc:
    def __init__(self):
        self.llc = None
        self.empty_symbol = _EMPTY_SYMBOL
        self.stack_bottom = _STACK_BOTTOM

    def create_llc(self, llc1):
        self.llc: LLC = llc1
        self.firsts = self.get_firsts()
        self.follows = self.get_follows()

    def read_llc(self, path):
        p = Parser()
        self.create_llc(p.parse(path))

    def get_firsts(self):
        # prepare firsts
        first = {a: set() for a in self.llc.non_terminals}
        first.update((a, {a}) for a in self.llc.terminals)
        first[self.empty_symbol] = {self.empty_symbol}

        epsilon = {self.empty_symbol}

        while True:
            updated = False

            for prod in self.llc.prods:
                # calculate firsts
                for s in prod.body:
                    updated |= unite(first[prod.head], first[s])

                    if s not in epsilon:
                        break

                    else:
                        first[prod.head] |= {self.empty_symbol}
                        updated |= unite(epsilon, {prod.head})

            # stops when nothing changed
            if not updated:
                break

        return first

    def get_follows(self):
        # prepare follows
        follow = {a: set() for a in self.llc.non_terminals}
        follow[self.empty_symbol] = {self.stack_bottom}
        follow[self.llc.start_s] = {self.stack_bottom}

        epsilon = {self.empty_symbol}

        while True:
            updated = False

            for prod in self.llc.prods:
                # calculate follows
                aux = follow[prod.head]
                rev = reversed(prod.body)

                for s in rev:
                    if s in follow:
                        updated |= unite(follow[s], aux)

                    if s in epsilon:
                        aux = aux.union(self.firsts[s])
                    else:
                        aux = self.firsts[s]

            # stops when nothing changed
            if not updated:
                break

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

    # checking if LLC is LL(1)
    def theorem_first_part(self, p1, p2):
        # checks if
        # first(p1) <intersection> first(p2) == empty

        p1_first = self.calculate_first_prod(p1.body)
        p2_first = self.calculate_first_prod(p2.body)

        checks = (p1_first.intersection(p2_first) == set())

        if not checks:
            print('The LLC is not LL(1)!')
            print('--> Firsts of first production: %s' % p1_first)
            print('--> Firsts of second production: %s' % p2_first)

        return checks

    def theorem_second_part(self, p1: Production, p2: Production):
        # checks if
        # for A -> p1 | p2
        # if(p1 -*> &) then (first(p2) <intersection> follow(A) = empty)
        # if(p2 -*> &) then (first(p1) <intersection> follow(A) = empty)

        check = True
        follow_head = self.follow[p1.head]

        p1_first = self.calculate_first_prod(p1.body)
        p2_first = self.calculate_first_prod(p2.body)

        if _EMPTY_SYMBOL in p2_first:
            check &= p1_first.intersection(follow_head) == set()

        if _EMPTY_SYMBOL in p1_first:
            check &= p2_first.intersection(follow_head) == set()

        if not check:
            print('The LLC is not LL(1)!')
            print('First of p1 %s' % p1_first)
            print('First of p2 %s' % p2_first)
            print('follow of head of prods %s' % follow_head)

        return check

    def is_ll1(self):
        for nt in self.llc.non_terminals:
            if not self.check_theorems_on_productions_of(nt):
                return False
            return True

    def check_theorems_on_productions_of(self, nt):
        productions = list(filter(lambda k: k.head == nt, self.llc.prods))

        for p1, p2 in combinations(productions, 2):
            first_part_of_theorem = self.theorem_first_part(p1, p2)
            second_part_of_theorem = self.theorem_second_part(p1, p2)
            if not (first_part_of_theorem and second_part_of_theorem):
                print('|Grammar is not LL(1), as shown by productions')
                print('|    | P1: %s' % p1)
                print('|    | P2: %s' % p2)
                return False

        return True

    def create_table(self):
        if not self.is_ll1():
            print("Can't generate the syntatic analyser table for a non-LL(1) grammar")
            return False

        table = TableSyntaticAnalyser(self.llc)

        for prod in self.llc.prods:
            first_body = self.calculate_first_prod(prod.body)

            for t in first_body - {self.empty_symbol}:
                table.add_prod(prod, t, prod.head)

            if self.empty_symbol in first_body:
                for t in self.follows[prod.head]:
                    table.add_prod(prod, t, prod.head)

        return table
