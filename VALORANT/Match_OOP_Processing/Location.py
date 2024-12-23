import utils
import json
import Match_OOP_Processing.All as All_Classes
import uuid



class Location:
    def __init__(self, info: dict) -> None:
        assert(utils.FUNCTIONS.isUuidFormat(info["mapUuid"]))
        assert(utils.FUNCTIONS.isPuuidFormat(info["playerPuuid"]))
        self.__dict__ = info
    

    def create(info: dict) -> object:
        return All_Classes.get_location_by_dict(info)
    
    def search_by_player(puuid: str) -> list:
        locations = []
        for location in All_Classes.ALL_LOCATIONS:
            if location.playerPuuid == puuid:
                locations.append(location)        
        return locations
