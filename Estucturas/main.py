from SpotifyAPI import getAccessToken, getPlayList
from Archivos import guardarCanciones, guardarArtistas
from Analisis import artistaMasCanciones, promedioBytes, buscarCancionesArtista
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

guardarCanciones(playlist['tracks']['items'], "canciones.txt")
archivo_canciones = "canciones.txt"  # o el nombre que le diste

guardarArtistas(playlist['tracks']['items'], "artistas.txt")
archivo_artistas = "artistas.txt"  # o el nombre que le diste

artista, cantidad = artistaMasCanciones(archivo_artistas)
print(f"🎤 El artista con más canciones es: {artista} con {cantidad} canciones.")

promedioArchivo1 =promedioBytes (archivo_artistas)
print(f"📊 El tamaño promedio de {archivo_artistas}  por registro es: {promedioArchivo1:.2f} bytes.")

promedioArchivo2 =promedioBytes (archivo_canciones)
print(f"📊 El tamaño promedio de {archivo_canciones} por registro es: {promedioArchivo2:.2f} bytes.")

artista_buscado = "Niall Horan"
total = buscarCancionesArtista(archivo_canciones, artista_buscado)
print(f"🎵 Total de canciones de '{artista_buscado}': {total}")