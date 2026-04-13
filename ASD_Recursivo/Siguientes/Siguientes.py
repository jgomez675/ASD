import sys
from collections import defaultdict

EPSILON = 'ε'

class Grammar:
    def __init__(self):
        self.productions = defaultdict(list)
        self.non_terminals = set()
        self.terminals = set()
        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.start_symbol = None

    def read_grammar(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                left, right = line.split("->")
                left = left.strip()
                productions = right.split("|")

                if not self.start_symbol:
                    self.start_symbol = left

                self.non_terminals.add(left)

                for prod in productions:
                    symbols = prod.strip().split()
                    self.productions[left].append(symbols)

        # identificar terminales
        for left in self.productions:
            for prod in self.productions[left]:
                for symbol in prod:
                    if symbol not in self.productions and symbol != EPSILON:
                        self.terminals.add(symbol)

    def compute_first(self):
        changed = True

        while changed:
            changed = False
            for non_terminal in self.productions:
                for prod in self.productions[non_terminal]:
                    for symbol in prod:
                        before = len(self.first[non_terminal])

                        if symbol in self.terminals:
                            self.first[non_terminal].add(symbol)
                            break

                        elif symbol == EPSILON:
                            self.first[non_terminal].add(EPSILON)
                            break

                        else:
                            self.first[non_terminal] |= (self.first[symbol] - {EPSILON})
                            if EPSILON not in self.first[symbol]:
                                break
                        after = len(self.first[non_terminal])
                        if after > before:
                            changed = True
                    else:
                        self.first[non_terminal].add(EPSILON)

    def compute_follow(self):
        self.follow[self.start_symbol].add('$')

        changed = True
        while changed:
            changed = False
            for left in self.productions:
                for prod in self.productions[left]:
                    trailer = self.follow[left].copy()

                    for symbol in reversed(prod):
                        if symbol in self.non_terminals:
                            before = len(self.follow[symbol])

                            self.follow[symbol] |= trailer

                            if EPSILON in self.first[symbol]:
                                trailer |= (self.first[symbol] - {EPSILON})
                            else:
                                trailer = self.first[symbol]

                            after = len(self.follow[symbol])
                            if after > before:
                                changed = True
                        else:
                            trailer = {symbol}

    def print_results(self):
        print("\n===== CONJUNTOS FIRST =====")
        for nt in self.non_terminals:
            print(f"FIRST({nt}) = {{ {', '.join(self.first[nt])} }}")

        print("\n===== CONJUNTOS FOLLOW =====")
        for nt in self.non_terminals:
            print(f"FOLLOW({nt}) = {{ {', '.join(self.follow[nt])} }}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python programa.py archivo.txt")
        sys.exit(1)

    filename = sys.argv[1]

    grammar = Grammar()
    grammar.read_grammar(filename)
    grammar.compute_first()
    grammar.compute_follow()
    grammar.print_results()
