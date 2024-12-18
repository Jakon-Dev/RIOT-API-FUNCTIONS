import json
from httpx import delete
import requests
from tqdm import tqdm
import time
import re
import os
import datetime
import pytz
from concurrent.futures import ThreadPoolExecutor


import SECRET_DATA as SECRETS


from Static_Game_Data import StaticGameData
from Static_Game_Data import processer as StaticDataProcesser
from Data_Base import DataBase as DB
import Match_OOP_Processing.Match as Match_Class
import Match_OOP_Processing.Player as Player_Class
import Match_OOP_Processing.Location as Location_Class
import Match_OOP_Processing.All as All_Classes





class SETTINGS:
    WAITING_TIME: int = 120
    
    PRINTABLES: bool = True

class GLOBALS:
    '''
        Global variables class, made a class for better fuction visualization 
        and variables accessing from other files.
    
    '''
    
   
    
    class DATA_BASE:
        SUPABASE_URL: str = SECRETS.SUPABASE_URL
        SUPABASE_KEY: str = SECRETS.SUPABASE_KEY
    
    class API:
        API_KEY: str = SECRETS.RIOT_API_KEY
            
        MATCH_DATA_URL: str = "https://eu.api.riotgames.com/val/match/v1/matches/{}?api_key={}"
        USER_DETAILS_URL: str = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{}?api_key={}"
        TOURNAMENT_DETAILS_URL: str = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/tournament-endpoint/{}"
        PUUID_DETAILS_URL: str = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{}/{}?api_key={}"
        CT_USER_DETAILS_URL: str = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/user/profile/{}?user={}"
        RECENT_MATCHES_URL: str = "https://eu.api.riotgames.com/val/match/v1/matchlists/by-puuid/{}?api_key={}"
        TEAM_DETAILS_URL: str = "https://api-ggtech.leagueoflegends.com/api/v001/showcase/circuito-tormenta-es/public/team/{}"

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
        
        API_KEY = GLOBALS.API.API_KEY
        REQUEST_URL = GLOBALS.API.MATCH_DATA_URL.format(matchId, API_KEY)
        
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
        
        API_KEY = GLOBALS.API.API_KEY
        REQUEST_URL = GLOBALS.API.USER_DETAILS_URL.format(puuid, API_KEY)
        
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
    
    def getPuuidAPIjson(fullName: str)-> json:
        '''
            Returns user puuid with format UUID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) from Riot API (https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={API_KEY}).

            Expects a String with format (XXXXXX#XXXX).
            Else it raises ValueError.
        '''
        
        gameName, tagLine = fullName.split("#")
        gameName = gameName.replace(" ", "%20")
        tagLine = tagLine.replace(" ", "%20")
        
        API_KEY = GLOBALS.API.API_KEY
        REQUEST_URL = GLOBALS.API.PUUID_DETAILS_URL.format(gameName, tagLine, API_KEY)
        # Solicitar los datos de la API
        response = requests.get(REQUEST_URL)
        while response.status_code == 429:  # Manejar error de límite de tasa
            #print(f"Error 429, retrying for player: {gameName}#{tagLine}")
            FUNCTIONS.wait()
            response = requests.get(REQUEST_URL)
        
        # Guardar los datos en el archivo JSON si la solicitud fue exitosa
        if response.status_code == 200:
            user_details = response.json()
            return user_details
        else:
            return None
    
    def getMatchHistory(puuid: str) -> json:
        API_KEY = GLOBALS.API.API_KEY
        REQUEST_URL = GLOBALS.API.RECENT_MATCHES_URL.format(puuid, API_KEY)        
        response = requests.get(REQUEST_URL)
        while response.status_code == 429:  # Manejar error de límite de tasa
            print(f"Error 429, retrying for puuid: {puuid}")
            FUNCTIONS.wait()
            response = requests.get(REQUEST_URL)
        
        # Guardar los datos en el archivo JSON si la solicitud fue exitosa
        if response.status_code == 200:
            match_history = response.json()
            return match_history
        else:
            print(f"Error al obtener datos para el puuid {puuid}: {response.status_code}")
            return None

    
from concurrent.futures import ThreadPoolExecutor

