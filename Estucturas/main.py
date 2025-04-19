from SpotifyAPI import getAccessToken, getPlayList, obtenerDatosDesdeSpotify, construirLineaCancion
from Archivos import guardarCanciones, guardarArtistas

from analisis.Artistas import artistaMasCanciones, artistaMasPopular
from analisis.Busqueda import Indice, buscarPorArtista, busquedaBinariaPopularidad
from analisis.Canciones import  mayorAlpromedio, buscarCancionesArtista, promedioDuracion
from analisis.Archivos import promedioBytes, obtenerCampo
from analisis.Ordenamiento import ordenarPorPopularidad, insertarCancionOrdenada

import os  

#Estas dos variables son para identificar a la app que quiere acceder a los datos de spotify
client_id= "5559ed36d1ff443db1bbc23292aee25a"
client_secret="65e6d5480a3c46be890d01dc216308fe"

# Obtener el token
token = getAccessToken(client_id, client_secret)

#Obtener la playlist
playlist = getPlayList(token, "5QHM2JUuKvFRFiRhOJx67p")
# Imprimir canciones
def printTrackNames(playlist_json):
    try:
        items = playlist_json['tracks']['items']
        print("Canciones en la playlist:")
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item['track']['name']}")
    except Exception as e:
        print("Error al imprimir canciones:", e)

# Crear la carpeta para los archivos generados si no existe
output_folder = "archivos_generados"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Actualizar las rutas de los archivos
archivo_canciones = os.path.join(output_folder, "canciones.txt")
archivo_artistas = os.path.join(output_folder, "artistas.txt")
archivo_canciones_ordenadas = os.path.join(output_folder, "canciones_ordenadas.txt")
archivo_artistas_ordenados = os.path.join(output_folder, "artistas_ordenados.txt")


guardarCanciones(playlist['tracks']['items'], archivo_canciones)
#archivo_canciones = "canciones.txt"

guardarArtistas(playlist['tracks']['items'], archivo_artistas, token)
#archivo_artistas = "artistas.txt"  

artista, cantidad = artistaMasCanciones(archivo_artistas)
print(f"El artista con más canciones es: {artista} con {cantidad} canciones.")

promedioArchivo1 =promedioBytes (archivo_artistas)
print(f"El tamaño promedio de {archivo_artistas}  por registro es: {promedioArchivo1:.2f} bytes.")

promedioArchivo2 =promedioBytes (archivo_canciones)
print(f"El tamaño promedio de {archivo_canciones} por registro es: {promedioArchivo2:.2f} bytes.")

artista_buscado =input ("Escriba el nombre del artista que desea buscar:")
total = buscarCancionesArtista(archivo_canciones, artista_buscado)
print(f" Total de canciones de '{artista_buscado}': {total}")

cont = mayorAlpromedio(archivo_canciones)
print(f"Hay '{cont}' canciones con mayor duración al promedio")

ordenarPorPopularidad(
    archivo_canciones,
    archivo_canciones_ordenadas,
    4,
    "CANCIONES ORDENADAS POR POPULARIDAD",
    f"{'ID':22} | {'Nombre':30} | {'Duración (ms)':13} | {'Popularidad':10} | Artistas"
)

ordenarPorPopularidad(
    archivo_artistas,
    archivo_artistas_ordenados,
    2,
    "ARTISTAS ORDENADOS POR POPULARIDAD",
    f"{'Artista':30} | {'Popularidad':12} | {'# Canciones':12} | Canciones"
)
artistaMasPopular(archivo_artistas)

continuar = True
while continuar== True:
    id_usuario = input("Ingresa el ID de la canción a añadir: ")
    
    # Obtener datos desde la API
    datos_cancion = obtenerDatosDesdeSpotify(id_usuario)

    if not os.path.exists(archivo_canciones_ordenadas):
        print(f"El archivo {archivo_canciones_ordenadas} no existe. Creándolo...")
        with open(archivo_canciones_ordenadas, 'w', encoding="ISO-8859-1") as archivo:
            archivo.write("")  # Crear el archivo vacío

    if datos_cancion:
        artistas_str = datos_cancion['artista']
        linea_cancion = f"{datos_cancion['id']:22} | {datos_cancion['nombre']:30} | {datos_cancion['duracion']:<13} | {datos_cancion['popularidad']:<10} | {artistas_str}\n"
        print("✅ Canción obtenida:")
        print(linea_cancion)
        insertarCancionOrdenada(archivo_canciones_ordenadas, linea_cancion, 4)
    else:
        print("❌ No se pudo obtener datos de la canción. Verifica el ID o las credenciales.")

    respuesta = input("¿Deseas continuar? (sí/no): ").strip().lower()
    if respuesta in ["no", "n"]:
        continuar = False


#Ejemplo de busqueda binaria por popularidad
popu = int(input("Ingresa la popularidad de la canción a buscar: "))
busquedaBinariaPopularidad(archivo_canciones_ordenadas, popu)

indice, canciones= Indice(archivo_canciones_ordenadas) #devuelve tanto indice como canciones
artista = input("Ingresa el nombre del artista a buscar: ")
resultados = buscarPorArtista(artista, indice, canciones)

if resultados:
    print("\n🎵 Canciones encontradas:")
    for cancion in resultados:
        print(cancion)
else:
    print("No se encontraron canciones para ese artista.")

