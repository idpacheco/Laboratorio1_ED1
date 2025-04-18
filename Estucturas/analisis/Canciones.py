from analisis.Archivos import obtenerCampo

#5. ¿Qué canciones tienen una duración superior al promedio de duración de todas las canciones en la playlist? D
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

#4. ¿Cuántas operaciones de lectura son necesarias para encontrar todas las canciones de un artista específico?
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
