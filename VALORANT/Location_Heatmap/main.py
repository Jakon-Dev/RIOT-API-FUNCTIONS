import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils


utils.FUNCTIONS.start_process()



def run(parameter = None) -> None:
    
    if not parameter:
        parameter = input("Insert player name: ")
    
    
    while not utils.FUNCTIONS.isFullName(parameter):
        print("Name not valid, valid format example is Jakon#Coach")
        print()
        parameter = input("Insert valid player name: ")
    
    
    

    

    

run()

utils.FUNCTIONS.end_process()