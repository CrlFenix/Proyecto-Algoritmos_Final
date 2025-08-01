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









































































































































def menu_jugador_logeado(ninjas_db, usuarios_db, usuario_actual):
    while True:
        print(f"\n--- MENÚ DE JUGADOR ({usuario_actual.nombres}) ---")
        print("1. Ver árbol de habilidades de un ninja seleccionado")
        print("2. Simular combate uno vs uno contra otros ninjas") 
        print("3. Simular un torneo completo de peleas")
        print("4. Consultar el ranking actualizado de ninjas")
        print("5. Ver progreso y historial de mis combates")
        print("6. Cerrar sesión")
        opcion = validar_string_no_vacio("Elija una opción: ")
        if opcion == '1':
            if not ninjas_db:
                print("No hay ninjas registrados para ver sus habilidades.")
                continue
            ninja = validar_ninja_existente("Ingrese el nombre del ninja para ver sus habilidades: ", ninjas_db)
            if ninja.arbol_habilidades:
                print(f"\n--- ÁRBOL DE HABILIDADES DE {ninja.nombre} (PREORDEN) ---")
                mostrar_habilidades_recorrido(ninja.arbol_habilidades, "preorden")
                print(f"Puntos totales de habilidades: {sumar_habilidades(ninja.arbol_habilidades)}")
            else:
                print("Este ninja aún no tiene un árbol de habilidades asignado.")
        elif opcion == '2':
            if len(ninjas_db) < 2:
                print("No hay suficientes ninjas para simular un combate.")
                continue
            print("\n--- SIMULAR COMBATE UNO A UNO ---")
            print("Ninjas disponibles:", ", ".join(ninjas_db.keys()))

            ninja1 = validar_ninja_existente("Ingrese el nombre de su ninja: ", ninjas_db)
            ninja2 = validar_ninja_diferente("Ingrese el nombre del ninja oponente (diferente a su ninja): ", ninjas_db, ninja1.nombre)
            
            simular_combate(ninja1, ninja2, usuario_actual)
            guardar_ninjas(ninjas_db)
            print(" Combate simulado y progreso actualizado.")
        elif opcion == '3':
            if len(ninjas_db) < 2:
                print("No hay suficientes ninjas para un torneo. Se necesitan al menos 2 ninjas.")
                continue
            
            # Aseguramos que haya al menos 2, 4, 8, etc. ninjas para un torneo más limpio
            num_ninjas = len(ninjas_db)
            # Encuentra la potencia de 2 más cercana y mayor o igual
            if not (num_ninjas > 0 and (num_ninjas & (num_ninjas - 1) == 0)): # Si no es potencia de 2
                print(f"Actualmente hay {num_ninjas} ninjas. Para un torneo óptimo, la cantidad de ninjas debería ser una potencia de 2 (2, 4, 8, etc.).")
                confirmar = validar_string_no_vacio("¿Desea continuar con el torneo con la cantidad actual de ninjas (algunos podrían tener BYE)? (s/n): ").lower()
                if confirmar != 's':
                    continue

            ninjas_para_torneo = list(ninjas_db.values())
            random.shuffle(ninjas_para_torneo)

            simular_torneo(ninjas_para_torneo)
            guardar_ninjas(ninjas_db)
            print("Torneo simulado y rankings actualizados.")
        elif opcion == '4':
            if not ninjas_db:
                print("No hay ninjas registrados.")
                continue
            ninjas_ordenados = quick_sort_ninjas(list(ninjas_db.values()), key="puntos_victoria")
            print("\n--- RANKING ACTUAL DE NINJAS POR PUNTOS DE VICTORIA ---")
            for i, ninja in enumerate(ninjas_ordenados):
                print(f"{i+1}. {ninja.nombre} - Puntos de Victoria: {ninja.puntos_victoria}")
        elif opcion == '5':
            print(f"\n--- PROGRESO DE {usuario_actual.nombres} ---")
            print(f"Combates ganados: {usuario_actual.combates_ganados}")
            print(f"Combates perdidos: {usuario_actual.combates_perdidos}")
            print("\n--- MI HISTORIAL DE COMBATES ---")
            historial_global = cargar_historial_combates()
            encontrado = False
            for combate in historial_global:
                if usuario_actual.email in combate:
                    print(combate)
                    encontrado = True
            if not encontrado:
                print("No se encontraron combates asociados a este usuario.")

        elif opcion == '6':
            print("Cerrando sesión.")
            break
        else:
            print("Opción inválida. Por favor, elija una opción del 1 al 6.")
            