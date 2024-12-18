from ast import arg
import signal
import sys
import utils
import Location_Heatmap.main as Location_Heatmap
import Match_OOP_Processing.All as All_Classes
import matplotlib.pyplot as plt
from IPython.display import display
import ipywidgets as widgets





def handle_sigint(signal_num, frame):
    """Handles Ctrl+C signal to execute FUNTIONS.exit() instead of immediate termination."""
    FUNTIONS.exit()

# Attach the signal handler for Ctrl+C
signal.signal(signal.SIGINT, handle_sigint)


utils.FUNCTIONS.start_process()

class FUNTIONS:
    
    def load(*args):
        
        def load_games(*args):
            for matchId in args:
                if utils.FUNCTIONS.isUuidFormat(matchId):
                    utils.MATCH_OOP.Match.create(matchId)
                else:
                    print(f"{matchId} is not a valid matchId")
        
        def load_users(*args):
            for param in args:
                if utils.FUNCTIONS.isFullName(param):
                    player = utils.MATCH_OOP.Player.find_player_with_puuid(utils.DATA_FINDERS.RIOT_USERS.get_puuid_by_name(param))
                    print(f"Uploaded {player.fullName}")
                elif utils.FUNCTIONS.isPuuidFormat(param):
                    player = utils.MATCH_OOP.Player.find_player_with_puuid(param)
                    print(f"Uploaded {player.fullName}")
                else:
                    print(f"{param} is not a valid player name or puuid")

        def load_comp_history(*args):
            for param in args:
                if utils.FUNCTIONS.isPuuidFormat(param):
                    puuid = param
                else:
                    puuid = utils.DATA_FINDERS.RIOT_USERS.get_puuid_by_name(param)
            matchHistory = utils.API_CALLS.getMatchHistory(puuid)
            for match in matchHistory["history"]:
                if match["queueId"] == "competitive" or match["queueId"] == "":
                    matchId = match["matchId"]
                    try:
                        utils.MATCH_OOP.Match.create(matchId)
                    except Exception as e:
                        print(f"Error loading match {matchId}: {e}")
    
        if args[0] == "games":
            load_games(*args[1:])
        elif args[0] == "users":
            load_users(*args[1:])
        elif args[0] == "history":
            load_comp_history(*args[1:])
        else:
            print(f"Invalid load type '{args[0]}'")

    def location_heatmap(*args):
        if args[0] == "":
            Location_Heatmap.run()
        else:
            for playerName in args[1:]:
                if utils.FUNCTIONS.isFullName(playerName):
        
                    imagesList = Location_Heatmap.run(args[0], playerName)
                    for image in imagesList:
                        plt.figure(figsize=(10, 10))
                        plt.imshow(image)
                        plt.axis('off')
                        plt.show()
                    
                    
                else:
                    print(f"{playerName} is not a valid player name")

    def exit():
        """End the process but allow the program to keep running for an additional command."""
        utils.FUNCTIONS.end_process()
        print("You have exited the current process. Type 'exit' to fully exit the program.")

    def full_exit():
        """Fully exits the program."""
        utils.FUNCTIONS.end_process()
        sys.exit()

    def help(*args):
        if args[0] == "":
            print("\n".join([f"    {cmd}: {details['definition']}" for cmd, details in COMMANDS.items()]))
        elif args[0] in COMMANDS:
            print(f"\n    {args[0]}: {COMMANDS[args[0]]['definition']}\nParameters: {COMMANDS[args[0]]['params']}")
        else:
            print(f"Command '{args[0]}' not found. Type 'help' for a list of commands.")
    
    def python(*args):
        """Executes the Python code provided as an argument."""
        code = " ".join(args)  # Join the args to form the complete code string
        try:
            exec(code)  # Execute the provided Python code
        except Exception as e:
            print(f"Error executing code: {e}")


COMMANDS = {
    "help": {
        "definition": "Prints all commands you can execute",
        "function": lambda params: FUNTIONS.help(*params.split(" ")),
        "params": "command"
    },
    "exit": {
        "definition": "Exits the program",
        "function": lambda: FUNTIONS.full_exit(),
        "params": ""
    },
    "load": {
        "definition": "Loads the type of data you want to input to the DataBase",
        "function": lambda params: FUNTIONS.load(*params.split(" ")),
        "params": '''
            games: Loads the games you enter its puuids after the command
            users: Loads the players you enter its names or puuids after the command
            history: Loads the competitive history of the player you enter its name or puuid after the command
        '''
    },
    "heatmap": {
        "definition": "Generates a location heatmap for given players",
        "function": lambda params: FUNTIONS.location_heatmap(*params.split(" ")),
        "params": "playerName"
    },
    "python": {
        "definition": "Executes raw Python code.",
        "function": lambda params: FUNTIONS.python(*params.split(" ")),
        "params": "Python code to execute"
    }
}

def run():
    while True:
        command_line = input("command_line: ")

        def run_command(command_line: str) -> None:
            parts = command_line.split(" ", 1)  # Split the command and its parameters
            command = parts[0]  # First part is the command
            params = parts[1] if len(parts) > 1 else ""  # Remaining part is the parameters (if any)

            if command in COMMANDS:
                func = COMMANDS[command]["function"]
                if func.__code__.co_argcount == 0:  # Check if the function takes no arguments
                    func()
                else:
                    func(params)
            else:
                print(f"Command '{command}' not found. Type 'help' for a list of commands.")

        run_command(command_line)



if __name__ == '__main__':
    run()