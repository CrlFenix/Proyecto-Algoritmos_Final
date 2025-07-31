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

class ArbolBinario:
    """Organiza las habilidades de un ninja en un árbol binario."""
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
