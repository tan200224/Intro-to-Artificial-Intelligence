# Developing Heuristics

## Sliding Puzzle Heuristic AnalysisSliding Puzzle Heuristic Analysis
<img width="491" alt="image" src="https://github.com/tan200224/Intro-to-Artificial-Intelligence/assets/68765056/504bb388-7ee4-46c6-bdbf-a2506eb99748">

## Sokoban Heuristic Description/Analysis
In this assignment, I thought about many different ways that might lower the efficiency
of putting all the boxes to the goals in order to lower the number of expanded nodes. First, I
make sure there are always equal amounts of goals and boxes, if not, there will be no way to
complete the game, thus returning an infinite heuristic. Secondly, If the player is standing on the
goal, the player must move. Therefore, increase the heuristic by 2 if there are players
standing on the goal. Third, I calculated the Manhattan distance between the player and the box
and added their distance to the heuristic. Then I matched the goals and boxes based on the
shortest distances and also added up all those distances into the heuristic.
Then, I start to check if there are boxes on the bottom, top, right, and left edges. If the
box is on the edges and there are no goals on those edges, there is no way that those boxes can
reach a goal, because you can’t pull those boxes away from the edges. Therefore, in those cases,
I returned an infinite heuristic.
Then I start to check the corners because if the boxes are on the corners and those
corners have no goals, we will not be able to move those boxes at all. Therefore the heuristic is
infinite.
Then I also checked if there is the possibility that the player keeps hitting the walls, which
might increase the costs, so I make sure the position of the player is not a wall, if so, I
will return an infinite heuristic.
Then I check if the boxes need to be turned around, which might take more steps. In
some cases like when the player and the goal are above the box, then the player has to make a
turn around the box, like moving to the bottom of the box in order to put it to the goal. Therefore,
I increased the number of heuristics by 9, which is around the number of steps you need to reach
the box, walk around the box and put the box back on top.
Then I check the neighbor around the goal to make sure the goal is not surrounded by
walls. All the neighbors are walls, there will be no way to reach that goal, and then heuristics
will be infinite. I return a heuristic of 3 or 5 based on the number of walls around the goals.
Since the more walls around the goal, the box might need to take more steps to go around the
walls.

Lastly, I check the boxes and goals that are on the same row or column and determine if
there are walls between them. If so, the box might need to climb over the walls. This will be 2
times the height of the wall and plus the width of the wall. In my case, I return a 9, which is
based on the side of the wall.

Result:
All admissibility checks passed in this example.

WARNING: there may be errors not detected by these test cases.
DO YOUR OWN TESTING AND ANALYSIS!

Nodes expanded: 6370 (max score: 12/10)

NOTE: this is an upper bound on your score, not your final score for this part; see project guidelines for
details

----------------------------------------------------------------------
Ran 106 tests in 0.248s
