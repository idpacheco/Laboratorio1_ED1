
from analisis.Archivos import obtenerCampo
def artistaMasCanciones (nombre_archivo):
    max_artista =None
    max_canciones = 0
    file = open (nombre_archivo, "r")
    for _ in range(4):  # Saltar las primeras 4 líneas decorativas
            next(file)

    for linea in file:
        if "|" in linea:
            #lista o vector que contiene los fragmentos del texto que estaban separados con |
            partes = linea.strip().split("|")  
            #divide la linea eliminando los espacios y dividiendola en subcadenas
            artista = partes [0].strip()
            popularidad = partes[1].strip()
            cantidad = int (partes [2].strip())
            canciones = partes [3].strip()
            if cantidad> max_canciones:
                max_canciones = cantidad
                max_artista = artista

    return max_artista, max_canciones

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
