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

class Ninja:
    
    def __init__(self, nombre, fuerza, agilidad, resistencia, estilo, puntos_victoria=0):
        self.nombre = nombre
        self.fuerza = int(fuerza)
        self.agilidad = int(agilidad)
        self.resistencia = int(resistencia)
        self.estilo = estilo
        self.puntos_victoria = int(puntos_victoria)
        self.arbol_habilidades = None  # Aquí se almacena el árbol de habilidades

    def __str__(self):
        return (f"Nombre: {self.nombre}, Fuerza: {self.fuerza}, Agilidad: {self.agilidad}, "
                f"Resistencia: {self.resistencia}, Estilo: {self.estilo}, Puntos de Victoria: {self.puntos_victoria}")

    # Método para guardar solo nombre y estilo en ninjas.txt
    def to_file_string_basic(self):
        return f"{self.nombre},{self.fuerza},{self.agilidad},{self.resistencia},{self.estilo},{self.puntos_victoria}"

    # Método para guardar las habilidades en habilidades_ninja.txt
    def to_habilidades_string(self):
        if self.arbol_habilidades:
            habilidades_list = []
            def serialize_tree_preorder(node):
                if node:
                    habilidades_list.append(f"{node.nombre},{node.puntos}")
                    serialize_tree_preorder(node.izquierda)
                    serialize_tree_preorder(node.derecha)
                else:
                    habilidades_list.append("None")
            serialize_tree_preorder(self.arbol_habilidades)
            return f"{self.nombre}{HABILIDAD_DELIMITER}{HABILIDAD_DELIMITER.join(habilidades_list)}"
        return f"{self.nombre}{HABILIDAD_DELIMITER}None" # Si no tiene habilidades, igual se guarda el nombre

    @staticmethod
    def from_file_string_basic(line):
        
        data = line.strip().split(',')
        if len(data) == 6: # Ahora son 6 campos (nombre, fuerza, agilidad, resistencia, estilo, puntos_victoria)
            return Ninja(data[0], data[1], data[2], data[3], data[4], data[5])
        return None

    @staticmethod
    def from_habilidades_string(line):
        
        parts = line.strip().split(HABILIDAD_DELIMITER, 1) # Separamos solo el primer delimitador
        if len(parts) == 2:
            nombre_ninja = parts[0]
            habilidades_str = parts[1]
            if habilidades_str != "None":
                habilidades_list = habilidades_str.split(HABILIDAD_DELIMITER)
                arbol_habilidades = NodoHabilidad.from_string(habilidades_list)
                return nombre_ninja, arbol_habilidades
        return None, None
    






















































def simular_combate(ninja1, ninja2, usuario_actual=None):
    print(f"\n⚔️ Combate: {ninja1.nombre} vs {ninja2.nombre} ⚔️")

    puntos_ninja1 = (ninja1.fuerza + ninja1.agilidad + ninja1.resistencia) * random.uniform(0.8, 1.2)
    puntos_ninja2 = (ninja2.fuerza + ninja2.agilidad + ninja2.resistencia) * random.uniform(0.8, 1.2)

    puntos_ninja1 += sumar_habilidades(ninja1.arbol_habilidades) if ninja1.arbol_habilidades else 0
    puntos_ninja2 += sumar_habilidades(ninja2.arbol_habilidades) if ninja2.arbol_habilidades else 0
    print(f"{ninja1.nombre}: {puntos_ninja1:.2f} pts (base + habilidades)")
    print(f"{ninja2.nombre}: {puntos_ninja2:.2f} pts (base + habilidades)")
    if puntos_ninja1 > puntos_ninja2:
        ganador = ninja1
        perdedor = ninja2
    elif puntos_ninja2 > puntos_ninja1:
        ganador = ninja2
        perdedor = ninja1
    else:
        print("¡Empate en puntos! El ganador se decidira al azar") 
        ganador = random.choice([ninja1, ninja2])
        perdedor = ninja1 if ganador == ninja2 else ninja2

print(f"🏆 Ganador: {ganador.nombre}! 🏆")
ganador.puntos_victoria += 1

fecha = datetime.date.today().strftime("%d/%m/%Y")
combate_info = f"{ninja1.nombre} vs {ninja2.nombre} - Ganador: {ganador.nombre} - Fecha: {fecha}"
if usuario_actual:
    if ganador.nombre == ninja1.nombre:
        usuario_actual.combates_ganados += 1
    else:
        usuario_actual.combates_perdidos += 1
    combate_info += f" – Jugador: {usuario_actual.email}"
    guardar_progreso_usuario(usuario_actual.email, usuario_actual.combates_ganados, usuario_actual.combates_perdidos)
    
guardar_historial_combates(combate_info)

return ganador































































def crear_arbol_habilidades_base():
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
    return (nodo.puntos + sumar_habilidades(nodo.izquierda) + sumar_habilidades(nodo.derecha))























































































































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
            
class Usuario:
    def __init__(self, nombres, identificacion, edad, email, password):
        self.nombre = nombres
        self.identificacion
