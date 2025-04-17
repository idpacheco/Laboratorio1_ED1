
from analisis.Archivos import obtenerCampo

#8. ¿Cómo implementarías una búsqueda binaria en un archivo secuencial ordenado?
def busquedaBinariaPorPopularidad(archivo, popularidad_buscada):
    encontrado = False

    with open(archivo, "r", encoding="utf-8") as file:
        # Saltar las primeras 4 líneas del encabezado decorativo
        for _ in range(4):
            next(file)

        print("🔍 Buscando canciones con popularidad:", popularidad_buscada)
        print()

        for linea in file:
            if linea.strip() == "" or "-" in linea:
                continue  # Saltar líneas vacías o divisores

            try:
                # Extraer los campos usando obtenerCampo
                id_cancion = obtenerCampo(linea, 1)
                nombre = obtenerCampo(linea, 2)
                duracion = obtenerCampo(linea, 3)
                popularidad = int(obtenerCampo(linea, 4))  # Convertir a entero
                artistas = obtenerCampo(linea, 5)

                if popularidad == popularidad_buscada:
                    encontrado = True
                    print("🎵 Nombre:", nombre)
                    print("🆔 ID:", id_cancion)
                    print("⏱️ Duración (ms):", duracion)
                    print("🔥 Popularidad:", popularidad)
                    print("👤 Artistas:", artistas)
                    print("-" * 60)

            except Exception as e:
                print("⚠️ Advertencia: no se pudo procesar esta línea.")
                print(linea.strip())
                print("Error:", e)

    if not encontrado:
        print("❌ No se encontró una canción con esa popularidad.")


#9. Propón una estructura de archivos de índices para acelerar las búsquedas por artista sin perder el enfoque secuencial.
def Indice(ruta_archivo):
    indice_artistas = {}
    canciones = []

    with open(ruta_archivo, "r", encoding="utf-8") as file:
        for _ in range(4):  # Saltar cabecera decorativa
            next(file)

        for linea in file:
            try:
                artistas = obtenerCampo(linea, 5).strip().split(", ")
                for artista in artistas:
                    if artista not in indice_artistas:
                        indice_artistas[artista] = []
                    indice_artistas[artista].append(linea)
                canciones.append(linea)
            except:
                print("⚠️ Advertencia: no se pudo procesar esta línea.")

    return indice_artistas, canciones

def buscarPorArtista(nombre_artista, indice, canciones):
    # Convertimos el nombre del artista a minúsculas para hacer la búsqueda insensible a mayúsculas
    nombre_artista = nombre_artista.lower()
    
    if nombre_artista in indice:
        return indice[nombre_artista]
    else:
        # Recorrer las canciones y buscar los artistas que contengan el nombre buscado
        resultados = []
        for cancion in canciones:
            try:
                artistas = obtenerCampo(cancion, 5).strip().lower().split(", ")
                # Si el artista está en la lista de artistas de la canción, lo añadimos
                if any(nombre_artista in artista for artista in artistas):
                    resultados.append(cancion)
            except:
                print("⚠️ Advertencia: no se pudo procesar esta línea.")
        return resultados
