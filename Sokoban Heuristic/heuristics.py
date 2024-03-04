'''Contains heuristics for sliding puzzles and Sokoban.'''


class NullHeuristic:
    '''The heuristic function that always returns 0.'''

    def __init__(self, problem):
        pass

    def eval(self, state):
        return 0


class NumMisplacedHeuristic:
    '''Gives the number of misplaced tiles.'''

    def __init__(self, problem):
        self.problem = problem

    def eval(self, state):
        curState = self.problem.getState()
        self.problem.setState(state)

        ######YOUR CODE BEGINS HERE######
        bound = 0  # Replace this with your code (set bound to what you want to return)
        #######YOUR CODE ENDS HERE#######
        board = self.problem.getBoard()
        solution = []
        rows, cols = self.problem.getDim()
        counter = 0
        for i in range(rows):
            solution.append([])
            for j in range(cols):
                solution[i].append(counter)
                counter += 1

        for row in range(rows):
            for col in range(cols):
                if board[row][col] != solution[row][col] and board[row][col] != 0:
                    bound += 1

        self.problem.setState(curState)
        return bound


class ManhattanHeuristic:
    '''Gives the Manhattan distance each tile's position to its position in the goal state.'''

    def __init__(self, problem):
        self.problem = problem

    def eval(self, state):
        curState = self.problem.getState()
        self.problem.setState(state)

        ######YOUR CODE BEGINS HERE######
        bound = 0  # Replace this with your code (set bound to what you want to return)
        #######YOUR CODE ENDS HERE#######

        if not (self.problem.isSolved()):

            solution = []
            dic_solution = {}
            rows, cols = self.problem.getDim()
            counter = 0
            for i in range(rows):
                solution.append([])
                for j in range(cols):
                    solution[i].append(counter)
                    dic_solution[counter] = (i, j)
                    counter += 1

            board = self.problem.getBoard()
            rows, cols = self.problem.getDim()

            for row in range(rows):
                for col in range(cols):
                    num = self.problem.getTile(row, col)
                    if num != 0:
                        x, y = dic_solution.get(num)
                        dx, dy = abs(x - row), abs(y - col)
                        bound += dx + dy

        self.problem.setState(curState)
        return bound


import random


class GaschnigsHeuristic:
    '''Gives the number of moves to the goal if any tile may swap with the blank tile.'''

    def __init__(self, problem):
        self.problem = problem

    def eval(self, state):
        curState = self.problem.getState()
        self.problem.setState(state)
        ######YOUR CODE BEGINS HERE######
        bound = 0  # Replace this with your code (set bound to what you want to return)
        #######YOUR CODE ENDS HERE#######

        # Create e solution and dic_solution that contains the number and their position in the goal state
        solution = []
        dic_solution = {}
        rows, cols = self.problem.getDim()
        board = self.problem.getBoard()

        counter = 0
        for i in range(rows):
            solution.append([])
            for j in range(cols):
                solution[i].append(counter)
                dic_solution[counter] = (i, j)
                counter += 1

        x, y = 0, 0
        while board != solution:
            # Get the position of blank tile
            for i in range(rows):
                for j in range(cols):
                    if board[i][j] == 0:
                        x, y = i, j

            # if the blank tile not in the right position
            if (x, y) != (0, 0):
                for num, position in dic_solution.items():
                    if (x, y) == position:

                        for row in range(rows):
                            for col in range(cols):
                                if board[row][col] == num:
                                    board[row][col] = 0

                        board[x][y] = num
                        break

            else:
                misplacedNum = []
                for row in range(rows):
                    for col in range(cols):
                        if board[row][col] != solution[row][col]:
                            misplacedNum.append(board[row][col])

                if len(misplacedNum) != 0:
                    replaceNum = random.choice(misplacedNum)
                    board[0][0] = replaceNum
                    tmpx, tmpy = dic_solution.get(replaceNum)
                    board[tmpx][tmpy] = 0

            bound = bound + 1

        self.problem.setState(curState)
        return bound


class ComboHeuristic:
    '''Gives the max of Manhattan and Gaschnig's.'''

    def __init__(self, problem):
        self.problem = problem
        self.manhattan_heuristic = ManhattanHeuristic(problem)
        self.gaschnig_heuristic = GaschnigsHeuristic(problem)
        # Put some code in here too!

    def eval(self, state):
        curState = self.problem.getState()
        self.problem.setState(state)

        ######YOUR CODE BEGINS HERE######
        bound = 0  # Replace this with your code (set bound to what you want to return)
        #######YOUR CODE ENDS HERE#######
        manhattan_bound = self.manhattan_heuristic.eval(state)
        gaschnig_bound = self.gaschnig_heuristic.eval(state)

        bound = max(int(manhattan_bound), int(gaschnig_bound))

        self.problem.setState(curState)
        return bound


import math


