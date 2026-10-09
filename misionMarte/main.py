
from collections import deque
import heapq

# Grafo del terreno marciano representado mediante lista de adyacencia.
mapa = {
    "A": ["B", "F"],
    "B": ["A", "C", "F", "D"],
    "C": ["B", "D"],
    "D": ["C", "E", "B"],
    "E": ["D", "F"],
    "F": ["E", "A", "B"]
}

BASE = "A"

# Pila LIFO que guarda las zonas de las rutas consultadas.
historial_movimientos = []

# Lista general, cola FIFO y cola de prioridad.
tareas = []
cola_tareas = deque()
cola_prioridad = []
siguiente_id_tarea = 1

# Lista de muestras precargadas para la simulacion.
muestras = [
    {"id": "M001", "zona": "B", "tipo": "Roca", "interes": 65},
    {"id": "M002", "zona": "D", "tipo": "Suelo", "interes": 42},
    {"id": "M003", "zona": "E", "tipo": "Mineral", "interes": 82},
    {"id": "M004", "zona": "C", "tipo": "Roca", "interes": 71},
    {"id": "M005", "zona": "F", "tipo": "Hielo", "interes": 90},
    {"id": "M006", "zona": "A", "tipo": "Sedimento", "interes": 35},
    {"id": "M007", "zona": "B", "tipo": "Mineral", "interes": 76},
    {"id": "M008", "zona": "D", "tipo": "Hielo", "interes": 88}
]


def mostrar_mapa():
    print("\n--- MAPA DE MARTE ---")
    for zona, vecinos in mapa.items():
        print(f"Zona {zona}: conectada con {', '.join(vecinos)}")


def buscar_ruta_bfs(origen, destino):
    # BFS utiliza una cola FIFO para explorar por niveles.
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
    # DFS utiliza una pila LIFO para profundizar por un camino.
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
    destino = input("Ingrese la zona de destino (A-F): ").upper()

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

    # pop() elimina y devuelve el ultimo elemento de la pila.
    eliminado = historial_movimientos.pop()

    print("Registro eliminado:", eliminado)
    print(
        "Historial restante:",
        " -> ".join(historial_movimientos)
        if historial_movimientos else "Vacio"
    )


def registrar_tarea():
    global siguiente_id_tarea

    print("\n--- REGISTRAR TAREA ---")
    descripcion = input("Descripcion de la tarea: ").strip()
    zona = input("Zona donde se realizara (A-F): ").upper()

    if not descripcion:
        print("La descripcion no puede estar vacia.")
        return

    if zona not in mapa:
        print("Zona no valida.")
        return

    print("Prioridades: 1-Critica, 2-Alta, 3-Normal, 4-Baja")
    prioridad_texto = input("Ingrese la prioridad (1-4): ")

    if prioridad_texto not in ["1", "2", "3", "4"]:
        print("Prioridad no valida.")
        return

    tarea = {
        "id": siguiente_id_tarea,
        "descripcion": descripcion,
        "zona": zona,
        "prioridad": int(prioridad_texto),
        "estado": "PENDIENTE"
    }

    tareas.append(tarea)
    cola_tareas.append(tarea)

    # El heap atiende primero el numero de prioridad mas pequeño.
    heapq.heappush(
        cola_prioridad,
        (tarea["prioridad"], tarea["id"], tarea)
    )

    siguiente_id_tarea += 1
    print("Tarea registrada correctamente.")


def quitar_de_cola_prioridad(id_tarea):
    # Reconstruimos el heap sin la tarea que ya fue atendida.
    cola_prioridad[:] = [
        elemento for elemento in cola_prioridad
        if elemento[2]["id"] != id_tarea
    ]
    heapq.heapify(cola_prioridad)


def quitar_de_cola_fifo(id_tarea):
    tareas_restantes = [
        tarea for tarea in cola_tareas
        if tarea["id"] != id_tarea
    ]

    cola_tareas.clear()
    cola_tareas.extend(tareas_restantes)


def consultar_tareas():
    print("\n--- LISTADO GENERAL DE TAREAS ---")

    if not tareas:
        print("No hay tareas registradas.")
        return

    nombres_prioridad = {
        1: "Critica",
        2: "Alta",
        3: "Normal",
        4: "Baja"
    }

    for tarea in tareas:
        print(
            f"ID: {tarea['id']} | "
            f"Tarea: {tarea['descripcion']} | "
            f"Zona: {tarea['zona']} | "
            f"Prioridad: {nombres_prioridad[tarea['prioridad']]} | "
            f"Estado: {tarea['estado']}"
        )


def atender_tarea():
    print("\n--- ATENDER SIGUIENTE TAREA (FIFO) ---")

    if not cola_tareas:
        print("No hay tareas pendientes.")
        return

    tarea = cola_tareas.popleft()
    quitar_de_cola_prioridad(tarea["id"])
    tarea["estado"] = "ATENDIDA"

    print("Tarea atendida:", tarea["descripcion"])
    print("Zona:", tarea["zona"])


def consultar_cola():
    print("\n--- COLA FIFO DE TAREAS PENDIENTES ---")

    if not cola_tareas:
        print("No hay tareas pendientes.")
        return

    for posicion, tarea in enumerate(cola_tareas, start=1):
        print(
            f"{posicion}. {tarea['descripcion']} "
            f"(Zona {tarea['zona']})"
        )


