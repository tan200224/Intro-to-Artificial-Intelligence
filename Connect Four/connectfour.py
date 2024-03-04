import random
import argparse
import time
import importlib
import signal
import os
import sys
#cImage = None #placeholder for cImage module

import util.cImage
global cImage
cImage = util.cImage

try:
    signal.SIGALRM
except Exception as ex:
    print("ERROR: " + str(ex))
    print("WARNING: Timeouts will not be enforced.")
    
import heuristic_minimax
from util.timeout import *

class ConnectFour:
    '''Represents the game Connect Four.'''
    
    def __init__(self):
        '''Initializes the game with an empty board.'''      
        self.__board = [["."]*7 for i in range(6)]
        self.__turn = 1
        self.__heights = [0]*7
        
    def getState(self):
        '''Returns the state of the game (as a string).'''
        rows = [" ".join(self.__board[i])+"\n" for i in range(len(self.__board)-1, -1, -1)]
        return "".join(rows)

    def setState(self, state):
        '''Takes a state (as returned by getState) and sets the state of the game.'''
        rows = state.split("\n")[:-1]
        newBoard = [rows[i].split() for i in range(len(rows)-1, -1, -1)]
        if len(newBoard) != 6:
            raise ValueError("Board is wrong size: " + str(len(newBoard)) + " rows, but expected 6")
        numX = 0
        numO = 0
        newHeights = [0]*7
        for i in range(6):
            if len(newBoard[i]) != 7:
                raise ValueError("Board is wrong size: " + str(len(newBoard[i])) + " columns in row " + str(i) + ", but expected 7")
            for j in range(7):
                if newBoard[i][j] == "X":
                    numX += 1
                    if newHeights[j] != i:
                        raise ValueError("Invalid board configuration: column " + str(j) + " has a missing piece.")
                    else:
                        newHeights[j] += 1                        
                elif newBoard[i][j] == "O":
                    numO += 1
                    if newHeights[j] != i:
                        raise ValueError("Invalid board configuration: column " + str(j) + " has a missing piece.")
                    else:
                        newHeights[j] += 1                        
                elif newBoard[i][j] != ".":
                    raise ValueError("Unrecognized board symbol: " + newBoard[i][j] + " (must be ., X, or O)")

        if numX == numO:            
            self.__turn = 1
        elif numX == numO + 1:
            self.__turn = -1
        else:
            raise ValueError("Invalid board configuration. Number of Xs: " + str(numX) + ". Number of Os: " + str(numO))

        self.__numTurns = numX + numO
        self.__board = newBoard
        self.__heights = newHeights
        if self.isTerminal():
            self.__turn = 2

    def getSuccessors(self, state):
        '''Takes a state and returns the possible successors as 4-tuples:
        (next state, action to get there, whose turn in the next state, final score).
        For the last two items, see getTurn() and finalScore().'''
        currentState = self.getState()
        succ = []
        self.setState(state)
        for a in self.legalMoves():
            self.move(a)
            succ.append((self.getState(), a, self.getTurn(), self.finalScore()))
            self.setState(state)
        self.setState(currentState)
        return succ

    def legalMoves(self):
        '''Returns the set of legal moves in the current state (a move is a column index).'''
        if self.__turn == 2:
            return []
        else:
            return [c for c in range(len(self.__heights)) if self.__heights[c] < len(self.__board)]
    
    def move(self, action):
        '''Takes an action (a column index) and, if it is valid, changes the state accordingly.'''
        if action not in range(len(self.__heights)):
            raise ValueError("Unrecognized action: " + str(action))
        if self.__heights[action] == len(self.__board):
            raise ValueError("Illegal move: column " + str(action) + " is full.")
        if self.__turn == 2:
            raise ValueError("Illegal move: game is terminated.")
        elif self.__turn == 1:
            self.__board[self.__heights[action]][action] = "X"
            self.__turn = -1
        elif self.__turn == -1:
            self.__board[self.__heights[action]][action] = "O"
            self.__turn = 1
        self.__heights[action] += 1

        if self.isTerminal():
            self.__turn = 2

    def __isFourInARow(self, positions):
        '''A private helper function that takes a sequence of positions and determines if any player has four pieces in a row within that sequence.'''
        last = "."
        numInARow = 0
        for p in positions:
            r = p[0]
            c = p[1]
            symb = self.__board[r][c]
            if symb != ".":
                if last == self.__board[r][c]:
                    numInARow += 1
                    if numInARow == 4:
                        if last == "X":
                            return 1
                        else:
                            return -1
                else:
                    numInARow = 1
                    last = self.__board[r][c]
            else:
                numInARow = 0
                last = "."
        return None
                        
    def finalScore(self):
        '''If the game is not over, returns None. If it is over, returns -1 if min won,
        +1 if max won, or 0 if it is a draw.'''
        #Check columns        
        for c in range(len(self.__heights)):
            positions = [(r, c) for r in range(self.__heights[c])]
            winner = self.__isFourInARow(positions)
            if winner != None:
                return winner
            
        #Check rows
        for r in range(len(self.__board)):
            positions = [(r, c) for c in range(len(self.__heights))]
            winner = self.__isFourInARow(positions)
            if winner != None:
                return winner

        #Check diagonals
        for i in range(3, len(self.__heights)-1):
            positions = [(i-j, j) for j in range(i+1)]
            winner = self.__isFourInARow(positions)
            if winner != None:
                return winner

            positions = [(len(self.__board)-1-i+j, len(self.__heights)-1-j) for j in range(i+1)]
            winner = self.__isFourInARow(positions)
            if winner != None:
                return winner
        
        #Check anti-diagonals
        for i in range(3, len(self.__heights)-1):
            positions = [(i-j, len(self.__heights)-1-j) for j in range(i+1)]
            winner = self.__isFourInARow(positions)
            if winner != None:
                return winner

            positions = [(len(self.__board)-1-i+j, j) for j in range(i+1)]
            winner = self.__isFourInARow(positions)
            if winner != None:
                return winner

        if self.__heights == [len(self.__board)]*len(self.__heights):
            return 0
        else:
            return None

    def isTerminal(self):
        '''Returns true if the game is over and false otherwise.'''
        return self.finalScore() != None

    def getTile(self, row, column):
        '''Returns the contents of the board at the given position ("X" for max, "O" for min, and "." for empty). NOTE: row 0 is the BOTTOM of the board.'''
        return self.__board[row][column]

    def getTurn(self):
        '''Determines whose turn it is. Returns 1 for max, -1 for min, or 2 if the state is terminal.'''
        return self.__turn

    def getHeights(self):
        '''Returns a list containing the height of the stack in each column.'''
        return self.__heights[:]

    def __str__(self):
        '''Returns a string representing the board (same as getState()).'''
        return self.getState()
    
