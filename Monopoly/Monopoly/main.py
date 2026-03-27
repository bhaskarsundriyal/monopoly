import random
import os
import time

# ================= COLORS =================
RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
BLUE="\033[94m"
CYAN="\033[96m"
MAGENTA="\033[95m"
PURPLE="\033[35m"
WHITE="\033[97m"
RESET="\033[0m"

os.system("color")

# ================ COLORS =================
TILE_COLORS=[
RED,GREEN,YELLOW,BLUE,CYAN,
MAGENTA,PURPLE,GREEN,YELLOW,BLUE,
CYAN,RED,MAGENTA,PURPLE,GREEN,
YELLOW,BLUE,CYAN,RED,MAGENTA
]

# ================= FILE =================
if not os.path.exists("highscore.txt"):
    open("highscore.txt","w").close()

# ================= BANNER =================
def mono_banner():
    art=r"""
 __  __  ____  _   _  ____ 
|  \/  |/ __ \| \ | |/ __ \
| \  / | |  | |  \| | |  | |
| |\/| | |  | | . ` | |  | |
| |  | | |__| | |\  | |__| |
|_|  |_|\____/|_| \_|\____/
        MONO BOARD
"""
    print(CYAN+art+RESET)

def clear():
    os.system("cls" if os.name=="nt" else "clear")

# ================= WINNER ANIMATION =================
def winner_animation(name):

    clear()
    mono_banner()

    colors=[RED,GREEN,YELLOW,BLUE,CYAN,MAGENTA]

    for i in range(8):

        clear()
        mono_banner()

        color=random.choice(colors)

        text=f"""
        🏆 WINNER 🏆

           {name}

      CONGRATULATIONS!
        """

        for char in text:
            print(color+char+RESET,end="",flush=True)
            time.sleep(0.002)

        time.sleep(0.4)

# ================= FILE HANDLING =================
def save_high_score(name,score):
    with open("highscore.txt","a") as f:
        f.write(f"{name}:{score}\n")

def show_high_score():

    clear()
    mono_banner()

    print(YELLOW+"\n--- HIGH SCORES ---\n"+RESET)

    scores=[]

    with open("highscore.txt","r") as f:

        for line in f:
            if ":" in line:
                name,score=line.strip().split(":")
                scores.append((name,int(score)))

    scores.sort(key=lambda x:x[1],reverse=True)

    for name,score in scores:
        print(GREEN+f"{name} - Rs{score}"+RESET)

    input("\nPress Enter...")

# ================= DATA =================
players=[]
pos=[]
money=[]
skip_turn=[]

board=[
"Start","Mumbai","Chance","Delhi","Tokyo","Jail",
"Kyoto","Chance","Rome","NewYork","Chance","Jail",
"Wash","Chance","Mumbai","Delhi","Chance","Tokyo","Rome","Jail"
]

property_price=200
rent_price=80
owner=[None]*len(board)

WIN_MONEY=5000

# ================= DICE ART =================
def dice_art(value):

    faces={
1:["┌─────┐","│     │","│  ●  │","│     │","└─────┘"],
2:["┌─────┐","│ ●   │","│     │","│   ● │","└─────┘"],
3:["┌─────┐","│ ●   │","│  ●  │","│   ● │","└─────┘"],
4:["┌─────┐","│ ● ● │","│     │","│ ● ● │","└─────┘"],
5:["┌─────┐","│ ● ● │","│  ●  │","│ ● ● │","└─────┘"],
6:["┌─────┐","│ ● ● │","│ ● ● │","│ ● ● │","└─────┘"]
    }

    return faces[value]

# ================= BOARD =================
def draw_board(dice=None):

    tokens=["♟","♜","♞","♝"]

    def tile(i):
        icon=""
        for p in range(len(players)):
            if pos[p]==i:
                icon+=tokens[p]

        name=board[i][:6]

        if owner[i]!=None:
            name=name+"*"

        color=TILE_COLORS[i]

        return color+f"{name}{icon}".center(14)+RESET

    top_line = BLUE+"+" + "+".join(["-"*14]*5) + "+"+RESET
    side_line = BLUE+"+" + "-"*14 + "+" + " "*46 + "+" + "-"*14 + "+"+RESET

    print("\n"+top_line)

    # TOP ROW
    print("|"+"|".join(tile(i) for i in range(0,5))+"|")
    print(top_line)

    # SIDE BOXES (separate, no center lines)
    print(f"|{tile(19)}|{' '*46}|{tile(5)}|")
    print(side_line)

    print(f"|{tile(18)}|{' '*46}|{tile(6)}|")
    print(side_line)

    # CENTER (DICE AREA)
    if dice:
        art=dice_art(dice)
        for i in range(5):
            if i==2:
                print(f"|{tile(17)}|{CYAN}{art[i].center(46)}{RESET}|{tile(7)}|")
            else:
                print(f"|{' '*14}|{CYAN}{art[i].center(46)}{RESET}|{' '*14}|")
        print(side_line)
    else:
        print(f"|{tile(17)}|{' '*46}|{tile(7)}|")
        print(side_line)

    print(f"|{tile(16)}|{' '*46}|{tile(8)}|")

    # BOTTOM
    print(top_line)
    print("|"+"|".join(tile(i) for i in range(15,10,-1))+"|")
    print(top_line)

    print("\nPlayers:\n")

    for i in range(len(players)):
        print(GREEN+f"{tokens[i]} {players[i]} Rs{money[i]}"+RESET)
