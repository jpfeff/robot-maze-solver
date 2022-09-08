# Written by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/2/2021

from SensorlessProblem import SensorlessProblem
from Maze import Maze

#from uninformed_search import bfs_search
from astar_search import astar_search

# test_maze3 = Maze("mazes/maze3.maz")
# test_sp = SensorlessProblem(test_maze3)

test_maze6x6 = Maze("mazes/6x6.maz")
test_sp = SensorlessProblem(test_maze6x6)

# this test takes about 5 minutes to run
# test_maze10x10 = Maze("mazes/10x10.maz")
# test_sp = SensorlessProblem(test_maze10x10)

result = astar_search(test_sp, test_sp.sensorless_heuristic)
print(result)
test_sp.animate_path(result.path)