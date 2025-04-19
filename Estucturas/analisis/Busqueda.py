
from analisis.Archivos import obtenerCampo
import os
import linecache

#8. ¿Cómo implementarías una búsqueda binaria en un archivo secuencial ordenado?
import linecache

def busquedaBinariaPopularidad(archivo, popularidad_buscada):
    import os

    # Paso 1: contar total de líneas de datos (excluyendo encabezado)
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    total_lineas = len(lineas) - 4  # excluye encabezado decorativo

    inicio = 5  # línea real donde empieza el contenido (línea 0 es la primera)
    fin = inicio + total_lineas - 1
    encontrado = False

    while inicio <= fin:
        mitad = (inicio + fin) // 2
        linea = linecache.getline(archivo, mitad).strip()

        if not linea or "-" in linea:
            inicio += 1
            continue

        try:
            popu_actual = int(obtenerCampo(linea, 4).strip())
        except:
            print("⚠️ Línea inválida:", linea)
            break

        if popu_actual == popularidad_buscada:
            print("\n✅ Canción encontrada:")
            print(linea)
            encontrado = True

            # Busca en la mitad izquierda (de forma binaria)
            izq_inicio, izq_fin = inicio, mitad - 1
            while izq_inicio <= izq_fin:
                izq_mitad = (izq_inicio + izq_fin) // 2
                linea_izq = linecache.getline(archivo, izq_mitad).strip()

                if not linea_izq or "-" in linea_izq:
                    izq_inicio = izq_mitad + 1
                    continue

                try:
                    popu_izq = int(obtenerCampo(linea_izq, 4).strip())
                    if popu_izq == popularidad_buscada:
                        print("✅ Canción encontrada:")
                        print(linea_izq)
                        izq_fin = izq_mitad - 1
                    else:
                        break
                except:
                    break
                izq_inicio = izq_mitad + 1

            # Busca en la mitad derecha (de forma binaria)
            der_inicio, der_fin = mitad + 1, fin
            while der_inicio <= der_fin:
                der_mitad = (der_inicio + der_fin) // 2
                linea_der = linecache.getline(archivo, der_mitad).strip()

                if not linea_der or "-" in linea_der:
                    der_fin = der_mitad - 1
                    continue

                try:
                    popu_der = int(obtenerCampo(linea_der, 4).strip())
                    if popu_der == popularidad_buscada:
                        print("✅ Canción encontrada:")
                        print(linea_der)
                        der_inicio = der_mitad + 1
                    else:
                        break
                except:
                    break
                der_fin = der_mitad - 1
            break

        elif popu_actual < popularidad_buscada:
            inicio = mitad + 1
        else:
            fin = mitad - 1

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
