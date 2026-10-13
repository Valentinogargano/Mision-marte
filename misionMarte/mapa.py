
from collections import deque


# Grafo del terreno marciano.
mapa = {
    "A": ["B", "F"],
    "B": ["A", "C", "F", "D"],
    "C": ["B", "D"],
    "D": ["C", "E", "B"],
    "E": ["D", "F"],
    "F": ["E", "A", "B"]
}

BASE = "A"

# Pila de historial de movimientos.
historial_movimientos = []


def mostrar_mapa():
    print("\n--- MAPA DE MARTE ---")
    for zona, vecinos in mapa.items():
        print(f"Zona {zona}: conectada con {', '.join(vecinos)}")


def buscar_ruta_bfs(origen, destino):
    cola = deque([[origen]])
    visitadas = {origen}

    while cola:
        ruta = cola.popleft()
        actual = ruta[-1]

        if actual == destino:
            return ruta

        for vecino in mapa[actual]:
            if vecino not in visitadas:
                visitadas.add(vecino)
                cola.append(ruta + [vecino])

    return None


def recorrer_dfs(origen):
    pila = [origen]
    visitadas = set()
    recorrido = []

    while pila:
        actual = pila.pop()

        if actual not in visitadas:
            visitadas.add(actual)
            recorrido.append(actual)

            for vecino in reversed(mapa[actual]):
                if vecino not in visitadas:
                    pila.append(vecino)

    return recorrido


def explorar_mapa():
    mostrar_mapa()

    print(f"\nEl robot parte desde la base {BASE}.")
    destino = input("Ingrese la zona de destino (A-F): ").strip().upper()

    if destino not in mapa:
        print("Zona no valida.")
        return

    ruta = buscar_ruta_bfs(BASE, destino)

    if ruta:
        print("\n--- RESULTADO BFS ---")
        print("Ruta:", " -> ".join(ruta))
        print("Cantidad de movimientos:", len(ruta) - 1)

        for zona in ruta:
            historial_movimientos.append(zona)

        print("Ruta guardada en el historial.")
    else:
        print("No existe una ruta hasta esa zona.")

    recorrido = recorrer_dfs(BASE)

    print("\n--- RESULTADO DFS ---")
    print("Recorrido:", " -> ".join(recorrido))
    print("Cantidad de movimientos DFS:", len(recorrido) - 1)


def consultar_movimientos():
    print("\n--- HISTORIAL DE MOVIMIENTOS ---")

    if not historial_movimientos:
        print("Todavia no hay movimientos registrados.")
        return

    print("Zonas registradas:", " -> ".join(historial_movimientos))
    print("Ultima zona registrada:", historial_movimientos[-1])


def desapilar_movimiento():
    print("\n--- DESAPILAR ULTIMO REGISTRO ---")

    if not historial_movimientos:
        print("El historial esta vacio.")
        return

    eliminado = historial_movimientos.pop()

    print("Registro eliminado:", eliminado)
    print(
        "Historial restante:",
        " -> ".join(historial_movimientos)
        if historial_movimientos else "Vacio"
    )
