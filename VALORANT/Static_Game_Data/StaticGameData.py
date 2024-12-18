import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor


class GLOBALS:
    
    # DATA NOT EXTRACTED FROM OFFICIAL RIOT API, BUT FROM 'https://valorant-api.com'
    
    URLS = [
        "https://valorant-api.com/v1/agents",
        "https://valorant-api.com/v1/maps",
        "https://valorant-api.com/v1/playercards",
        "https://valorant-api.com/v1/playertitles",
        "https://valorant-api.com/v1/weapons",
        "https://valorant-api.com/v1/gear"
    ]
    
    FILES = [
        "VALORANT/Static_Game_Data/agents.json",
        "VALORANT/Static_Game_Data/maps.json",
        "VALORANT/Static_Game_Data/playercards.json",
        "VALORANT/Static_Game_Data/playertitles.json",
        "VALORANT/Static_Game_Data/weapons.json",
        "VALORANT/Static_Game_Data/gear.json"
    ]


    

def update() -> None:
    '''
    Updates data from 'https://valorant-api.com'. This info should be static 
    but can change once in a while because of Valorant game updates.
    '''
    def fetch_and_save(url, file):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open(file, "w") as f:
                json.dump(data["data"], f, indent=4)
        else:
            print(f"Failed to fetch {url}: {response.status_code}")

    with ThreadPoolExecutor() as executor:
        executor.map(fetch_and_save, GLOBALS.URLS, GLOBALS.FILES)

def delete() -> None:
    '''
        Deletes data from 'https://valorant-api.com'.
        
    '''
    
    for file in GLOBALS.FILES:
        if os.path.exists(file):
            os.remove(file)

def getAgents() -> json:
    with open("VALORANT/Static_Game_Data/agents.json", "r") as f:
        return json.load(f)
def getMaps() -> json:
    with open("VALORANT/Static_Game_Data/maps.json", "r") as f:
        return json.load(f)
def getPlayerCards() -> json:
    with open("VALORANT/Static_Game_Data/playercards.json", "r") as f:
        return json.load(f)
def getPlayerTitles() -> json:
    with open("VALORANT/Static_Game_Data/playertitles.json", "r") as f:
        return json.load(f)
def getWeapons() -> json:
    with open("VALORANT/Static_Game_Data/weapons.json", "r") as f:
        return json.load(f)
def getGear() -> json:
    with open("VALORANT/Static_Game_Data/gear.json", "r") as f:
        return json.load(f)

    
    

    