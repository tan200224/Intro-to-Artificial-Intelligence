import unittest
#from gradescope_utils.autograder_utils.decorators import weight, visibility
#from gradescope_utils.autograder_utils.files import check_submitted_files
#import heuristics_sol
#import sys
#sys.path.append("../submission/")
import heuristics
#sys.path.append("./project1_nodisplay/")
import slidingpuzzle
#from util.timeout import *

class TestSlidingPuzzleHeuristic(unittest.TestCase):
    def __init__(self, puzzle, heuristicToTest, answer, label, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        self.puzzle = puzzle
        self.heuristicToTest = heuristicToTest
        self.answer = answer
        self.label = label

    def runTest(self):
        bound = self.heuristicToTest.eval(self.puzzle)
        #boundSol = self.heuristicToCompare.eval(self.puzzle)
        self.assertEqual(bound, self.answer, "Testing " + self.label + " on...\n" + self.puzzle)

class TestComboHeuristic(unittest.TestCase):
    def __init__(self, puzzle, combo, manhattan, gaschnigs, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        
        self.puzzle = puzzle
        self.combo = combo
        self.manhattan = manhattan
        self.gaschnigs = gaschnigs


    def runTest(self):
        bound = self.combo.eval(self.puzzle)
        manBound = self.manhattan.eval(self.puzzle)
        gaschBound = self.gaschnigs.eval(self.puzzle)
        boundMax = max(manBound, gaschBound)
        self.assertEqual(bound, boundMax, "Testing Combo on...\n" + self.puzzle + "Manhattan: " + str(manBound) + "\nGaschnig's: " + str(gaschBound))
        
def suite():
    tests = ['3 8 1\n6 5 4\n2 7 0\n', '3 1 0\n8 2 6\n7 5 4\n', '0 8 1\n4 5 2\n6 3 7\n',
             '6 5 2\n7 0 1\n3 8 4\n', '7 8 5\n2 0 6\n1 3 4\n', '5 4 0\n6 3 8\n2 1 7\n',
             '1 4 0\n3 8 5\n7 2 6\n', '5 4 1\n3 6 8\n7 2 0\n', '0 5 8\n4 1 3\n6 7 2\n',
             '4 2 3\n8 6 1\n7 5 0\n', '3 1 5\n2 7 4\n0 6 8\n', '0 3 5\n4 2 8\n6 1 7\n',
             '3 1 2\n5 6 8\n4 7 0\n', '3 2 4\n6 0 1\n7 8 5\n', '4 3 1\n5 7 2\n0 6 8\n',
             '0 2 5\n1 3 7\n6 8 4\n', '3 2 0\n4 8 5\n6 1 7\n', '1 4 0\n7 6 2\n3 8 5\n',
             '3 1 2\n8 0 4\n6 7 5\n', '3 4 1\n6 8 2\n0 7 5\n', '0 1 2\n3 4 5\n6 7 8\n',
             '0 2 1\n3 4 5\n6 7 8\n']
    #print(len(tests))
    solutionMisplaced = [7,7,7,7,8,8,6,7,6,8,6,7,5,8,7,7,6,8,4,7,0,2] # 4

    #print(len(solutionMisplaced))
    solutionManhattan = [12, 14, 10, 12, 20, 14, 10, 12, 10, 16, 8, 10, 8, 10, 10, 10, 8, 10, 6, 8, 0, 2] # 4
    #print(len(solutionManhattan))
    solutionG = [8, 8, 8, 8, 8, 8, 6, 8, 8, 8, 6, 8, 6, 8, 8, 8, 6, 8, 4, 8, 0, 3] # 4
    #print(len(solutionG))

    all_solutions = [solutionMisplaced, solutionManhattan, solutionG]

    sp = slidingpuzzle.SlidingPuzzle(3, 3, 0)
    submittedHeuristics = [heuristics.NumMisplacedHeuristic(sp),
                           heuristics.ManhattanHeuristic(sp),
                           heuristics.GaschnigsHeuristic(sp),
                           heuristics.ComboHeuristic(sp)]

    #solutionHeuristics = [heuristics_sol.NumMisplacedHeuristic(sp), heuristics_sol.ManhattanHeuristic(sp), heuristics_sol.GaschnigsHeuristic(sp), heuristics_sol.ComboHeuristic(sp)]

    biggerTest = '1 6 2 3 4\n5 7 12 8 9\n10 11 0 13 14\n15 16 17 18 19\n'
    sp2 = slidingpuzzle.SlidingPuzzle(4, 5, 0)
    submittedHeuristics2 = [heuristics.NumMisplacedHeuristic(sp2),
                            heuristics.ManhattanHeuristic(sp2),
                            heuristics.GaschnigsHeuristic(sp2),
                            heuristics.ComboHeuristic(sp2)]
    #solutionHeuristics2 = [heuristics_sol.NumMisplacedHeuristic(sp2), heuristics_sol.ManhattanHeuristic(sp2), heuristics_sol.GaschnigsHeuristic(sp2), heuristics_sol.ComboHeuristic(sp2)]
    solutionHeuristics2 = [4,4,4]
    hLabels = ["Misplaced", "Manhattan", "Gaschnig's"]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for i in range(len(hLabels)):
        for j in range(len(tests)):
            puzzle = tests[j]
            #case = TestSlidingPuzzleHeuristic(puzzle, submittedHeuristics[i], solutionHeuristics[i], hLabels[i])
            case = TestSlidingPuzzleHeuristic(puzzle, submittedHeuristics[i], all_solutions[i][j], hLabels[i])
            suite.addTest(case)
        case = TestSlidingPuzzleHeuristic(biggerTest, submittedHeuristics2[i], solutionHeuristics2[i], hLabels[i])
        suite.addTest(case)

    for puzzle in tests:
        case = TestComboHeuristic(puzzle, submittedHeuristics[3], submittedHeuristics[1], submittedHeuristics[2])
        suite.addTest(case)
    case = TestComboHeuristic(biggerTest, submittedHeuristics2[3], submittedHeuristics2[1], submittedHeuristics2[2])
    suite.addTest(case)
    return suite

