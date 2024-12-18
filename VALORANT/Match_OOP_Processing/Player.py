import utils
import json
import Match_OOP_Processing.All as All_Classes


class Player:
    
    def __init__(self, puuid: str) -> None:
        self.puuid = puuid
        self.fullName = utils.DATA_FINDERS.RIOT_USERS.get_name_by_puuid(puuid)
        self.STATS_JSONS = []
        def globalStats():
            self.matchesPlayed = 0
            self.score = 0
            self.kills = 0
            self.deaths = 0
            self.assists = 0
            
        globalStats()
    
    def add_stats(stats_json: json) -> None:
        player = Player.find_player_with_puuid(stats_json["puuid"])
        player.STATS_JSONS.append(stats_json)
        def update_stats():
            player.matchesPlayed += 1
        update_stats()
        player.matchesPlayed += 1
    
    
    
    def find_player_with_puuid(puuid: str) -> object:
        for player in All_Classes.ALL_PLAYERS:
            if player.puuid == puuid:
                return player
        newPlayer = Player(puuid)
        All_Classes.ALL_PLAYERS.append(newPlayer)
        return newPlayer