from analisis.Canciones import obtenerCampo

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

