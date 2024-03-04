"""
The sokoban module contains classes for representing and displaying sokoban puzzles. It also contains a main function for automatically solving sokoban puzzles.
"""

import turtle
from heuristics import *
import util.search as search
import argparse
import time

class SokobanPuzzle:
    """Represents a sokoban puzzle."""
    def __init__(self, puzzleStr):
        """The constructor takes a string representing the initial state of the puzzle and calls setState (see the description for details)."""
        self.__setBoardStr(puzzleStr)

    def __setBoardStr(self, boardStr):
        """Takes a string, representing a board state. The string should contain the layout of the puzzle, with rows separated by newline characters. Each row should be the same length and be made of the following symbols:
           . - Empty space
           # - Wall
           * - Goal
           O - Box on floor
           o - Box on goal
           + - Player on floor
           = - Player on goal
           There should be exactly one player and the number of goals should equal the number of boxes. The room should be surrounded by walls."""
            
        rows = boardStr.split()
        self.__board = [list(rows[i]) for i in range(len(rows))]

        self.__playerPos = None
        self.__boxPos = []
        self.__goalPos = []
        self.__numBoxes = 0
        self.__numGoals = 0
        self.__numOnGoal = 0
        for r in range(len(self.__board)):
            if len(self.__board[r]) != len(self.__board[0]):
                raise ValueError("Unequal row lengths.")
            
            for c in range(len(self.__board[r])):
                if self.__board[r][c] not in ['.', '#', '*', 'O', 'o', '+', '=']:
                    raise ValueError("Unexpected symbol: " + self.__board[r][c])
                
                if self.__board[r][c] in ['+', '=']:
                    if self.__playerPos != None:
                        raise ValueError("Multiple players at " + str(self.__playerPos) + " and " + str((r, c)))

                    self.__playerPos = (r, c)

                if self.__board[r][c] in ['*', 'o', '=']:
                    self.__numGoals += 1
                    self.__goalPos.append((r, c))
            
                if self.__board[r][c] in ['O', 'o']:
                    self.__numBoxes += 1
                    self.__boxPos.append((r, c, self.__board[r][c] == 'o'))
                    
                if self.__board[r][c] == 'o':
                    self.__numOnGoal += 1

        self.__goalPos.sort()
        self.__boxPos.sort()
                    
        if self.__playerPos == None:
            raise ValueError("No player found.")

        if self.__numGoals != self.__numBoxes:
            raise ValueError("Unequal boxes and goals: " + str(self.__numBoxes) + " boxes and " + str(self.__numGoals) + " goals.")

    def __getBoardStr(self):
        """Generates and returns a string that represents the current board state (in the format expected by setState."""
        rows = ["".join(self.__board[i])+"\n" for i in range(len(self.__board))]
        return "".join(rows)

    def getState(self):
        """Returns the state of the puzzle, represented as a tuple which contains the results of getPos and getBoxes."""
        return (self.getPos(), self.getBoxes())
    
    def setState(self, state):
        """Sets the state of the puzzle, represented as a tuple in the format returned by getState."""
        if len(self.__boxPos) != len(state[1]):
            raise ValueError("Incorrect number of boxes. Expected " + str(len(self.__boxPos)) + " but got " + str(len(state[1])))
        
        if self.__playerPos != state[0]:
            if state[0][0] < 0 or state[0][0] >= len(self.__board) or state[0][1] < 0 or state[0][1] >= len(self.__board[state[0][0]]):
                raise ValueError("Player position out of bounds: " + str(state[0]))
            
            if self.__board[self.__playerPos[0]][self.__playerPos[1]] == '+':
                self.__board[self.__playerPos[0]][self.__playerPos[1]] = '.'
            else:
                self.__board[self.__playerPos[0]][self.__playerPos[1]] = '*'

        for b in range(len(self.__boxPos)):
            if self.__boxPos[b] != state[1][b]:
                if state[1][b][0] < 0 or state[1][b][0] >= len(self.__board) or state[1][b][1] < 0 or state[1][b][1] >= len(self.__board[state[1][b][0]]):
                    raise ValueError("Box " + str(b) + " position out of bounds: " + str(state[0]))

                if self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] == 'O':
                    self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] = '.'
                else:
                    self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] = '*'
                    self.__numOnGoal -= 1

        if self.__playerPos != state[0]:
            self.__playerPos = state[0]
            if self.__board[self.__playerPos[0]][self.__playerPos[1]] == '.':
                self.__board[self.__playerPos[0]][self.__playerPos[1]] = '+'
            elif self.__board[self.__playerPos[0]][self.__playerPos[1]] == '*':
                self.__board[self.__playerPos[0]][self.__playerPos[1]] = '='
            else:
                raise ValueError("Invalid player position. Position " + str(state[0]) + " currently contains " + self.__board[self.__playerPos[0]][self.__playerPos[1]])

        for b in range(len(self.__boxPos)):
            if self.__boxPos[b] != state[1][b]:
                self.__boxPos[b] = state[1][b]
                if self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] == '.':
                    self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] = 'O'
                    if self.__boxPos[b][2] == True:
                        raise ValueError("Box " + str(b) + " incorrectly marked as on goal.")
                elif self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] == '*':
                    self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]] = 'o'
                    self.__numOnGoal += 1
                    if self.__boxPos[b][2] == False:
                        raise ValueError("Box " + str(b) + " incorrectly marked as off goal.")
                else:
                    raise ValueError("Invalid box position. Box " + str(b) + " position " + str(state[0]) + " currently contains " + self.__board[self.__boxPos[b][0]][self.__boxPos[b][1]])
    
    def move(self, dir):
        """Performs a move on the puzzle and returns the cost of the move. A non-pushing move costs 1. A pushing move costs 2. A failed move (due to obstruction) costs 3. The variable dir represents the direction and should be one of the following tuples:
           Up: (-1, 0)
           Left: (0, -1)
           Right: (0, 1)
           Down: (1, 0)"""

        if dir not in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            raise ValueError("Unrecognized direction: " + str(dir))

        newPos = (self.__playerPos[0]+dir[0], self.__playerPos[1]+dir[1])
        replacementSymb = '.'
        if self.__board[self.__playerPos[0]][self.__playerPos[1]] == '=':
            replacementSymb = '*'
        newSymb = '+'
        if self.__board[newPos[0]][newPos[1]] in ['*', 'o']:
            newSymb = '='

        cost = 3
        if self.__board[newPos[0]][newPos[1]] in ['.', '*']: #Empty space
            self.__board[newPos[0]][newPos[1]] = newSymb
            self.__board[self.__playerPos[0]][self.__playerPos[1]] = replacementSymb
            self.__playerPos = newPos
            cost = 1
        elif self.__board[newPos[0]][newPos[1]] in ['O', 'o']: #Box
            newBoxPos = (newPos[0] + dir[0], newPos[1] + dir[1])
            if self.__board[newBoxPos[0]][newBoxPos[1]] in ['.', '*']: #Box can move
                wasOnGoal = False
                if self.__board[newPos[0]][newPos[1]] == 'o': 
                    self.__numOnGoal -= 1 #Moving off a goal, subtract
                    wasOnGoal = True

                isOnGoal = False
                if self.__board[newBoxPos[0]][newBoxPos[1]] == '.':
                    self.__board[newBoxPos[0]][newBoxPos[1]] = 'O'
                else:
                    self.__board[newBoxPos[0]][newBoxPos[1]] = 'o' 
                    self.__numOnGoal += 1 #Moving onto a goal, add
                    isOnGoal = True
                    
                self.__boxPos.remove(newPos+tuple([wasOnGoal]))
                self.__boxPos.append(newBoxPos+tuple([isOnGoal]))
                self.__boxPos.sort()

                self.__board[newPos[0]][newPos[1]] = newSymb
                self.__board[self.__playerPos[0]][self.__playerPos[1]] = replacementSymb
                self.__playerPos = newPos
                
                cost = 2
        #else: either a wall or a box that can't move                   

        return cost

    def getSuccessors(self, state):
        """Takes a state string and returns a list of its successors. Each successor consists of a 4-tuple: (state string, action taken, step cost, goal):
        state string: the string representing the state
        action taken: the action tuple that led to this state
        step cost: the cost of the step taken to reach this state
        goal: True if the state is a goal state, False otherwise"""
        actions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        currentState = self.getState()
        self.setState(state)
        succ = []
        for a in actions:
            cost = self.move(a)
            succ.append((self.getState(), a, cost, self.isSolved()))
            self.setState(state)
        self.setState(currentState)
        return succ
    
    def isSolved(self):
        """Returns true if the puzzle is solved. False otherwise."""
        return self.__numOnGoal == self.__numBoxes

    def getPos(self):
        """Returns a tuple containing the position of the player."""
        return self.__playerPos

    def getGoals(self):
        """Returns a sorted list of the positions of the goals (as tuples)."""
        return tuple(self.__goalPos)

    def getBoxes(self):
        """Returns a sorted list of the boxes as triples: (row, column, onGoal)."""
        return tuple(self.__boxPos)

    def getItem(self, row, col):
        """Returns the item at the given board position (as a character from the string representation)."""
        return self.__board[row][col]

    def getDim(self):
        return len(self.__board), len(self.__board[0])
    
    def __str__(self):
        return self.__getBoardStr()

