import random
from collections import deque
import datetime
import re

HABILIDAD_DELIMITER = "|"

class NodoHabilidad:
    def __init__(self,nombre,puntos):
        self.nombre=nombre
        self.puntos=puntos
        self.izquierda=None
        self.derecha=None
    def to_string(self):
        left_str=self.izquierda.to_string() if self.izquierda else "None"
        right_str=self.derecha.to_string() if self.derecha else "None"
        return f"{self.nombre}{HABILIDAD_DELIMITER}{self.puntos}{HABILIDAD_DELIMITER}{left_str}{HABILIDAD_DELIMITER}{right_str}"
    @staticmethod
    def from_string(data_list):
        if not data_list or data_list[0] == "None":
            if data_list:
                data_list.pop(0)
            return None
        node_data=data_list.pop(0)
        parts=node_data.split(';')
        if len(parts) !=2:
            return None
        
        nodo=NodoHabilidad(parts[0], int(parts[1]))
        nodo.izquierda = NodoHabilidad.from_string(data_list)
        nodo.derecha = NodoHabilidad.from_string(data_list)
        return nodo
    









































































































































































def crear_arbol_habilidades_base():
    raiz=NodoHabilidad("Ataque rapido", random.randint(5, 10))
    raiz = NodoHabilidad("Ataque rapido", random.randint(5, 10))
    raiz.izquierda = NodoHabilidad("Golpe fuerte", random.randint(5, 10))
    raiz.derecha = NodoHabilidad("Esquiva veloz", random.randint(5, 10))
    raiz.izquierda.izquierda = NodoHabilidad("Barrido bajo", random.randint(5, 10))
    raiz.izquierda.derecha = NodoHabilidad("Lanzamiento de shuriken", random.randint(5, 10))
    raiz.derecha.izquierda = NodoHabilidad("Bloqueo alto", random.randint(5, 10))
    raiz.derecha.derecha = NodoHabilidad("Patada giratoria", random.randint(5, 10))
    return raiz

def sumar_habilidades(nodo):
    if nodo is None:
        return 0
    return (nodo.puntos+sumar_habilidades(nodo.izquierda)+sumar_habilidades(nodo.derecha))

