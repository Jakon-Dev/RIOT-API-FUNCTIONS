import json
from turtle import update
import requests
import pandas as pd
from tqdm import tqdm
import time
import re



from Static_Game_Data import updateStaticGameData


class GLOBALS:
    '''
        Global variables class, made a class for better fuction visualization 
        and variables accessing from other files.
    
    '''
    
    def API_KEY() -> str:
        with open('clave.txt', 'r') as archivo:
            return archivo.read().strip()

    WAITING_TIME = 120
    
    MATCH_DATA_URL = "https://eu.api.riotgames.com/val/match/v1/matches/{}?api_key={}"
    USER_DETAILS_URL = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}"
    TOURNAMENT_DETAILS_URL = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/tournament-endpoint/{}"
    PUUID_DETAILS_URL = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}"
    CT_USER_DETAILS_URL = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/user/profile/{}?user={}"
    RECENT_MATCHES_URL = "https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{}?api_key={}"
    TEAM_DETAILS_URL = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/public/team/{}"


class API_CALLS:
    '''
        All API calls needed are located here except the ones 
        for Static data (located on 'Static_Game_Data/updateStaticGameData.py').
    
    '''
    
    def getRiotMatchData(matchId: str) -> json:
        '''
            Returns match information JSON from Riot API (https://eu.api.riotgames.com/val/match/v1/matches/{matchId}?api_key={API_KEY}).

            Expects a String with format UUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).
            Else it raises ValueError.
        '''
        
        if not FUNCTIONS.isUuidFormat(matchId):
            raise ValueError(f"Invalid matchId format: {matchId}. Expected UUID format.")
        
        API_KEY = GLOBALS.API_KEY()
        REQUEST_URL = GLOBALS.MATCH_DATA_URL.format(matchId, API_KEY)
        
        # Solicitar los datos de la API
        response = requests.get(REQUEST_URL)
        while response.status_code == 429:  # Manejar error de límite de tasa
            print(f"Error 429, retrying for matchId: {matchId}")
            FUNCTIONS.wait()
            response = requests.get(REQUEST_URL)
        
        # Guardar los datos en el archivo JSON si la solicitud fue exitosa
        if response.status_code == 200:
            match_data = response.json()
            return match_data
        else:
            print(f"Error al obtener datos para el matchId {matchId}: {response.status_code}")
            return None
    
    def getRiotUserInfo(puuid: str) -> json:
        '''
            Returns player information JSON from Riot API (https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={API_KEY}).

            Expects a String with format PUUID (78 chars/nums/-/_ ).
            Else it raises ValueError.
        '''
        
        if not FUNCTIONS.isPuuidFormat(puuid):
            raise ValueError(f"Invalid matchId format: {puuid}. Expected UUID format.")
        
        API_KEY = GLOBALS.API_KEY()
        REQUEST_URL = GLOBALS.USER_DETAILS_URL.format(puuid, API_KEY)
        
        # Solicitar los datos de la API
        response = requests.get(REQUEST_URL)
        while response.status_code == 429:  # Manejar error de límite de tasa
            print(f"Error 429, retrying for puuid: {puuid}")
            FUNCTIONS.wait()
            response = requests.get(REQUEST_URL)
            
        # Guardar los datos en el archivo JSON si la solicitud fue exitosa
        if response.status_code == 200:
            user_details = response.json()
            return user_details
        else:
            print(f"Error al obtener datos para el puuid {puuid}: {response.status_code}")
            return None
    


class STATIC_GAME_DATA:
    '''
        Static Game Data functions but accessed from here for better access from other files.
    
    '''
    
    def update():
        updateStaticGameData.update()
    def delete():
        updateStaticGameData.delete()









class FUNCTIONS:
    def wait() -> None:
        with tqdm(range(GLOBALS.WAITING_TIME), unit="segundos", bar_format="{l_bar}{bar:40}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as progress_bar:
            for _ in progress_bar:
                time.sleep(1)
    
    def isUuidFormat(uuid: str) -> bool:
        uuid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return bool(re.match(uuid_regex, uuid))

    def isPuuidFormat(puuid: str) -> bool:
        puuid_regex = r'^[0-9a-zA-Z\-_]{78}$'
        return bool(re.match(puuid_regex, puuid))
        