class ConnectFourDisplay:
    '''Displays a Connect Four game.'''
    def __init__(self, problem):
        '''Takes a ConnectFour and initializes the display.'''
        self.__problem = problem
        
        self.__numCols = 7
        self.__numRows = 6

        self.__heights = self.__problem.getHeights().copy()
        
        self.__images = []
        for r in range(self.__numRows):
            self.__images.append([])
            for c in range(self.__numCols):
                self.__images[r].append([])
                self.__images[r][c].append(cImage.FileImage("images/c4blank.gif"))
                self.__images[r][c].append(cImage.FileImage("images/c4max.gif"))
                self.__images[r][c].append(cImage.FileImage("images/c4min.gif"))
                for i in range(3):
                    img = self.__images[r][c][i]
                    img.setPosition(c*img.getWidth(), r*img.getHeight())

        self.__tileWidth = self.__images[0][0][0].getWidth()
        self.__tileHeight = self.__images[0][0][0].getHeight()
        self.__win = cImage.ImageWin("Connect Four!", self.__numCols*self.__tileWidth, self.__numRows*self.__tileHeight)
        self.update(init=True)

    def update(self, init=False):
        '''Updates the game display based on the game's current state.'''
        if init:
            newHeights = [self.__numRows]*self.__numCols
        else:
            newHeights = self.__problem.getHeights()
            
        for c in range(self.__numCols):
            print(self.__heights[c], newHeights[c])
            for r in range(self.__heights[c], newHeights[c]):
                t = self.__problem.getTile(r, c)
                drawRow = self.__numRows - 1 - r
                if t == ".":
                    self.__images[drawRow][c][0].draw(self.__win)
                elif t == "X":
                    self.__images[drawRow][c][1].draw(self.__win)
                else: #"O"
                    self.__images[drawRow][c][2].draw(self.__win)
            if not init:
                self.__heights[c] = newHeights[c]
                
    def getMove(self):
        '''Allows the user to click to decide which column to move in.'''
        pos = self.__win.getMouse()
        col = pos[0]//self.__tileWidth
        while col not in self.__problem.legalMoves():
            print("Illegal move! Please click on a column with an empty space.")
            pos = self.__win.getMouse()
            col = pos[0]//self.__tileWidth
        return col

    def exitonclick(self):
        self.__win.exitonclick()

