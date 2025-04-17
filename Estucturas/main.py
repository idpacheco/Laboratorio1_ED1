from SpotifyAPI import getAccessToken, getPlayList, obtenerDatosDesdeSpotify, construirLineaCancion
from Archivos import guardarCanciones, guardarArtistas

from analisis.Artistas import artistaMasCanciones, artistaMasPopular
from analisis.Canciones import promedioDuracion, mayorAlpromedio, buscarCancionesArtista
from analisis.Archivos import promedioBytes, obtenerCampo
from analisis.Ordenamiento import ordenarPorPopularidad, insertarCancionOrdenada

import os  

#Estas dos variables son para identificar a la app que quiere acceder a los datos de spotify
client_id= "d6d0ada48ab5470b8751788ecf8624c8"
client_secret="ac7a2ed9117241e7adb9ea2418b2371f"

# Paso 1: Obtener el token
token = getAccessToken(client_id, client_secret)

# Paso 2: Obtener la playlist
playlist = getPlayList(token, "1iFJnL9bCaSkDRMua0gMGY")

# Imprimir canciones
def printTrackNames(playlist_json):
    try:
        items = playlist_json['tracks']['items']
        print("Canciones en la playlist:")
        for i, item in enumerate(items, start=1):
            print(f"{i}. {item['track']['name']}")
    except Exception as e:
        print("Error al imprimir canciones:", e)

printTrackNames(playlist)

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
#archivo_canciones = "canciones.txt"  # o el nombre que le diste

guardarArtistas(playlist['tracks']['items'], archivo_artistas, token)
#archivo_artistas = "artistas.txt"  # o el nombre que le diste

artista, cantidad = artistaMasCanciones(archivo_artistas)
print(f"🎤 El artista con más canciones es: {artista} con {cantidad} canciones.")

promedioArchivo1 =promedioBytes (archivo_artistas)
print(f"📊 El tamaño promedio de {archivo_artistas}  por registro es: {promedioArchivo1:.2f} bytes.")

promedioArchivo2 =promedioBytes (archivo_canciones)
print(f"📊 El tamaño promedio de {archivo_canciones} por registro es: {promedioArchivo2:.2f} bytes.")

artista_buscado = "Niall Horan"
total = buscarCancionesArtista(archivo_canciones, artista_buscado)
print(f"🎵 Total de canciones de '{artista_buscado}': {total}")

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

id_usuario = input("🆔 Ingresa el ID de la canción a añadir: ")

# Buscar datos reales en la API
datos_cancion = obtenerDatosDesdeSpotify(id_usuario)

# Convertirlo a una línea
if datos_cancion:
    linea_cancion = construirLineaCancion(datos_cancion)
    print(linea_cancion)
    insertarCancionOrdenada("canciones_ordenadas.txt", linea_cancion, 4)
else:
    print("❌ No se pudo obtener datos de la canción. Verifica el ID o las credenciales.")

