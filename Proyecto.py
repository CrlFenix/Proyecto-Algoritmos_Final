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


    def to_file_string_basic(self):
        return f"{self.nombre},{self.fuerza},{self.agilidad},{self.resistencia},{self.estilo},{self.puntos_victoria}"

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

def simular_torneo(ninjas_participantes):
    print("\n--- ¡COMIENZA EL TORNEO! ---")
    rondas_nombres = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final"]
    participantes_actuales = deque(ninjas_participantes[:])
    ronda_idx = 0
    while len(participantes_actuales) > 1:
        nombre_ronda = rondas_nombres[ronda_idx] if ronda_idx < len(rondas_nombres) else f"Ronda {ronda_idx + 1}"
        print(f"\n--- RONDA DE {nombre_ronda.upper()} ({len(participantes_actuales)} NINJAS) ---")
        siguiente_ronda = []
        if len(participantes_actuales) % 2 != 0:
            print(f"Numero impar de ninjas ({len(participantes_actuales)}). Un ninja pasa automaticamente a la siguiente ronda.")
            siguiente_ronda.append(participantes_actuales.popleft())
        combates_ronda = []
        while len(participantes_actuales) >= 2:
            ninja1 = participantes_actuales.popleft()
            ninja2 = participantes_actuales.popleft()
            combates_ronda.append((ninja1, ninja2))
        for ninja1, ninja2 in combates_ronda:
            ganador = simular_combate(ninja1, ninja2)
            siguiente_ronda.append(ganador)
        participantes_actuales = deque(siguiente_ronda)
        ronda_idx += 1
    campeon = participantes_actuales[0] if participantes_actuales else None
    if campeon:
        print(f"\n ¡EL CAMPEON DEL TORNEO ES: {campeon.nombre}! ")
        print("\nHabilidades del campeon:")
        mostrar_habilidades_recorrido(campeon.arbol_habilidades, "preorden")
    else:
        print("\nNo se pudo determinar un campeon, insuficientes ninjas.")
    guardar_ninjas(dict(zip([n.nombre for n in ninjas_participantes], ninjas_participantes)))
    

if __name__ == "__main__":
    main()
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
    
