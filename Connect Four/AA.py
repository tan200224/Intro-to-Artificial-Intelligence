class C4HeuristicEval:
    def __init__(self, problem):
        self.__problem = problem
        self.rows = 6
        self.cols = 7
        ###If you want to do any pre-processing, do it here
        ###(note: time limit for the constructors is 2 seconds!)

    def horizontal(self, board, turn, player):
        count = 0
        possibleHorWinIndex = []
        # The win closer to the bottom is better
        dic = {self.rows-1:0.004, self.rows-2:0.003, self.rows-3:0.002, self.rows-4:0.001, self.rows-5:0.0005, self.rows-6:0.0004}

        if turn == -1:
            possibleWin = [["O", "O", "O", "."],
                           [".", "O", "O", "O"],
                           ["O", ".", "O", "O"],
                           ["O", "O", ".", "O"]]
        elif turn == 1:
            possibleWin = [["X", "X", "X", "."],
                           [".", "X", "X", "X"],
                           ["X", ".", "X", "X"],
                           ["X", "X", ".", "X"]]
        else:
            return 0, 0


        for row in range(self.rows):
            for col in range(5):
                if board[row][col:col+4] in possibleWin:
                    possibleHorWinIndex.append([row, col])

                    if self.checkisOdd(board, turn, player) == True:
                        if row % 2 == 1:
                            #print("odd player on odd row", row, board[row][col:col+4].index(".")+col)
                            count += 1 + dic[row] * 1.25
                        else:
                            count += 1 + dic[row]
                            #print("odd player on even row", row,board[row][col:col+4].index(".")+col)


                    elif self.checkisOdd(board, turn, player) == False:
                        if row % 2 == 0:
                            #print("even player on even row", row,board[row][col:col+4].index(".")+col)
                            count += 1 + dic[row] * 1.25
                        else:
                            #print("even player on odd row", row,board[row][col:col+4].index(".")+col)

                            count += 1 + dic[row]


        return possibleHorWinIndex, count

    def vertical(self, board, turn):
        count = 0

        if turn == -1:
            possibleWin = [".", "O", "O", "O"]
        elif turn == 1:
            possibleWin = [".", "X", "X", "X"]
        else:
            return 0

        tmp = []
        for col in range(self.cols):
            tmp.append([board[row][col] for row in range(self.rows)])
        for row in range(len(tmp)):
            for col in range(4):
                if tmp[row][col:col+4] in possibleWin:
                    count += 1

        return count

    def positiveD(self, board, turn, player):
        count = 0
        dic = {self.rows - 1: 0.004, self.rows - 2: 0.003, self.rows - 3: 0.002, self.rows - 4: 0.001, self.rows - 5: 0.0005, self.rows - 6: 0.0004, 6:0}

        if turn == -1:
            possibleWin = [["O", "O", "O", "."],
                           [".", "O", "O", "O"],
                           ["O", ".", "O", "O"],
                           ["O", "O", ".", "O"]]
        elif turn == 1:
            possibleWin = [["X", "X", "X", "."],
                           [".", "X", "X", "X"],
                           ["X", ".", "X", "X"],
                           ["X", "X", ".", "X"]]
        else:
            return 0


        diagonals = []
        positionD = []
        for i in range(3, len(self.__problem.getHeights())-1):

            positions = [(i-j, j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])
            positionD.append([[pos[0],pos[1]] for pos in positions])


        for i in range(3, len(self.__problem.getHeights()) - 1):
            positions = [(len(board)-1-i+j, len(self.__problem.getHeights())-1-j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])
            positionD.append([[pos[0],pos[1]] for pos in positions])


        for row in range(len(diagonals)):
            for col in range(len(diagonals[row])):
                if col+4 <= len(diagonals[row]) and (diagonals[row][col:col+4] in possibleWin):
                    if self.checkisOdd(board, turn, player) == True:
                        if (positionD[row][diagonals[row][col:col+4].index(".")+col][0]) % 2 == 1:
                            count += 1 + dic[row] * 1.25
                            #print("ood player on odd row", positionD[row][diagonals[row][col:col+4].index(".")+col])
                        else:
                            count += 1 + dic[row]
                            #print("odd player on even row", positionD[row][diagonals[row][col:col + 4].index(".") + col])
                    elif self.checkisOdd(board, turn, player) == False:
                        if (positionD[row][diagonals[row][col:col+4].index(".")+col][0]) % 2 == 0:
                            count += 1 + dic[row] * 1.25
                            #print("even player on even row", positionD[row][diagonals[row][col:col + 4].index(".") + col])
                        else:
                            count += 1 + dic[row]
                            #print("even player on odd row", positionD[row][diagonals[row][col:col + 4].index(".") + col])
                    break

        return count

    def negativeD(self, board, turn, player):
        count = 0
        dic = {self.rows-1:0.004, self.rows-2:0.003, self.rows-3:0.002, self.rows-4:0.001, self.rows-5:0.0005, self.rows-6:0.0004}

        if turn == -1:
            possibleWin = [["O", "O", "O", "."],
                           [".", "O", "O", "O"],
                           ["O", ".", "O", "O"],
                           ["O", "O", ".", "O"]]
        elif turn == 1:
            possibleWin = [["X", "X", "X", "."],
                           [".", "X", "X", "X"],
                           ["X", ".", "X", "X"],
                           ["X", "X", ".", "X"]]
        else:
            return 0

        # Getting the diagonal indexes
        positionD = []
        diagonals = []
        for i in range(3, len(self.__problem.getHeights())-1):
            positions = [(i-j, len(self.__problem.getHeights())-1-j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])
            positionD.append([[pos[0],pos[1]] for pos in positions])


        for i in range(3, len(self.__problem.getHeights()) - 1):
            positions = [(len(board)-1-i+j, j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])
            positionD.append([[pos[0],pos[1]] for pos in positions])

        # Check if there is diagonal wins
        for row in range(len(diagonals)):
            for col in range(len(diagonals[row])):
                if col+4 <= len(diagonals[row]) and (diagonals[row][col:col+4] in possibleWin):
                    if self.checkisOdd(board, turn, player) == True:
                        if (positionD[row][diagonals[row][col:col+4].index(".")+col][0]) % 2 == 1:
                            count += 1 + dic[row] * 1.25
                            #print("ood player on odd row", positionD[row][diagonals[row][col:col + 4].index(".") + col])
                        else:
                            count += 1 + dic[row]
                            #print("ood player on even row", positionD[row][diagonals[row][col:col + 4].index(".") + col])



                    elif self.checkisOdd(board, turn, player) == False:
                        if (positionD[row][diagonals[row][col:col+4].index(".")+col][0]) % 2 == 0:
                            count += 1 + dic[row] * 1.25
                            #print("even player on even row", positionD[row][diagonals[row][col:col + 4].index(".") + col])
                        else:
                            count += 1 + dic[row]
                            #print("even player on odd row", positionD[row][diagonals[row][col:col + 4].index(".") + col])
                    break
        return count

    def checkEarlyEdges(self, board, turn):

        eval = 0

        if turn == -1:
            player="O"
            counterplayer="X"
        elif turn == 1:
            player="X"
            counterplayer="O"
        else:
            return 0
        # Check if it is still a early game
        count = 0
        isEarly = False
        for row in range(self.rows):
            for col in range(self.cols):
                if board[row][col] == player or board[row][col] == counterplayer:
                    count += 1
        if count <= 6:
            isEarly = True

        if isEarly:
            for row in range(self.rows):
                if board[row][0] == player:
                    eval += 0.5 * (-1*turn)

            for row in range(self.rows):
                if board[row][self.cols-1] == player:
                    eval += 0.5 * (-1*turn)

        return eval

    def checkCenter(self, board, turn):
        eval = 0

        if turn == -1:
            player="O"
            counterplayer="X"
        elif turn == 1:
            player="X"
            counterplayer="O"
        else:
            return 0


        for row in range(self.rows-2):
            if board[row][3] == player:
                eval += 0.05*turn



        if board[3][3] == player:
            eval += 0.05*turn
        if board[2][3] == player:
            eval += 0.025*turn

        return eval

    def checkisOdd(self, board, turn, player):

        # Prioritize even or odd row
        maxcount = 0
        mincount = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if board[row][col] == "O":
                    mincount += 1
                elif board[row][col] == "X":
                    maxcount += 1
        #print(maxcount, mincount)

        # If the min and max have the same count, the current player is odd
        if maxcount == mincount:
            if turn == player:
                return True
            else:
                return False
        # If the min and max is not the same count, the current player is even
        elif mincount < maxcount:
            if turn == player:
                return False
            else:
                return True
        elif maxcount < mincount:
            if turn == player:
                return False
            else:
                return True

    def checkTrap(self, board, turn):

        eval = 0
        if turn == -1:
            possibleWin = [".", ".", "O", "O", ".", "."]
        elif turn == 1:
            possibleWin = [".", ".", "X", "X", ".", "."]
        else: return 0

        for row in range(self.rows):
            for col in range(2):
                if board[row][col:col+6] == possibleWin:
                    eval += 0.3 * turn
        return eval

    def eval(self, state):
        '''Gives a heuristic evaluation of the given state.'''
        curState = self.__problem.getState()
        self.__problem.setState(state)

        #####YOUR CODE BEGINS HERE#####
        # You should take a look at connectfour.py to see what methods self.__problem has, but here are some that will probably be helpful:
        # get/setState()
        # getTurn() -- returns a number indicating whose turn it is in the current state: -1 for min, 1 for max, 2 if the state is terminal
        # getSuccessors(state) -- returns the successors of the given state as 4-tuples: (next state, action to get there, whose turn it is in that state, the final score)
        # getTile(row, col) -- returns the contents of the given position on the board ("X" for max, "O" for min, "." for empty)
        # getHeights() -- returns a list of the heights of the stacks in the 7 columns

        eval = 0
        board = []
        turn = self.__problem.getTurn()

        #print(state)
        #print(turn)

        # Convert state into a board (list)
        for row in range(self.rows):
            tmp = []
            for col in range(self.cols):
                tmp.append(self.__problem.getTile(row, col))
            board.insert(0, tmp)


        # Check how both side are playing on the center
        eval += self.checkCenter(board, turn)
        # Check if player are placing their move on the edge when it is still a early game
        eval += self.checkEarlyEdges(board, turn)

        # Check if there are trap in the board
        eval += self.checkTrap(board, turn)

        # Check which side have more possible wins
        possibleWin = 0
        possibleLost = 0

        playerHorWinIndex, playerNumHorWins = self.horizontal(board, turn, turn)
        counterplayerHorWinIndex, counterPlayerNumHorWins = self.horizontal(board, -1*turn, turn)

        possibleWin += playerNumHorWins + self.negativeD(board, turn, turn) + self.positiveD(board, turn, turn)
        possibleLost += counterPlayerNumHorWins + self.negativeD(board, -1*turn, turn) + self.positiveD(board, -1*turn, turn)

        possibleWin += self.vertical(board, turn)
        possibleLost += self.vertical(board, -1*turn)

        if possibleWin > possibleLost:
            eval += 0.7*turn
        elif possibleWin < possibleLost:
            eval += -(0.7*turn)
        else:
            eval += 0


        # Make sure eval is still in the boundary
        if eval > 1:
            eval = 1
        elif eval < -1:
            eval = -1

        ######YOUR CODE ENDS HERE######

        self.__problem.setState(curState)
        return eval


