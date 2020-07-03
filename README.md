# simple-minimax-tictactoe
## Description
A simple implementation of the minimax algorithm to make an advanced tic-tac-toe computer.

##  Usage
There are three available agents to play the game:
```python
player_agent # user plays
random_agent # computer randomly chooses a valid space to fill
minimax_agent # computer uses minimax algorithm to choose what space to fill
```
You can watch/play a game between two agents with the function:
```python
agent_play(agent_x, agent_o)
```
You can simulate x number of games between two agents (obviously not the player_agent) and see the % results with the function:
```python 
agent_play_sim(agent_x, agent_o, epochs)
```

## Minimax algorithm implementation
The algorithm used was based on the psuedocode found on https://en.wikipedia.org/wiki/Minimax#Pseudocode

## Further uses
With obvious tweaks to the game functions this same agent could be used for more complicated games such as connect 4. Furthermore with the addition of alpha-beta pruning the algorithm can be used to create a chess computer.
