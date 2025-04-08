def guardarCanciones (canciones, nombreArchivo):
    file=open(nombreArchivo, "w") #Crear el archivo y escribir sobre el archivo
    file.write("CANCIONES".center(100, "=") + "\n\n")
    # Encabezado
    file.write(f"{'ID':22} | {'Nombre':30} | {'Duración (ms)':13} | {'Popularidad':10} | Artistas\n")
    file.write("-" * 100 + "\n")
    
    for item in canciones:
        track = item['track']
        id_cancion = track['id']
        nombre = track['name']
        duracion = track['duration_ms']
        popularidad = track['popularity']

        artistas = [artista['name'] for artista in track['artists']]
        artistas_str = ", ".join(artistas)
        # Escribir en una línea todos los datos de la canción separados por |
        # Formato alineado
        file.write(f"{id_cancion:22} | {nombre:30} | {duracion:<13} | {popularidad:<10} | {artistas_str}\n")
    file.close()

def guardarArtistas (canciones, nombreArchivo):
    file=open(nombreArchivo, "w") #Crear el archivo y escribir sobre el archivo
    #un diccionario para agrupar al artista con las canciones
    #n diccionario puedes asociar una clave con un valor, y ese valor puede ser cualquier cosa: un número, una cadena, una lista, otro diccionario, etc.
    artistas_agrup = {}
    for item in canciones: 
        track= item['track']
        id_cancion = track['id']
        nombre_cancion = track['name']
        for artista in track ['artists']:
            nombre_artista= artista['name']
            if nombre_artista not in artistas_agrup:
                #si el artista no esta todavia guardado en el diccionario
                # entonces creale una lista vacía donde le vamos a meter las canciones
                artistas_agrup [nombre_artista]=[]
            artistas_agrup [nombre_artista].append(id_cancion)

    #Recorre el diccionario que se acabo de crear para ponerlo en el archivo
     # Escribimos un título centrado
    file.write("ARTISTAS".center(100, "=") + "\n\n")
        # Por cada artista en el diccionario
    for artista, canciones_ids in artistas_agrup.items():
        cantidad = len (canciones_ids)
        canciones_str = ", ".join(canciones_ids)
        linea = f"{artista} | {cantidad}| {canciones_str}\n"
        file.write(linea)

    file.close()
