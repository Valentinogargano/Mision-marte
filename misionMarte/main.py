
from mapa import (
    explorar_mapa,
    consultar_movimientos,
    desapilar_movimiento
)
from tareas import gestionar_tareas
from muestras import gestionar_muestras


def main():
    while True:
        print("\n=== MISION MARTE ===")
        print("1. Explorar el mapa")
        print("2. Gestionar tareas")
        print("3. Gestionar muestras")
        print("4. Consultar movimientos")
        print("5. Desapilar ultimo movimiento")
        print("0. Salir")

        opcion = input("Seleccione una opcion: ").strip()

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


if __name__ == "__main__":
    main()
