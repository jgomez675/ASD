import sys
from collections import defaultdict
 
EPSILON = 'ε'
ARROW   = '->'
 
def leer_gramatica(ruta: str):
    gramatica  = defaultdict(list)
    orden_nt   = []
 
    with open(ruta, encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            if ARROW not in linea:
                print(f"  [AVISO] Línea ignorada (sin '{ARROW}'): {linea}")
                continue
 
            izq, der = linea.split(ARROW, 1)
            nt  = izq.strip()
            produccion = der.strip().split()
 
            if not produccion:
                produccion = [EPSILON]
 
            if nt not in gramatica:
                orden_nt.append(nt)
            gramatica[nt].append(produccion)
 
    if not orden_nt:
        print("ERROR: El archivo no contiene producciones válidas.")
        sys.exit(1)
 
    return dict(gramatica), orden_nt, orden_nt[0]
 
def calcular_primeros(gramatica: dict) -> dict:

    no_terminales = set(gramatica.keys())
    primeros = {nt: set() for nt in no_terminales}
    cambio = True
 
    while cambio:
        cambio = False
        for A, producciones in gramatica.items():
            for produccion in producciones:
 
                if produccion == [EPSILON]:
                    if EPSILON not in primeros[A]:
                        primeros[A].add(EPSILON)
                        cambio = True
                    continue
 
                todos_epsilon = True
                for simbolo in produccion:
                    if simbolo not in no_terminales:
                        if simbolo not in primeros[A]:
                            primeros[A].add(simbolo)
                            cambio = True
                        todos_epsilon = False
                        break
                    else:
                        antes = len(primeros[A])
                        primeros[A].update(primeros[simbolo] - {EPSILON})
                        if len(primeros[A]) > antes:
                            cambio = True
                        if EPSILON not in primeros[simbolo]:
                            todos_epsilon = False
                            break
                if todos_epsilon:
                    if EPSILON not in primeros[A]:
                        primeros[A].add(EPSILON)
                        cambio = True 
    return primeros

def formatear_conjunto(conjunto: set) -> str:
    """Muestra el conjunto ordenado, ε siempre al final."""
    sin_eps = sorted(x for x in conjunto if x != EPSILON)
    con_eps = sin_eps + ([EPSILON] if EPSILON in conjunto else [])
    return '{ ' + ', '.join(con_eps) + ' }' if con_eps else '{ }'
def mostrar_resultados(ruta: str, gramatica: dict, orden_nt: list,
                       simbolo_inicial: str, primeros: dict):
    ancho = 62
    print()
    print('╔' + '═' * ancho + '╗')
    print('║' + ' CONJUNTO DE PRIMEROS (FIRST) '.center(ancho) + '║')
    print('╚' + '═' * ancho + '╝')
    print()
    print('┌' + '─' * ancho + '┐')
    print('│' + ' GRAMÁTICA '.center(ancho) + '│')
    print('├' + '─' * ancho + '┤')
    for nt in orden_nt:
        for prod in gramatica[nt]:
            regla = f"  {nt}  →  {' '.join(prod)}"
            print('│' + regla.ljust(ancho) + '│')
    print('└' + '─' * ancho + '┘')
    print()
    print(f"  Símbolo inicial : {simbolo_inicial}")
    print(f"  Archivo         : {ruta}")
    print()
    print('┌' + '─' * ancho + '┐')
    print('│' + ' RESULTADOS '.center(ancho) + '│')
    print('├' + '─' * ancho + '┤')
    for nt in orden_nt:
        etiqueta  = f"  PRIMEROS( {nt} )"
        conjunto  = formatear_conjunto(primeros[nt])
        linea     = f"{etiqueta:<20}=  {conjunto}"
        print('│' + linea.ljust(ancho) + '│')
    print('└' + '─' * ancho + '┘')
    print()
 
def main():
    if len(sys.argv) != 2:
        print()
        print("  Uso: python primeros.py <archivo.txt>")
        print()
        print("  Formato del archivo:")
        print("    S -> A B")
        print("    A -> a")
        print("    A -> ε")
        print()
        sys.exit(1)
 
    ruta = sys.argv[1]
 
    try:
        gramatica, orden_nt, simbolo_inicial = leer_gramatica(ruta)
    except FileNotFoundError:
        print(f"\n  ERROR: No se encontró el archivo '{ruta}'\n")
        sys.exit(1)
 
    primeros = calcular_primeros(gramatica)
    mostrar_resultados(ruta, gramatica, orden_nt, simbolo_inicial, primeros)
 
 
if __name__ == '__main__':
    main()
