import unittest
#from gradescope_utils.autograder_utils.decorators import weight, visibility
#from gradescope_utils.autograder_utils.files import check_submitted_files
#import heuristics_sol
#import sys
#sys.path.append("../submission/")
import heuristics
#sys.path.append("./project1_nodisplay/")
import sokoban
import util.search as search


class TestSokobanHeuristic(unittest.TestCase):
    def __init__(self, puzzle, actionLabels, actions, trueCosts, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        
        self.puzzle = puzzle
        self.actionLabels = actionLabels
        self.actions = actions
        self.trueCosts = trueCosts


    def testConsistency(self):
        initState = self.puzzle.getState()
        initBoard = str(self.puzzle)

        h = heuristics.SokobanHeuristic(self.puzzle)
        prevHVal = h.eval(initState)
        prevBoard = str(self.puzzle)
        self.assertLessEqual(prevHVal, self.trueCosts[0], "INADMISSIBLE\n" + prevBoard + "h(s) =  " + str(prevHVal) + "\nh*(s) = " + str(self.trueCosts[0]) + "\n")

        for j in range(len(self.actions)):
            cost = self.puzzle.move(self.actions[j])
            newBoard = str(self.puzzle)

            hVal = h.eval(self.puzzle.getState())
            self.assertLessEqual(hVal, self.trueCosts[j+1], "INADMISSIBLE\n" + newBoard + "h(s) =  " + str(hVal) + "\nh*(s) = " + str(self.trueCosts[j+1]) + "\n")
            #self.assertLessEqual(prevHVal - hVal, cost, "INCONSISTENT\n" + prevBoard + "h(s) = " + str(prevHVal) + "\na" + str(j+1) + ": " + self.actionLabels[self.actions[j]] + "\n" + newBoard + "h(s') = " + str(hVal) + "\nh(s) - h(s') = " + str(prevHVal - hVal) + "\ncost: " + str(cost))
            
            
            prevBoard = newBoard
            prevHVal = hVal

        print(initBoard)
        print("Actions Taken: " + " ".join([self.actionLabels[a] for a in self.actions]))
        print("All admissibility checks passed in this example.")
        print("WARNING: there may be errors not detected by these test cases.\nDO YOUR OWN TESTING AND ANALYSIS!")
            
class TestSokobanBenchmark(unittest.TestCase):

    def testBenchmark(self):
        fin = open("puzzles/benchmark.txt")
        stateStr = fin.read()
        p = sokoban.SokobanPuzzle(stateStr)

        h = heuristics.SokobanHeuristic(p)
        path,cost,numExpanded = search.aStarSearch(p, h)
        maxScore = 0
        if numExpanded <= 8000:
            maxScore = 12
        elif numExpanded < 20000:
            maxScore = 11
        elif numExpanded < 30000:
            maxScore = 10
        elif numExpanded < 50000:
            maxScore = 8
        elif numExpanded < 60000:
            maxScore = 6
        elif numExpanded < 100000:
            maxScore = 4
        elif numExpanded < 193390:
            maxScore = 2
        print("Nodes expanded: " + str(numExpanded) + " (max score: " + str(maxScore) + "/10)")
        self.assertTrue(path != [] or p.isSolved(), "ERROR: No solution found")
        self.assertEqual(cost, 78, "ERROR: Suboptimal solution (cost + " + str(cost) + "). Your heuristic must be inadmissible!")
        print("NOTE: this is an upper bound on your score, not your final score for this part; see project guidelines for details")
        
def suite():
    actionLabels = {(0, 1):"E", (0, -1):"W", (1, 0):"S", (-1, 0):"N"}
    filenames = ["simplest.txt", "toward.txt", "closest.txt", "easy.txt", "easy2.txt", "sorted.txt", "toward2.txt", "stairs.txt", "block.txt", "matching.txt", "livelock.txt", "livelock2.txt", "goals2box.txt"]
    actions = [[(0, 1), (0, 1), (0, 1)], [(0, 1), (0, 1), (0, 1), (0, -1), (1, 0), (0, 1)], [(0, -1), (0, -1), (0, -1)], [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0)], [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0)], [(0, -1), (0, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (0, 1), (-1, 0)], [(1, 0), (1, 0), (0, -1), (0, -1), (0, -1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1), (1, 0), (1, 0), (0, -1), (0, -1), (0, -1)], [(0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1), (1, 0), (0, 1)], [(0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)], [(-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (0, 1), (0, 1), (0, 1), (0, 1)], [(0, -1), (-1, 0), (0, 1)], [(0, -1), (-1, 0), (0, -1), (0, -1), (1, 0), (0, 1)], [(1, 0), (1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, 1), (-1, 0), (-1, 0), (0, 1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (-1, 0), (0, -1), (0, -1), (0, -1), (0, -1), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0), (1, 0)]]
    trueCosts = [[5, 4, 2, 0], [9, 8, 6, 4, 3, 2, 0], [15, 14, 13, 11], [9, 8, 7, 6, 5, 4, 2, 0], [14, 12, 10, 8, 6, 4, 2, 0], [17, 16, 14, 13, 12, 10, 9, 8, 7, 6, 4, 3, 2, 0], [21, 19, 17, 16, 15, 13, 12, 11, 10, 9, 8, 6, 5, 4, 3, 2, 0], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 0], [18, 16, 14, 12, 10, 8, 6, 4, 2, 0], [6, 4, 2, 0], [9, 7, 5, 4, 3, 2, 0], [47, 45, 43, 42, 41, 40, 39, 38, 37, 36, 35, 33, 31, 29, 27, 25, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 10, 8, 6, 4, 2, 0]]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for i in range(len(filenames)):
        fin = open("puzzles/"+filenames[i])
        stateStr = fin.read()
        p = sokoban.SokobanPuzzle(stateStr)
        case = TestSokobanHeuristic(p, actionLabels, actions[i], trueCosts[i], methodName="testConsistency")
        suite.addTest(case)
    case = TestSokobanBenchmark(methodName="testBenchmark")
    suite.addTest(case)
    return suite
        
