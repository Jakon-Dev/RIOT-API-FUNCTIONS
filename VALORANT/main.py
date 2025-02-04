from ast import arg
import signal
import sys
import utils
import Location_Heatmap.main as Location_Heatmap
import Loadouts.main as Loadouts
import Match_OOP_Processing.All as All_Classes
import matplotlib.pyplot as plt
import os





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
        SUB_COMMANDS = {
            "-map": {
                "definition": "Makes only heatmaps for maps selected.",
                "params": "[mapName] [mapName] [mapName] ..."
            },
            "-players": {
                "definition": "Makes heatmaps for that players.",
                "params": "[playerName/puuid] [playerName/puuid] ..."
            },
            "-agent": {
                "definition": "Makes only heatmaps for agents selected.",
                "params": "[agentName] [agentName] [agentName] ..."
            },
            "-matches": {
                "definition": "Makes heatmaps for matches selected, else it makes heatmaps for all matches.",
                "params": "[matchId] [matchId] [matchId] ..."
            },
            "-rtime": {
                "definition": "Only takes locations displayed during that interval of milliseconds.",
                "params": "[StartMillis] [EndMillis]"
            },
            "-side": {
                "definition": "Makes only heatmaps for the side chosen",
                "params": "[atk/def]"
            },
            "-round":{
                "definition": "Only takes locations from rounds selected",
                "params": "[roundNumber] [roundNumber] ..."
            }
        }
        if args[0] == "":
            Location_Heatmap.run()
        elif args[0] == "help":
            print("Heatmap options are:")
            print("\n".join([f"    {subCommand}: {details['definition']}" for subCommand, details in SUB_COMMANDS.items()]))
        else:
            def get_commands(args):
                result = []
                                
                while args:
                    command = args[0]
                    args = args[1:]
                    if not args:
                        print(f"Wrong parameter for command {command}")
                    elif command[0] != "-" or command not in SUB_COMMANDS:
                        print(f"Wrong parameter for command {command}")
                        for subCommand in SUB_COMMANDS:
                            print(f"    {subCommand}: {SUB_COMMANDS[subCommand]['definition']}")
                    else:
                        command_params = []
                        while args and args[0][0] != "-":  # Ensure args is not empty before checking args[0][0]
                            command_params.append(args[0])
                            args = args[1:]
                        command_dict = {
                            "command": command,
                            "params": command_params
                        }
                        result.append(command_dict)  # Add the parsed command to the result
                return result
            commands = get_commands(args)
            def valid_commands(commands) -> bool:
                result = True
                if not any(cmd["command"] == "-players" for cmd in commands):
                    print("'-players' command is mandatory")
                    result = False
                for command in commands:
                    cmd = command["command"]
                    params = command["params"]
                    if cmd == "-map":
                        for mapName in params:
                            if mapName not in [map["displayName"] for map in utils.ALL_DATA.STATIC_GAME_DATA.getMaps()]:
                                print(f"Map '{mapName}' not found. Insert a valid map name.")
                                result = False
                    elif cmd == "-players":
                        for player in params:
                            if not utils.FUNCTIONS.isFullName(player) and not utils.FUNCTIONS.isPuuidFormat(player):
                                print(f"Player '{player}' is not a valid name or puuid.")
                                result = False
                    elif cmd == "-agent":
                        for agent in params:
                            if agent not in [agent["displayName"] for agent in utils.ALL_DATA.STATIC_GAME_DATA.getAgents()]:
                                print(f"Agent '{agent}' not found.")
                                result = False
                    elif cmd == "-matches":
                        for matchId in params:
                            if not utils.FUNCTIONS.isUuidFormat(matchId):
                                print(f"MatchId '{matchId}' is not a valid UUID.")
                                result = False
                    elif cmd == "-rtime":
                        if len(params) != 2:
                            print("Wrong parameters for -rtime, it needs 2 parameters")
                            result = False
                        else:
                            try:
                                int(params[0])
                                int(params[1])
                            except:
                                print("Wrong parameters for -rtime, it needs 2 integers")
                                result = False
                    elif cmd == "-side":
                        if params[0] not in ["atk", "def", "both"]:
                            print("Wrong parameters for -side, it needs 'atk', 'def' or 'both'")
                            result = False
                return result
            if valid_commands(commands):
                def execute_commands(commands) -> list:
                    maps = None
                    players = None
                    agents = None
                    matches = None
                    side = None
                    rtime = None
                    rounds = None
                    
                    for command in commands:
                        cmd = command["command"]
                        params = command["params"]
                        if cmd == "-map":
                            maps = params
                        elif cmd == "-players":
                            players = params
                        elif cmd == "-agent":
                            agents = params
                        elif cmd == "-matches":
                            matches = params
                        elif cmd == "-rtime":
                            rtime = params
                        elif cmd == "-side":
                            side = params[0]
                        elif cmd == "-round":
                            rounds = params
                    
                    imagesList = Location_Heatmap.run(maps, players, agents, matches, side, rtime, rounds)
                    return imagesList
                imagesList = execute_commands(commands)
                
                for image in imagesList:
                    plt.figure(figsize=(10, 10))
                    plt.imshow(image)
                    plt.axis('off')
                    plt.show()
            else:
                print("Invalid parameters. Please check your input. Or write 'heatmap help'")

    def exit(*args):
        """Fully exits the program."""
        if not args:
            sys.exit()
        if "del" in args and "upt" in args:
            utils.FUNCTIONS.end_process()
        elif "del" in args:
            utils.ALL_DATA.DATA_BASE.delete()
        elif "upt" in args:
            utils.ALL_DATA.DATA_BASE.update()
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

    def loadouts():
        matchId = input("    MatchId:")
        round = input("    Round:")
        player = input("    Player:")
        
        # Validar MatchId como UUID
        while not utils.FUNCTIONS.isUuidFormat(matchId):
            matchId = input("    MatchId:")
        
        # Validar que el round sea un número o esté vacío
        while not (round.isdigit() or round == ""):
            round = input("    Round:")
        
        # Validar que el jugador tenga formato de nombre completo o PUUID, o esté vacío
        while not (utils.FUNCTIONS.isFullName(player) or utils.FUNCTIONS.isPuuidFormat(player) or player == ""):
            player = input("    Player:")
        
        # Si el jugador se ingresó como nombre completo, convertirlo a PUUID
        if utils.FUNCTIONS.isFullName(player):
            player = utils.DATA_FINDERS.RIOT_USERS.get_puuid_by_name(player)
        
        Loadouts.run(matchId, round, player)


        
 
        
        

COMMANDS = {
    "help": {
        "definition": "Prints all commands you can execute",
        "function": lambda params: FUNTIONS.help(*params.split(" ")),
        "params": "command"
    },
    "exit": {
        "definition": "Exits the program",
        "function": lambda params: FUNTIONS.exit(*params.split(" ")),
        "params": '''
            del: Deletes all data stored in csv files.
        '''
    },
    "clear":{
        "definition": "Clears the console",
        "function": lambda: os.system('cls' if os.name == 'nt' else 'clear'),
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
    },
    "loadouts": {
        "definition": "Gives loadout information",
        "function": lambda : FUNTIONS.loadouts(),
        "params": ""
    }
}

def run():
    def start_process():
        # If files "Riot-Matches.csv" and "Riot-Users.csv" are not created, it executes start_process from utils.
        if not os.path.exists("VALORANT/Data_Base/Riot-Matches.csv") or not os.path.exists("VALORANT/Data_Base/Riot-Users.csv"):
            utils.FUNCTIONS.start_process()
        else:
            utils.FUNCTIONS.start_process(1)
    start_process()

    while True:
        command_line = input("command$ ")

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