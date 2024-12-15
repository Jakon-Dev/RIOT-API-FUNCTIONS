import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils


utils.FUNCTIONS.start_process()



def run(parameter = None) -> None:
    
    if not parameter:
        parameter = input("Insert matchId name: ")
    
    '''
    while not utils.FUNCTIONS.isFullName(parameter):
        print("Name not valid, valid format example is Jakon#Coach")
        print()
        parameter = input("Insert valid player name: ")
    '''
    utils.MATCH_OOP.Match.create(parameter)
    
    parameter = input("Insert player name: ")
    print(f"Played matches: {utils.DATA_FINDERS.RIOT_MATCHES.get_played_matches_by_puuid(parameter)}")

    

    

run()

utils.FUNCTIONS.end_process()