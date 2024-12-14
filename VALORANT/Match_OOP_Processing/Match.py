import utils
import Match_OOP_Processing.All as All_Classes


class Match:
    def __init__(self, matchId: str) -> None:
        self.matchId = matchId
        self.API_json = utils.API_CALLS.getRiotMatchData(matchId)
        print(self.API_json)
    
    def create(matchId: str) -> None:
        new = Match(matchId)
        All_Classes.ALL_MATCHES.append(new)