class SokobanHeuristic:
    def __init__(self, problem):
        self.problem = problem
        # You may add some pre-processing code here, if you want (must be poly-time!)
        self.rows, self.cols = self.problem.getDim()


    def getKey(self, val, dictionary):
        for key, value in dictionary.items():
            if val == value:
                return key
            else:
                return 0

    def checkRightEdge(self, boxes, goals):

        numRightGoal = 0
        numRightBox = 0
        for i in range(len(boxes)):
            if boxes[i][1] == self.cols - 2 and boxes[i][2] == False:
                numRightBox += 1

            if goals[i][1] == self.cols - 2:
                numRightGoal += 1

        if numRightBox > numRightGoal:
            return float('inf')
        else:
            return 0

    def checkLeftEdge(self, boxes, goals):

        numLeftGoal = 0
        numLeftBox = 0
        for i in range(len(boxes)):
            if boxes[i][1] == 1 and boxes[i][2] == False:
                numLeftBox += 1

            if goals[i][1] == 1:
                numLeftGoal += 1

        if numLeftBox > numLeftGoal:
            return float('inf')
        else:
            return 0

    def checkTopEdge(self, boxes, goals):

        numTopGoal = 0
        numTopBox = 0
        for i in range(len(boxes)):
            if boxes[i][0] == 1 and boxes[i][2] == False:
                numTopBox += 1

            if goals[i][0] == 1:
                numTopGoal += 1

        if numTopBox > numTopGoal:
            return float('inf')
        else:
            return 0

    def checkBotEdge(self, boxes, goals):

        numBotGoal = 0
        numBotBox = 0
        for i in range(len(boxes)):
            if boxes[i][0] == self.rows - 2 and boxes[i][2] == False:
                numBotBox += 1

            if goals[i][0] == self.rows - 2:
                numBotGoal += 1

        if numBotBox > numBotGoal:
            return float('inf')
        else:
            return 0

    def checkCorners(self, boxes):

        for i in range(len(boxes)):
            if boxes[i][2] == False:
                if boxes[i][0] == 1 and boxes[i][1] == 1:
                    return float('inf')
                elif boxes[i][0] == 1 and boxes[i][1] == self.cols-2:
                    return float('inf')
                elif boxes[i][0] == self.rows-2 and boxes[i][1] == 1:
                    return float('inf')
                elif boxes[i][0] == self.rows-2 and boxes[i][1] == self.cols-2:
                    return float('inf')

        return 0

    def checkBlockers(self, boxes):
        #blockers = ["#", "o", "O"]
        for i in range(len(boxes)):

            if boxes[i][2] == False:
            # Top left of the box
                if self.problem.getItem(boxes[i][0] - 1, boxes[i][1]) == "#" \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] - 1) in ["#","o","O"] \
                        or self.problem.getItem(boxes[i][0] - 1, boxes[i][1]) in ["#","o","O"] \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] - 1) == "#":
                    return float('inf')

                # Top right of the box
                elif self.problem.getItem(boxes[i][0] - 1, boxes[i][1]) == "#" \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] + 1) in ["#","o","O"] \
                        or self.problem.getItem(boxes[i][0] - 1, boxes[i][1]) in ["#","o","O"] \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] + 1) == "#":
                    return float('inf')

                # Bottom right of the box
                elif self.problem.getItem(boxes[i][0] + 1, boxes[i][1]) == "#" \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] + 1) in ["#","o","O"] \
                        or self.problem.getItem(boxes[i][0] + 1, boxes[i][1]) in ["#","o","O"] \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] + 1) == "#":
                    return float('inf')

                # Bottom left of the box
                elif self.problem.getItem(boxes[i][0] + 1, boxes[i][1]) == "#" \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] - 1) in ["#","o","O"] \
                        or self.problem.getItem(boxes[i][0] + 1, boxes[i][1]) in ["#","o","O"] \
                        and self.problem.getItem(boxes[i][0], boxes[i][1] - 1) == "#":
                    return float('inf')

        return 0

    def turnupDown(self, x, y, boxes, goals):
        score = 0
        for box in range(len(boxes)):
            if boxes[box][2] == False:
                # Player is above the box
                if x < boxes[box][0]:
                    count = 0
                    for goal in range(len(goals)):
                        # Check if there are empty goal below the box
                        if goals[goal][0] >= boxes[box][0] and self.problem.getItem(goals[goal][0], goals[goal][1]) == '*':
                            count += 1
                    if count == 0:
                        score += 9

                # Player is below the box
                elif x > boxes[box][0]:
                    count = 0
                    for goal in range(len(goals)):
                        # Check if there are empty goal above the box
                        if goals[goal][0] <= boxes[box][0] and self.problem.getItem(goals[goal][0], goals[goal][1]) == '*':
                            count += 1
                    if count == 0:
                        score += 9
        return score

    def playerMoves(self, x, y):
        if self.problem.getItem(x, y) == "#":
            return float('inf')
        return 0

    def checkgoalNeighbors(self, goals):

        for i in range(len(goals)):
            count = 0
            if self.problem.getItem(goals[i][0], goals[i][1]) == '*':
                # Top Left
                if self.problem.getItem(goals[i][0]-1, goals[i][1]-1) == '#':
                    count += 1

                # Top Right
                if self.problem.getItem(goals[i][0]-1, goals[i][1]+1) == '#':
                    count += 1

                # Top
                if self.problem.getItem(goals[i][0]-1, goals[i][1]) == '#':
                    count += 1

                # Bottom Right
                if self.problem.getItem(goals[i][0]+1, goals[i][1]+1) == '#':
                    count += 1

                # Bottom Left
                if self.problem.getItem(goals[i][0]+1, goals[i][1]-1) == '#':
                    count += 1

                # Bottom
                if self.problem.getItem(goals[i][0]+1, goals[i][1]) == '#':
                    count += 1

                # Left
                if self.problem.getItem(goals[i][0], goals[i][1]-1) == '#':
                    count += 1

                # Right
                if self.problem.getItem(goals[i][0], goals[i][1]+1) == '#':
                    count += 1

            if count >= 9:
                return float('inf')
            elif count >= 8:
                return 5
            elif count >= 7:
                return 3
            else:
                return 0

    def checkSameLineBlock(self, boxes, goals):

        score = 0
        minBoxToGoal = {}
        for goal in range(len(goals)):
            # find all the goals that are not complete yet
            if self.problem.getItem(goals[goal][0], goals[goal][1]) == '*':
                # Store the value of the distance between goals and boxes
                boxNum_Distances = {}
                for box in range(len(boxes)):
                    if boxes[box][2] == False:
                        # If the box is not on the goal
                        distance = abs(goals[goal][0] - boxes[box][0]) + abs(goals[goal][1] - boxes[box][1])
                        boxNum_Distances[box] = distance
                # Match the goal with box
                if min(boxNum_Distances.values()) >= 2:
                    boxNum = self.getKey(min(boxNum_Distances.values()), boxNum_Distances)
                    minBoxToGoal[goal] = boxNum

        for goal, box in minBoxToGoal.items():
            # if goal and box are on the same row
            if goals[goal][0] == boxes[box][0]:
                # Check if there are wall or box between the goal and box on the same col
                if goals[goal][1] > boxes[box][1]:
                    a = boxes[box][1]
                    b = goals[goal][1]
                else:
                    a = goals[goal][1]
                    b= boxes[box][1]
                for col in range(a, b):
                    if self.problem.getItem(goals[goal][0], col) == '#':
                        score += 9

            # if goal and box are on the same col
            if goals[goal][1] == boxes[box][1]:
                # Check if there are wall or box between the goal and box on the same row
                if goals[goal][0] > boxes[box][0]:
                    a = boxes[box][0]
                    b = goals[goal][0]
                else:
                    a = goals[goal][0]
                    b = boxes[box][0]
                for row in range(a, b):
                    if self.problem.getItem(row, goals[goal][1]) == '#':
                        score += 9

        return score


    def eval(self, state):
        curState = self.problem.getState()
        self.problem.setState(state)

        boxes = self.problem.getBoxes()
        goals = self.problem.getGoals()
        self.x, self.y = self.problem.getPos()



        ######YOUR CODE BEGINS HERE######
        bound = 0  # Replace this with your code (set bound to what you want to return)

        bound += self.checkBotEdge(boxes, goals)
        bound += self.checkTopEdge(boxes, goals)
        bound += self.checkLeftEdge(boxes, goals)
        bound += self.checkRightEdge(boxes, goals)
        bound += self.checkCorners(boxes)
        bound += self.checkBlockers(boxes)
        bound += self.playerMoves(self.x, self.y)
        bound += self.turnupDown(self.x, self.y, boxes, goals)
        bound += self.checkgoalNeighbors(goals)
        bound += self.checkSameLineBlock(boxes, goals)


        # if the games have more goals than boxes
        if len(self.problem.getGoals()) > len(self.problem.getBoxes()):
            return float('inf')

        # if player is on top of the goal, it has to be moved
        if self.problem.getItem(self.x, self.y) == '=':
            bound += 2

        # Find the distance between the player and the boxes
        for i in range(len(boxes)):
            if boxes[i][2] == False:
                distance = math.floor(math.sqrt(abs(self.x - boxes[i][0])**2 + abs(self.y - boxes[i][1])**2))-3
                bound += distance


        # Find the distance between the boxes and goals
        for i in range(len(goals)):
            # find all the goals that are not complete yet
            if self.problem.getItem(goals[i][0], goals[i][1]) in ['*', '=']:
                # Store the value of the box index and the distance
                minDisBox = {}
                for j in range(len(boxes)):
                    if boxes[j][2] == False:
                        # If the box is not on the goal
                        distance = abs(goals[i][0] - boxes[j][0]) + abs(goals[i][1] - boxes[j][1])
                        minDisBox[j] = distance

                bound += min(minDisBox.values())



        #######YOUR CODE ENDS HERE#######

        self.problem.setState(curState)
        return bound