def roll_dice():

    for i in range(5):
        print("\r🎲 Rolling...",end="",flush=True)
        time.sleep(0.08)

    value=random.randint(1,6)

    print(f"\rDice Result : {YELLOW}{value}{RESET}")
    time.sleep(0.3)

    return value

# ================= CHANCE =================
def chance_event(player_index):

    events=[
        ("Lottery +300",300),
        ("Teleport to Start",0),
        ("Bonus +200",200)
    ]

    text,value=random.choice(events)

    print(MAGENTA+text+RESET)

    if text=="Teleport to Start":
        pos[player_index]=0
        money[player_index]+=200
    else:
        money[player_index]+=value

# ================= JAIL =================
def jail_animation(player_index):

    print(RED+"Going to Jail..."+RESET)

    for i in range(3):
        print("LOCKED"+("."*i))
        time.sleep(0.5)

    skip_turn[player_index]=True

# ================= TILE LOGIC =================
def handle_tile(player_index):

    tile_name=board[pos[player_index]]

    print(CYAN+f"{players[player_index]} landed on {tile_name}"+RESET)

    if tile_name=="Chance":

        chance_event(player_index)

    elif tile_name=="Jail":

        jail_animation(player_index)

    elif tile_name!="Start":

        if owner[pos[player_index]]==None:

            ch=input("Buy property for Rs200 ? (y/n): ").lower()

            if ch=="y" and money[player_index]>=property_price:

                owner[pos[player_index]]=player_index
                money[player_index]-=property_price

                print(GREEN+"Property Bought!"+RESET)

        elif owner[pos[player_index]]!=player_index:

            print(RED+"Paying rent!"+RESET)

            money[player_index]-=rent_price
            money[owner[pos[player_index]]]+=rent_price

    input("Press Enter...")

# ================= BANKRUPTCY =================
def check_bankruptcy(player_index):

    if money[player_index] < 0:

        print(RED+f"{players[player_index]} is BANKRUPT!"+RESET)

        for i in range(len(owner)):
            if owner[i]==player_index:
                owner[i]=None

        players.pop(player_index)
        pos.pop(player_index)
        money.pop(player_index)
        skip_turn.pop(player_index)

        return True

    return False

# ================= MOVE PLAYER =================
def move_player(player_index):

    if skip_turn[player_index]:

        print(RED+f"{players[player_index]} is in Jail - Turn Skipped!"+RESET)

        skip_turn[player_index]=False
        time.sleep(1)

        return True

    cmd=input(f"\n{players[player_index]} turn - ENTER roll | q quit : ")

    if cmd.lower()=="q":
        return False

    dice_value=roll_dice()

    for _ in range(dice_value):

        clear()
        mono_banner()
        draw_board(dice_value)

        old_pos=pos[player_index]

        pos[player_index]=(pos[player_index]+1)%len(board)

        if old_pos>pos[player_index]:

            money[player_index]+=200
            print(GREEN+"Passed START +200 BONUS"+RESET)
            time.sleep(0.4)

        print(CYAN+f"P{player_index+1} walking..."+RESET)
        time.sleep(0.3)

    clear()
    mono_banner()
    draw_board(dice_value)

    handle_tile(player_index)

    return True

# ================= GAME =================
def start_game():

    global players,pos,money,skip_turn,owner

    players=[]
    owner=[None]*len(board)

    clear()
    mono_banner()

    for i in range(3):

        name=input(f"Enter name for Player {i+1}: ")
        players.append(name)

    pos=[0]*len(players)
    money=[1000]*len(players)
    skip_turn=[False]*len(players)

    round_number=1

    while True:

        clear()
        mono_banner()

        print(YELLOW+f"\n===== ROUND {round_number} ====="+RESET)

        draw_board()

        time.sleep(1)

        i=0

        while i < len(players):

            keep_playing=move_player(i)

            if keep_playing==False:

                # determine winner
                winner=max(range(len(players)),key=lambda x:money[x])

                winner_animation(players[winner])

                for p in range(len(players)):
                    save_high_score(players[p],money[p])

                input("\nPress Enter...")
                return

            if check_bankruptcy(i):
                continue

            if money[i]>=WIN_MONEY:

                winner_animation(players[i])

                save_high_score(players[i],money[i])

                input("Press Enter...")

                return

            i+=1

        round_number+=1

# ================= MENU =================
choice_menu={
1:"START",
2:"highest score",
3:"property",
4:"instructions",
5:"exit"
}

def main():

    while True:

        clear()
        mono_banner()

        print(YELLOW+"\nMenu:"+RESET)

        for k,v in choice_menu.items():
            print(f"{k}. {v}")

        try:
            choice=int(input("Choice: "))
        except:
            continue

        if choice==1:
            start_game()

        elif choice==2:
            show_high_score()

        elif choice==3:
            print("Properties auto managed.")
            input("Press Enter...")

        elif choice==4:
            print("Chance events, Jail locks, Bankruptcy enabled.")
            input("Press Enter...")

        elif choice==5:
            break

if __name__=="__main__":
    main()