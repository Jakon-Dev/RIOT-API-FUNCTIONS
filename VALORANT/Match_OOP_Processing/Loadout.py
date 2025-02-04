import utils
import json
import Match_OOP_Processing.All as All_Classes
import uuid



class Loadout:
    def __init__(self, info: dict) -> None:
        assert(utils.FUNCTIONS.isUuidFormat(info["mapUuid"]))
        assert(utils.FUNCTIONS.isPuuidFormat(info["playerPuuid"]))
        self.__dict__ = info
        
    def create(info: dict) -> object:
        return All_Classes.get_loadout_by_dict(info)
    
    def search_by_player(puuid: str) -> list:
        Loadouts = []
        for Loadout in All_Classes.ALL_LOADOUTS:
            if Loadout.playerPuuid == puuid:
                Loadouts.append(Loadout)        
        return Loadouts

    

    