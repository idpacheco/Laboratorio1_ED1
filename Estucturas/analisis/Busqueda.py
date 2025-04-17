
from analisis.Archivos import obtenerCampo
def busquedaBinariaPorPopularidad(archivo, popularidad_buscada):
    encontrado = False

    with open(archivo, "r", encoding="utf-8") as file:
        # Saltar las primeras 4 líneas del encabezado decorativo
        for _ in range(4):
            next(file)

        print("🔍 Buscando canciones con popularidad:", popularidad_buscada)
        print()

        for linea in file:
            if linea.strip() == "" or "-" in linea:
                continue  # Saltar líneas vacías o divisores

            try:
                # Extraer los campos usando obtenerCampo
                id_cancion = obtenerCampo(linea, 1)
                nombre = obtenerCampo(linea, 2)
                duracion = obtenerCampo(linea, 3)
                popularidad = int(obtenerCampo(linea, 4))  # Convertir a entero
                artistas = obtenerCampo(linea, 5)

                if popularidad == popularidad_buscada:
                    encontrado = True
                    print("🎵 Nombre:", nombre)
                    print("🆔 ID:", id_cancion)
                    print("⏱️ Duración (ms):", duracion)
                    print("🔥 Popularidad:", popularidad)
                    print("👤 Artistas:", artistas)
                    print("-" * 60)

            except Exception as e:
                print("⚠️ Advertencia: no se pudo procesar esta línea.")
                print(linea.strip())
                print("Error:", e)

    if not encontrado:
        print("❌ No se encontró una canción con esa popularidad.")
