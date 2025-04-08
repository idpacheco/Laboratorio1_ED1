def artistaMasCanciones (nombre_archivo):
    max_artista =None
    max_canciones = 0
    file = open (nombre_archivo, "r")
    for linea in file:
        if "|" in linea:
            #lista o vector que contiene los fragmentos del texto que estaban separados con |
            partes = linea.strip().split("|")  
            #divide la linea eliminando los espacios y dividiendola en subcadenas
            artista = partes [0].strip()
            cantidad = int (partes [1].strip())
            canciones = partes [2].strip()
            if cantidad> max_canciones:
                max_canciones = cantidad
                max_artista = artista

    return max_artista, max_canciones

def promedioBytes(nombre_archivo):
    total_bytes = 0
    total_registros = 0
    # Abrir el archivo en modo lectura binaria para calcular el tamaño real en bytes
    file = open(nombre_archivo, "rb")  #"rb"
    for linea in file:
            # Contamos la línea completa como un registro
            linea = linea.strip()
            if b"|" in linea:  # solo si es un registro válido
                total_bytes += len(linea)  # Tamaño total de la línea en bytes
                total_registros += 1       # Cuenta el número de registros

    if total_registros > 0:
       return  total_bytes / total_registros
       
    else:
        return 0

def buscarCancionesArtista(nombre_archivo, artista_buscado):
    try:
        with open(nombre_archivo, "r") as f:
            count = 0    # Cantidad de canciones encontradas
            lecturas = 0   # Cantidad de líneas leídas (operaciones de lectura)

            for linea in f:
                lecturas += 1
                if artista_buscado.lower() in linea.lower():
                    count += 1

        print(f"Se realizaron {lecturas} operaciones de lectura.")
        return count
    except Exception as e:
        print("error al buscar canciones: ", e)
        return 0
    
def obtenerCampo(linea, numero_campo):
    campo = ""
    separadores = 0
    i = 0

    while i < len(linea):
        char = linea[i]

        if char == "|":
            separadores += 1
        elif separadores == numero_campo - 1:
            campo += char
        elif separadores >= numero_campo:
            break

        i += 1

    return campo

def promedioDuracion(nombre_archivo):
    total_duracion = 0
    total_canciones = 0
    primera = True

    file = open(nombre_archivo, "r")
    for _ in range(4):  # Saltar las primeras 4 líneas decorativas
            next(file)

    for linea in file:
        if "|" in linea: 
          if linea.endswith("\n"): 
              linea = linea[:-1]  
              #duracion_str = obtenerCampo(linea, 3).strip() 
              duracion_str = obtenerCampo(linea,3) #campo 3 =duración de la canción 
              total_duracion += float(duracion_str) 
              total_canciones+=1 

    return total_duracion/total_canciones

def mayorAlpromedio (nombre_archivo):
    promedio = promedioDuracion(nombre_archivo) #Se llama la función promedioDuración para obtener un promedio para comparar
    cont =0

    print(f"🎶 Canciones con duración mayor al promedio ({promedio:.2f} ms):")
    file = open(nombre_archivo)
    for _ in range(4):  # Saltar las primeras 4 líneas decorativas
        next(file)

    for linea in file:
        if linea.endswith("\n"):
            linea = linea[:-1]
            duracioncancion_str = obtenerCampo(linea,3) # Da el dato de duración de la canción en Str
            duracioncancion = float(duracioncancion_str) # Toma el dato y lo convierte en float
            cancionName = obtenerCampo(linea,2)
            if duracioncancion > promedio:
                print(f"- {cancionName} ({duracioncancion} ms)")
                cont+=1

    if (cont ==0):    
        print (f"No hay canciones con duración mayor al promedio")
    return cont 





           
