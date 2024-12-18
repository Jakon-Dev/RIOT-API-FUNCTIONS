import utils
import json
import Match_OOP_Processing.All as All_Classes
import uuid



class Location:
    def __init__(self, x: int, y: int, mapUuid: str, matchId: str, playerPuuid: str, viewRadians: float, side: str) -> None:
        assert(utils.FUNCTIONS.isUuidFormat(mapUuid))
        assert(utils.FUNCTIONS.isPuuidFormat(playerPuuid))
        self.locationId = uuid.uuid4()
        self.viewRadians = viewRadians
        self.matchId = matchId
        self.x = x
        self.y = y
        self.mapUuid = mapUuid
        self.playerPuuid = playerPuuid
        self.side = side
    

    def create(info: dict) -> object:
        return All_Classes.get_location_by_dict(info)
    
    def search_by_player(puuid: str) -> list:
        locations = []
        for location in All_Classes.ALL_LOCATIONS:
            if location.playerPuuid == puuid:
                locations.append(location)        
        return locations
