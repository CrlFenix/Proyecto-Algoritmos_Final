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