class C4OrderHeuristic:
    def __init__(self, problem):
        self.__problem = problem
        ###If you want to do any pre-processing, do it here
        ###(note: time limit for the constructors is 2 seconds!)

    def vertical(self, board, turn):
        count = 0

        if turn == -1:
            possibleWin = [".", "O", "O", "O"]
        elif turn == 1:
            possibleWin = [".", "X", "X", "X"]
        else:
            return 0

        tmp = []
        colNum = None
        for col in range(self.cols):
            tmp.append([board[row][col] for row in range(self.rows)])
        for row in range(len(tmp)):
            for col in range(4):
                if tmp[row][col:col+4] == possibleWin:
                    colNum = row

        return colNum
    def checkVeticalLost(self, turn, successors):

        # The player don't have any vertical 3, and the counter play has
            for successor in successors:
                if self.vertical(self.toBoard(successor[0]), -turn) != None:
                    if successor[1] == self.vertical(self.toBoard(successor[0]), -turn):
                        tmp = successor
                        successors.remove(successor)
                        successors.insert(0, tmp)
    def horizontal(self, board, turn):
        # The win closer to the bottom is better

        if turn == -1:
            possibleWin = [["O", "O", "O", "."],
                           [".", "O", "O", "O"],
                           ["O", ".", "O", "O"],
                           ["O", "O", ".", "O"]]
        elif turn == 1:
            possibleWin = [["X", "X", "X", "."],
                           [".", "X", "X", "X"],
                           ["X", ".", "X", "X"],
                           ["X", "X", ".", "X"]]
        else:
            return 0, 0

        position = []
        for row in range(self.rows):
            for col in range(5):
                if board[row][col:col+4] in possibleWin:
                    position.append([row, board[row][col:col+4].index(".")+col])

        return position
    def checkHorLost(self, turn, successors):

        for successor in successors:

            # Check if the other player have a possible win
            if len(self.horizontal(self.toBoard(successor[0]), -turn)) > 0:

                # Check the distance from horizontal win
                for pos in self.horizontal(self.toBoard(successor[0]), -turn):
                    if (pos[0] + 1) < self.rows-1 and self.toBoard(successor[0])[pos[0]+1][pos[1]] != ".":
                        for successor in successors:
                            if successor[1] == pos[1]:
                                tmp = successor
                                successors.remove(successor)
                                successors.insert(0, tmp)
                    elif pos[0] == self.rows-1:
                        for successor in successors:
                            if successor[1] == pos[1]:
                                tmp = successor
                                successors.remove(successor)
                                successors.insert(0, tmp)
    def checkEval(self, turn, successors, score):

        if turn == -1:
            for i in range(len(score)):
                for j in range(i, len(score)):
                    if score[j] < score[i]:
                        tmp = score[i]
                        score[i] = score[j]
                        score[j] = tmp

                        tmp = successors[i]
                        successors[i] = successors[j]
                        successors[j] = tmp

        elif turn == 1:
            for i in range(len(score)):
                for j in range(i, len(score)):
                    if score[j] > score[i]:
                        tmp = score[i]
                        score[i] = score[j]
                        score[j] = tmp

                        tmp = successors[i]
                        successors[i] = successors[j]
                        successors[j] = tmp

        else: score = 0
    def Center(self, successors):

        for successor in successors:
            count = 0
            for row in range(self.rows-2):
                if self.toBoard(successor[0])[row][3] == "O" or self.toBoard(successor[0])[row][3] == "X":
                    count += 1

            if count <= 3:
                for successor in successors:
                    if successor[1] == 3:
                        tmp = successor
                        successors.remove(successor)
                        successors.insert(0, tmp)
                        break

    def checkCenter(self, successors, score, board):

        # Assuming the successors is sorted based on eval
        for i in range(len(score)):
            for j in range(i, len(score)):
                if score[i] == score[j]:

                    # Check which succcessor play on the center, but keep it as low as possible
                    if successors[j][1] == 3 and board[2][4] == ".":
                        tmp = score[i]
                        score[i] = score[j]
                        score[j] = tmp

                        tmp = successors[i]
                        successors[i] = successors[j]
                        successors[j] = tmp
    def Trap(self, turn, successors):
        position = []

        if turn == -1:
            possibleWin = [".", "O", "O", "O", "."]
        elif turn == 1:
            possibleWin = [".", "X", "X", "X", "."]
        else: return 0

        for successor in successors:
            board = self.toBoard(successor[0])

            for row in range(self.rows):
                for col in range(3):
                    # print(board[row][col:col+5])
                    if board[row][col:col+5] == possibleWin:
                        tmp = successor
                        successors.remove(successor)
                        successors.insert(0, tmp)
                        break
    def toBoard(self, input_string):
        rows = input_string.strip().split("\n")
        board = []
        for row in rows:
            tmp = []
            for col in row:
                if col != " ":
                    tmp.append(col)
            board.append(tmp)
        return board
    def positiveDWins(self, turn, successors):

        if turn == -1:
            possibleWin = ["O", "O", "O", "O"]
        elif turn == 1:
            possibleWin = ["X", "X", "X", "X"]
        else:
            return 0

        for successor in successors:
            diagonals = []
            board = self.toBoard(successor[0])

            for i in range(3, len(self.__problem.getHeights()) - 1):
                positions = [(i - j, j) for j in range(i + 1)]
                diagonals.append([board[pos[0]][pos[1]] for pos in positions])

            for i in range(3, len(self.__problem.getHeights()) - 1):
                positions = [(len(board) - 1 - i + j, len(self.__problem.getHeights()) - 1 - j) for j in range(i + 1)]
                diagonals.append([board[pos[0]][pos[1]] for pos in positions])

            for row in range(len(diagonals)):
                for col in range(len(diagonals[row])):
                    if col + 4 <= len(diagonals[row]) and (possibleWin == diagonals[row][col:col + 4]):
                        tmp = successor
                        successors.remove(successor)
                        successors.insert(0, tmp)
                        break
    def negativeDWins(self, turn, successors):

        if turn == -1:
            possibleWin = ["O", "O", "O", "O"]
        elif turn == 1:
            possibleWin = ["X", "X", "X", "X"]
        else:
            return 0

        for successor in successors:
            diagonals = []
            board = self.toBoard(successor[0])

            # Getting the diagonal indexes
            for i in range(3, len(self.__problem.getHeights())-1):
                positions = [(i-j, len(self.__problem.getHeights())-1-j) for j in range(i+1)]
                diagonals.append([board[pos[0]][pos[1]] for pos in positions])


            for i in range(3, len(self.__problem.getHeights()) - 1):
                positions = [(len(board)-1-i+j, j) for j in range(i+1)]
                diagonals.append([board[pos[0]][pos[1]] for pos in positions])

            # Check if there is diagonal wins
            for row in range(len(diagonals)):
                for col in range(len(diagonals[row])):
                    if col+4 <= len(diagonals[row]) and (diagonals[row][col:col+4] == possibleWin):
                        tmp = successor
                        successors.remove(successor)
                        successors.insert(0, tmp)
                        break
    def checkVerHorWins(self, turn, successors):
        if turn == -1:
            possibleWin = "O O O O"
        elif turn == 1:
            possibleWin = "X X X X"


        for successor in successors:
            if  possibleWin in successor[0]:
                tmp = successor
                successors.remove(successor)
                successors.insert(0, tmp)
                break



        if turn == -1:
            possibleWin = "OOOO"
        elif turn == 1:
            possibleWin = "XXXX"

        for successor in successors:

            rows = successor[0].strip().split("\n")
            cols = len(rows[0])

            rotated_string = [' ' * len(rows) for _ in range(cols)]

            for i in range(len(rows)):
                for j in range(cols):
                    rotated_string[j] = rotated_string[j][:i] + rows[i][j] + rotated_string[j][i + 1:]


            tmp = '\n'.join(rotated_string[::-1])

            if possibleWin in tmp:
                tmp = successor
                successors.remove(successor)
                successors.insert(0, tmp)
                break


    def getSuccessors(self, state):

        curState = self.__problem.getState()
        self.__problem.setState(state)
        self.rows = 6
        self.cols = 7

        #####YOUR CODE BEGINS HERE#####
        successors = self.__problem.getSuccessors(state)
        evalHeuristic = C4HeuristicEval(self.__problem)
        turn = self.__problem.getTurn()

    # Create a 2d array for the current state
        board = []
        for row in range(self.rows):
            tmp = []
            for col in range(self.cols):
                tmp.append(self.__problem.getTile(row, col))
            board.insert(0, tmp)

        # Evaluate each successor using eval()
        score = []
        for successor in successors:
            score.append(evalHeuristic.eval(successor[0]))


        # Sort successor based on eval score
        self.checkEval(turn, successors, score)


        # Prioritize center play
        self.Trap(turn, successors)
        self.Center(successors)


        self.checkHorLost(turn, successors)
        self.checkVeticalLost(turn, successors)

        # Evaluate how far away the current state is from wining
        # React and prevent lost from horizon and vertical 4

        self.positiveDWins(turn, successors)
        self.negativeDWins(turn, successors)
        self.checkVerHorWins(turn, successors)


        ######YOUR CODE ENDS HERE######

        self.__problem.setState(curState)
        return successors
