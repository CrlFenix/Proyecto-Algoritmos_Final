import random
from collections import deque
import datetime
import re

HABILIDAD_DELIMITER = "|"

class NodoHabilidad:
    def __init__(self, nombre, puntos):
        self.nombre = nombre
        self.puntos = puntos
        self.izquierda = None
        self.derecha = None

    def to_string(self):
        left_str = self.izquierda.to_string() if self.izquierda else "None"
        right_str = self.derecha.to_string() if self.derecha else "None"
        return f"{self.nombre},{self.puntos}{HABILIDAD_DELIMITER}{left_str}{HABILIDAD_DELIMITER}{right_str}"
        
    @staticmethod
    def from_string(data_list):
        if not data_list or data_list[0] == "None":
            if data_list:
                data_list.pop(0)
            return None
        node_data = data_list.pop(0)
        parts = node_data.split(',')
        if len(parts) != 2:
            return None
            
        nodo = NodoHabilidad(parts[0], int(parts[1]))
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
        self.arbol_habilidades = None
    
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
        return f"{self.nombre}{HABILIDAD_DELIMITER}None"

    @staticmethod
    def from_file_string_basic(line):
        data = line.strip().split(',')
        if len(data) == 6:
            return Ninja(data[0], data[1], data[2], data[3], data[4], data[5])
        return None

    @staticmethod
    def from_habilidades_string(line):
        parts = line.strip().split(HABILIDAD_DELIMITER, 1)
        if len(parts) == 2:
            nombre_ninja = parts[0]
            habilidades_str = parts[1]
            if habilidades_str != "None":
                habilidades_list = habilidades_str.split(HABILIDAD_DELIMITER)
                arbol_habilidades = NodoHabilidad.from_string(habilidades_list)
                return nombre_ninja, arbol_habilidades
        return None, None

class Usuario:
    def __init__(self, nombres, identificacion, edad, email, password):
        self.nombres = nombres
        self.identificacion = identificacion
        self.edad = edad
        self.email = email
        self.password = password
        self.combates_ganados = 0
        self.combates_perdidos = 0
        
    def to_file_string(self):
        return f"{self.nombres},{self.identificacion},{self.edad},{self.email},{self.password},{self.combates_ganados},{self.combates_perdidos}"

def cargar_usuarios():
    usuarios = {}
    try:
        with open("usuarios.txt", "r") as f:
            for line in f:
                data = line.strip().split(',')
                if len(data) == 7:
                    user = Usuario(data[0], data[1], data[2], data[3], data[4])
                    user.combates_ganados = int(data[5])
                    user.combates_perdidos = int(data[6])
                    usuarios[user.email] = user
    except FileNotFoundError:
        pass
    return usuarios

def guardar_usuarios(usuarios):
    with open("usuarios.txt", "w") as f:
        for user in usuarios.values():
            f.write(user.to_file_string() + "\n")

def cargar_ninjas():
    ninjas = {}
    try:
        with open("ninjas.txt", "r") as f:
            for line in f:
                ninja = Ninja.from_file_string_basic(line)
                if ninja:
                    ninjas[ninja.nombre] = ninja
    except FileNotFoundError:
        pass
    
    try:
        with open("habilidades_ninja.txt", "r") as f:
            for line in f:
                nombre_ninja, arbol_habilidades = Ninja.from_habilidades_string(line)
                if nombre_ninja and nombre_ninja in ninjas:
                    ninjas[nombre_ninja].arbol_habilidades = arbol_habilidades
    except FileNotFoundError:
        pass

    return ninjas

def guardar_ninjas(ninjas):
    with open("ninjas.txt", "w") as f_ninjas, \
            open("habilidades_ninja.txt", "w") as f_habilidades:
        for ninja in ninjas.values():
            f_ninjas.write(ninja.to_file_string_basic() + "\n")
            f_habilidades.write(ninja.to_habilidades_string() + "\n")

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

def crear_arbol_habilidades_base():
    raiz = NodoHabilidad("Ataque Rapido", random.randint(5, 10))
    raiz.izquierda = NodoHabilidad("Golpe Fuerte", random.randint(5, 10))
    raiz.derecha = NodoHabilidad("Esquiva Veloz", random.randint(5, 10))
    raiz.izquierda.izquierda = NodoHabilidad("Barrido Bajo", random.randint(5, 10))
    raiz.izquierda.derecha = NodoHabilidad("Lanzamiento de shuriken", random.randint(5, 10))
    raiz.derecha.izquierda = NodoHabilidad("Bloqueo Alto", random.randint(5, 10))
    raiz.derecha.derecha = NodoHabilidad("Patada giratoria", random.randint(5, 10))
    return raiz

