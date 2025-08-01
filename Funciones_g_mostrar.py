def guardar_ninjas(ninjas):
    with open("ninjas.txt", "w") as f_ninjas, \
         open("habilidades_ninja.txt", "w") as f_habilidades:
        for ninja in ninjas.values():
            f_ninjas.write(ninja.to_file_string_basic() + "\n")
            f_habilidades.write(ninja.to_habilidades_string() + "\n")

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