class DefaultMoveOrder:
    def __init__(self, problem):
        self.__problem = problem

    def getSuccessors(self, state):
        return self.__problem.getSuccessors(state)

def playConnectFour(problem, initState, players, playerPrograms, numTrials, swaps, tournament, display, nodisplay, testDefault):
    wins = [0, 0, 0]
    times = [0, 0]
    turns = [0, 0]
    nodes = [0, 0]
    defaultNodes = [0, 0]
    defaultOrder = DefaultMoveOrder(problem)
    for i in range(swaps):
        for t in range(numTrials):
            problem.setState(initState)
            while not problem.isTerminal():
                turn = problem.getTurn()
                playerIdx = (1 - turn)//2
                playerIdx = (playerIdx + i)%2
                if players[playerIdx] == "random":
                    move = random.choice(problem.legalMoves())
                elif players[playerIdx] == "human":
                    move = display.getMove()
                else: #minimax
                    startT = time.time()
                    try:
                        with timeout(2):
                            if tournament:
                                move = playerPrograms[playerIdx].getMove()
                                numNodes = 0
                            else:
                                move, numNodes = heuristic_minimax.getMove(problem.getState(), problem.getTurn(), 4, playerPrograms[playerIdx][0], playerPrograms[playerIdx][1])
                                nodes[playerIdx] += numNodes
                                    
                            endT = time.time()
                            times[playerIdx] += endT - startT
                            turns[playerIdx] += 1

                        if not tournament and testDefault[playerIdx]:
                            moveD, numNodesD = heuristic_minimax.getMove(problem.getState(), problem.getTurn(), 4, playerPrograms[playerIdx][0], defaultOrder)
                            defaultNodes[playerIdx] += numNodesD

                    except TimeoutError:
                        print(players[playerIdx] + " timed out after 2 seconds. Choosing random action.")
                        move = random.choice(problem.legalMoves())

                problem.move(move)                
                if swaps == 1 and not nodisplay:
                    print("About to display")                    
                    display.update()
                    print("Finished displaying")

            if problem.finalScore() == 0:
                whoWon = "Draw"
                wins[2] += 1
            elif problem.finalScore() < 0:
                whoWon = players[(1+i)%2] + " wins!"
                wins[(1+i)%2] += 1
            elif problem.finalScore() > 0:
                whoWon = players[(0+i)%2] + " wins!"
                wins[(0+i)%2] += 1

            if swaps == 2:
                whoWon = players[(0+i)%2] + " vs. " + players[(1+i)%2] + " game " + str(t+1) + ": " + whoWon
            print(whoWon)
    return wins, times, turns, nodes, defaultNodes
    
