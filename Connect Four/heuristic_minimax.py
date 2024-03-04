def heuristicGetMax(state, bestMin, bestMax, depth, terminalEval, moveOrder):
    successors = moveOrder.getSuccessors(state)

    bestScore = float("-inf")
    bestMove = -1
    bound = bestMax
    subtreeNodes = 1
    s = 0
    while s < len(successors) and bestScore < bestMin:
        succ = successors[s]
        if succ[2] == 2:
            score = succ[3]
            subtreeNodes += 1
        elif depth == 1:
            score = terminalEval.eval(succ[0])
            subtreeNodes += 1
        elif succ[2] == 1:
            score, moves, nodes = heuristicGetMax(succ[0], bestMin, bound, depth-1, terminalEval, moveOrder)
            subtreeNodes += nodes
        elif succ[2] == -1:
            score, moves, nodes = heuristicGetMin(succ[0], bestMin, bound, depth-1, terminalEval, moveOrder)
            subtreeNodes += nodes

        if score > bestScore:
            bestScore = score
            bestMove = succ[1]

        if bestScore > bound:
            bound = bestScore

        s += 1

    return bestScore, bestMove, subtreeNodes

def heuristicGetMin(state, bestMin, bestMax, depth, terminalEval, moveOrder):
    successors = moveOrder.getSuccessors(state)

    bestScore = float("inf")
    bestMove = -1
    bound = bestMin
    subtreeNodes = 1
    s = 0
    while s < len(successors) and bestScore > bestMax:
        succ = successors[s]       
        if succ[2] == 2:
            score = succ[3]
            subtreeNodes += 1
        elif depth == 1:
            score = terminalEval.eval(succ[0])
            subtreeNodes += 1
        elif succ[2] == 1:
            score, moves, nodes = heuristicGetMax(succ[0], bound, bestMax, depth-1, terminalEval, moveOrder)
            subtreeNodes += nodes
        elif succ[2] == -1:
            score, moves, nodes = heuristicGetMin(succ[0], bound, bestMax, depth-1, terminalEval, moveOrder)
            subtreeNodes += nodes

        if score < bestScore:
            bestScore = score
            bestMove = succ[1]

        if bestScore < bound:
            bound = bestScore

        s += 1

    return bestScore, bestMove, subtreeNodes

""" 
This is the main entry point for this class.
The function returns the move deemed best by minimax with alpha-beta pruning as well as the number of 
nodes expanded during the search.

The function takes as input:
- state: the object referring to the current state of the game 
- turn: an integer, either 1 if it is max's turn or -1 if it is min's turn.
- depth: an integer >= 1 indicating the maximum depth of the search
- terminalEval: c4agent's C4HeuristicEval object or other object that has an eval() function for the game
- moveOrder: c4agent's C4OrderHeuristic object or other object that has an getSuccessors() function for the game
"""
def getMove(state, turn, depth, terminalEval, moveOrder):
    
    if turn == 1:
        score, move, numNodes = heuristicGetMax(state, float("inf"), float("-inf"), 4, terminalEval, moveOrder)
    elif turn == -1:
        score, move, numNodes = heuristicGetMin(state, float("inf"), float("-inf"), 4, terminalEval, moveOrder)
    return move, numNodes
