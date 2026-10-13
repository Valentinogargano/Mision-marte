
import heapq
from collections import deque
from mapa import mapa


# Estructuras para gestionar las tareas.
tareas = []
cola_tareas = deque()
cola_prioridad = []
siguiente_id_tarea = 1


def registrar_tarea():
    global siguiente_id_tarea

    print("\n--- REGISTRAR TAREA ---")
    descripcion = input("Descripcion de la tarea: ").strip()
    zona = input("Zona donde se realizara (A-F): ").strip().upper()

    if not descripcion:
        print("La descripcion no puede estar vacia.")
        return

    if zona not in mapa:
        print("Zona no valida.")
        return

    print("Prioridades: 1-Critica, 2-Alta, 3-Normal, 4-Baja")
    prioridad_texto = input("Ingrese la prioridad (1-4): ").strip()

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

    # El heap atiende primero la prioridad numericamente menor.
    heapq.heappush(
        cola_prioridad,
        (tarea["prioridad"], tarea["id"], tarea)
    )

    siguiente_id_tarea += 1
    print("Tarea registrada correctamente.")


def quitar_de_cola_prioridad(id_tarea):
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

        opcion = input("Seleccione una opcion: ").strip()

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
