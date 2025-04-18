from analisis.Canciones import obtenerCampo
import os
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
        except:
            raise ValueError(f"No se pudo obtener popularidad de: {linea}")

    try:
        archivo_temp = nombre_archivo + ".temp"
        with open(nombre_archivo, "r", encoding="utf-8") as archivo_lectura, \
             open(archivo_temp, "w", encoding="utf-8") as archivo_escritura:
            # Copiar encabezado
            for _ in range(4):
                archivo_escritura.write(archivo_lectura.readline())
            insertado = False
            # Leer el archivo (desde la linea 5) y buscar la posición correcta para insertar
            for linea in archivo_lectura:
                if not insertado and "|" in linea:
                    try:
                        popu_actual = obtenerPopularidad(linea)
                        nueva_popu = obtenerPopularidad(nueva_linea)
                        if nueva_popu > popu_actual:
                            archivo_escritura.write(nueva_linea)
                            insertado = True
                    except:
                        pass  # Si no se puede obtener popularidad, igual escribe la línea
                archivo_escritura.write(linea)
            if not insertado:
                archivo_escritura.write(nueva_linea.strip() + "\n")
        # Reemplazar archivo original con el nuevo
        os.replace(archivo_temp, nombre_archivo)
        print("✅ Canción insertada correctamente y en orden.")
    except Exception as e:
        print(f"❌ Error: {e}")

