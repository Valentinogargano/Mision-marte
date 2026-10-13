
# Lista de muestras precargadas.
muestras = [
    {"id": "M001", "zona": "B", "tipo": "Roca", "interes": 65},
    {"id": "M002", "zona": "D", "tipo": "Suelo", "interes": 42},
    {"id": "M003", "zona": "E", "tipo": "Mineral", "interes": 82},
    {"id": "M004", "zona": "C", "tipo": "Roca", "interes": 71},
    {"id": "M005", "zona": "F", "tipo": "Hielo", "interes": 90},
    {"id": "M006", "zona": "A", "tipo": "Sedimento", "interes": 35},
    {"id": "M007", "zona": "B", "tipo": "Mineral", "interes": 76},
    {"id": "M008", "zona": "D", "tipo": "Hielo", "interes": 88},
    {"id": "M009", "zona": "C", "tipo": "Mineral", "interes": 55}
]


# Nodo del arbol binario de busqueda.
class Nodo:
    def __init__(self, muestra):
        self.muestra = muestra
        self.izquierda = None
        self.derecha = None


def insertar_en_arbol(raiz, muestra):
    if raiz is None:
        return Nodo(muestra)

    if muestra["id"] < raiz.muestra["id"]:
        raiz.izquierda = insertar_en_arbol(raiz.izquierda, muestra)
    elif muestra["id"] > raiz.muestra["id"]:
        raiz.derecha = insertar_en_arbol(raiz.derecha, muestra)

    return raiz


def buscar_en_arbol(raiz, id_buscado):
    comparaciones = 0
    actual = raiz

    while actual is not None:
        comparaciones += 1

        if actual.muestra["id"] == id_buscado:
            return actual.muestra, comparaciones
        elif id_buscado < actual.muestra["id"]:
            actual = actual.izquierda
        else:
            actual = actual.derecha

    return None, comparaciones


def construir_arbol():
    orden_ids = [
        "M005", "M003", "M007", "M002", "M004",
        "M006", "M008", "M001", "M009"
    ]

    raiz = None

    for id_muestra in orden_ids:
        for muestra in muestras:
            if muestra["id"] == id_muestra:
                raiz = insertar_en_arbol(raiz, muestra)
                break

    return raiz


# El arbol se construye al cargar el modulo.
arbol_muestras = construir_arbol()


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

    for muestra in muestras:
        comparaciones += 1

        if muestra["id"] == id_buscado:
            return muestra, comparaciones

    return None, comparaciones


def buscar_muestra_binaria(id_buscado):
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
    id_buscado = input(
        "Ingrese el identificador (ej. M005): "
    ).strip().upper()

    resultado, comparaciones = buscar_muestra_secuencial(id_buscado)
    mostrar_resultado_busqueda(resultado, comparaciones)


def buscar_muestra_binaria_menu():
    print("\n--- BUSQUEDA BINARIA ---")
    id_buscado = input(
        "Ingrese el identificador (ej. M005): "
    ).strip().upper()

    resultado, comparaciones = buscar_muestra_binaria(id_buscado)
    mostrar_resultado_busqueda(resultado, comparaciones)


def buscar_muestra_arbol():
    print("\n--- BUSQUEDA EN ARBOL BINARIO ---")
    id_buscado = input(
        "Ingrese el identificador (ej. M005): "
    ).strip().upper()

    resultado, comparaciones = buscar_en_arbol(
        arbol_muestras, id_buscado
    )
    mostrar_resultado_busqueda(resultado, comparaciones)


def ordenar_muestras_por_interes():
    print("\n--- MUESTRAS ORDENADAS POR INTERES CIENTIFICO ---")

    ordenadas = muestras.copy()

    # Ordenamiento por seleccion: buscamos el mayor interes restante.
    for i in range(len(ordenadas)):
        posicion_mayor = i

        for j in range(i + 1, len(ordenadas)):
            if (
                    ordenadas[j]["interes"]
                    > ordenadas[posicion_mayor]["interes"]
            ):
                posicion_mayor = j

        ordenadas[i], ordenadas[posicion_mayor] = (
            ordenadas[posicion_mayor],
            ordenadas[i]
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
        print("5. Buscar muestra por ID (arbol binario)")
        print("0. Volver al menu principal")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            consultar_muestras()
        elif opcion == "2":
            buscar_muestra()
        elif opcion == "3":
            ordenar_muestras_por_interes()
        elif opcion == "4":
            buscar_muestra_binaria_menu()
        elif opcion == "5":
            buscar_muestra_arbol()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")
