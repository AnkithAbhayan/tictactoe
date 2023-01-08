#mygame.py
import random
import playsound
from datetime import datetime
import os

#printf
def printf(message, t=1, n=0, n2=0):
    print("\n"*n,"\t"*t,message,"\n"*n2,sep="")

def clear():
    cmd = "clear"
    if os.name == "nt":
        cmd = "cls"
    os.system(cmd)


def get_name(message):
    while True:
        name = input(message).strip()
        if len(name) < 3 or len(name) > 20:
            printf("Name has to be between 3 and 20 characters long.")
        elif name.isdigit():
            printf("Name must include characters.")
        elif name.lower() in ["computer", "computer1", "computer2", "", "x", "o", "draw","win","lose"]:
            printf("Invalid name.")
        else:
            return name
            break

def get_num(message):
    while True:
        ch = input(message).strip()
        if not ch.isdigit():
            printf("Enter a valid number.",n2=1)
            continue
        break
    return int(ch)

class Client:
    def __init__(self, name1, name2, mode):
        list1 = [name1, name2]
        if name1 != "computer":
            random.shuffle(list1)
            
        self.mode = mode
        self.grid = [" "," "," "," "," "," "," "," "," "]
        self.players = {
            "X":list1[0],
            "O":list1[1]
        }
        self.current = "X" #decides who plays first
        self.turn = self.players["X"] #name of person currently playing
        self.warning = False
        self.moves = []
        self.winner = ""
        self.time = [datetime.now().timestamp()]

    def swap_turn(self):
        if self.current == "X":
            self.current = "O"
            self.turn = self.players["O"]
        else:
            self.current = "X"
            self.turn = self.players["X"]

    def print_board(self):
        printf("     |     |                                             ",t=2,n=1) 
        printf("  "+self.grid[0]+"  |  "+self.grid[1]+"  |  "+self.grid[2],t=2)
        printf("_ _ _|_ _ _|_ _ _                                        ",t=2)
        printf("     |     |                                             ",t=2)
        printf("  "+self.grid[3]+"  |  "+self.grid[4]+"  |  "+self.grid[5],t=2)
        printf("_ _ _|_ _ _|_ _ _                                        ",t=2)
        printf("     |     |                                             ",t=2)
        printf("  "+self.grid[6]+"  |  "+self.grid[7]+"  |  "+self.grid[8],t=2)
        printf("     |     |",t=2,n2=2)
    
    def process_choice(self):
        while True:
            ch = input("\t"+self.turn+", Enter choice:").strip()
            print()
            if not ch.isdigit():
                printf("Invalid number. (1-9 only)")
                playsound.playsound("audio/OutOfBound.mp3")
                continue
            ch = int(ch)         
            if ch > 9 or ch <= 0:
                printf("Invalid number. (1-9 only)")
                playsound.playsound("audio/OutOfBound.mp3")
                continue 

            elif self.grid[ch-1] != " ":
                printf("Place already occupied.")
                playsound.playsound("audio/OutOfBound.mp3")
                continue
            else:
                del self.grid[ch-1]
                self.grid.insert(ch-1, self.current)
                return ch-1

    def showwarning(self):
        for i in ["X","O"]:
            count = 0
            for x in [0,2,6,8]:
                if self.grid[x] == i:
                    count += 1
            if count >= 3:
                if self.warning == False:
                    self.warning = True
                    return True
        return False
        

    def make_move(self):
        def find_triangle(x,y):
            if y not in [0,1,2] and x in [0,1,2]:
                return [0,2][[0,2].index(x)-1]
            elif y not in [2,5,8] and x in [2,5,8]:
                return [2,8][[2,8].index(x)-1]
            elif y not in [6,7,8] and x in [6,7,8]:
                return [6,8][[6,8].index(x)-1]
            elif y not in [0,3,6] and x in [0,3,6]:
                return [0,6][[0,6].index(x)-1]
        #all win possibilities
        a = self.current
        if a == "X":
            b = "O"
        else:
            b = "X"

        if self.grid.count(" ") == 7:
            posx,posy = self.grid.index("X"), self.grid.index("O")
            return find_triangle(posx,posy)

        for i in [a,b]: #first try to win, then defend against defeat
            #horizontal win possibilities
            if self.grid[0:3] == [i,i," "]:
                return 2
            elif self.grid[3:6] == [i,i," "]:
                return 5
            elif self.grid[6:9] == [i,i," "]:
                return 8

            elif self.grid[0:3] == [" ",i,i]:
                return 0
            elif self.grid[3:6] == [" ",i,i]:
                return 3
            elif self.grid[6:9] == [" ",i,i]:
                return 6

            elif self.grid[0:3] == [i," ",i]:
                return 1
            elif self.grid[3:6] == [i," ",i]:
                return 4
            elif self.grid[6:9] == [i," ",i]:
                return 7
            
            #vertical win possibilities
            elif [self.grid[0], self.grid[3], self.grid[6]] == [i,i," "]:
                return 6
            elif [self.grid[1], self.grid[4], self.grid[7]] == [i,i," "]:
                return 7
            elif [self.grid[2], self.grid[5], self.grid[8]] == [i,i," "]:
                return 8

            elif [self.grid[0], self.grid[3], self.grid[6]] == [" ",i,i]:
                return 0
            elif [self.grid[1], self.grid[4], self.grid[7]] == [" ",i,i]:
                return 1
            elif [self.grid[2], self.grid[5], self.grid[8]] == [" ",i,i]:
                return 2

            elif [self.grid[0], self.grid[3], self.grid[6]] == [i," ",i]:
                return 3
            elif [self.grid[1], self.grid[4], self.grid[7]] == [i," ",i]:
                return 4
            elif [self.grid[2], self.grid[5], self.grid[8]] == [i," ",i]:
                return 5

            #diagonal win possibilities
            elif [self.grid[0], self.grid[4], self.grid[8]] == [" ",i,i]:
                return 0
            elif [self.grid[0], self.grid[4], self.grid[8]] == [i," ",i]:
                return 4
            elif [self.grid[0], self.grid[4], self.grid[8]] == [i,i, " "]:
                return 8

            elif [self.grid[2], self.grid[4], self.grid[6]] == [" ",i,i]:
                return 2
            elif [self.grid[2], self.grid[4], self.grid[6]] == [i," ",i]:
                return 4
            elif [self.grid[2], self.grid[4], self.grid[6]] == [i,i," "]:
                return 6

        else:
            #use b
            if [self.grid[1], self.grid[5]] == [b,b] or [self.grid[5], self.grid[7]] == [b,b] or [self.grid[7], self.grid[3]] == [b,b] or [self.grid[3], self.grid[1]] == [b,b]:
                if self.grid[4] == " ": return 4
            vals = [0,2,6,8]
            random.shuffle(vals)
            if self.mode == "cvc":
                vals.insert(2,4)
            else:
                vals.append(4)

            e = [1,3,5,7]
            random.shuffle(e)
            vals.extend(e)

            for i in vals:
                if self.grid[i] == " ":
                    return i
                
                
    def check_win(self):
        won = True
        grid = self.grid
        #checking for draw
        for key in ["X", "O"]:
            #horizontal win possibilities
            if [grid[0], grid[1], grid[2]] == [key, key, key]:
                break
            elif [grid[3], grid[4], grid[5]] == [key, key, key]:
                break
            elif [grid[6], grid[7], grid[8]] == [key, key, key]:
                break
            #vertical win possibilities
            elif [grid[0], grid[3], grid[6]] == [key, key, key]:
                break
            elif [grid[1], grid[4], grid[7]] == [key, key, key]:
                break
            elif [grid[2], grid[5], grid[8]] == [key, key, key]:
                break
            #diagonal win possibilities
            elif [grid[0], grid[4], grid[8]] == [key, key, key]:
                break
            elif [grid[2], grid[4], grid[6]] == [key, key, key]:
                break
        else:
            if grid.count(" ") == 0:
                self.winner = "draw"
                self.time.append(datetime.now().timestamp())
                return self.winner
            else:
                won = False
        
        if won == True:
            self.time.append(datetime.now().timestamp())
            if key == "X":
                self.winner = self.players["X"]
                return self.winner
            else:
                self.winner = self.players["O"]
                return self.winner
        else:
            return False