class ALL_DATA:
    @staticmethod
    def update():
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(ALL_DATA.STATIC_GAME_DATA.update),
                executor.submit(ALL_DATA.DATA_BASE.update)
            ]
            for future in futures:
                future.result()

    @staticmethod
    def delete():
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(ALL_DATA.STATIC_GAME_DATA.delete),
                executor.submit(ALL_DATA.DATA_BASE.delete)
            ]
            for future in futures:
                future.result()
        
    class DATA_BASE:
        @staticmethod
        def update():
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(ALL_DATA.DATA_BASE.RIOT_USERS.update),
                    executor.submit(ALL_DATA.DATA_BASE.RIOT_MATCHES.update)
                ]
                for future in futures:
                    future.result()

        @staticmethod
        def delete():
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(ALL_DATA.DATA_BASE.RIOT_USERS.delete),
                    executor.submit(ALL_DATA.DATA_BASE.RIOT_MATCHES.delete)
                ]
                for future in futures:
                    future.result()
        @staticmethod
        def upload():
            ALL_DATA.DATA_BASE.RIOT_USERS.upload()
            ALL_DATA.DATA_BASE.RIOT_MATCHES.upload()


        
        class RIOT_USERS(DB.RIOT_USERS):
            pass
        
        class RIOT_MATCHES(DB.RIOT_MATCHES):
            pass
    
    class STATIC_GAME_DATA:
        '''
            Static Game Data functions but accessed from here for better access from other files.
        
        '''
        
        def update():
            StaticGameData.update()
        def delete():
            StaticGameData.delete()
        
        def getAgents():
            return StaticGameData.getAgents()
        def getMaps():
            return StaticGameData.getMaps()
        def getPlayerCards():
            return StaticGameData.getPlayerCards()
        def getPlayerTitles():
            return StaticGameData.getPlayerTitles()
        def getWeapons():
            return StaticGameData.getWeapons()
        def getGear():
            return StaticGameData.getGear()
        
        class AGENTS(StaticDataProcesser.AGENTS):
            pass
        
        class MAPS(StaticDataProcesser.MAPS):
            pass
        
        class PLAYERCARDS(StaticDataProcesser.PLAYERCARDS):
            pass
        
        class PLAYERTITLES(StaticDataProcesser.PLAYERTITLES):
            pass
        
        class WEAPONS(StaticDataProcesser.WEAPONS):
            pass
        
        class GEAR(StaticDataProcesser.GEAR):
            pass

class MATCH_OOP:
    class Match(Match_Class.Match):
        pass
    
    class Player(Player_Class.Player):
        pass
    
    class Location(Location_Class.Location):
        pass
    

class DATA_FINDERS:
    class RIOT_USERS:
        def get_puuid_by_name(name: str) -> str:
            if not FUNCTIONS.isFullName(name):
                raise ValueError(f"Not valid name format {name}")
            
            data = ALL_DATA.DATA_BASE.RIOT_USERS.search(name, "fullName")
            if not data:
                data = API_CALLS.getPuuidAPIjson(name)
                if data:
                    puuid = data.get("puuid")
                    ALL_DATA.DATA_BASE.RIOT_USERS.upsert(puuid, name, data)
                    
                    
                
            return data.get("puuid")

        def get_name_by_puuid(puuid: str) -> str:
            if not FUNCTIONS.isPuuidFormat(puuid):
                raise ValueError(f"Not valid puuid format {puuid}")
            
            data = ALL_DATA.DATA_BASE.RIOT_USERS.search(puuid, "puuid")
            if not data:
                data = API_CALLS.getRiotUserInfo(puuid)
                if data:
                    name = data.get("gameName") + "#" + data.get("tagLine")
                    ALL_DATA.DATA_BASE.RIOT_USERS.upsert(puuid, name, data)
            
            return data.get("gameName") + "#" + data.get("tagLine")

        def get_db_matches_by_puuid(puuid: str) -> list:
            if not FUNCTIONS.isPuuidFormat(puuid):
                raise ValueError(f"Not valid puuid format {puuid}")
            
            


    class RIOT_MATCHES:
        def get_json_by_matchId(matchId: str) -> json:
            if not FUNCTIONS.isUuidFormat(matchId):
                raise ValueError(f"Not valid matchId format {matchId}")
            
            data = ALL_DATA.DATA_BASE.RIOT_MATCHES.search(matchId)
            if not data:
                data = API_CALLS.getRiotMatchData(matchId)
            return data
        
        def get_played_matches_by_puuid(puuid: str) -> list:
            return DB.RIOT_MATCHES.played_matches_by_puuid(puuid)  
    
