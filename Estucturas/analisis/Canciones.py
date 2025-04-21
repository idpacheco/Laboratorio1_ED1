from analisis.Archivos import obtenerCampo

#5. ¿Qué canciones tienen una duración superior al promedio de duración de todas las canciones en la playlist? 
def promedioDuracion(nombre_archivo):
    total_duracion = 0
    total_canciones = 0
    linea_num = 0

    with open(nombre_archivo, "r", encoding="utf-8") as file:
        for _ in range(4):  # Saltar las primeras 4 líneas
            next(file)
            linea_num += 1

        for linea in file:
            linea_num += 1
            if "|" in linea: 
                if linea.endswith("\n"): 
                    linea = linea[:-1]  
                duracion_str = obtenerCampo(linea, 3).strip().strip('.')

                try:
                    duracion = float(duracion_str)
                    total_duracion += duracion
                    total_canciones += 1
                except ValueError:
                    print(f"⚠️ Línea {linea_num}: '{duracion_str}' no es un número. Línea saltada.")
                    continue  # Salta a la siguiente sin romper

    if total_canciones == 0:
        return 0  # evitar división por cero si todo es inválido

    return total_duracion / total_canciones


def mayorAlpromedio(nombre_archivo):
    promedio = promedioDuracion(nombre_archivo)
    cont = 0
    linea_num = 0

    print(f"🎶 Canciones con duración mayor al promedio ({promedio:.2f} ms):")
    with open(nombre_archivo, "r", encoding="utf-8") as file:
        for _ in range(4):  # Saltar encabezado
            next(file)
            linea_num += 1

        for linea in file:
            linea_num += 1
            if linea.endswith("\n"):
                linea = linea[:-1]

            duracioncancion_str = obtenerCampo(linea,3).strip().strip('.')

            try:
                duracioncancion = float(duracioncancion_str)
            except ValueError:
                print(f"⚠️ Línea {linea_num}: '{duracioncancion_str}' inválida. Saltando...")
                continue  # Salta la línea con error

            cancionName = obtenerCampo(linea,2).strip()
            if duracioncancion > promedio:
                print(f"- {cancionName} ({duracioncancion} ms)")
                cont += 1

    if cont == 0:    
        print("No hay canciones con duración mayor al promedio.")
    return cont
 

#4. ¿Cuántas operaciones de lectura son necesarias para encontrar todas las canciones de un artista específico?
def buscarCancionesArtista(nombre_archivo, artista_buscado):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as f:
            count = 0    # Cantidad de canciones encontradas
            lecturas = 0   # Cantidad de líneas leídas (operaciones de lectura)

            for linea in f:
                lecturas += 1
                if artista_buscado.lower() in linea.lower():
                    count += 1 

        print(f"Se realizaron {lecturas} operaciones de lectura.")
        return count
    except Exception as e:
        print("error al buscar canciones: ", e)
        return 0
