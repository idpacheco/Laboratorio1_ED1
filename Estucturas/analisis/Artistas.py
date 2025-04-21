
from analisis.Archivos import obtenerCampo

#1. ¿Qué artista tiene mayor número de canciones en la playlist?
def artistaMasCanciones(nombre_archivo):
    max_artista = None
    max_canciones = 0
    file = open(nombre_archivo, "r",encoding="utf-8")

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
        max_artista = None
        max_popularidad = -1  # Inicializamos con un valor imposible de popularidad

        with open(nombre_archivo, "r",encoding="utf-8") as f:
            # Saltamos las primeras 4 líneas si son encabezados
            for _ in range(4):
                next(f)
            
            # Iteramos sobre cada línea del archivo
            for linea in f:
                if "|" in linea:
                    linea = linea.strip()
                    
                    # Obtenemos los campos de artista y popularidad
                    artista = obtenerCampo(linea, 1).strip()
                    popularidad_str = obtenerCampo(linea, 2).strip()
                    
                    # Convertimos la popularidad a entero
                    popularidad = int(popularidad_str)
                    
                    # Verificamos si esta popularidad es mayor que la máxima encontrada
                    if popularidad > max_popularidad:
                        max_popularidad = popularidad
                        max_artista = artista

        print(f"El artista más popular es: {max_artista} con una popularidad de {max_popularidad}")
        return max_artista, max_popularidad
    except Exception as e:
        print("Error al buscar artista con mayor índice de popularidad:", e)
        return None