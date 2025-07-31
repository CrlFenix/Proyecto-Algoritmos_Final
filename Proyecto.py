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