def sumar_habilidades(nodo):
    if nodo is None:
        return 0
    return (nodo.puntos + sumar_habilidades(nodo.izquierda) + sumar_habilidades(nodo.derecha))

def mostrar_habilidades_recorrido(nodo, tipo_recorrido="preorden", nivel=0):
    if nodo:
        if tipo_recorrido == "preorden":
            print("  " * nivel + f"- {nodo.nombre} ({nodo.puntos} pts)")
            mostrar_habilidades_recorrido(nodo.izquierda, tipo_recorrido, nivel + 1)
            mostrar_habilidades_recorrido(nodo.derecha, tipo_recorrido, nivel + 1)
        elif tipo_recorrido == "inorden":
            mostrar_habilidades_recorrido(nodo.izquierda, tipo_recorrido, nivel + 1)
            print("  " * nivel + f"- {nodo.nombre} ({nodo.puntos} pts)")
            mostrar_habilidades_recorrido(nodo.derecha, tipo_recorrido, nivel + 1)
        elif tipo_recorrido == "postorden":
            mostrar_habilidades_recorrido(nodo.izquierda, tipo_recorrido, nivel + 1)
            mostrar_habilidades_recorrido(nodo.derecha, tipo_recorrido, nivel + 1)
            print("  " * nivel + f"- {nodo.nombre} ({nodo.puntos} pts)")

