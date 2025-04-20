
#3. ¿Cuál es el tamaño promedio (en bytes) de cada registro en tus archivos secuenciales?
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
