import utils

ALL_MATCHES = []
ALL_PLAYERS = []
ALL_ROUNDS = []
ALL_TEAMS = []
ALL_COACHES = []
ALL_ASSISTS = []
ALL_KILLS = []
ALL_LOCATIONS = []



def get_match_by_matchId(matchId: str) -> object:
    for match in ALL_MATCHES:
        if match.matchId == matchId:
            return match
    newMatch = utils.MATCH_OOP.Match(matchId)
    ALL_MATCHES.append(newMatch)
    return newMatch

def get_player_by_puuid(puuid: str) -> object:
    for player in ALL_PLAYERS:
        if player.puuid == puuid:
            return player
    newPlayer = utils.MATCH_OOP.Player(puuid)
    ALL_PLAYERS.append(newPlayer)
    return newPlayer

def get_location_by_dict(info: dict) -> object:
    for location in ALL_LOCATIONS:
        if location.x == info["x"] and location.y == info["y"] and location.mapUuid == info["mapUuid"] and location.matchId == info["matchId"] and location.playerPuuid == info["playerPuuid"] and location.viewRadians == info["viewRadians"]:
            return location
    newLocation = utils.MATCH_OOP.Location(info["x"], info["y"], info["mapUuid"], info["matchId"], info["playerPuuid"], info["viewRadians"], info["side"])
    ALL_LOCATIONS.append(newLocation)
    return newLocation