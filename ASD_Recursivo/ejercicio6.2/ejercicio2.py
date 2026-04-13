import sys
from collections import defaultdict

EPSILON = 'ε'

class Grammar:
    def __init__(self):
        self.productions = {
            'A': [['a', 'B', 'C']],
            'B': [['b', 'bas'], ['big', 'C', 'boss']],
            'C': [[EPSILON], ['c']]
        }

        self.non_terminals = set(self.productions.keys())
        self.terminals = {'a', 'b', 'c', 'bas', 'big', 'boss'}

        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.predict = []
        self.table = defaultdict(dict)
        self.start = 'A'

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for nt in self.productions:
                for prod in self.productions[nt]:
                    before = len(self.first[nt])

                    if prod[0] in self.terminals:
                        self.first[nt].add(prod[0])

                    elif prod[0] == EPSILON:
                        self.first[nt].add(EPSILON)

                    else:
                        self.first[nt] |= (self.first[prod[0]] - {EPSILON})

                        if EPSILON in self.first[prod[0]]:
                            self.first[nt].add(EPSILON)

                    if len(self.first[nt]) > before:
                        changed = True

    def first_of_string(self, symbols):
        result = set()

        for sym in symbols:
            if sym in self.terminals:
                result.add(sym)
                return result

            elif sym == EPSILON:
                result.add(EPSILON)
                return result

            else:
                result |= (self.first[sym] - {EPSILON})
                if EPSILON not in self.first[sym]:
                    return result

        result.add(EPSILON)
        return result

    def compute_follow(self):
        self.follow[self.start].add('$')

        changed = True
        while changed:
            changed = False

            for A in self.productions:
                for prod in self.productions[A]:
                    trailer = self.follow[A].copy()

                    for symbol in reversed(prod):
                        if symbol in self.non_terminals:
                            before = len(self.follow[symbol])
                            self.follow[symbol] |= trailer

                            if EPSILON in self.first[symbol]:
                                trailer |= (self.first[symbol] - {EPSILON})
                            else:
                                trailer = self.first[symbol]

                            if len(self.follow[symbol]) > before:
                                changed = True
                        else:
                            trailer = {symbol}

    def compute_predict(self):
        for A in self.productions:
            for prod in self.productions[A]:
                first_alpha = self.first_of_string(prod)

                predict = set()

                if EPSILON in first_alpha:
                    predict |= (first_alpha - {EPSILON})
                    predict |= self.follow[A]
                else:
                    predict |= first_alpha

                self.predict.append((A, prod, predict))

    def build_table(self):
        conflict = False

        for A, prod, pred_set in self.predict:
            for terminal in pred_set:
                if terminal in self.table[A]:
                    conflict = True
                self.table[A][terminal] = prod

        return conflict

    def print_results(self):
        print("\n===== FIRST =====")
        for nt in self.non_terminals:
            print(f"FIRST({nt}) = {self.first[nt]}")

        print("\n===== FOLLOW =====")
        for nt in self.non_terminals:
            print(f"FOLLOW({nt}) = {self.follow[nt]}")

        print("\n===== PREDICT =====")
        for A, prod, pred in self.predict:
            print(f"{A} → {' '.join(prod)} : {pred}")

        print("\n===== TABLA LL(1) =====")
        for nt in self.table:
            for t in self.table[nt]:
                print(f"M[{nt}, {t}] = {nt} → {' '.join(self.table[nt][t])}")

if __name__ == "__main__":
    grammar = Grammar()

    grammar.compute_first()
    grammar.compute_follow()
    grammar.compute_predict()

    conflict = grammar.build_table()

    grammar.print_results()

    print("\n===== RESULTADO =====")
    if conflict:
        print("La gramática NO es LL(1) (hay conflictos)")
    else:
        print("La gramática ES LL(1)")
