import heapq

class PriorityQueue:
    '''A priority queue. Each item in the queue is associated with a priority. The queue gives efficient access to the minimum priority item.'''
    def __init__(self):
        self.__heap = []

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.__heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.__heap)
        return item, priority

    def isEmpty(self):
        return len(self.__heap) == 0

def aStarSearch(problem, heuristic):
    fringe = PriorityQueue()
    visited = {}
    inFringe = {}
    startState = problem.getState()
    fringe.push((startState, [], 0, problem.isSolved()), heuristic.eval(startState))
    inFringe[startState] = True
    numExpanded = 0
    while not fringe.isEmpty():
        s, score = fringe.pop()
        inFringe[s[0]] = False
        if s[3]:
            return s[1], s[2], numExpanded
        elif (s[0] not in visited) or visited[s[0]] > score:
            numExpanded += 1
            visited[s[0]] = score
            successors = problem.getSuccessors(s[0])
            for succ in successors:
                if succ[0] not in visited:# and succ[0] not in inFringe:
                    fringe.push((succ[0], s[1] + [succ[1]], s[2] + succ[2], succ[3]), s[2] + succ[2] + heuristic.eval(succ[0]))
                    inFringe[succ[0]] = True
    return [], float("inf"), numExpanded
