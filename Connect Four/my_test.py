import AA
import connectfour
def makeState(board):
    '''Returns the state of the game (as a string).'''
    rows = [" ".join(board[i]) + "\n" for i in range(len(board) - 1, -1, -1)]
    return "".join(rows)


# Option 1 - making a board with hard code.
empty = ["."] * 7
row6 = [".", ".", "O", "X", ".", ".", "."]
row5 = [".", ".", "O", "X", ".", "O", "."]
board = [row6, empty, empty, empty, empty, empty]

# Option 2 - Reading a board from a file.
file = open('sample_board.txt', 'r')
lines = file.readlines()
board = [[letter for letter in line.strip()] for line in lines]
board.reverse()
# Print the board if you want to see it
print(board)

# Either way, this code will draw the board you made if you want.
# BUT - First you should go to the connectfour file and replace the line
# cImage = None
# with these lines:

#import util.cImage
#global cImage
#cImage = util.cImage

problem = connectfour.ConnectFour()
display = connectfour.ConnectFourDisplay(problem)
state_of_interest = makeState(board)
problem.setState(state_of_interest)
display.update()

# And this is to test your code
my_code = c4agent.C4HeuristicEval(problem)
print("Your evaluation of this board is: ")
print(my_code.eval(state_of_interest))

display.exitonclick()


