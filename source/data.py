import json
from datetime import datetime
from source.mygame import printf, get_num, get_name, convert_time

class SaveData:
    def __init__(self):
        self.path = "data\\data.json"
        with open(self.path, "r") as JsonFile:
            self.data = json.load(JsonFile)

    def savedata(self):
        with open(self.path, "w") as JsonFile:
            json.dump(self.data, JsonFile, indent=4)

    def createaccount(self):
        def check_pass(password):
            if len(password) < 8 or len(password) > 32:
                printf("Password has to be between 8 and 32 characters long.",n2=1)
            elif password.isspace():
                printf("Password must contain characters.",n2=1)
            else:
                return True

        name = get_name("\n\tEnter new account name:")
        if name in self.data["players"]:
            printf("Username already taken! Try again.")
            self.createaccount()
 
        while True:
            password = input("\tEnter a password:")
            if not check_pass(password):
                continue
            break

        newplayerdict = {
            name:{
                "created":datetime.now().timestamp(),
                "last played":0,
                "games played":0,
                "wins/loss/draw":[0,0,0],
                "gameids":[],
                "level":1,
                "xp":0,
                "password":password
            }
        }
        self.data["players"].update(newplayerdict)
        self.savedata()
        printf("New account made!")
        return name

    def logdata(self, gamedata):
        gamenum = self.data["totalgames"]+1
        data = {
            gamenum:{
                "players":[gamedata.players["X"], gamedata.players["O"]],
                "winner":gamedata.winner,
                "time":gamedata.time,
                "moves":gamedata.moves
            }
        }
        self.data["totalgames"] += 1
        self.data["games"].update(data)

        for item in data[gamenum]["players"]:
            self.data["players"][item]["last played"] = gamedata.time[-1]
            self.data["players"][item]["games played"] += 1
            self.data["players"][item]["gameids"].append(gamenum)
            if gamedata.winner == item: #this guy won
                self.data["players"][item]["wins/loss/draw"][0] += 1
                xp = 100 + (1000/abs(round(gamedata.time[1]-gamedata.time[0])))
                self.data["players"][item]["xp"] += xp
            elif gamedata.winner == "draw":
                self.data["players"][item]["wins/loss/draw"][2] += 1
                self.data["players"][item]["xp"] += 20
            else:
                self.data["players"][item]["wins/loss/draw"][1] += 1
        self.savedata()

    def checkuser(self, name):
        if name in self.data["players"]:
            return True
        return False

    def shell(self):
        with open(self.path, "r") as JsonFile:
            self.data = json.load(JsonFile)
        def invalid():
            if cmd[0] != "":
                printf("\tInvalid command. Enter 'help' for more info or 'exit' to exit.",n2=1,n=1)

        def playercmd():
            if len(cmd)==1:
                printf("\tNo player name entered.",n=1)
                printf("\tformat: player/(playername)",n2=1)
                return
            name = cmd[1]
            if not self.checkuser(name):
                printf(f"\tPlayer '{name}' doesn't exist.",n=1,n2=1)
                return
            data = self.data["players"][name]
            ttime = 0
            for item in data["gameids"]:
                ttime += (self.data["games"][str(item)]["time"][1]-self.data["games"][str(item)]["time"][0])
            ttime = convert_time(round(ttime))

            printf(f"\tShowing data for player '{name}':",n=2)
            printf(f"\t+{'-'*35}")
            printf(f"\t| Created:         {datetime.utcfromtimestamp(data['created']).strftime('%Y-%m-%d %H:%M:%S')}")
            printf(f"\t| Last played:     {datetime.utcfromtimestamp(data['last played']).strftime('%Y-%m-%d %H:%M:%S')}")
            printf(f"\t| Games played:    {data['games played']}")
            printf(f"\t| Most recent IDs: {data['gameids'][-5:]}")
            printf(f"\t| Time played:     {ttime}")
            printf(f"\t| wins/loss/draw:  {data['wins/loss/draw']}")
            printf(f"\t| total xp:        {round(data['xp'])}")
            printf(f"\t| level:           {data['xp']//250}")
            printf(f"\t+{'-'*35}",n2=2)


        def gamecmd():
            if len(cmd) == 1:
                printf(f"No game ID entered. (enter between 1 - {self.data['totalgames']})",n=1)
                printf("format: game/(gameid)",n2=1)
                return

            try:
                gid = int(cmd[1])
            except:
                printf(f"Invalid number. (enter between 1 - {self.data['totalgames']})",n=1)
                printf("format: game/(gameid)",n2=1)
                return

            if gid > self.data["totalgames"] or gid<1:
                printf(f"Invalid number. (enter between 1 - {self.data['totalgames']})",n=1)
                printf("format: game/(gameid)",n2=1)
                return
            gid = str(gid)

            game = self.data["games"][gid]
            printf(f"\tShowing data of Game no. #{gid}:",n=2)
            printf(f"\t+{'-'*35}")
            printf(f"\t| Players:    {game['players']}")
            if game["winner"] not in game["players"]:
                printf(f"\t| Result:     DRAW")
            else:
                printf(f"\t| Winner:     {game['winner']}")

            ttime = round(game['time'][1]-game['time'][0])
            ttime = convert_time(ttime)
            printf(f"\t| Duration:   {ttime}")
            printf(f"\t| Start time: {datetime.utcfromtimestamp(game['time'][0]).strftime('%Y-%m-%d %H:%M:%S')}")
            printf(f"\t| End time:   {datetime.utcfromtimestamp(game['time'][1]).strftime('%Y-%m-%d %H:%M:%S')}")
            printf(f"\t| Moves:      {game['moves']}")
            printf(f"\t+{'-'*35}",n2=2)

        def helpcmd():
            printf("Help Message.")
            printf("Commands:")
            printf("   players/(playername)")
            printf("   games/(gameid)")
            printf("   help")
            printf("   exit")

        def exit():
            printf("Returning to main menu...")
            return "exit"

        cmds = {
            "player":playercmd,
            "players":playercmd,
            "game":gamecmd,
            "games":gamecmd,
            "help":helpcmd,
            "exit":exit
        }
        printf("Entering Data Fetching mode, enter 'help' for more information.",n=1)
        while True:
            cmd = input("\t$tictactoe> ").split("/")
            func = cmds.get(cmd[0], invalid)
            if func() == "exit":
                break

    def login(self, name, sname=None):
        if name.isdigit():
            name = get_name("\tEnter your name:")
        elif name in ["computer", "computer1", "computer2"]:
            return name

        while True:
            if not self.checkuser(name):
                printf(f"Username {name} doesn't exist. (1. Create an account/2. Enter another account/3. Exit game)",n=1)
                ch = get_num("\tEnter choice (1/2/3):")
                if ch == 1:
                    return self.createaccount()
                elif ch == 2:
                    name = get_name("\tEnter your name:")
                elif ch == 3:
                    return False
                else:
                    printf("Enter either 1,2 or 3 only.",n2=1)
            else:
                if name == sname:
                    printf("Account already chosen for player1. Choose another.",n2=1)
                    return self.login("2", sname)
                break

        while True:
            password = input(f"\tEnter password for '{name}':")
            if self.data["players"][name]["password"] == password:
                printf("Correct password!")
                break
            else:
                printf("Wrong password! (1. Try again/2. Use another account/3. Exit Game)",n=1)
                ch = get_num("\tEnter choice (1/2/3):")
                if ch == 1:
                    continue
                elif ch == 2:
                    name = get_name("\n\tEnter your name:")
                    self.checkuser(name)
                elif ch == 3:
                    return False
                else:
                    printf("Enter either 1,2 or 3 only.",n2=1)

        return name






        