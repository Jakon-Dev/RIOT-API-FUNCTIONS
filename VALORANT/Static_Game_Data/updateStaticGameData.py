import requests
import json
import os

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
        Updates data from 'https://valorant-api.com', this info should be static 
        but can change once in a while because of Valorant game updates.
        
    '''
    for url, file in zip(GLOBALS.URLS, GLOBALS.FILES):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open(file, "w") as f:
                json.dump(data["data"], f, indent=4)

def delete() -> None:
    '''
        Deletes data from 'https://valorant-api.com'.
        
    '''
    
    for file in GLOBALS.FILES:
        if os.path.exists(file):
            os.remove(file)
