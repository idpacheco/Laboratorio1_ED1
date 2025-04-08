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
    with open(nombre_archivo, "rb") as file: #"rb"
        for linea in file:
            if b"|" in linea:  #  b"|" porque la línea es tipo bytes
                registros = linea.strip().split(b"|")  # también bytes
                total_bytes += sum(len(registro) for registro in registros) #suma todos los bytes en cada registro
                total_registros += len(registros) 

    if total_registros > 0: #Calcula el promedio 
       return total_bytes / total_registros
     
    else:
       return 0