def quick_sort_ninjas(ninjas_list, key="puntos_victoria"):
    if len(ninjas_list) <= 1:
        return ninjas_list
    pivot = ninjas_list[len(ninjas_list) // 2]
    left = [x for x in ninjas_list if getattr(x, key) > getattr(pivot, key)]
    middle = [x for x in ninjas_list if getattr(x, key) == getattr(pivot, key)]
    right = [x for x in ninjas_list if getattr(x, key) < getattr(pivot, key)]
    return quick_sort_ninjas(left, key) + middle + quick_sort_ninjas(right, key)

def busqueda_lineal_ninja(ninjas, query, by="nombre"):
    results = []
    for ninja in ninjas.values():
        if by == "nombre" and query.lower() in ninja.nombre.lower():
            results.append(ninja)
        elif by == "estilo" and query.lower() in ninja.estilo.lower():
            results.append(ninja)
    return results

def simular_combate(ninja1, ninja2, usuario_actual=None):
    print(f"\nCombate: {ninja1.nombre} vs {ninja2.nombre} ")
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
        print("Empate en puntos! El ganador se decidira al azar.")
        ganador = random.choice([ninja1, ninja2])
        perdedor = ninja1 if ganador == ninja2 else ninja2
    print(f"Ganador: {ganador.nombre}!")
    ganador.puntos_victoria += 1
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    combate_info = f"{ninja1.nombre} vs {ninja2.nombre} - Ganador: {ganador.nombre} - Fecha: {fecha}"
    if usuario_actual:
        if ganador.nombre == ninja1.nombre:
            usuario_actual.combates_ganados += 1
        else:
            usuario_actual.combates_perdidos += 1
        combate_info += f" - Jugador: {usuario_actual.email}"
        guardar_progreso_usuario(usuario_actual.email, usuario_actual.combates_ganados, usuario_actual.combates_perdidos)
    guardar_historial_combates(combate_info)
    return ganador

def simular_torneo(ninjas_participantes):
    print("\n--- COMIENZA EL TORNEO! ---")
    rondas_nombres = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final"]
    participantes_actuales = deque(ninjas_participantes[:])
    ronda_idx = 0
    while len(participantes_actuales) > 1:
        nombre_ronda = rondas_nombres[ronda_idx] if ronda_idx < len(rondas_nombres) else f"Ronda {ronda_idx + 1}"
        print(f"\n--- RONDA DE {nombre_ronda.upper()} ({len(participantes_actuales)} NINJAS) ---")
        siguiente_ronda = []
        if len(participantes_actuales) % 2 != 0:
            print(f"Numero impar de ninjas ({len(participantes_actuales)}). Un ninja pasa automaticamente a la siguiente ronda (BYE).")
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
        print(f"\nEL CAMPEON DEL TORNEO ES: {campeon.nombre}!")
        print("\nHabilidades del campeon:")
        mostrar_habilidades_recorrido(campeon.arbol_habilidades, "preorden")
    else:
        print("\nEl torneo no pudo determinar un campeon (tal vez no habia suficientes ninjas).")
    guardar_ninjas(dict(zip([n.nombre for n in ninjas_participantes], ninjas_participantes)))

def validar_entero(mensaje, min_val=None, max_val=None):
    while True:
        try:
            valor_str = input(mensaje)
            valor = int(valor_str)
            if min_val is not None and valor < min_val:
                print(f" Error: El valor debe ser mayor o igual a {min_val}. Por favor, intente de nuevo.")
            elif max_val is not None and valor > max_val:
                print(f" Error: El valor debe ser menor o igual a {max_val}. Por favor, intente de nuevo.")
            else:
                return valor
        except ValueError:
            print(" Error: Entrada invalida. Por favor, ingrese un numero entero.")

def validar_string_no_vacio(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        else:
            print(" Error: La entrada no puede estar vacia. Por favor, intente de nuevo.")

def validar_solo_letras(mensaje):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print(" Error: La entrada no puede estar vacia. Por favor, intente de nuevo.")
        elif not re.fullmatch(r'[a-zA-Z\s]+', valor):
            print(" Error: Solo se permiten letras y espacios. Por favor, intente de nuevo.")
        else:
            return valor

def validar_solo_numeros(mensaje):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            print(" Error: La entrada no puede estar vacia. Por favor, intente de nuevo.")
        elif not valor.isdigit():
            print(" Error: Solo se permiten numeros. Por favor, intente de nuevo.")
        else:
            return valor

def validar_email(mensaje, usuarios_db, es_registro=True):
    email_regex = re.compile(r'^[a-zA-Z]+\.[a-zA-Z]+@gmail\.com$')
    while True:
        email = input(mensaje).strip()
        if not email_regex.match(email):
            print(" Error: Formato de email invalido. Debe ser nombre.apellido@gmail.com. Por favor, intente de nuevo.")
        elif es_registro and email in usuarios_db:
            print(" Error: Ya existe un usuario con este email. Por favor, intente con otro.")
        elif not es_registro and email not in usuarios_db:
            print(" Error: Usuario no encontrado con este email. Por favor, verifique.")
        else:
            return email

def validar_password(mensaje):
    while True:
        password = input(mensaje)
        if len(password) < 8:
            print(" Error: La contrasena debe tener al menos 8 caracteres.")
        elif not any(char.isupper() for char in password):
            print(" Error: La contrasena debe contener al menos una letra mayuscula.")
        elif not any(char.isdigit() for char in password):
            print(" Error: La contrasena debe contener al menos un numero.")
        else:
            return password

def validar_ninja_existente(mensaje, ninjas_db):
    while True:
        nombre = validar_solo_letras(mensaje)
        if nombre in ninjas_db:
            return ninjas_db[nombre]
        else:
            print(f" Error: El ninja '{nombre}' no se encontro. Ninjas disponibles: {', '.join(ninjas_db.keys()) if ninjas_db else 'Ninguno'}. Por favor, intente de nuevo.")

def validar_ninja_diferente(mensaje, ninjas_db, ninja_excluido_nombre):
    while True:
        ninja = validar_ninja_existente(mensaje, ninjas_db)
        if ninja.nombre != ninja_excluido_nombre:
            return ninja
        else:
            print(f" Error: No puede seleccionar el mismo ninja. Por favor, elija un ninja diferente a '{ninja_excluido_nombre}'.")

def menu_administrador(ninjas_db, usuarios_db):
    while True:
        print("\n--- MENU DE ADMINISTRADOR ---")
        print("1. Agregar nuevo ninja")
        print("2. Listar ninjas (ordenados por puntos de victoria)")
        print("3. Consultar ninja (por nombre o estilo)")
        print("4. Organizar/Generar Arbol de Habilidades de un ninja")
        print("5. Mostrar clasificaciones y estadisticas del torneo")
        print("6. Salir")
        opcion = validar_string_no_vacio("Elija una opcion: ")
        if opcion == '1':
            nombre = validar_solo_letras("Nombre del ninja: ")
            if nombre in ninjas_db:
                print(f" Error: El ninja '{nombre}' ya existe. Intente con otro nombre.")
                continue
            fuerza = validar_entero("Fuerza (1-10): ", 1, 10)
            agilidad = validar_entero("Agilidad (1-10): ", 1, 10)
            resistencia = validar_entero("Resistencia (1-10): ", 1, 10)
            estilo = validar_string_no_vacio("Estilo de combate: ")
            nuevo_ninja = Ninja(nombre, fuerza, agilidad, resistencia, estilo)
            nuevo_ninja.arbol_habilidades = crear_arbol_habilidades_base()
            ninjas_db[nombre] = nuevo_ninja
            guardar_ninjas(ninjas_db)
            print(f" Ninja {nombre} agregado con exito y con arbol de habilidades base.")
        elif opcion == '2':
            if not ninjas_db:
                print("No hay ninjas registrados.")
                continue
            ninjas_ordenados = quick_sort_ninjas(list(ninjas_db.values()), key="puntos_victoria")
            print("\n--- CLASIFICACION DE NINJAS POR PUNTOS DE VICTORIA ---")
            for i, ninja in enumerate(ninjas_ordenados):
                print(f"{i+1}. {ninja.nombre} - Puntos de Victoria: {ninja.puntos_victoria}")
        elif opcion == '3':
            criterio = validar_string_no_vacio("Buscar por (nombre/estilo): ").lower()
            if criterio not in ["nombre", "estilo"]:
                print(" Error: Criterio de busqueda invalido. Debe ser 'nombre' o 'estilo'.")
                continue
            query = validar_string_no_vacio(f"Ingrese el {criterio} a buscar: ")
            resultados = busqueda_lineal_ninja(ninjas_db, query, by=criterio)
            if resultados:
                print("\n--- NINJAS ENCONTRADOS ---")
                for ninja in resultados:
                    print(ninja)
                    if ninja.arbol_habilidades:
                        print("Habilidades (Preorden):")
                        mostrar_habilidades_recorrido(ninja.arbol_habilidades, "preorden")
                    else:
                        print("Este ninja no tiene un arbol de habilidades.")
            else:
                print("No se encontraron ninjas con ese criterio.")
        elif opcion == '4':
            if not ninjas_db:
                print("No hay ninjas registrados para organizar habilidades.")
                continue
            ninja_a_actualizar = validar_ninja_existente("Ingrese el nombre del ninja para generar/organizar habilidades: ", ninjas_db)
            ninja_a_actualizar.arbol_habilidades = crear_arbol_habilidades_base()
            guardar_ninjas(ninjas_db)
            print(f" Arbol de habilidades para {ninja_a_actualizar.nombre} generado/actualizado.")
        elif opcion == '5':
            print("\n--- HISTORIAL DE COMBATES ---")
            historial = cargar_historial_combates()
            if historial:
                for combate in historial:
                    print(combate)
            else:
                print("No hay historial de combates.")
            print("\n--- CLASIFICACION ACTUAL DE NINJAS ---")
            if not ninjas_db:
                print("No hay ninjas para clasificar.")
                continue
            ninjas_ordenados = quick_sort_ninjas(list(ninjas_db.values()), key="puntos_victoria")
            for i, ninja in enumerate(ninjas_ordenados):
                print(f"{i+1}. {ninja.nombre} - Puntos de Victoria: {ninja.puntos_victoria}")
        elif opcion == '6':
            print(" Saliendo del menu de administrador.")
            break
        else:
            print(" Opcion invalida. Por favor, elija una opcion del 1 al 6.")

def menu_jugador(ninjas_db, usuarios_db):
    usuario_actual = None
    while True:
        print("\n--- MENU DE JUGADOR ---")
        print("1. Registrarse")
        print("2. Iniciar sesion")
        print("3. Salir")
        opcion = validar_string_no_vacio("Elija una opcion: ")
        if opcion == '1':
            nombres = validar_solo_letras("Nombres y apellidos: ")
            identificacion = validar_solo_numeros("Identificacion (solo numeros): ")
            edad = validar_entero("Edad: ", 1)
            email = validar_email("Email (formato nombre.apellido@gmail.com): ", usuarios_db, es_registro=True)
            password = validar_password("Contrasena (min. 8 caracteres, 1 mayuscula, 1 numero): ")
            nuevo_usuario = Usuario(nombres, identificacion, edad, email, password)
            usuarios_db[email] = nuevo_usuario
            guardar_usuarios(usuarios_db)
            print(" Registro exitoso. Bienvenido!")
        elif opcion == '2':
            email = validar_email("Email: ", usuarios_db, es_registro=False)
            password = validar_string_no_vacio("Contrasena: ")
            if email in usuarios_db and usuarios_db[email].password == password:
                usuario_actual = usuarios_db[email]
                print(f" Bienvenido, {usuario_actual.nombres}!")
                menu_jugador_logeado(ninjas_db, usuarios_db, usuario_actual)
                usuario_actual = None
            else:
                print(" Credenciales incorrectas. Verifique su email y contrasena.")
        elif opcion == '3':
            print(" Saliendo del menu de jugador.")
            break
        else:
            print(" Opcion invalida. Por favor, elija una opcion del 1 al 3.")

def menu_jugador_logeado(ninjas_db, usuarios_db, usuario_actual):
    while True:
        print(f"\n--- MENU DE JUGADOR ({usuario_actual.nombres}) ---")
        print("1. Ver arbol de habilidades de un ninja seleccionado")
        print("2. Simular combate uno vs uno contra otros ninjas")
        print("3. Simular un torneo completo de peleas")
        print("4. Consultar el ranking actualizado de ninjas")
        print("5. Ver progreso y historial de mis combates")
        print("6. Cerrar sesion")
        opcion = validar_string_no_vacio("Elija una opcion: ")
        if opcion == '1':
            if not ninjas_db:
                print("No hay ninjas registrados para ver sus habilidades.")
                continue
            ninja = validar_ninja_existente("Ingrese el nombre del ninja para ver sus habilidades: ", ninjas_db)
            if ninja.arbol_habilidades:
                print(f"\n--- ARBOL DE HABILIDADES DE {ninja.nombre} (PREORDEN) ---")
                mostrar_habilidades_recorrido(ninja.arbol_habilidades, "preorden")
                print(f"Puntos totales de habilidades: {sumar_habilidades(ninja.arbol_habilidades)}")
            else:
                print("Este ninja aun no tiene un arbol de habilidades asignado.")
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
            num_ninjas = len(ninjas_db)
            if not (num_ninjas > 0 and (num_ninjas & (num_ninjas - 1) == 0)):
                print(f"Actualmente hay {num_ninjas} ninjas. Para un torneo optimo, la cantidad de ninjas deberia ser una potencia de 2 (2, 4, 8, etc.).")
                confirmar = validar_string_no_vacio("Desea continuar con el torneo con la cantidad actual de ninjas (algunos podrian tener BYE)? (s/n): ").lower()
                if confirmar != 's':
                    continue
            ninjas_para_torneo = list(ninjas_db.values())
            random.shuffle(ninjas_para_torneo)
            simular_torneo(ninjas_para_torneo)
            guardar_ninjas(ninjas_db)
            print(" Torneo simulado y rankings actualizados.")
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
            print(" Cerrando sesion.")
            break
        else:
            print(" Opcion invalida. Por favor, elija una opcion del 1 al 6.")

def main():
    ninjas_db = cargar_ninjas()
    usuarios_db = cargar_usuarios()
    if not ninjas_db:
        print("Creando ninjas de ejemplo...")
        nombres_ejemplo = ["Kyo", "Iori", "May", "Ryu", "Benimaru", "Leona", "Clark", "Atena"]
        for nombre in nombres_ejemplo:
            fuerza = random.randint(5, 10)
            agilidad = random.randint(5, 10)
            resistencia = random.randint(5, 10)
            estilo = random.choice(["Fuego", "Agua", "Viento", "Tierra", "Electrico"])
            ninja = Ninja(nombre, fuerza, agilidad, resistencia, estilo)
            ninja.arbol_habilidades = crear_arbol_habilidades_base()
            ninjas_db[nombre] = ninja
        guardar_ninjas(ninjas_db)
        print(" Ninjas de ejemplo creados y guardados.")
    print("\nBienvenido al Sistema de Gestion de Ninjas y Combates!")
    while True:
        print("\n--- SELECCION DE ROL ---")
        print("1. Administrador")
        print("2. Jugador")
        print("3. Salir")
        rol_opcion = validar_string_no_vacio("Elija su rol: ")
        if rol_opcion == '1':
            admin_user = "admin"
            admin_pass = "admin123"
            user_input = validar_string_no_vacio("Usuario administrador: ").lower()
            pass_input = validar_string_no_vacio("Contrasena: ").lower()
            if user_input == admin_user and pass_input == admin_pass:
                menu_administrador(ninjas_db, usuarios_db)
            else:
                print(" Credenciales de administrador incorrectas.")
        elif rol_opcion == '2':
            menu_jugador(ninjas_db, usuarios_db)
        elif rol_opcion == '3':
            print("Gracias por usar el sistema! Hasta la proxima.")
            break
        else:
            print(" Opcion invalida. Por favor, elija una opcion del 1 al 3.")

if __name__ == "__main__":
    main()