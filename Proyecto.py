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













































































def validar_solo_letras(mensaje):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print("⚠️ Error: La entrada no puede estar vacía. Por favor, intente de nuevo.")
        elif not re.fullmatch(r'[a-zA-Z\s]+', valor):
            print("⚠️ Error: Solo se permiten letras y espacios. Por favor, intente de nuevo.")
        else:
            return valor 



































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



def validar_ninja_existente(mensaje, ninjas_db):
    while True:
        nombre = validar_solo_letras(mensaje)
        if nombre in ninjas_db:
            return ninjas_db[nombre]
        else:
            print(f"⚠️ Ninja '{nombre}' no encontrado. Ninjas disponibles: {', '.join(ninjas_db.keys()) if ninjas_db else 'Ninguno'}. Intenta de nuevo.")





































































































































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
            