def main():
    parser = argparse.ArgumentParser(description='Play Connect 4 with computer or human players.')
    parser.add_argument('-p1', '--player1', type=str, default='random', help='the name of a Python file containing a Connect4Agent, or "random" or "human" (default: random)')
    parser.add_argument('-p2', '--player2', type=str, default='random', help='the name of a Python file containing a Connect4Agent, or "random" or "human" (default: random)')
    parser.add_argument('-t', '--trials', type=int, help='plays TRIALS games, then swaps the players and plays TRIALS more games (has no effect if either player is human; with this option the game will not be displayed)')
    parser.add_argument('-nd', '--nodisplay', action='store_true', default=False, help='do not display the game (has no effect if a player is human or if -t is used)')
    parser.add_argument('-d1', '--default1', action='store_true', default=False, help='measures nodes expanded by Player 1 with the default move order during the game (has no effect with -r)')
    parser.add_argument('-d2', '--default2', action='store_true', default=False, help='measures nodes expanded by Player 2 with the default move order during the game (has no effect with -r)')
    parser.add_argument('-r', '--tournament', action='store_true', default=False, help='turns on tournament mode (loads tournament agents from the given files)')
    
    args = parser.parse_args()

    problem = ConnectFour()   
    initState = problem.getState()

    players = [args.player1, args.player2]

    if args.trials != None:
        swaps = 2
        numTrials = args.trials
    else:
        swaps = 1
        numTrials = 1

    displayError = False
    if not args.nodisplay:
        try:
            global cImage
            import util.cImage
            cImage = util.cImage
        except Exception as ex:
            displayError = True
            print("ERROR: " + str(ex))
            print("WARNING: Unable to initialize the GUI. Display will be disabled.")

    if args.player1 == "human" or args.player2 == "human":
        if(displayError):
            print("ERROR: The GUI is disabled so human play is not supported. Sorry!")
            exit(1)
        swaps = 1
        numTrials = 1
        args.nodisplay = False
        print("Please click on a column with an empty space.")       

    if displayError:
        args.nodisplay = True
        
    if swaps == 1 and not args.nodisplay:
        display = ConnectFourDisplay(problem)
    else:
        display = None

    if swaps == 2:
        random.seed(42)
        
    playerPrograms = [None, None]
    for i in range(2):
        if players[i] != "random" and players[i] != "human":
            mod = importlib.import_module(".".join(players[i].split("/")[-1].split(".")[:-1]))
            with timeout(2):
                if args.tournament:
                    playerPrograms[i] = mod.C4TournamentAgent(problem)
                else:
                    leafEval = mod.C4HeuristicEval(problem)
                    order = mod.C4OrderHeuristic(problem)
                    playerPrograms[i] = (leafEval, order)
              
    defaultOrder = [args.default1, args.default2]
    wins, times, turns, nodes, defaultNodes = playConnectFour(problem, initState, players, playerPrograms, numTrials, swaps, args.tournament, display, args.nodisplay, defaultOrder)
            
    if swaps == 2:
        print("Stats:")
        print(players[0] + " wins: " + str(wins[0]))
        print(players[1] + " wins: " + str(wins[1]))
        print("Draws: " + str(wins[2]))
        
    for i in range(2):
        if turns[i] > 0:
            print(players[i] + ":\n  " + str(times[i]/turns[i]) + " seconds per step, on average")
            if not args.tournament:
                if defaultOrder[i]:
                    print("  " + str(defaultNodes[i]/turns[i]) + " nodes expanded per step, on average, using the default move order")
                print("  " + str(nodes[i]/turns[i]) + " nodes expanded per step, on average, using the order heuristic")

    if swaps == 1 and not args.nodisplay:
        print("Click on the window to exit")
        display.exitonclick()
            
if __name__ == "__main__":
    main()