class SokobanDisplay:
    """Uses turtles to create a graphical display of a sokoban puzzle."""
    def __init__(self, problem):
        """Takes a SokobanPuzzle and initializes the display."""
        self.__problem = problem
        self.__totalScore = 0

        #Create the window
        numR, numC = self.__problem.getDim()
        squareWidth = 50
        turtle.setup(numC*squareWidth+10, numR*squareWidth+10)
        turtle.setworldcoordinates(0, numR+10/squareWidth, numC+10/squareWidth, 0)
        turtle.title("Sokoban")
        turtle.bgcolor(.85, .85, .6)

        #Draw the grid
        self.__gridT = turtle.Turtle()
        self.__gridT.width(3)
        self.__gridT.hideturtle()
        self.__gridT.pencolor(0.4, 0.3, 0.1)
        self.__gridT.fillcolor(0.5, 0.4, 0.2)
        turtle.tracer(0)
        for r in range(numR):
            for c in range(numC):
                self.__gridT.penup()
                self.__gridT.goto(c, r)
                if self.__problem.getItem(r, c) == '#':
                    self.__gridT.begin_fill()
                self.__gridT.pendown()
                for i in range(4):
                    self.__gridT.forward(1)
                    self.__gridT.left(90)
                if self.__problem.getItem(r, c) == '#':
                    self.__gridT.end_fill()

        #Create the boxes
        self.__boxTurtles = []
        for b in self.__problem.getBoxes():
            bTurtle = turtle.Turtle()
            bTurtle.shape("square")
            bTurtle.shapesize(1.5, 1.5, 3)
            bTurtle.fillcolor(0.8, 0.7, 0.2)
            bTurtle.pencolor(0.2, 0.2, 0)
            bTurtle.penup()
            self.__boxTurtles.append(bTurtle)            

        #Create the player
        self.__playerTurtle = turtle.Turtle()
        self.__playerTurtle.shape("circle")
        self.__playerTurtle.shapesize(1.5, 1.5, 3)
        self.__playerTurtle.fillcolor(0.5, 0.6, 0.7)
        self.__playerTurtle.pencolor(0.0, 0.1, 0.2)
        self.__playerTurtle.penup()

        self.update()
    
    def update(self):
        """Updates the puzzle display based on the problem's current state."""
        #Update the goals
        emptyGoalColor = (0.3, 0.8, 0.2)
        fullGoalColor = (0.8, 0.3, 0.2)
        for g in self.__problem.getGoals():
            if self.__problem.getItem(g[0], g[1]) == 'o':
                self.__gridT.pencolor(emptyGoalColor)
                self.__gridT.fillcolor(emptyGoalColor)
            else:
                self.__gridT.pencolor(fullGoalColor)
                self.__gridT.fillcolor(fullGoalColor)
            self.__gridT.penup()
            self.__gridT.goto(g[1]+0.15, g[0]+0.15)
            self.__gridT.begin_fill()
            self.__gridT.pendown()        
            for i in range(4):
                self.__gridT.forward(0.7)
                self.__gridT.left(90)
            self.__gridT.end_fill()    

        #Update the boxes
        boxes = self.__problem.getBoxes()
        for i in range(len(boxes)):
            self.__boxTurtles[i].goto(boxes[i][1]+0.5, boxes[i][0]+0.5)

        #Update the player
        playerPos = self.__problem.getPos()
        self.__playerTurtle.goto(playerPos[1]+0.5, playerPos[0]+0.5)

        turtle.update()

    def move(self, dir):
        """Performs a move in the puzzle and updates the display accordingly."""
        self.__totalScore += self.__problem.move(dir)
        self.update()
        if self.__problem.isSolved():
            print("Congratulations! Your total cost was: " + str(self.__totalScore))
            print("Click the main window to exit.")
            turtle.onkey(None, "Up")
            turtle.onkey(None, "Down")
            turtle.onkey(None, "Left")
            turtle.onkey(None, "Right")
            turtle.exitonclick()
    
    def moveNorth(self):
        """Performs a move to the north in the puzzle."""
        self.move((-1, 0))

    def moveSouth(self):
        """Performs a move to the south in the puzzle."""        
        self.move((1, 0))

    def moveWest(self):
        """Performs a move to the west in the puzzle."""        
        self.move((0, -1))

    def moveEast(self):
        """Performs a move to the east in the puzzle."""        
        self.move((0, 1))
           
