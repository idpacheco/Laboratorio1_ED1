import time
import requests
def guardarCanciones(canciones, nombreArchivo):
    with open(nombreArchivo, "w", encoding="utf-8") as file:
        file.write("CANCIONES".center(100, "=") + "\n\n")
        file.write(f"{'ID':22} | {'Nombre':30} | {'Duración (ms)':13} | {'Popularidad':10} | Artistas\n")
        file.write("-" * 100 + "\n")

        for index, item in enumerate(canciones, start=1):
            try:
                # verifica si item es None o no tiene 'track'
                if item is None or 'track' not in item or item['track'] is None:
                    raise ValueError(f"Track en item #{index} es None o no existe.")

                track = item['track']

                id_cancion = track['id']
                nombre = track['name']
                duracion = track['duration_ms']
                popularidad = track['popularity']

                artistas = [artista['name'] for artista in track['artists']]
                artistas_str = ", ".join(artistas)

                file.write(f"{id_cancion:22} | {nombre:30} | {duracion:<13} | {popularidad:<10} | {artistas_str}\n")

            except Exception as e:
                print(f"⚠️ Error en la canción #{index}: {e}")
                continue  # Salta y sigue con la siguiente canción.


# los datos que se obtienen de los artistas son limitados (nombre, ID, etc.), pero no incluyen la popularidad del artista.
def getPopularidadArtista(artist_id, token):  # La única forma de obtener el campo 'popularidad' de un artista es haciendo una solicitud directa al endpoint del artista.
    try:
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json().get("popularity", 0)
        else:
            print(f"Error al obtener artista {artist_id}: {res.status_code}")
            return 0
    except Exception as e:
        print(f"Error al obtener popularidad del artista: {e}")
        return 0

def guardarArtistas(canciones, nombreArchivo, token):
    file = open(nombreArchivo, "w", encoding="utf-8")  # Crear el archivo y escribir sobre el archivo

    artistas_agrup = {}
    popularidades = {}  # caché de popularidades

    for index, item in enumerate(canciones, start=1):
        try:
            if item is None or 'track' not in item or item['track'] is None:
                raise ValueError(f"Track en item #{index} es None o no existe.")

            track = item['track']
            id_cancion = track['id']

            for artista in track['artists']:
                nombre_artista = artista['name']
                id_artista = artista['id']

                if nombre_artista not in artistas_agrup:
                    artistas_agrup[nombre_artista] = {
                        'id': id_artista,
                        'canciones': []
                    }

                artistas_agrup[nombre_artista]['canciones'].append(id_cancion)

        except Exception as e:
            print(f"⚠️ Error en item #{index}: {e}")
            continue  # salta al siguiente item y no rompe

    # Escribir encabezados
    file.write("ARTISTAS".center(120, "=") + "\n\n")
    file.write(f"{'Artista':30} | {'Popularidad':12} | {'# Canciones':12} | Canciones\n")
    file.write("-" * 120 + "\n")

    for artista, datos in artistas_agrup.items():
        id_artista = datos['id']
        canciones_ids = datos['canciones']

        # Obtener popularidad (con caché y pausa para evitar 429)
        if id_artista not in popularidades:
            popularidades[id_artista] = getPopularidadArtista(id_artista, token)
            time.sleep(0.3)  # pausa para no saturar Spotify API

        popularidad = popularidades[id_artista]
        cantidad = len(canciones_ids)
        canciones_str = ", ".join(canciones_ids)

        linea = f"{artista:30} | {popularidad:<12} | {cantidad:<12} | {canciones_str}\n"
        file.write(linea)

    file.close()
