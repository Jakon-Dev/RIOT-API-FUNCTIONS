import utils
import json
import Match_OOP_Processing.All as All_Classes
import Match_OOP_Processing.Player as Player_Class
import Match_OOP_Processing.Team as Team_Class
import Match_OOP_Processing.Round as Round_Class
import Match_OOP_Processing.Assist as Assist_Class
import Match_OOP_Processing.Kill as Kill_Class
import Match_OOP_Processing.Location as Location_Class
import Match_OOP_Processing.Loadout as Loadout_Class







class Match:
    def __init__(self, matchId: str) -> None:
        self.matchId = matchId
        
        try:
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
                self.LOCATIONS = []
                self.LOADOUTS = []
            init_lists()
            
            
            self.process()
        except:
            pass
        
        
        
        
        
        if False:
            for key, value in self.__dict__.items():
                if type(value).__name__ == "dict" or type(value).__name__ == "list":
                    print(f"{key} -> {type(value).__name__}")
                else:
                    # Prints key and value
                    print(f"{key} = {value}")


        utils.ALL_DATA.DATA_BASE.RIOT_MATCHES.upsert(matchId, self.API_json, self.PLAYERS_PUUIDS)
        
    
    
    def process(self) -> None:
        def process_players():
            for player in self.API_json["players"]:
                self.PLAYERS_PUUIDS.append(player["puuid"])
                player_class = Player_Class.Player.find_player_with_puuid(player["puuid"])
                Player_Class.Player.add_stats(player)
                
                
                
                
                
        process_players()
        
        def process_rounds():
            for rounde in self.API_json["roundResults"]:
                # self.ROUNDS.append(Round_Class.Round(rounde))
                def get_teams() -> str:
                    def_puuids, atk_puuids = [], []
                    winning_team = rounde["winningTeam"]
                    winning_team_role = rounde["winningTeamRole"]
                    red_puuids = []
                    blue_puuids = []
                    for player in self.API_json["players"]:
                        if player["teamId"] == "Red":
                            red_puuids.append(player["puuid"])
                        elif player["teamId"] == "Blue":
                            blue_puuids.append(player["puuid"])
                    if winning_team == "Red":
                        if winning_team_role == "Defender":
                            def_puuids = red_puuids
                            atk_puuids = blue_puuids
                        else:
                            def_puuids = blue_puuids
                            atk_puuids = red_puuids
                    elif winning_team == "Blue":
                        if winning_team_role == "Defender":
                            def_puuids = blue_puuids
                            atk_puuids = red_puuids
                        else:
                            def_puuids = red_puuids
                            atk_puuids = blue_puuids
                    
                    return def_puuids, atk_puuids
                def_puuids, atk_puuids = get_teams()               
                
                
                def players_agents():
                    result = []
                    for player in self.API_json["players"]:
                        
                        result.append([player["puuid"],player["characterId"]])
                    return result
                playersAgents = players_agents()
                
                def process_locations():
                    for stat in rounde["playerStats"]:
                        for kill in stat["kills"]:
                            def victim_location():
                                victim_side = ""
                                if kill["victim"] in def_puuids:
                                    victim_side = "def"
                                elif kill["victim"] in atk_puuids:
                                    victim_side = "atk"
                                def get_agent():
                                    agent = ""
                                    for playerAgent in playersAgents:
                                        if playerAgent[0] == kill["victim"]:
                                            agent = playerAgent[1]
                                    return utils.ALL_DATA.STATIC_GAME_DATA.AGENTS.GET_BY_UUID.name(agent)
                                agent = get_agent()
                                victim_location = {
                                    "x": kill["victimLocation"]["x"],
                                    "y": kill["victimLocation"]["y"],
                                    "mapUuid": self.mapUuid,
                                    "matchId": self.matchId,
                                    "playerPuuid": kill["victim"],
                                    "side": victim_side,
                                    "agent": agent,
                                    "roundTime": kill["timeSinceRoundStartMillis"],
                                    "viewRadians": 0,
                                    "roundNumber": rounde["roundNum"]
                                }
                                Location_Class.Location.create(victim_location)
                            victim_location()
                            
                            for location in kill["playerLocations"]:
                                side = ""
                                if location["puuid"] in def_puuids:
                                    side = "def"
                                elif location["puuid"] in atk_puuids:
                                    side = "atk"
                                def get_agent():
                                    agent = ""
                                    for playerAgent in playersAgents:
                                        if playerAgent[0] == location["puuid"]:
                                            agent = playerAgent[1]
                                    return utils.ALL_DATA.STATIC_GAME_DATA.AGENTS.GET_BY_UUID.name(agent)
                                agent = get_agent()
                                dict = {
                                    "x": location["location"]["x"],
                                    "y": location["location"]["y"],
                                    "mapUuid": self.mapUuid,
                                    "matchId": self.matchId,
                                    "playerPuuid": location["puuid"],
                                    "viewRadians": location["viewRadians"],
                                    "side": side,
                                    "agent": agent,
                                    "roundTime": kill["timeSinceRoundStartMillis"],
                                    "roundNumber": rounde["roundNum"]
                                }
                                Location_Class.Location.create(dict) 
                process_locations()
                
               
                def process_loadouts():
                    playerStats = rounde["playerStats"]
                    for player in playerStats:
                        economy = player["economy"]
                        dict = {
                            "matchId": self.matchId,
                            "mapUuid": self.mapUuid,
                            "playerPuuid": player["puuid"],
                            "roundNumber": rounde["roundNum"],
                            "value": economy["loadoutValue"],
                            "remaining": economy["remaining"],
                            "spent": economy["spent"],
                            "weaponId": economy["weapon"],
                            "armorId": economy["armor"]
                        }
                        loadout = Loadout_Class.Loadout.create(dict)
                        self.LOADOUTS.append(loadout)
                        
                process_loadouts()
                
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
        
        

    
    
    def create(matchId: str, append: bool = True) -> object:
        assert(utils.FUNCTIONS.isUuidFormat(matchId))
        match = All_Classes.get_match_by_matchId(matchId, append) 
        return match
        