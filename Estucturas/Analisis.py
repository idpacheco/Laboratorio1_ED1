def artistaMasCanciones (nombre_archivo):
    max_artista =None
    max_canciones = 0
    file = open (nombre_archivo, "r")
    for _ in range(4):  # Saltar las primeras 4 líneas decorativas
            next(file)

    for linea in file:
        if "|" in linea:
            #lista o vector que contiene los fragmentos del texto que estaban separados con |
            partes = linea.strip().split("|")  
            #divide la linea eliminando los espacios y dividiendola en subcadenas
            artista = partes [0].strip()
            popularidad = partes[1].strip()
            cantidad = int (partes [2].strip())
            canciones = partes [3].strip()
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

def ordenarPorPopularidad(nombre_archivo, nombre_salida, campo_popularidad, titulo, encabezados):
    def obtenerPopularidad(linea):
        # Obtiene el campo de Popularidad (asumimos que empieza en la línea 5)
        return int(obtenerCampo(linea, campo_popularidad).strip())
    
    def estaProcesada(linea):
        return "[X]" in linea

    def marcarComoProcesada(linea):
        return "[X] " + linea  # le agrega un prefijo para saber que ya fue procesada

    # Copiamos el archivo original a uno temporal donde vamos a marcar las líneas procesadas
    import shutil
    archivo_temp = "archivo_temp.txt"
    shutil.copy(nombre_archivo, archivo_temp)

    with open(nombre_salida, "w", encoding="utf-8") as salida:
        salida.write(titulo.center(100, "=") + "\n\n")
        salida.write(encabezados + "\n")
        salida.write("-" * 100 + "\n")

        while True:
            max_linea = None
            max_popu = -1

            # Abrimos el archivo temporal y buscamos la canción más popular no procesada
            with open(archivo_temp, "r", encoding="ISO-8859-1") as temp:
                for linea in temp:
                    if "|" in linea and not estaProcesada(linea):
                        try:
                            popu = obtenerPopularidad(linea)
                            if popu > max_popu:
                                max_popu = popu
                                max_linea = linea
                        except:
                            continue  # por si falla al convertir algo

            if not max_linea:
                break  # ya no quedan canciones sin procesar

            salida.write(max_linea)

            # Ahora que encontramos la canción más popular, la marcamos como procesada
            with open(archivo_temp, "r+", encoding="ISO-8859-1") as temp:
                contenido = temp.readlines()
                temp.seek(0)  # Volvemos al inicio para sobrescribir el archivo
                for linea in contenido:
                    if linea == max_linea:
                        temp.write(marcarComoProcesada(linea))
                    else:
                        temp.write(linea)
                temp.truncate()  # Aseguramos que el archivo no quede con datos sobrantes

    print(f"✅ Ordenación por popularidad guardada en '{nombre_salida}'")

def artistaMasPopular(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as f:
            # Saltamos las primeras 4 líneas si son encabezados
            for _ in range(4):
                next(f)
            
            # Leemos la primera línea después de los encabezados
            linea = next(f, None)  # Usamos next para leer la siguiente línea de manera segura
            if linea:
                #se obtienen los campos de artista y popularidad
                max_artista = obtenerCampo(linea, 1)  # El nombre del artista
                max_popularidad = obtenerCampo(linea, 2) # La popularidad 

                # Como el archivo está ordenado, ya no necesitamos continuar
                print(f"El artista más popular es: {max_artista} con una popularidad de {max_popularidad}")
    except Exception as e:
        print("Error al buscar artista con mayor índice de popularidad:", e)
        return None

def insertarCancionOrdenada(nombre_archivo, nueva_linea, campo_popularidad):
    def obtenerPopularidad(linea):
        try:
            valor = obtenerCampo(linea, campo_popularidad).strip()
            return int(valor)
        except ValueError:
            raise ValueError(f"Error al obtener popularidad de la línea: {linea}") # en este sale una advertencia por las primeras 4 lineas que no encuentra la popularidad

    try:
        # Leer todas las líneas actuales del archivo
        with open(nombre_archivo, "r", encoding="ISO-8859-1") as archivo:
            lineas = archivo.readlines()

        # Validar la nueva línea
        if "|" not in nueva_linea:
            raise ValueError(f"La nueva línea no tiene el formato esperado: {nueva_linea}")

        nueva_popu = obtenerPopularidad(nueva_linea)
        nuevas_lineas = []
        insertado = False

        for linea in lineas:
            if not insertado and "|" in linea:
                try:
                    popu_actual = obtenerPopularidad(linea)
                    if nueva_popu > popu_actual:
                        nuevas_lineas.append(nueva_linea)
                        insertado = True
                except ValueError as e:
                    print(f"Advertencia: {e}")
            nuevas_lineas.append(linea)

        if not insertado:
            nuevas_lineas.append(nueva_linea)

        # Escribir las líneas actualizadas en el archivo
        with open(nombre_archivo, "w", encoding="ISO-8859-1") as archivo:
            archivo.writelines(nuevas_lineas)

        print("✅ Canción insertada en el lugar correcto.")
    except Exception as e:
        print(f"❌ Error al insertar la canción: {e}")

