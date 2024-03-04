
# Our Agent (AA)
For our connect four agent, we looked at the state of the board and determined how likely either
the min or max player is to win the game. Our agent contains methods for evaluating horizontal,
vertical, and diagonal connections on the game board. We count the number of possible
horizontal, vertical, and diagonal wins for both sides and then we increase/decrease the eval
score accordingly. We also evaluate how close the wins are. If the win is closer to the bottom, it
means the win is more achievable then we increase/decrease the eval score accordingly. Lastly,
we determine the side on which player is the first player, then they would be more likely to win
by playing odd rows; on the other hand, the second player is more likely to win by playing even
rows. It is because at the end of the games when there is 1 column left, when both sides have
no option to place. If the odd player has a win on the odd row that is closer to the bottom (like
row 1, 3), then the odd/first player will win. On the other hand, if the even player has a win on
row lower and it is closer to the bottom (like row 2, 4) then the even player will win. Additionally,

it considers certain strategic elements, such as early game moves on the edges and middle. It
will penalize the player because you don’t want to play the first one on the col 0 or the last
column because they are less likely to give you a win compared to the middle. It also considers
potential traps such as (..00.. Or ..XX..). The overall evaluation combines these factors, resulting
in a numerical score that indicates who is more likely to win based on the current game state.
For the eval, we counted all the possible wins and losses on the horizontal plane and vertical
plane and added it to eval based on those numbers. We also implemented a checker to see
who played first (odd player) and second (even player), because the player who plays first has
an advantage playing on odd rows while the player who plays second has an advantage playing
on even rows, so we took this into account when calculating our eval. We also normalized our
eval value to ensure that it stays in the range of 1 to -1.

Investigations
The biggest difference makers in the agent are the possible horizontal and vertical win counters.
With those methods removed the agent performs significantly worse. With both removed the
agent still wins against the benchmark, however, there are a lot more draws. With only one
removed the agent wins more but still not as much as the full agent. Removing either the
horizontal or vertical yield similar results of the agent not performing as well. The center play
and early edge methods don’t not have as big of an impact. The agent still wins a good amount
with those methods removed. For all the trials, we ran the comparison agents 10 times against
the benchmark agent to record and check the performance.

# Agent Results
-p1 c4benchmarkagent.pyc -p2 c4agent.py -t25
Stats:
c4benchmarkagent.pyc wins: 3
c4agent.py wins: 42
Draws: 5
c4benchmarkagent.pyc:
0.060079140449637795 seconds per step, on average
183.1915422885572 nodes expanded per step, on average, using the
order heuristic
c4agent.py:
0.16219887368887373 seconds per step, on average
176.82645631067962 nodes expanded per step, on average, using the
order heuristic

-p1 c4agent.py -d1 -p2 c4benchmarkagent.pyc -t5
Stats:
c4agent.py wins: 10
c4benchmarkagent.pyc wins: 0
Draws: 0
c4agent.py:
0.15726061063270047 seconds per step, on average
327.3082191780822 nodes expanded per step, on average, using the
default move order
170.13698630136986 nodes expanded per step, on average, using the
order heuristic
c4benchmarkagent.pyc:
0.060504539638546344 seconds per step, on average
187.7872340425532 nodes expanded per step, on average, using the
order heuristic
-r -p1 AA.py -p2 c4benchmarkagent.pyc -t 25
Stats:
AA.py wins: 46
c4benchmarkagent.pyc wins: 3
Draws: 1
AA.py:
0.16273189715061234 seconds per step, on average
c4benchmarkagent.pyc:
0.05892826463006864 seconds per step, on average

-r -p1 AA.py -p2 c4qualifyingagent.pyc -t 25
Stats:
AA.py wins: 50
c4qualifyingagent.pyc wins: 0
Draws: 0
AA.py:
0.1275325334072113 seconds per step, on average
c4qualifyingagent.pyc:
0.0619309210165953 seconds per step, on average