def atender_por_prioridad():
    print("\n--- ATENDER POR PRIORIDAD ---")

    if not cola_prioridad:
        print("No hay tareas pendientes.")
        return

    # heappop() extrae la tarea con el numero de prioridad mas pequeño.
    _, _, tarea = heapq.heappop(cola_prioridad)

    quitar_de_cola_fifo(tarea["id"])
    tarea["estado"] = "ATENDIDA"

    print("Tarea atendida:", tarea["descripcion"])
    print("Zona:", tarea["zona"])
    print("Prioridad:", tarea["prioridad"])


def consultar_prioridades():
    print("\n--- TAREAS ORDENADAS POR PRIORIDAD ---")

    if not cola_prioridad:
        print("No hay tareas pendientes.")
        return

    nombres_prioridad = {
        1: "Critica",
        2: "Alta",
        3: "Normal",
        4: "Baja"
    }

    copia = sorted(cola_prioridad)

    for _, _, tarea in copia:
        print(
            f"ID: {tarea['id']} | "
            f"{tarea['descripcion']} | "
            f"Prioridad: {nombres_prioridad[tarea['prioridad']]}"
        )


def gestionar_tareas():
    while True:
        print("\n--- GESTION DE TAREAS ---")
        print("1. Registrar tarea")
        print("2. Consultar todas las tareas")
        print("3. Atender siguiente tarea (FIFO)")
        print("4. Consultar cola FIFO")
        print("5. Atender tarea por prioridad")
        print("6. Consultar tareas por prioridad")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            registrar_tarea()
        elif opcion == "2":
            consultar_tareas()
        elif opcion == "3":
            atender_tarea()
        elif opcion == "4":
            consultar_cola()
        elif opcion == "5":
            atender_por_prioridad()
        elif opcion == "6":
            consultar_prioridades()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")


def consultar_muestras():
    print("\n--- MUESTRAS CIENTIFICAS ---")

    for muestra in muestras:
        print(
            f"ID: {muestra['id']} | "
            f"Zona: {muestra['zona']} | "
            f"Tipo: {muestra['tipo']} | "
            f"Interes cientifico: {muestra['interes']}/100"
        )


def buscar_muestra_secuencial(id_buscado):
    comparaciones = 0

    # Recorremos la lista hasta encontrar el identificador.
    for muestra in muestras:
        comparaciones += 1

        if muestra["id"] == id_buscado:
            return muestra, comparaciones

    return None, comparaciones


def buscar_muestra_binaria(id_buscado):
    # La busqueda binaria necesita los identificadores ordenados.
    ordenadas = sorted(muestras, key=lambda muestra: muestra["id"])
    izquierda = 0
    derecha = len(ordenadas) - 1
    comparaciones = 0

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        id_medio = ordenadas[medio]["id"]
        comparaciones += 1

        if id_medio == id_buscado:
            return ordenadas[medio], comparaciones
        elif id_medio < id_buscado:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return None, comparaciones


def mostrar_resultado_busqueda(resultado, comparaciones):
    if resultado:
        print("Muestra encontrada:")
        print("ID:", resultado["id"])
        print("Zona:", resultado["zona"])
        print("Tipo:", resultado["tipo"])
        print("Interes cientifico:", resultado["interes"], "/100")
    else:
        print("No se encontro una muestra con ese identificador.")

    print("Comparaciones realizadas:", comparaciones)


def buscar_muestra():
    print("\n--- BUSQUEDA SECUENCIAL ---")
    id_buscado = input("Ingrese el identificador (ej. M005): ").strip().upper()

    resultado, comparaciones = buscar_muestra_secuencial(id_buscado)
    mostrar_resultado_busqueda(resultado, comparaciones)


def buscar_muestra_binaria_menu():
    print("\n--- BUSQUEDA BINARIA ---")
    id_buscado = input("Ingrese el identificador (ej. M005): ").strip().upper()

    resultado, comparaciones = buscar_muestra_binaria(id_buscado)
    mostrar_resultado_busqueda(resultado, comparaciones)


def ordenar_muestras_por_interes():
    print("\n--- MUESTRAS ORDENADAS POR INTERES CIENTIFICO ---")

    ordenadas = sorted(
        muestras,
        key=lambda muestra: muestra["interes"],
        reverse=True
    )

    for muestra in ordenadas:
        print(
            f"ID: {muestra['id']} | "
            f"Tipo: {muestra['tipo']} | "
            f"Interes: {muestra['interes']}/100"
        )


def gestionar_muestras():
    while True:
        print("\n--- MUESTRAS CIENTIFICAS ---")
        print("1. Consultar muestras")
        print("2. Buscar muestra por ID (secuencial)")
        print("3. Ordenar por interes cientifico")
        print("4. Buscar muestra por ID (binaria)")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            consultar_muestras()
        elif opcion == "2":
            buscar_muestra()
        elif opcion == "3":
            ordenar_muestras_por_interes()
        elif opcion == "4":
            buscar_muestra_binaria_menu()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")


# Menu principal
while True:
    print("\n=== MISION MARTE ===")
    print("1. Explorar el mapa")
    print("2. Gestionar tareas")
    print("3. Gestionar muestras")
    print("4. Consultar movimientos")
    print("5. Desapilar ultimo movimiento")
    print("0. Salir")

    opcion = input("Seleccione una opcion: ")

    if opcion == "1":
        explorar_mapa()
    elif opcion == "2":
        gestionar_tareas()
    elif opcion == "3":
        gestionar_muestras()
    elif opcion == "4":
        consultar_movimientos()
    elif opcion == "5":
        desapilar_movimiento()
    elif opcion == "0":
        print("Mision finalizada.")
        break
    else:
        print("Opcion no valida.")
