import requests
import sys

API_KEY = "7c68dbe6-4be9-4b57-ac50-4b4d5247eed9"

# 🔹 1. Función para obtener coordenadas de ciudad
def get_coordinates(city_name):
    url = f"https://graphhopper.com/api/1/geocode?q={city_name}&locale=es&key={API_KEY}"
    res = requests.get(url)
    data = res.json()
    if data['hits']:
        lat = data['hits'][0]['point']['lat']
        lng = data['hits'][0]['point']['lng']
        return (lng, lat)
    else:
        print(f"No se encontró la ciudad: {city_name}")
        sys.exit()

# 🔹 2. Función para obtener ruta
def get_route(from_coords, to_coords, vehicle):
    url = f"https://graphhopper.com/api/1/route?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {
        "points": [from_coords, to_coords],
        "vehicle": vehicle,
        "locale": "es",
        "instructions": True
    }
    res = requests.post(url, headers=headers, json=body)
    return res.json()

# 🔹 3. Función principal
def main():
    print("🧭 Calculadora de ruta entre Chile y Perú")

    # ✅ 2. Solicita ciudad origen y destino
    origen = input("Ciudad de Origen (o 's' para salir): ")
    if origen.lower() == "s":
        sys.exit("Programa finalizado.")
    
    destino = input("Ciudad de Destino (o 's' para salir): ")
    if destino.lower() == "s":
        sys.exit("Programa finalizado.")

    # ✅ 5. Elegir tipo de transporte
    print("\nSeleccione tipo de transporte:")
    print("Opciones válidas: car (carro), bike (bicicleta), foot (a pie)")
    transporte = input("Tipo de transporte (o 's' para salir): ")
    if transporte.lower() == "s":
        sys.exit("Programa finalizado.")
    
    if transporte not in ["car", "bike", "foot"]:
        print("❌ Tipo de transporte no válido. Use: car, bike o foot.")
        sys.exit()

    # 🔄 Lógica
    origen_coords = get_coordinates(origen)
    destino_coords = get_coordinates(destino)

    ruta = get_route(origen_coords, destino_coords, transporte)

    try:
        distancia_m = ruta['paths'][0]['distance']
        duracion_s = ruta['paths'][0]['time'] / 1000
        instrucciones = ruta['paths'][0]['instructions']

        # ✅ 3. Distancia y duración
        km = round(distancia_m / 1000, 2)
        millas = round(km * 0.621371, 2)
        duracion_min = round(duracion_s / 60, 1)

        print(f"\nDistancia: {km} km / {millas} mi")
        print(f"Duración estimada: {duracion_min} minutos")

        # ✅ 4. Narrativa del viaje
        print("\nNarrativa del viaje:")
        for paso in instrucciones:
            print("-", paso['text'])

    except KeyError:
        print("❌ Error: verifica las ciudades y el tipo de transporte.")

# 🔁 Ejecutar programa
if __name__ == "__main__":
    main()