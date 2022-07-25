import random
import matplotlib
from matplotlib import pyplot as plt
import copy
from matplotlib.animation import FuncAnimation 
#Connect four where the player will have the "x" symbol, and the computer will use the "o" symbol.

def build_grid():          
    l = []
    for i in range(7):
        l.append([""]*7)
    return l

def display_grid(grid):                
    for line in grid:                  
        print("|", end="")

        for x in line:                  
            if(x != ""):
                print(x, end="")
            else:
                print(x, end=" ")
        print("|")
    print()

def play_move(grid, symbol, column, is_real_player=False):
    try:
        column = int(column) - 1
    except:
        return False
    if column < 0 or column > 6:
        return False
    if grid[0][column] != "":
        if is_real_player == True:
            print("Yo, this column is already full. Choose another column")
        return False
    for i in range(7):
        if grid[6-i][column] == "":
            grid[6-i][column] = symbol
            break
    return grid

def game_loop(grid, display=True):
    turns_taken = 0
    while turns_taken < 49 and wonGame(grid) == False:
        
        Computer(grid, "o")

        if wonGame(grid) != False:      #In case the first player has won on his last turn.
            break
        
        Computer(grid, "x")

        if display:
            display_grid(grid)

        turns_taken += 1
    
    winner = wonGame(grid)
    if display:
        display_grid(grid)
    if winner == "o":
        print("The player using the 'o'-symbol has won")
    elif winner == "x":
        print("The player using the 'x'-symbol has won")
    else:
        print("It was a tie!")

    return turns_taken

def Player(grid, symbol):     #Should probably be a class, but..... too much work
    player_column = input("Player, choose a column to drop your piece in, ")
    while play_move(grid, symbol, player_column, is_real_player=True) == False:
        player_column = int(input("Player, choose a column to drop your piece in, "))

def Computer(grid, symbol):
    while play_move(grid, symbol, computer_play(grid, symbol)) == False:
        computer_play(grid, symbol)

def hasWinningMove(grid, symbol):
    for i in range(1, 8):          #Check whether it has a winning move
        copy_grid = copy.deepcopy(grid)
        play_move(copy_grid, symbol, i)
        if wonGame(copy_grid) == symbol:
            return [True, i]
    return False
    
def computer_play(grid, symbol):
    available_moves = [1, 2, 3, 4, 5, 6, 7]
    for i in grid:  #Iterate through grid and see if the column is full, if so remove that column as a possible move
        for j in i:
            if i == 6 and grid[i][j] != "":
                available_moves.remove(j)
    if hasWinningMove(grid, symbol):          #Check whether it has a winning move
        return hasWinningMove(grid, symbol)[1]
    else:                                      #If it has no winning move, it ensures that the move it plays doesn't allow for any moves for the opponent
        if symbol == "x":
            other_symbol = "o"
        elif symbol == "o":
            other_symbol = "x"
        for i in range(1, 8):
            grid_copy = copy.deepcopy(grid)
            play_move(grid_copy, symbol, i)
            if hasWinningMove(grid_copy, other_symbol):
                available_moves.remove(i)
        if available_moves != []:       #Maybe the computer just doesn't have a move that can prevent the opponent from winning. In that case it'll just choose a random move and accept defeat...
            return random.choice(available_moves)

    return random.randint(1, 7)


    #If there isn't a winning move, does the move played give an opportunity for the opponent to win the game
    return random.randint(1, 7)

def wonGame(grid):
    different_symbols = ["o", "x"]
    for symbol in different_symbols:
        for i in range(len(grid)):
            for j in range(len(grid)):
                try:
                    if grid[6-i][j] == symbol:      #6-i so that the iteration starts from the bottom of the grid
                        #Analyse whether they have four in a row vertically
                        if grid[6-i-1][j] == symbol and grid[6-i-2][j] == symbol and grid[6-i-3][j] == symbol:
                            return symbol
                        #Analyse whether they have four in a row horizontally
                        if grid[6-i][j+1] == symbol and grid[6-i][j+2] == symbol and grid[6-i][j+3] == symbol:
                            return symbol
                        #Analyse whether they have four in a row diagonally (upwards-sloping diagonal)
                        if grid[6-i-1][j+1] == symbol and grid[6-i-2][j+2] == symbol and grid[6-i-3][j+3] == symbol:
                            return symbol
                        #Analyse whether they have four in a row diagonally (downwards-sloping diagonal)
                        if grid[6-i-1][j-1] == symbol and grid[6-i-2][j-2] == symbol and grid[6-i-3][j-3] == symbol:
                            return symbol
                except IndexError:
                    continue
    return False    #By process of abduction
                    
def prep_grid_for_animation(grid):      #Using interpolation to correlate values to colours
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == "":
                grid[i][j] = 0
            elif grid[i][j] == "o":
                grid[i][j] = 125
            elif grid[i][j] == "x":
                grid[i][j] = 255
            else:
                continue
    return grid

game_board = build_grid()
Computer(game_board, "x") # player using "x" symbol starts by putting the first move. Without this line of code, animation will not work.

fig = plt.figure()       
ax = plt.axes()
game_board_copy = copy.deepcopy(game_board)   
game_board_init_anim = prep_grid_for_animation(game_board_copy)
img = ax.imshow(game_board_init_anim, cmap="YlOrRd")       

def animate(i, img, grid):    
    if i!=0 and wonGame(grid)==False: #For some reason the first frame repeats, giving the first player two turns, so we just skip it for the sake of the game. Now "x" starts
        print("Frame", i)
        if i % 2 == 1:
            Computer(grid, "o")
        elif i % 2 == 0:
            Computer(grid, "x")
        else:
            print("An error occurred")
        display_grid(grid)

    grid_copy_for_anim = copy.deepcopy(grid)
    grid_for_anim = prep_grid_for_animation(grid_copy_for_anim)
    img.set_data(grid_for_anim)

    
    return img




animation = FuncAnimation(fig, animate, fargs=(img, game_board), interval=50, frames=50, repeat=False)
animation.save("connect-four.gif", writer="imagemagick")
plt.show()
display_grid(game_board)

winner = wonGame(game_board)
if winner == "o":
    print("The player using the 'o'-symbol has won")
elif winner == "x":
    print("The player using the 'x'-symbol has won")
else:
    print("It was a tie!")
     
