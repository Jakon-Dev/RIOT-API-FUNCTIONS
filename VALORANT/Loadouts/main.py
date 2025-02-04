import sys
import os
from tabulate import tabulate



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils


def run(matchId: str, round: str, player: str):
    assert(utils.FUNCTIONS.isUuidFormat(matchId))
    if round != "":
        assert(round.isdigit())
    if player != "":
        assert(utils.FUNCTIONS.isPuuidFormat(player))
    
    match = utils.MATCH_OOP.Match.create(matchId)
    Matchloadouts = match.LOADOUTS
    trueLoadouts = []
    
    if round != "":
        round = int(round)
    
    for loadout in Matchloadouts:
        if round != "" and player != "":
            if loadout.roundNumber == round and loadout.playerPuuid == player:
                trueLoadouts.append(loadout)
        elif round != "":
            if loadout.roundNumber == round:
                trueLoadouts.append(loadout)
        elif player != "":
            if loadout.playerPuuid == player:
                trueLoadouts.append(loadout)
        else:
            trueLoadouts.append(loadout)
    
    Players_Print = []
    rounds_Prints = []
    gunNames_Prints = []
    gearNames_Prints = []
    values_Prints = []
    remaining_Prints = []
    spent_Prints = []
    
    for loadout in trueLoadouts:
        gunName = utils.ALL_DATA.STATIC_GAME_DATA.WEAPONS.GET_BY_UUID.name(loadout.weaponId.lower())
        gunNames_Prints.append(gunName)
        gearName = utils.ALL_DATA.STATIC_GAME_DATA.GEAR.GET_BY_UUID.name(loadout.armorId.lower())
        gearNames_Prints.append(gearName)
        playerName = utils.DATA_FINDERS.RIOT_USERS.get_name_by_puuid(loadout.playerPuuid)
        Players_Print.append(playerName)
        roundNumber = loadout.roundNumber
        rounds_Prints.append(roundNumber)
        value = loadout.value
        values_Prints.append(value)
        remaining = loadout.remaining
        remaining_Prints.append(remaining)
        spent = loadout.spent
        spent_Prints.append(spent)
        
    info = tabulate({
        "PLAYER": Players_Print,
        "ROUND": rounds_Prints,
        "GUN": gunNames_Prints,
        "GEAR": gearNames_Prints,
        "VALUE": values_Prints,
        "REMAINING": remaining_Prints,
        "SPENT": spent_Prints
    }, headers="keys", tablefmt="grid")
    print(info)
        
        


if __name__ == '__main__':
    run()