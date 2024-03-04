# Reinforcement Project Reflection 

The initialization of the Q-values is an important aspect of Q-learning; it can influence the learning process. However, in this cases, I can set the initial Q-values to be all zero. Since there is no prior knowledge about the state

The value of epsilon determines the probability of which the agent explores at a random action rather than exploiting its current knowledge. Decreasing the epsilon is used to balance the exploration and exploitation over time. As the state are mostly explored over time, I want to prioritize exploitation. Therefore, the value of epsilon gets lower and lower as I explore more over time. 

### Write what parameters you used for the crawling bot and what the highest 100-step velocity achieved was.

3.13

Discount = 0.919

Learning rate = 0.261

Epsilon = 0.985

numTraining = 10000

START_DEGRADE = .75

RATE_OF_DECAY = .1
