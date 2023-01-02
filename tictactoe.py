#Tictactoe.py

from source.mygame import Client 
from source.mygame import printf, get_name, get_num
from source.core import Core
from source.data import SaveData
import playsound

DataClient = SaveData()
while True:
    name1, name2, mode = Core.gamemenu() #returns names and game mode after running function
    if not mode: #if exit option was pressed
        break
    else:
        name1 = DataClient.login(name1)
        if not name1:
            continue
        name2 = DataClient.login(name2)
        if not name2:
            continue
            
        while True:  #while true loop because the player can play again
            client = Client(name1, name2, mode)
            playsound.playsound("audio/GenericNotify.mp3")
            gamedata = Core.startgame(client)
            DataClient.logdata(gamedata)
            again = input("\tPlay again? (y/n):").lower()
            if again == "n":
                break
            elif again == "y":
                continue
            else:
                print("incorrect option, Taken as No.")
                playsound.playsound("audio/OutOfBound.mp3")
                break
    printf("Returning to main menu.",n2=2)
    
