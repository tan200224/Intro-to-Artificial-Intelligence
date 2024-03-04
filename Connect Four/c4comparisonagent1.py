class C4HeuristicEval:
    def __init__(self, problem):
        self.__problem = problem 
        ###If you want to do any pre-processing, do it here
        ###(note: time limit for the constructors is 2 seconds!)
        
    def eval(self, state):
        '''Gives a heuristic evaluation of the given state.'''
        curState = self.__problem.getState()
        self.__problem.setState(state)

        #####YOUR CODE BEGINS HERE#####
        #You should take a look at connectfour.py to see what methods self.__problem has, but here are some that will probably be helpful:
        #get/setState()
        #getTurn() -- returns a number indicating whose turn it is in the current state: -1 for min, 1 for max, 2 if the state is terminal
        #getSuccessors(state) -- returns the successors of the given state as 4-tuples: (next state, action to get there, whose turn it is in that state, the final score)
        #getTile(row, col) -- returns the contents of the given position on the board ("X" for max, "O" for min, "." for empty)
        #getHeights() -- returns a list of the heights of the stacks in the 7 columns

        eval = 0
        ######YOUR CODE ENDS HERE######

        self.__problem.setState(curState)
        return eval

class C4OrderHeuristic:
    def __init__(self, problem):
        self.__problem = problem
        ###If you want to do any pre-processing, do it here
        ###(note: time limit for the constructors is 2 seconds!)

    def getSuccessors(self, state):
        curState = self.__problem.getState()
        self.__problem.setState(state)

        #####YOUR CODE BEGINS HERE#####
        successors = self.__problem.getSuccessors(state)
        ######YOUR CODE ENDS HERE######
        
        self.__problem.setState(curState)
        return successors
