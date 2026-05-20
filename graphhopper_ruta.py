import requests

API_KEY = "e75acdc3-037d-4b96-bc48-82e2dee22ef7"

def obtener_coordenadas(ciudad):
    url = "https://graphhopper.com/api/1/geocode"
    parametros = {
        "q": ciudad,
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)
    datos = respuesta.json()

    if "hits" in datos and len(datos["hits"]) > 0:
        punto = datos["hits"][0]["point"]
        return punto["lat"], punto["lng"]
    else:
        return None

def calcular_ruta(origen, destino, vehiculo):
    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)

    if coord_origen is None or coord_destino is None:
        print("No se pudo encontrar una de las ciudades ingresadas.")
        return

    url = "https://graphhopper.com/api/1/route"
    parametros = {
        "point": [
            f"{coord_origen[0]},{coord_origen[1]}",
            f"{coord_destino[0]},{coord_destino[1]}"
        ],
        "vehicle": vehiculo,
        "locale": "es",
        "instructions": "true",
        "calc_points": "true",
        "key": API_KEY
    }

    respuesta = requests.get(url, params=parametros)
    datos = respuesta.json()

    if "paths" not in datos:
        print("Error al calcular la ruta.")
        print(datos)
        return

    ruta = datos["paths"][0]

    distancia_metros = ruta["distance"]
    distancia_km = distancia_metros / 1000
    distancia_millas = distancia_km * 0.621371
    duracion_ms = ruta["time"]
    duracion_min = duracion_ms / 60000
    horas = int(duracion_min // 60)
    minutos = int(duracion_min % 60)

    print("\n===== RESULTADO DEL VIAJE =====")
    print(f"Ciudad de Origen: {origen}")
    print(f"Ciudad de Destino: {destino}")
    print(f"Medio de transporte: {vehiculo}")
    print(f"Distancia en kilómetros: {distancia_km:.2f} km")
    print(f"Distancia en millas: {distancia_millas:.2f} mi")
    print(f"Duración estimada: {horas} horas y {minutos} minutos")

    print("\n===== NARRATIVA DEL VIAJE =====")
    for paso in ruta["instructions"]:
        print("-", paso["text"])

while True:
    print("\n===== APLICACIÓN GRAPHHOPPER =====")
    print("Escriba 'v' para salir")

    origen = input("Ciudad de Origen: ")
    if origen.lower() == "v":
        print("Programa finalizado.")
        break

    destino = input("Ciudad de Destino: ")
    if destino.lower() == "v":
        print("Programa finalizado.")
        break

    print("\nSeleccione medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Ingrese opción: ")

    if opcion == "1":
        vehiculo = "car"
    elif opcion == "2":
        vehiculo = "bike"
    elif opcion == "3":
        vehiculo = "foot"
    else:
        print("Opción no válida. Se usará auto por defecto.")
        vehiculo = "car"

    calcular_ruta(origen, destino, vehiculo)
