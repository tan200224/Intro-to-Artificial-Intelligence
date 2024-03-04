class C4HeuristicEval:
    def __init__(self, problem):
        self.__problem = problem
        self.rows = 6
        self.cols = 7
        ###If you want to do any pre-processing, do it here
        ###(note: time limit for the constructors is 2 seconds!)

    def horizontal(self, board, turn, odd):
        count = 0
        possibleHorWinIndex = []
        even = 0
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

        if odd == -1:
            even = 1
        elif odd == 1:
            even = -1

        for row in range(self.rows):
            for col in range(5):
                if board[row][col:col+4] in possibleWin:
                    possibleHorWinIndex.append([row, col])

                    if odd == turn:
                        if row % 2 == 1:
                            count += 1 + dic[row]*2
                        else:
                            count += 1 + dic[row]
                    elif even == turn:
                        if row % 2 == 0:
                            count += 1 + dic[row]*2
                        else:
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
                if tmp[row][col:col+4] == possibleWin:
                    count += 1

        return count

    def positiveD(self, board, turn, odd):
        count = 0
        dic = {self.rows - 1: 0.004, self.rows - 2: 0.003, self.rows - 3: 0.002, self.rows - 4: 0.001, self.rows - 5: 0.0005, self.rows - 6: 0.0004, 6:0}
        even = 0

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

        if odd == -1:
            even = 1
        elif odd == 1:
            even = -1

        diagonals = []
        for i in range(3, len(self.__problem.getHeights())-1):

            positions = [(i-j, j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])


            positions = [(len(board)-1-i+j, len(self.__problem.getHeights())-1-j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])

        for row in range(len(diagonals)):
            for col in range(len(diagonals[row])):
                if col + 4 <= len(diagonals[row]) and (diagonals[row][col:col + 4] in possibleWin):
                    count += 1
                    break

        return count

    def negativeD(self, board, turn):
        count = 0

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
        for i in range(3, len(self.__problem.getHeights())-1):
            positions = [(i-j, len(self.__problem.getHeights())-1-j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])


            positions = [(len(board)-1-i+j, j) for j in range(i+1)]
            diagonals.append([board[pos[0]][pos[1]] for pos in positions])

        for row in range(len(diagonals)):
            for col in range(len(diagonals[row])):
                if col+4 <= len(diagonals[row]) and (diagonals[row][col:col+4] in possibleWin):
                    count += 1
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
                    eval += 0.4*-1*turn

            for row in range(self.rows):
                if board[row][self.cols-1] == player:
                    eval += 0.4*-1*turn

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

        win=0
        lost=0
        for row in range(self.rows):
            if board[row][3] == player:
                win+=1
            elif board[row][3] == counterplayer:
                lost+=1

        if win > lost:
            eval += 0.1*turn
        elif win < lost:
            eval += 0.1*-1*turn
        else:
            if board[3][3] == player:
                eval += 0.1*turn
            if board[2][3] == player:
                eval += 0.05*turn

        return eval

    def checkTrap(self, board, turn):

        eval = 0
        if turn == -1:
            possibleWin = [[".", ".", "O", "O", ".", "."]]
        elif turn == 1:
            possibleWin = [[".", ".", "X", "X", ".", "."]]
        else: return 0

        for row in range(self.rows):
            for col in range(2):
                if board[row][col:col+6] in possibleWin:
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

        possibleWin += playerNumHorWins + self.negativeD(board, turn) + self.positiveD(board, turn, turn)
        possibleLost += counterPlayerNumHorWins + self.negativeD(board, -1*turn) + self.positiveD(board, -1*turn, turn)

        possibleWin += self.vertical(board, turn)*2
        possibleLost += self.vertical(board, -1*turn)*2

        if possibleWin > possibleLost:
            eval += 0.5*turn
        elif possibleWin < possibleLost:
            eval += -(0.5*turn)
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

    def checkVeticalWins(self, board, turn, successors):

        # The player dont have any vertical 3, and the counter play has
        if self.vertical(board, turn) == None and self.vertical(board, -turn) != None:
            for successor in successors:
                if successor[1] == self.vertical(board, -turn):
                    tmp = successor
                    successors.remove(successor)
                    successors.insert(0, tmp)

        elif self.vertical(board, turn) != None:
            for successor in successors:
                if successor[1] == self.vertical(board, turn):
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

    def checkHorWins(self, board, turn, successors):

        count = 0
        colNum = None

        # Calculate how far the player from the horizontal win
        if len(self.horizontal(board, turn)) == 0:
            if len(self.horizontal(board, -turn)) > 0:
                # Calculate the distance from wining
                for pos in self.horizontal(board, -turn):
                    for row in range(pos[0]+1, self.rows):
                        if board[row][pos[1]] == ".":
                            count += 1
                    if count == 0:
                        colNum = pos[1]
                        break

                # Prioritize the successors
                if colNum != None:
                    for successor in successors:
                        if successor[1] == colNum:
                            tmp = successor
                            successors.remove(successor)
                            successors.insert(0, tmp)

        elif len(self.horizontal(board, turn)) > 0:
            # Calculate the distance from horizontal win
            for pos in self.horizontal(board, turn):
                for row in range(pos[0] + 1, self.rows):
                    if board[row][pos[1]] == ".":
                        count += 1
                if count == 0:
                    colNum = pos[1]
                    break

                if colNum != None:
                    for successor in successors:
                        if successor[1] == colNum:
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

    def checkCenter(self, successors, score, board):

        # Assuming the successors is sorted based on eval
        for i in range(len(score)):
            for j in range(i, len(score)):
                if score[i] == score[j]:

                    # Check which succcessor play on the center, but keep it as low as possible
                    if successors[j][1] == 3 and board[2][3] == ".":
                        tmp = score[i]
                        score[i] = score[j]
                        score[j] = tmp

                        tmp = successors[i]
                        successors[i] = successors[j]
                        successors[j] = tmp

    def checkOdd(self, successors, turn, score):

        # Meaning Min is the second play
        if turn == -1:
            counts = []
            # Count the number of min in the odd even
            for successor in successors:
                count = 0

                board = []
                tmp = successor[0].split("\n")
                tmp.pop()
                for row in tmp:
                    board.append(list(row.split(" ")))

                for row in range(self.rows):
                    for col in range(self.cols):
                        if row % 2 == 1 and board[row][col] == "O":
                            count += 1
                counts.append(count)

            for i in range(len(score)):
                for j in range(i, len(score)):
                    if score[i] == score[j]:

                        # Check which successor play more on the even row
                        if counts[j] > counts[i]:
                            tmp = counts[i]
                            counts[i] = counts[j]
                            counts[j] = tmp

                            tmp = score[i]
                            score[i] = score[j]
                            score[j] = tmp

                            tmp = successors[i]
                            successors[i] = successors[j]
                            successors[j] = tmp


        # Meaning Max is the second play
        elif turn == 1:
            counts = []
            # Count the number of min in the even row
            for successor in successors:
                count = 0

                board = []
                tmp = successor[0].split("\n")
                tmp.pop()
                for row in tmp:
                    board.append(list(row.split(" ")))

                for row in range(self.rows):
                    for col in range(self.cols):
                        if row % 2 == 1 and board[row][col] == "X":
                            count += 1
                counts.append(count)

            for i in range(len(score)):
                for j in range(i, len(score)):
                    if score[i] == score[j]:
                        if counts[j] > counts[i]:
                            tmp = counts[i]
                            counts[i] = counts[j]
                            counts[j] = tmp

                            tmp = score[i]
                            score[i] = score[j]
                            score[j] = tmp

                            tmp = successors[i]
                            successors[i] = successors[j]
                            successors[j] = tmp

        else:
            return 0

    def checkEven(self, successors, turn, score):

        # Meaning Min is the second play
        if turn == -1:
            counts = []
            # Count the number of min in the odd even
            for successor in successors:
                count = 0

                board = []
                tmp = successor[0].split("\n")
                tmp.pop()
                for row in tmp:
                    board.append(list(row.split(" ")))

                for row in range(self.rows):
                    for col in range(self.cols):
                        if row % 2 == 0 and board[row][col] == "O":
                            count += 1
                counts.append(count)

            for i in range(len(score)):
                for j in range(i, len(score)):
                    if score[i] == score[j]:

                        # Check which successor play more on the even row
                        if counts[j] > counts[i]:
                            tmp = counts[i]
                            counts[i] = counts[j]
                            counts[j] = tmp

                            tmp = score[i]
                            score[i] = score[j]
                            score[j] = tmp

                            tmp = successors[i]
                            successors[i] = successors[j]
                            successors[j] = tmp


        # Meaning Max is the second play
        elif turn == 1:
            counts = []
            # Count the number of min in the even row
            for successor in successors:
                count = 0

                board = []
                tmp = successor[0].split("\n")
                tmp.pop()
                for row in tmp:
                    board.append(list(row.split(" ")))

                for row in range(self.rows):
                    for col in range(self.cols):
                        if row % 2 == 0 and board[row][col] == "X":
                            count += 1
                counts.append(count)

            for i in range(len(score)):
                for j in range(i, len(score)):
                    if score[i] == score[j]:
                        if counts[j] > counts[i]:
                            tmp = counts[i]
                            counts[i] = counts[j]
                            counts[j] = tmp

                            tmp = score[i]
                            score[i] = score[j]
                            score[j] = tmp

                            tmp = successors[i]
                            successors[i] = successors[j]
                            successors[j] = tmp

        else:
            return 0

    def Trap(self, board, turn):
        position = []
        if turn == -1:
            possibleWin = [[".", ".", "O", "O", ".", "."]]
        elif turn == 1:
            possibleWin = [[".", ".", "X", "X", ".", "."]]
        else: return 0

        for row in range(self.rows):
            for col in range(2):
                if board[row][col:col+6] in possibleWin:
                    position.append([row, board[row][col:col + 6].index(".") + col+1])

        return position

    def checkTrap(self, board, turn, successors):
        count = 0
        colNum = None

        # Calculate how far the player from the horizontal win
        if len(self.Trap(board, turn)) == 0:
            if len(self.Trap(board, -turn)) > 0:
                # Calculate the distance from wining
                for pos in self.Trap(board, -turn):
                    for row in range(pos[0] + 1, self.rows):
                        if board[row][pos[1]] == "." or board[row][pos[1]+3] == ".":
                            count += 1
                    if count == 0:
                        colNum = [pos[1], pos[1]+3]
                        break

                # Prioritize the successors
                if colNum != None:
                    for successor in successors:
                        if successor[1] in colNum:
                            tmp1 = successor
                            successors.remove(successor)
                            successors.insert(0, tmp1)
                            break

        elif len(self.Trap(board, turn)) > 0:
            # Calculate the distance from horizontal win
            for pos in self.Trap(board, turn):
                for row in range(pos[0] + 1, self.rows):
                    if board[row][pos[1]] == "." or board[row][pos[1]+3] == ".":
                        count += 1
                if count == 0:
                    colNum = [pos[1], pos[1]+3]
                    break

                if colNum != None:
                    for successor in successors:
                        if successor[1] in colNum:
                            tmp = successor
                            successors.remove(successor)
                            successors.insert(0, tmp)


    def getSuccessors(self, state):

        curState = self.__problem.getState()
        self.__problem.setState(state)
        self.rows = 6
        self.cols = 7

        #####YOUR CODE BEGINS HERE#####
        successors = self.__problem.getSuccessors(state)
        evalHeuristic = C4HeuristicEval(self.__problem)
        turn = self.__problem.getTurn()

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
        self.checkCenter(successors, score, board)

        # Prioritize even or odd row
        maxcount = 0
        mincount = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if board[row][col] == "O":
                    mincount += 1
                elif board[row][col] == "X":
                    maxcount += 1

        if maxcount == mincount:
            self.checkOdd(successors, turn, score)
        if mincount < maxcount:
            self.checkEven(successors, turn, score)
        elif maxcount < mincount:
            self.checkEven(successors, turn, score)


        # Evaluate how far away the current state is from wining
        # React and prevent lost from horizon and vertical 4
        self.checkVeticalWins(board, turn, successors)
        self.checkHorWins(board, turn, successors)
        self.checkTrap(board, turn, successors)



        ######YOUR CODE ENDS HERE######

        self.__problem.setState(curState)
        return successors
