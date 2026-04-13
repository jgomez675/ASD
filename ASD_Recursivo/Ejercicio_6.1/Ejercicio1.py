import sys
from collections import deque

EPSILON = 'ε'

class Grammar:
    def __init__(self):
        self.productions = {
            'A': [['a', 'B', 'C']],
            'B': [['b', 'bas'], ['big', 'C', 'boss']],
            'C': [[EPSILON], ['c']]
        }
        self.start = 'A'

        self.terminals = sorted(
            ['big', 'boss', 'bas', 'a', 'b', 'c'],
            key=len,
            reverse=True
        )

    def tokenize(self, string):
        tokens = []
        i = 0
        string = string.strip().lower()

        while i < len(string):
            match = None

            for t in self.terminals:
                if string.startswith(t, i):
                    match = t
                    break

            if match:
                tokens.append(match)
                i += len(match)
            else:
                return None

        return tokens

    def clean_epsilon(self, symbols):
        return [s for s in symbols if s != EPSILON]

    def derive(self, target_string):
        print("\n===== PROCESO DE DERIVACIÓN =====")

        target_tokens = self.tokenize(target_string)

        if target_tokens is None:
            print("Cadena NO válida (no pertenece al lenguaje)")
            return False

        print("Tokens:", target_tokens)

        queue = deque()
        queue.append(([self.start], ["A"]))

        visited = set()
        max_steps = 1000
        steps = 0

        while queue and steps < max_steps:
            current, path = queue.popleft()
            steps += 1

            current_clean = self.clean_epsilon(current)

            print("→", " ".join(current_clean))

            if current_clean == target_tokens:
                print("\n✔ DERIVACIÓN ENCONTRADA:")
                for p in path:
                    print("→", p)
                print("\nCadena válida!")
                return True

            if len(current_clean) > len(target_tokens):
                continue

            state_id = tuple(current_clean)
            if state_id in visited:
                continue
            visited.add(state_id)

            for i, symbol in enumerate(current_clean):
                if symbol in self.productions:
                    for prod in self.productions[symbol]:
                        new_symbols = (
                            current_clean[:i] +
                            self.clean_epsilon(prod) +
                            current_clean[i+1:]
                        )

                        if len(new_symbols) <= len(target_tokens):
                            new_path = path + [" ".join(new_symbols)]
                            queue.append((new_symbols, new_path))
                    break

        print("\nCadena NO válida")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python programa.py archivo.txt")
        sys.exit(1)

    archivo = sys.argv[1]
    grammar = Grammar()

    try:
        with open(archivo, 'r') as f:
            cadenas = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: archivo no encontrado")
        sys.exit(1)

    print("\n========== ANALIZADOR DE GRAMÁTICA ==========")

    for cadena in cadenas:
        print("\n===========================================")
        print(f"Evaluando cadena: {cadena}")
        grammar.derive(cadena)

    print("\n========== FIN DEL ANÁLISIS ==========")
