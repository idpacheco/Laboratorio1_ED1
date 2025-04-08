import requests # type: ignore #Esto es para poderle solicitar los datos a la API

#Estas dos variables son para identificar a la app que quiere acceder a los datos de spotify
client_id= "d6d0ada48ab5470b8751788ecf8624c8"
client_secret="ac7a2ed9117241e7adb9ea2418b2371f"

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

def getPlayList(access_token: str, playlist_id):
    try:
        return requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", 
                            headers={"Authorization": f"Bearer {access_token}"}).json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

playlist = getPlayList(token, "1iFJnL9bCaSkDRMua0gMGY")