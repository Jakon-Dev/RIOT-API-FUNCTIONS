import json
from turtle import update
import requests
import pandas as pd
from tqdm import tqdm
import time



from Static_Game_Data import updateStaticGameData


class GLOBALS:
    def API_KEY() -> str:
        with open('clave.txt', 'r') as archivo:
            return archivo.read().strip()

    WAITING_TIME = 120
    
    MATCH_DETAILS_URL = "https://eu.api.riotgames.com/val/match/v1/matches/{}?api_key={}"
    USER_DETAILS_URL = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}"
    TOURNAMENT_DETAILS_URL = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/tournament-endpoint/{}"
    PUUID_DETAILS_URL = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}"
    CT_USER_DETAILS_URL = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/user/profile/{}?user={}"
    RECENT_MATCHES_URL = "https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{}?api_key={}"
    TEAM_DETAILS_URL = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/public/team/{}"


class API_CALLS:
    def getMatchAPIjson(matchId: str) -> json:
        API_KEY = GLOBALS.API_KEY()
        REQUEST_URL = GLOBALS.MATCH_DETAILS_URL.format(matchId, API_KEY)
        
        # Solicitar los datos de la API
        response = requests.get(REQUEST_URL)
        while response.status_code == 429:  # Manejar error de límite de tasa
            print(f"Error 429, retrying for matchId: {matchId}")
            FUNCTIONS.wait()
            response = requests.get(REQUEST_URL)
        
        # Guardar los datos en el archivo JSON si la solicitud fue exitosa
        if response.status_code == 200:
            match_details = response.json()
            return match_details
        else:
            print(f"Error al obtener datos para el matchId {matchId}: {response.status_code}")
            return None



class STATIC_GAME_DATA:
    def update():
        updateStaticGameData.update()
    def delete():
        updateStaticGameData.delete()









class FUNCTIONS:
    def wait() -> None:
        with tqdm(range(GLOBALS.WAITING_TIME), unit="segundos", bar_format="{l_bar}{bar:40}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as progress_bar:
            for _ in progress_bar:
                time.sleep(1)

        
