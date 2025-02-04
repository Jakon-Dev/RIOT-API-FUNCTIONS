import sys
import os
import uuid
import cv2
import numpy as np
import matplotlib.pyplot as plt
import requests



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils


def run(maps: list = None, players: list = None, agents: list = None, matches: list = None, side: str = None, rtime: list = None, rounds: list = None) -> list:
    '''
    Parameters:
        :maps: List of mapNames to include in the heatmap.
        :players: List of playerNames or puuids to base the heatmaps on.
        :agents: List of agentNames to include in the heatmap.
        :matches: List of matchIds to include in the heatmap.
        :side: Side to include in the heatmap ("atk" or "def").
        :rtime: List of [StartRoundTime, EndRoundTime]
        :rounds: List of rounds to include in the heatmap.
    Returns: 
        List of heatmaps, one for each map.
    '''
    
    for player in players:
        if not utils.FUNCTIONS.isPuuidFormat(player):
            player = utils.DATA_FINDERS.RIOT_USERS.get_puuid_by_name(player)

        def ensure(player, matches):
            utils.MATCH_OOP.Player.find_player_with_puuid(player)
            if matches:
                for match in matches:
                    utils.MATCH_OOP.Match.create(match)
        ensure(player, matches)
        
        def get_locations():
            locations = utils.MATCH_OOP.Location.search_by_player(player)
            if maps:
                locations = [location for location in locations if utils.ALL_DATA.STATIC_GAME_DATA.MAPS.GET_BY_UUID.name(location.mapUuid) in maps]
            if agents:
                locations_ = []
                for location in locations:
                    if location.agent in agents:
                        locations_.append(location)
                locations = locations_
            if matches:
                locations = [location for location in locations if location.matchId in matches]
            if rtime:
                locations = [location for location in locations if rtime[0] <= location.roundTime <= rtime[1]]
            if rounds:
                locations = [location for location in locations if location.roundNumber in rounds]
            if side:
                if side == "both":
                    return locations
                locations = [location for location in locations if location.side == side]
            return locations
        locations = get_locations()

        static_maps = utils.ALL_DATA.STATIC_GAME_DATA.getMaps()
        def used_static_maps():
            new_static_maps = []
            for map in static_maps:
                for myMaps in maps:
                    if map["displayName"] == myMaps:
                        new_static_maps.append(map)
            return new_static_maps
        if maps:
            static_maps = used_static_maps()


        
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
    
    
    

