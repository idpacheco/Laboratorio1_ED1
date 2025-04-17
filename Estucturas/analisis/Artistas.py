
from analisis.Archivos import obtenerCampo

#1. ¿Qué artista tiene mayor número de canciones en la playlist?
def artistaMasCanciones(nombre_archivo):
    max_artista = None
    max_canciones = 0
    file = open(nombre_archivo, "r")

    for _ in range(4):  # Saltar cabecera decorativa
        next(file)

    for linea in file:
        if "|" in linea:
            linea = linea.strip()

            artista = obtenerCampo(linea, 1).strip()
            popularidad = obtenerCampo(linea, 2).strip()
            cantidad_str = obtenerCampo(linea, 3).strip()
            canciones = obtenerCampo(linea, 4).strip()

            cantidad = int(cantidad_str)

            if cantidad > max_canciones:
                max_canciones = cantidad
                max_artista = artista

    file.close()
    return max_artista, max_canciones


#2. ¿Qué artista tiene mayor índice de popularidad?
def artistaMasPopular(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as f:
            # Saltamos las primeras 4 líneas si son encabezados
            for _ in range(4):
                next(f)
            
            # Leemos la primera línea después de los encabezados
            linea = next(f, None)  # Usamos next para leer la siguiente línea de manera segura
            if linea:
                #se obtienen los campos de artista y popularidad
                max_artista = obtenerCampo(linea, 1)  # El nombre del artista
                max_popularidad = obtenerCampo(linea, 2) # La popularidad 

                # Como el archivo está ordenado, ya no necesitamos continuar
                print(f"El artista más popular es: {max_artista} con una popularidad de {max_popularidad}")
    except Exception as e:
        print("Error al buscar artista con mayor índice de popularidad:", e)
        return None
