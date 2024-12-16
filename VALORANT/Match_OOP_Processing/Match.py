import utils
import json
import Match_OOP_Processing.All as All_Classes
import Match_OOP_Processing.Player as Player_Class
import Match_OOP_Processing.Team as Team_Class
import Match_OOP_Processing.Round as Round_Class
import Match_OOP_Processing.Assist as Assist_Class
import Match_OOP_Processing.Kill as Kill_Class



class Match:
    def __init__(self, matchId: str) -> None:
        self.matchId = matchId
        self.API_json = utils.DATA_FINDERS.RIOT_MATCHES.get_json_by_matchId(matchId)
        
        def matchInfo():
            matchInfo = self.API_json["matchInfo"]
            self.matchInfoJson = matchInfo
            
            def mapInfo():
                self.mapId = matchInfo["mapId"]
                self.mapUuid = utils.ALL_DATA.STATIC_GAME_DATA.MAPS.GET_UUID.by_url(self.mapId)
                self.mapName = utils.ALL_DATA.STATIC_GAME_DATA.MAPS.GET_BY_UUID.name(self.mapUuid)
                self.mapImages = utils.ALL_DATA.STATIC_GAME_DATA.MAPS.GET_BY_UUID.images(self.mapUuid)
            mapInfo()
            
            self.queueId = matchInfo["queueId"]
            
            def timeInfo():
                self.gameLengthMillis = matchInfo["gameLengthMillis"]
                self.gameStartMillis = matchInfo["gameStartMillis"]
                self.gameLengthTime = utils.FUNCTIONS.TIME.millis_to_time(self.gameLengthMillis)
                self.gameStartDate = utils.FUNCTIONS.TIME.millis_to_date(self.gameStartMillis)
            timeInfo()
            
        matchInfo()
        
        
        def init_lists():
            self.PLAYERS_PUUIDS = []
            self.PLAYERS = []
            self.ROUNDS = []
            self.TEAMS = []
            self.COACHES = []
            self.ASSISTS = []
            self.KILLS = [] 
        init_lists()
        
        
        self.process()
        
        for key, value in self.__dict__.items():
            if type(value).__name__ == "dict" or type(value).__name__ == "list":
                print(f"{key} -> {type(value).__name__}")
            else:
                # Prints key and value
                print(f"{key} = {value}")


        All_Classes.ALL_MATCHES.append(self)
        utils.ALL_DATA.DATA_BASE.RIOT_MATCHES.upsert(matchId, self.API_json, self.PLAYERS_PUUIDS)
        
    def process(self) -> None:
        def process_players():
            for player in self.API_json["players"]:
                self.PLAYERS_PUUIDS.append(player["puuid"])
                player_class = Player_Class.Player.find_player_with_puuid(player["puuid"])
                Player_Class.Player.add_stats(player)
                
                
                
                
                
        process_players()
        
        def process_rounds():
            pass
        process_rounds()
        
        def process_teams():
            pass
        process_teams()
        
        def process_coaches():
            pass
        process_coaches()

        def process_assists():
            pass
        process_assists()

        def process_kills():
            pass
        process_kills()

    
    def create(matchId: str) -> None:
        Match(matchId)
        