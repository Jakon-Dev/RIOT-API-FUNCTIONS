import utils

ALL_MATCHES = []
ALL_PLAYERS = []
ALL_ROUNDS = []
ALL_TEAMS = []
ALL_COACHES = []
ALL_ASSISTS = []
ALL_KILLS = []


def get_match_by_matchId(matchId: str) -> object:
    for match in ALL_MATCHES:
        if match.matchId == matchId:
            return match
    newMatch = utils.MATCH_OOP.Match(matchId)
    return newMatch

