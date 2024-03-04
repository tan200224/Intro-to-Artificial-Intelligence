"""
The slidingpuzzle module contains classes for representing and displaying sliding puzzles. It also contains a main function for automatically solving sliding puzzles.
"""
import random
import util.cImage as cImage

from heuristics import *
import time
import util.search as search
import argparse


class SlidingPuzzle:
    """Represents a sliding puzzle."""
    def __init__(self, numRows, numColumns, numTurns):
        """The constructor takes the dimensions of the puzzle and initializes it to a random state that takes numTurns moves to solve."""
        self.__numR = numRows
        self.__numC = numColumns
        self.__board = []
        num = 0
        for i in range(numRows):
            row = []
            for j in range(numColumns):
                row.append(num)
                num+=1
            self.__board.append(row)
        self.__blank = 0
        self.__pos = (self.__blank//self.__numC, self.__blank%self.__numC)
        self.__numMisplaced = 0
        self.setState(self.getScrambledStates(numTurns)[0])


    def getScrambledStates(self, numTurns, numStates=1):
        """Randomly generates numStates states that take numTurns moves to solve and returns them in a list."""
        fringe = []
        visited = {}
        inFringe = {}
        startState = self.getState()
        fringe.append((startState, 0))
        inFringe[startState] = True
        while fringe[0][1] < numTurns:
            s = fringe.pop(0)
            successors = self.getSuccessors(s[0])
            for succ in successors:
                if succ[0] not in inFringe:
                    fringe.append((succ[0], s[1]+1))
                    inFringe[succ[0]] = True
        states = random.sample(fringe, numStates)
        return [s[0] for s in states]

    def getState(self):
        """Returns the state of the puzzle represented as a string."""
        stateStr = ""
        for row in self.__board:
            stateStr += str(row[0])
            for i in range(1, len(row)):
                stateStr += " "+str(row[i])
            stateStr += "\n"
        return stateStr

    def setState(self, state):
        """Sets the state of the puzzle, represented as a string in the format returned by getState."""
        rows = state.split("\n")[:-1]
        if len(rows) != self.__numR:
            raise ValueError("Given puzzle has incorrect size. Number of rows: " + str(len(rows)-1) + " (expected " + str(self.__numR) + ")")

        seen = [False]*self.__numR*self.__numC
        misplaced = 0
        newPos = None
        place = 0
        newBoard = []
        for i in range(len(rows)):
            row = rows[i].split()
            if len(row) != len(self.__board[i]):
                raise ValueError("Given puzzle has incorrect size. In row " + str(i) + " number of columns: " + str(len(row)) + " (expected " + str(self.numC) + ")")
            newBoard.append([])
            for j in range(len(row)):
                tile = int(row[j])
                if tile < 0 or tile >= self.__numR*self.__numC:
                    raise ValueError("Invalid state: " + str(tile) + " is not a valid tile index.")
                if seen[tile]:
                    raise ValueError("Invalid state: contains tile " + str(tile) + " at least twice.")
                newBoard[i].append(tile)
                seen[tile] = True
                if tile == self.__blank:
                    newPos = (i, j)
                if tile != place:
                    misplaced += 1
                place += 1
        self.__pos = newPos
        self.__numMisplaced = misplaced
        self.__board = newBoard

    def move(self, dir):
        """Performs a move in the puzzle and returns the cost of the move. All legal moves cost 1. Illegal moves will cause an error. The variable dir represents the direction and should be one of the following tuples, representing the direction the "blank" tile should move:
           Up: (-1, 0)
           Left: (0, -1)
           Right: (0, 1)
           Down: (1, 0)"""
        if dir not in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            raise ValueError("Unrecognized direction: " + str(dir))
        newPos = (self.__pos[0]+dir[0], self.__pos[1]+dir[1])
        if newPos[0] < 0 or newPos[0] >= self.__numR or newPos[1] < 0 or newPos[1] >= self.__numC:
            raise ValueError("Illegal move. Current position of blank tile: " + str(self.__pos) + " Direction: " + str(dir))
        tile = self.__board[newPos[0]][newPos[1]]

        blankPos = (self.__blank//self.__numC, self.__blank%self.__numC)
        if self.__pos == blankPos:
            self.__numMisplaced += 1
        if newPos == blankPos:
            self.__numMisplaced -= 1
        if tile == newPos[0]*self.__numC + newPos[1]:
            self.__numMisplaced += 1
        if tile == self.__pos[0]*self.__numC + self.__pos[1]:
            self.__numMisplaced -= 1

        self.__board[self.__pos[0]][self.__pos[1]] = tile
        self.__board[newPos[0]][newPos[1]] = self.__blank
        self.__pos = newPos
        return 1

    def legalMoves(self):
        """Returns a list of all legal moves from the current state."""
        legalMoves = []
        if self.__pos[0] > 0:
            legalMoves.append(tuple([-1, 0]))
        if self.__pos[0]<self.__numR - 1:
            legalMoves.append(tuple([1, 0]))
        if self.__pos[1] > 0:
            legalMoves.append(tuple([0, -1]))
        if self.__pos[1] < self.__numC - 1:
            legalMoves.append(tuple([0, 1]))
        return legalMoves

    def getSuccessors(self, state):
        """Takes a state string and returns a list of its successors. Each successor consists of a 4-tuple: (state string, action taken, step cost, goal):
        state string: the string representing the state
        action taken: the action tuple that led to this state
        step cost: the cost of the step taken to reach this state
        goal: True if the state is a goal state, False otherwise"""
        currentState = self.getState()
        self.setState(state)
        succ = []
        for a in self.legalMoves():
            cost = self.move(a)
            succ.append((self.getState(), a, cost, self.isSolved()))
            self.setState(state)
        self.setState(currentState)
        return succ

    def isSolved(self):
        """Returns true if the puzzle is solved. False otherwise."""
        return self.__numMisplaced == 0

    def __str__(self):
        """Returns a string representation of the puzzle (same as getState)."""
        return self.getState()

    def getDim(self):
        return self.__numR, self.__numC

    def getTile(self, row, column):
        """Returns the tile index at the given position."""
        return self.__board[row][column]

    def getBoard(self):
        """Returns a copy of the puzzle board."""
        return [self.__board[r][:] for r in range(self.__numR)]

    def getPos(self):
        """Returns the position of the blank tile."""
        return self.__pos

    def getBlank(self):
        """Returns the index of the blank tile."""
        return self.__blank

class SlidingPuzzleDisplay:
    """Displays the sliding puzzle with a given image."""
    def __init__(self, problem, imageFilename):
        """Takes a SlidingPuzzle and the filename for a GIF image and initializes the display."""
        self.__problem = problem
        self.__totalScore = 0
        numRows, numCols = problem.getDim()

        image = cImage.FileImage(imageFilename)
        self.__tileHeight = image.getHeight()//numRows
        self.__tileWidth = image.getWidth()//numCols
        self.__tileList = []
        for i in range(numRows*numCols):
            self.__tileList.append(cImage.EmptyImage(self.__tileWidth, self.__tileHeight))

        t = 0
        for r in range(numRows):
            for c in range(numCols):
                for x in range(self.__tileWidth):
                    for y in range(self.__tileHeight):
                        self.__tileList[t].setPixel(x, y, image.getPixel(c*self.__tileWidth + x, r*self.__tileHeight + y))
                t = t + 1

        for x in range(self.__tileWidth):
            for y in range(self.__tileHeight):
                imagePix = image.getPixel(x, y)
                newPix = [imagePix[i]+75 for i in range(3)]
                for i in range(len(newPix)):
                    if newPix[i] > 255:
                        newPix[i] = 255
                self.__tileList[self.__problem.getBlank()].setPixel(x, y, cImage.Pixel(newPix[0], newPix[1], newPix[2]))

        self.__win = cImage.ImageWin("Sliding Puzzle!", numCols*self.__tileWidth, numRows*self.__tileHeight)
        self.update()

    def update(self):
        """Updates the puzzle display based on the problem's current state."""
        numRows, numCols = self.__problem.getDim()
        for r in range(numRows):
            for c in range(numCols):
                self.__tileList[self.__problem.getTile(r, c)].setPosition(c*self.__tileWidth, r*self.__tileHeight)
                self.__tileList[self.__problem.getTile(r, c)].draw(self.__win)

    def move(self, dir):
        """Perform a move in the puzzle and update the display accordingly."""
        self.__totalScore += self.__problem.move(dir)
        self.update()
        if self.__problem.isSolved():
            print("Congratulations! Your total cost was: " + str(self.__totalScore))
            print("Click the main window to exit.")
            self.__win.exitOnClick()

    def clickMove(self):
        """Allows the user to click to decide which tile to move."""
        pos = self.__win.getMouse()
        row = pos[1]//self.__tileHeight
        col = pos[0]//self.__tileWidth
        blankPos = self.__problem.getPos()
        dir = (row-blankPos[0], col-blankPos[1])

        if dir in self.__problem.legalMoves():
            self.move(dir)
        else:
            print("Illegal move! Please select a position adjacent to the blank tile.")


def main():
    """Automatically solve randomly generated sliding puzzles."""
    parser = argparse.ArgumentParser(description='Solve sliding puzzles automatically or by hand.')
    parser.add_argument('-f', '--file', type=str, help='display the puzzle using the image in FILE (must be a GIF). Has no effect if TRIALS > 1')
    parser.add_argument('-p', '--playable', action='store_true', default=False, help='make the puzzle human-playable using the mouse (requires an image file)')
    parser.add_argument('-r', '--rows', type=int, default=3, help='the puzzle will have ROWS rows (default 3)')
    parser.add_argument('-c', '--columns', type=int, default=3, help='the puzzle will have COLUMNS columns (default 3)')
    parser.add_argument('-d', '--depth', default=4, type=int, help='the solution depth -- the scrambled puzzle will take DEPTH steps to solve (default 4)')
    parser.add_argument('-t', '--trials', type=int, default=1, help='independently generate TRIALS puzzles to solve and report average results (default 1). Has no effect with -p')

    args = parser.parse_args()

    if args.playable:
        if args.file == None:
            raise FileNotFoundError("No image file specified. Use -f FILE to specify a filename.")
        p = SlidingPuzzle(args.rows, args.columns, args.depth)
        print(p, end="")
        initState = p.getState()
        display = SlidingPuzzleDisplay(p, args.file)
        print("Click to move tiles.")
        while(not p.isSolved()):
            display.clickMove()
    else:
        if args.trials > 1:
            random.seed(0)
        p = SlidingPuzzle(args.rows, args.columns, 0)
        startStates = p.getScrambledStates(args.depth, args.trials)

        heuristics = [NullHeuristic(p), NumMisplacedHeuristic(p), ManhattanHeuristic(p), GaschnigsHeuristic(p), ComboHeuristic(p)]
        avgTimes = [0]*len(heuristics)
        avgExpanded = [0]*len(heuristics)
        for t in range(args.trials):
            initState = startStates[t]
            p.setState(initState)
            if args.trials > 1:
                print("Trial " + str(t+1))
            print(p, end="")

            if args.file != None and args.trials == 1:
                display = SlidingPuzzleDisplay(p, args.file)

            times = []
            expanded = []
            for h in range(len(heuristics)):
                p.setState(initState)
                startT = time.time()
                path,cost,numExpanded = search.aStarSearch(p, heuristics[h])
                endT = time.time()
                avgTimes[h] += endT-startT
                avgExpanded[h] += numExpanded
                times.append("{0:.5f}".format(endT-startT))
                expanded.append(str(numExpanded))
            print("Heuristic:\tNull\t\t# Misplaced\tManhattan\tGaschnig's\tCombo")
            print("Time Taken:\t"+"\t\t".join(times))
            print("Nodes Expanded:\t" + "\t\t".join(expanded))
            if path == [] and not p.isSolved():
                print("No solution found!")
                quit()
            else:     
                actionSeq = ""
                actions = {(0, 1):"E", (0, -1):"W", (1, 0):"S", (-1, 0):"N"}
                for a in path:
                    actionSeq += actions[a]+" "       
                print("Action sequence: " + actionSeq)
                if args.file == None or args.trials != 1:
                    print("Total cost: " + str(cost))
                else:
                    p.setState(initState)
                    for m in path:
                        display.move(m)
                        time.sleep(0.2)
            print("-----------------------------")

        if args.trials > 1:
            avgTimes = ["{0:.5f}".format(avgTimes[i]/args.trials) for i in range(len(avgTimes))]
            avgExpanded = [str(avgExpanded[i]/args.trials) for i in range(len(avgExpanded))]
            print("Heuristic:\t\tNull\t\t# Misplaced\tManhattan\tGaschnig's\tCombo")
            print("Avg. Time Taken:\t"+"\t\t".join(avgTimes))
            print("Avg. Nodes Expanded:\t" + "\t\t".join(avgExpanded))
                                                
if __name__ == "__main__":
    main()