class FUNCTIONS:
    def wait() -> None:
        with tqdm(range(SETTINGS.WAITING_TIME), unit="segundos", bar_format="{l_bar}{bar:40}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as progress_bar:
            for _ in progress_bar:
                time.sleep(1)
    
    def start_process() -> None:
        '''
        Updates all data and prints the Process start message:
        "Starting process -> Made By Jakon" in ASCII
        
        '''
        os.system('cls' if os.name == 'nt' else 'clear')
        if SETTINGS.PRINTABLES:
            print()
            print()
            print(R"######################################################################################################################################################################")
            print(R"#                                                                                                                                                                    #")
            print(R"#  ________  ________  ________  ________  _______   ________   ________           ________  _________  ________  ________  _________  ___  ________   ________      #")
            print(R"# |\   __  \|\   __  \|\   __  \|\   ____\|\  ___ \ |\   ____\ |\   ____\         |\   ____\|\___   ___\\   __  \|\   __  \|\___   ___\\  \|\   ___  \|\   ____\     #")
            print(R"# \ \  \|\  \ \  \|\  \ \  \|\  \ \  \___|\ \   __/|\ \  \___|_\ \  \___|_        \ \  \___|\|___ \  \_\ \  \|\  \ \  \|\  \|___ \  \_\ \  \ \  \\ \  \ \  \___|     #")
            print(R"#  \ \   ____\ \   _  _\ \  \\\  \ \  \    \ \  \_|/_\ \_____  \\ \_____  \        \ \_____  \   \ \  \ \ \   __  \ \   _  _\   \ \  \ \ \  \ \  \\ \  \ \  \  ___   #")
            print(R"#   \ \  \___|\ \  \\  \\ \  \\\  \ \  \____\ \  \_|\ \|____|\  \\|____|\  \        \|____|\  \   \ \  \ \ \  \ \  \ \  \\  \|   \ \  \ \ \  \ \  \\ \  \ \  \|\  \  #")
            print(R"#    \ \__\    \ \__\\ _\\ \_______\ \_______\ \_______\____\_\  \ ____\_\  \         ____\_\  \   \ \__\ \ \__\ \__\ \__\\ _\    \ \__\ \ \__\ \__\\ \__\ \_______\ #")
            print(R"#     \|__|     \|__|\|__|\|_______|\|_______|\|_______|\_________\\_________\       |\_________\   \|__|  \|__|\|__|\|__|\|__|    \|__|  \|__|\|__| \|__|\|_______| #")
            print(R"#                                                      \|_________\|_________|       \|_________|                                                                    #")
            print(R"#                                                                                                                                                                    #")
            print(R"#                                           __  __   ____   ____  ____    _____ __  __     __   ____   __  __  ____  __  _                                           #")
            print(R"#                                          |  \/  | / () \ | _) \| ===|   | () )\ \/ /   __) | / () \ |  |/  // () \|  \| |                                          #")
            print(R"#                                          |_|\/|_|/__/\__\|____/|____|   |_()_) |__|    \___//__/\__\|__|\__\\____/|_|\__|                                          #")
            print(R"#                                                                                                                                                                    #")
            print(R"######################################################################################################################################################################")
            print()
            print()
                
        ALL_DATA.update()

    def end_process() -> None:
        ALL_DATA.DATA_BASE.upload()
        ALL_DATA.DATA_BASE.delete()
    
    def isFullName(name: str) -> bool:
        """
        Checks if the input string follows the pattern:
        - A sequence of 3 to 16 UTF-8 characters
        - Followed by a '#' character
        - Followed by another sequence of 3 to 5 UTF-8 characters
        
        Args:
        name (str): The input string to be checked.
        
        Returns:
        bool: True if the string matches the pattern, False otherwise.
        """
        pattern = r'^.{3,16}#.{3,5}$'
        return bool(re.match(pattern, name))

    def isUuidFormat(uuid: str) -> bool:
        uuid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        return bool(re.match(uuid_regex, uuid))

    def isPuuidFormat(puuid: str) -> bool:
        puuid_regex = r'^[0-9a-zA-Z\-_]{78}$'
        return bool(re.match(puuid_regex, puuid))
        
    class TIME():
        def millis_to_date(millis):
            return datetime.datetime.fromtimestamp(millis / 1000.0, tz=datetime.timezone.utc).astimezone(pytz.timezone('Europe/Berlin')).strftime("%d-%m-%Y %H:%M")

        def millis_to_time(millis):
            seconds = (millis / 1000) % 60
            seconds = int(seconds)
            minutes = (millis / (1000 * 60)) % 60
            minutes = int(minutes)
            hours = (millis / (1000 * 60 * 60))
            hours = int(hours)

            if hours == 0:
                return f"{minutes:02d}m {seconds:02d}s"
            else:
                return f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
        
        