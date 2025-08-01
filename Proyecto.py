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








































































































































def validar_entero(mensaje,min_val=None, max_val=None):
    while True:
        try:
            valor_str=input(mensaje)
            valor=int(valor_str)
            if min_val is not None and valor <min_val:
                print(f"Error:  el valor debe ser mayor o igual a {min_val}. Por favor, intente de nuevo.")
            elif max_val is not None and valor < max_val:
                print(f"Error: el valor debe ser menor o igual a {max_val}. Por favor, intente de nuevo.")
            else:
                return valor
        except ValueError:
            print("Error: Entrada invalida. Por favor , ingrese un numero entero")
def validar_solo_letras(mensaje):
    while True:
        valor=input(mensaje).strip()
        if valor:
            return valor
        else:
            print("Error: La entrada no puede estar vacia. Por favor, intente de nuevo. ")
            