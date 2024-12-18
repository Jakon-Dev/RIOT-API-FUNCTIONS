import sys
import os
import uuid
import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from ipywidgets import interact
import ipywidgets as widgets



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils


def run( side: str = None, parameter:str = None) -> list:
    if not parameter:
        def ask_name():
            parameter = input("Insert player name: ")
            while not utils.FUNCTIONS.isFullName(parameter):
                print("Name not valid, valid format example is Jakon#Coach")
                print()
                parameter = input("Insert valid player name: ")
            return parameter
        parameter = ask_name()
    
    if not utils.FUNCTIONS.isPuuidFormat(parameter):
        parameter = utils.DATA_FINDERS.RIOT_USERS.get_puuid_by_name(parameter)

    locations = utils.MATCH_OOP.Location.search_by_player(parameter)
    
    if not side:
        def ask_side():
            side = input("Insert side: ")
            sides = ["def", "atk", "both"]
            while side not in sides:
                print("Side not valid, valid sides are 'def', 'atk' or 'both'")
                print()
                side = input("Insert side: ")
            return side
        side = ask_side()
    
    if side == "def":
        locations = [location for location in locations if location.side == "def"]
    elif side == "atk":
        locations = [location for location in locations if location.side == "atk"]
    
    
    static_maps = utils.ALL_DATA.STATIC_GAME_DATA.getMaps()
    
    def get_mapsLists():
        result = []
        for map in static_maps:
            map_uuid = map["uuid"]
            dict = {
                "mapName": map["displayName"],
                "image_url": map["displayIcon"],
                "points": [],
                "x_multiplier": map["xMultiplier"],
                "y_multiplier": map["yMultiplier"],
                "x_scalar_to_add": map["xScalarToAdd"],
                "y_scalar_to_add": map["yScalarToAdd"]
            }
            for location in locations:
                if location.mapUuid == map_uuid:
                    dict["points"].append({"x": location.x, "y": location.y})
            if not dict["points"]:
                continue
            result.append(dict)
        return result
    
    mapsList = get_mapsLists()
        
    overlaysList = []
    for map in mapsList:
        mapName = map["mapName"]
        image = generate_heatmap(map["image_url"], map["points"], map["x_multiplier"], map["y_multiplier"], map["x_scalar_to_add"], map["y_scalar_to_add"])
        overlaysList.append(image)
        
        output_dir = 'VALORANT/Location_Heatmap/OUTPUT'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the result
        output_path = os.path.join(output_dir, 'heatmap_' + mapName + '.jpg')  # You can change the filename if needed
        cv2.imwrite(output_path, image)

    
    
        

    
    return overlaysList
    
        
def generate_heatmap(image_url, points, x_multiplier, y_multiplier, x_scalar_to_add, y_scalar_to_add):
    """
    Genera un heatmap a partir de una imagen y una lista de puntos (x, y).
    
    Parámetros:
    - image_url (str): URL de la imagen de entrada.
    - points (list of dicts): Lista de diccionarios con las claves 'x' e 'y' que representan las posiciones en coordenadas de juego.
    - x_multiplier (float): Factor por el cual multiplicar cada coordenada x.
    - y_multiplier (float): Factor por el cual multiplicar cada coordenada y.
    - x_scalar_to_add (float): Valor a sumar a cada coordenada x.
    - y_scalar_to_add (float): Valor a sumar a cada coordenada y.
    
    Retorna:
    - None: Muestra la imagen con el heatmap superpuesto.
    """
        
    # 1️⃣ Descargar la imagen desde la URL
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception(f"No se pudo cargar la imagen desde la URL: {image_url}")
    
    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    if image is None:
        raise Exception(f"No se pudo decodificar la imagen desde la URL: {image_url}")
    
    # Convertir la imagen de BGR a RGB (cv2 carga imágenes en BGR por defecto)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 2️⃣ Obtener dimensiones de la imagen
    height, width, _ = image.shape
    
    # Crear un mapa de calor vacío con las mismas dimensiones que la imagen
    heatmap = np.zeros((height, width), dtype=np.float32)
    
    
    # 3️⃣ Ajustar cada punto de acuerdo con los multiplicadores, escalares y el tamaño de la imagen
    for point in points:
        # Intercambiar game_x y game_y de acuerdo con la documentación de Riot
        game_x = point['x']
        game_y = point['y']
        
        # Aplicar la fórmula de la API de Valorant
        image_x = game_y * x_multiplier + x_scalar_to_add
        image_y = game_x * y_multiplier + y_scalar_to_add
        
        # Convertir a coordenadas de imagen (multiplicar por width y height)
        image_x = int(image_x * width)
        image_y = int(image_y * height)
        
        # Asegurarse de que los puntos estén dentro de los límites de la imagen
        if 0 <= image_x < width and 0 <= image_y < height:
            heatmap[image_y, image_x] += 1  # Incrementar la intensidad en el punto
    
    # 4️⃣ Suavizar el mapa de calor con una función gaussiana (blur) para una mejor visualización
    heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)  # Reduce el kernel
    
    # 5️⃣ Normalizar el heatmap a un rango entre 0 y 1
    if np.max(heatmap) > 0:
        heatmap = heatmap / np.max(heatmap)
    
    # 6️⃣ Aplicar un mapa de colores al heatmap
    heatmap_colored = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)
    
    # 7️⃣ Mezclar la imagen original con el mapa de calor coloreado
    overlay = cv2.addWeighted(image, 0.6, heatmap_colored, 0.4, 0)
    
    return overlay
    
    
    

