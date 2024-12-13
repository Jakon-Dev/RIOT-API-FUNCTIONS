import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils


utils.FUNCTIONS.start_process()



def run(parameter = None) -> None:
    
    if not parameter:
        parameter = input("Insert player name: ")
    
    '''
    while not utils.FUNCTIONS.isFullName(parameter):
        print("Name not valid, valid format example is Jakon#Coach")
        print()
        parameter = input("Insert valid player name: ")
    
    puuid = utils.RIOT_USERS.get_puuid_by_name(parameter)
    
    if utils.SETTINGS.PRINTABLES:
        print("Puuid: " + puuid)
        print("Name: " + utils.RIOT_USERS.get_name_by_puuid(puuid))

    '''
        
    print(utils.STATIC_GAME_DATA.AGENTS.GET_UUID.by_name(parameter))    

run()

utils.FUNCTIONS.end_process()