def main():
    """Automatically solve sokoban puzzles."""
    parser = argparse.ArgumentParser(description='Solve Sokoban puzzles automatically or by hand.')
    parser.add_argument('puzzle_file', help='file containing the puzzle layout.')
    parser.add_argument('-p', '--playable', action='store_true', default=False, help='make the puzzle human-playable using the arrow keys')
    parser.add_argument('-nd', '--nodisplay', action='store_true', default=False, help='do not display the solution (has no effect with -p)')
    parser.add_argument('-n', '--null', action='store_true', default=False, help='use the null heuristic (has no effect with -p)')

    args = parser.parse_args()
    
    fin = open(args.puzzle_file)
    stateStr = fin.read()
    p = SokobanPuzzle(stateStr)
    print(p, end="")
    initState = p.getState()

    if not args.nodisplay or args.playable:
        display = SokobanDisplay(p)   

    if args.playable:
        turtle.onkey(display.moveNorth, "Up")
        turtle.onkey(display.moveSouth, "Down")
        turtle.onkey(display.moveWest, "Left")
        turtle.onkey(display.moveEast, "Right")
        print("Make sure the main window has focus.")
        print("Use the arrow keys to move.")
        print("If you get stuck, close the window to exit.")
        turtle.Screen().listen()
        turtle.mainloop()
    else:
        startT = time.time()
        if args.null:
            h = NullHeuristic(p)
        else:
            h = SokobanHeuristic(p)
        path,cost,numExpanded = search.aStarSearch(p, h)
        endT = time.time()

        print("Time spent: " + str(endT-startT) + " seconds")
        print("Nodes expanded: " + str(numExpanded))
        if path == [] and not p.isSolved():
            print("No solution found!")
            quit()
        else:     
            actionSeq = ""
            actions = {(0, 1):"E", (0, -1):"W", (1, 0):"S", (-1, 0):"N"}
            for a in path:
                actionSeq += actions[a]+" "       
            print("Action sequence: " + actionSeq)
            if args.nodisplay:
                print("Total cost: " + str(cost))
            else:
                p.setState(initState)
                for m in path:
                    display.move(m)
                    time.sleep(0.2)
    
if __name__ == "__main__":
    main()
