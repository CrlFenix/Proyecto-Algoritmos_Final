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

class ArbolBinario:

    def __init__(self):
        self.raiz = None

    def insertar(self, habilidad):
        if self.raiz is None:
            self.raiz = NodoArbol(habilidad)
        else:
            self._insertar_recursivo(self.raiz, habilidad)

    def _insertar_recursivo(self, nodo, habilidad):
        if habilidad < nodo.habilidad:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(habilidad)
            else:
                self._insertar_recursivo(nodo.izquierda, habilidad)
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(habilidad)
            else:
                self._insertar_recursivo(nodo.derecha, habilidad)

    def preorden(self):
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.habilidad)
            self._preorden_recursivo(nodo.izquierda, resultado)
            self._preorden_recursivo(nodo.derecha, resultado)

    def inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierda, resultado)
            resultado.append(nodo.habilidad)
            self._inorden_recursivo(nodo.derecha, resultado)

    def postorden(self):
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo, resultado):
        if nodo:
            self._postorden_recursivo(nodo.izquierda, resultado)
            self._postorden_recursivo(nodo.derecha, resultado)
            resultado.append(nodo.habilidad)

class Cola():
    def __init__(self):self.items=deque()
    def esta_vacia(self): return len(self.items)==0
    def encolar(self, item): self.items.append(item)
    def desencolar(self): return self.items.popleft()if not self.esta_vacia() else None
    def __len__(self): return len(self.items)


def main():
    while True:
        limpiar_pantalla()
        print("  =====================================\n  |   BIENVENIDO AL TORNEO NINJA POLITECNICA   |\n  =====================================")
        print("\n Elige tu rol: \n 1. Administrador\n 2. Jugador\n 3. Salir")
        opcion = input("\n > ")
        if opcion=='1':menu_admin()
        elif opcion=='2':menu_jugador()
        elif opcion=='3':print("Chaooooo...Saliendo del programa"); break
        else: print("Opcion no valida."); input("\nEnter para continuar...")

def guardar_historial_combates(combate_info):

    with open("combates.txt", "a") as f:
        f.write(combate_info + "\n")

def cargar_historial_combates():
    combates = []
    try:
        with open("combates.txt", "r") as f:
            for line in f:
                combates.append(line.strip())
    except FileNotFoundError:
        pass
    return combates

def guardar_progreso_usuario(email_usuario, ganados, perdidos):
    usuarios = cargar_usuarios()
    if email_usuario in usuarios:
        usuarios[email_usuario].combates_ganados = ganados
        usuarios[email_usuario].combates_perdidos = perdidos
        guardar_usuarios(usuarios)


if __name__ == "__main__":
    main()