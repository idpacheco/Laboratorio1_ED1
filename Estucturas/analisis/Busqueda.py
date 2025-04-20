
from analisis.Archivos import obtenerCampo
import os
import linecache

#8. ¿Cómo implementarías una búsqueda binaria en un archivo secuencial ordenado?
def busquedaBinariaPopularidad(archivo, popularidad_buscada):
    linecache.clearcache()

    # Contar número total de líneas del archivo
    total_lineas = 0
    with open(archivo, "r", encoding="utf-8") as f:
        for _ in f:
            total_lineas += 1

    # Calcular cantidad de datos reales (descontando cabecera)
    total_datos = total_lineas - 4
    if total_datos <= 0:
        print("❌ No hay datos válidos para buscar.")
        return

    # Inicializar variables para búsqueda binaria
    inicio = 0
    fin = total_datos - 1
    encontrado = False

    while inicio <= fin:
        mitad = (inicio + fin) // 2
        linea_archivo = 5 + mitad  # Asumiendo que los datos comienzan en la línea 5
        linea = linecache.getline(archivo, linea_archivo).strip()

        # Depuración: Mostrar la línea que estamos procesando
        #print(f"\nBuscando popularidad: {popularidad_buscada}")
        #print(f"Línea actual: {linea} (Línea en el archivo: {linea_archivo})")

        # Limpiar espacios extra y caracteres no visibles
        linea_limpia = ''.join(linea.split())  # Elimina todos los espacios
        print(f"Línea limpia: {linea_limpia}")

        # Saltar líneas vacías o mal formateadas
        if not linea_limpia:
            print("⚠️ Línea vacía o mal formada.")
            inicio += 1
            continue

        try:
            # Limpiar el campo de la popularidad para eliminar posibles espacios extra
            popu_actual = int(obtenerCampo(linea, 4).strip())
        except:
            print("⚠️ Línea inválida:", linea)
            break

        # Depuración: Ver la popularidad que estamos procesando
        # print(f"Popularidad actual: {popu_actual}")

        # Mostrar los valores que estamos comparando
        # print(f"Comparando: popularidad_buscada ({popularidad_buscada}) con popu_actual ({popu_actual})")

        if popu_actual == popularidad_buscada:
            print("\n✅ Canción encontrada:")
            print(linea)
            encontrado = True

            # Buscar más coincidencias hacia la izquierda
            i = mitad - 1
            while i >= 0:
                linea_izq = 5 + i
                l_izq = linecache.getline(archivo, linea_izq).strip()
                if not l_izq:
                    break
                try:
                    popu_izq = int(obtenerCampo(l_izq, 4).strip())
                    if popu_izq == popularidad_buscada:
                        print("✅ Canción encontrada:")
                        print(l_izq)
                        i -= 1
                    else:
                        break
                except:
                    break

            # Buscar más coincidencias hacia la derecha
            i = mitad + 1
            while i < total_datos:
                linea_der = 5 + i
                l_der = linecache.getline(archivo, linea_der).strip()
                if not l_der:
                    break
                try:
                    popu_der = int(obtenerCampo(l_der, 4).strip())
                    if popu_der == popularidad_buscada:
                        print("✅ Canción encontrada:")
                        print(l_der)
                        i += 1
                    else:
                        break
                except:
                    break
            break

        # Lógica para archivos ordenados de mayor a menor
        elif popu_actual < popularidad_buscada:
            print(f"Ajustando el rango de búsqueda: fin = {mitad - 1}")
            fin = mitad - 1
        else:
            print(f"Ajustando el rango de búsqueda: inicio = {mitad + 1}")
            inicio = mitad + 1

        # Depuración: Mostrar los índices de búsqueda en cada paso
        print(f"Rango de búsqueda: inicio={inicio}, fin={fin}, mitad={mitad}")

    if not encontrado:
        print("❌ No se encontró ninguna canción con esa popularidad.")

    linecache.clearcache()



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
                print("Advertencia: no se pudo procesar esta línea.")

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
                print("Advertencia: no se pudo procesar esta línea.")
        return resultados
