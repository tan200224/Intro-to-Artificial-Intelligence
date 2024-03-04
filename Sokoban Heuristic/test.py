import sokoban
import heuristics

fin = open("puzzles/benchmark.txt")
stateStr = fin.read()
p = sokoban.SokobanPuzzle(stateStr)

answer = heuristics.SokobanHeuristic(p)
print(answer.eval(p.getState()))
