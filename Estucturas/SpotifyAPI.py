import spotipy # type: ignore #Esto es para poder usar la API de spotify
import requests # type: ignore #Esto es para poderle solicitar los datos a la API
from spotipy.oauth2 import SpotifyClientCredentials

#Estas dos variables son para identificar a la app que quiere acceder a los datos de spotify
client_id= "5559ed36d1ff443db1bbc23292aee25a"
client_secret="65e6d5480a3c46be890d01dc216308fe"

def getAccessToken(client_id: str, client_secret: str):
    try:
        res = requests.post("https://accounts.spotify.com/api/token", 
                            headers={"Content-Type": "application/x-www-form-urlencoded"}, 
                            data={"grant_type": "client_credentials",
                                  "client_id": client_id,
                                  "client_secret": client_secret 
                                  })
        return res.json()['access_token']
        
    except Exception as e:
        print(e)
token = getAccessToken(client_id, client_secret)
import requests

def getPlayList(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    all_tracks = []
    offset = 0
    limit = 100  # Spotify API permite un máximo de 100 canciones por solicitud

    while True:
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error al obtener la playlist: {response.status_code}")
            break

        data = response.json()
        tracks = data.get("items", [])
        all_tracks.extend(tracks)

        # Verificar si hay más canciones
        if len(tracks) < limit:
            break

        offset += limit

    return {"tracks": {"items": all_tracks}}


def obtenerDatosDesdeSpotify(id_cancion):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

        # Obtener datos de la canción
        track = sp.track(id_cancion)
        datos = {
            "id": track["id"],
            "nombre": track["name"],
            "duracion": track["duration_ms"],
            "popularidad": track["popularity"],
            "artista": ", ".join([artista["name"] for artista in track["artists"]]),
        }
        return datos
    except Exception as e:
        print(f"❌ Error al obtener datos desde Spotify: {e}")
        return None
# Convertir los datos en una línea estilo archivo
def construirLineaCancion(datos):
    return f"{datos['id']}|{datos['nombre']}|{datos['duracion']}|{datos['popularidad']}|{datos['artista']}|\n"
