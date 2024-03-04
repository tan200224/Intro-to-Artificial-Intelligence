import AA
import heuristic_minimax


class C4TournamentAgent:
    def __init__(self, problem):
        self.__problem = problem
        self.__eval = AA.C4HeuristicEval(problem)
        self.__order = AA.C4OrderHeuristic(problem)

    def getMove(self):
        return heuristic_minimax.getMove(self.__problem.getState(),
                                         self.__problem.getTurn(), 4, self.__eval, self.__order)[0]

