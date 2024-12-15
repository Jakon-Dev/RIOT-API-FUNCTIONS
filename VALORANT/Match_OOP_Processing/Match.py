import utils
import Match_OOP_Processing.All as All_Classes


class Match:
    def __init__(self, matchId: str) -> None:
        self.matchId = matchId
        self.API_json = utils.DATA_FINDERS.RIOT_MATCHES.get_json_by_matchId(matchId)
        
        def init_lists():
            self.PLAYERS = []
            self.ROUNDS = []
            self.TEAMS = []
            self.COACHES = []
            self.ASSISTS = []
            self.KILLS = [] 
        init_lists()
        
        self.process()
                
        All_Classes.ALL_MATCHES.append(self)
        utils.ALL_DATA.DATA_BASE.RIOT_MATCHES.upsert(matchId, self.API_json, self.PLAYERS)
        
    def process(self) -> None:
        def process_players():
            for player in self.API_json["players"]:
                self.PLAYERS.append(player["puuid"])
                
                
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
        