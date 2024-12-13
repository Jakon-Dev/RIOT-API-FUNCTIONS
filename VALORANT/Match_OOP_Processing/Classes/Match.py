import utils

class Match:
    def __init__(self, matchId: str) -> None:
        self.matchId = matchId
        self.API_json = utils.API_CALLS.getRiotMatchData(matchId)
        json = f'''
        "hola" = "{self.API_json}"
        '''