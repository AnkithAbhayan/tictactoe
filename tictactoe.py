#Tictactoe.py

from source.mygame import Client 
from source.mygame import printf, get_name, get_num
import playsound

class PlayGame:
    def gamemenu():        
        printf(f"+{'-'*104}+", n=1)
        #print(pyfiglet.figlet_format("TIC TAC TOE", font="wavy"))
        printf("OXOXXOXOXO  OX   OXOXOXO     OXOXOXOXOX   XOXOXXOXO    OXXOXOX     XOXOXOXOXO   XOOXOXOX   OXOXOXOXO")
        printf("    OX      XO  OX               XO      XO       XO  OX               OX      XO      OX  XO ") 
        printf("    XO      OX  XO               OX      OX       OX  XO               XO      OX      XO  OX ")
        printf("    OX      XO  OX      XXXXX    XO      XOXOXOXOXOX  OX      OOOOO    OX      XO      OX  XOXOXOXOX ")
        printf("    XO      OX  XO               OX      OX       OX  XO               XO      OX      XO  OX ")
        printf("    OX      XO  OX               XO      XO       XO  OX               OX      XO      OX  XO ")
        printf("    OX      XO   XOXOXOX         OX      XO       XO   XOOXOXO         OX       OXXOXOXO   XOXOXOXOX")
        printf(f"+{'-'*104}+",n2=3)


        printf(f"+{'-'*20}+", t=6)
        printf("| 1. Play.           |", t=6)
        printf("| 2. Instructions.   |", t=6)
        printf("| 3. Credits.        |", t=6)
        printf("| 4. Exit.           |", t=6)
        printf(f"+{'-'*20}+",n2=2,t=6)
        #playsound.playsound("audio/genericnotify.mp3")
        while True: #determining name and mode
            opt = get_num("\tEnter option:")
            if opt == 1:
                printf(f"+{'-'*26}+", n=1,t=2)
                printf("|  MODES:                  |",t=2)
                printf("|  1. player vs player     |",t=2)
                printf("|  2. player vs Computer   |",t=2)
                printf("|  3. Computer vs Computer |",t=2)
                printf(f"+{'-'*26}+\n",t=2)
                opt = get_num("\tEnter mode:")
                if opt == 1:
                    mode = "pvp"
                    name1 = get_name("\tEnter player1 name:")
                    name2 = get_name("\tEnter player2 name:")
                    break
                elif opt == 2:
                    mode = "pvc"
                    name1 = "Computer"
                    name2 = get_name("\tEnter your name:")
                    break
                elif opt == 3:
                    mode = "cvc"
                    name1, name2 = "Computer1", "Computer2"
                    break
                else:
                    printf("Wrong option. Enter 1,2 or 3 only.")
                    playsound.playsound("audio/OutOfBound.mp3")
                    printf("Going back to main menu..")

            elif opt == 2:
                printf(f"+{'-'*64}+",t=2,n=1)
                printf("|    INSTRUCTIONS:                                               |",t=2)
                printf("|                                                                |",t=2)
                printf("|                     BOARD FORMAT                               |",t=2)
                printf("|                          |     |                               |",t=2) 
                printf("|                       1  |  2  |  3                            |",t=2)
                printf("|                     _ _ _|_ _ _|_ _ _                          |",t=2)
                printf("|                          |     |                               |",t=2)
                printf("|                       4  |  5  |  6                            |",t=2)
                printf("|                     _ _ _|_ _ _|_ _ _                          |",t=2)
                printf("|                          |     |                               |",t=2)
                printf("|                       7  |  8  |  9                            |",t=2)
                printf("|                          |     |                               |",t=2)
                printf("|                                                                |",t=2)
                printf("|    1. The numbers on the board above represent the positions   |",t=2)
                printf("|       where your sign (X or O) is to be entered.               |",t=2)
                printf("|    2. You will be randomly assigned X or O and you will take   |",t=2)
                printf("|       turns placing your sign in a vacant square on the board  |",t=2)
                printf("|    3. Fill an entire row, column or a diagonal with just your  |",t=2)
                printf("|       sign to win the game.                                    |",t=2)
                printf(f"+{'-'*64}+",t=2)
            elif opt == 3:
                printf("Built by Ankith Abhayan, 11C.")
            elif opt == 4:
                printf("Exiting...")
                return "", "", ""
            else:
                printf("Enter a valid option.")
                playsound.playsound("audio/OutOfBound.mp3")
            print()
        return name1, name2, mode

    def startgame(client):
        printf(f"{client.players['X']} will use X.\n\t{client.players['O']} will use O.",n2=2,n=1)
        client.print_board()
        while True:
            #make player input move depending on game mode
            if client.mode == "pvc":
                if client.players[client.current] == "Computer":
                    printf("Computer is making a move...")
                    pos = client.make_move()
                    client.grid[pos] = client.current
                else:
                    client.process_choice()
                    
            elif client.mode == "pvp":
                client.process_choice()
                
            elif client.mode == "cvc":
                printf(f"{client.turn} is making a move...")
                pos = client.make_move()
                client.grid[pos] = client.current
                  
            client.print_board()
            playsound.playsound("audio/Capture.mp3")

            #check if theres a win
            if winner:=client.check_win():
                if winner == "draw":
                    printf("DRAW")
                else:
                    printf(f"WINNER IS: {winner}")
                playsound.playsound("audio/GenericNotify.mp3")
                break

            if client.showwarning():
                playsound.playsound("audio/LowTime.mp3")
            #turn to next person
            client.swap_turn()
            
while True:
    name1, name2, mode = PlayGame.gamemenu() #returns names and game mode after running function
    if not mode: #if exit option was pressed
        break
    else:
        while True:
            client = Client(name1, name2, mode)
            playsound.playsound("audio/GenericNotify.mp3")
            PlayGame.startgame(client) 
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
    #while true loop because the player can play again
