import requests
import json
import os

class GLOBALS:
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


    

def update():
    def update_json(url, file):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            with open(file, "w") as f:
                json.dump(data["data"], f, indent=4)

    for url, file in zip(GLOBALS.URLS, GLOBALS.FILES):
        update_json(url, file)

def delete():
    for file in GLOBALS.FILES:
        if os.path.exists(file):
            os.remove(file)



if __name__ == "__main__":
    update()
    delete()