print ("Hola Mundo")

import os
import getpass
import re
import hashlib
import random
import time
from datetime import datetime
from collections import deque

RUTA_NINJAS="ninjas.txt"
RUTA_HABILIDADES="habilidades_ninja.txt"
RUTA_USUARIOS="usuarios.txt"
RUTA_COMBATES="combates.txt"    

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

class NodoArbol:
    def __init__(self, habilidad):
        self.habilidad = habilidad
        self.izquierda = None
        self.derecha = None



def main():
    while True:
        limpiar_pantalla()
        print("  =====================================\n  |   BIENVENIDO AL TORNEO NINJA POLITECNICA   |\n  =====================================")
        print("\n Elige tu rol: 1. Administrador\n 2. Juagador\n 3. Salir")
        opcion = input("\n > ")
        if opcion=='1':menu_admin()
        elif opcion=='2':menu_jugador()
        elif opcion=='3':print("Chaooooo...Saliendo del programa"); break
        else: print("Opcion no valida."); input("\nEnter para continuar...")


if __name__ == "__main__":
    main()