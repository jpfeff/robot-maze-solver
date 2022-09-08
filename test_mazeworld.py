# Modified by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/2/2021

from MazeworldProblem import MazeworldProblem
from Maze import Maze
import time

#from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test problems

# test_maze3 = Maze("mazes/maze3.maz")
# test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

# test_maze4 = Maze("mazes/maze4.maz")
# test_mp = MazeworldProblem(test_maze4, (3, 1, 3, 2, 4, 1))

# test_maze6x6 = Maze("mazes/6x6.maz")
# test_mp = MazeworldProblem(test_maze6x6, (5,4))

# test_maze10x10 = Maze("mazes/10x10.maz")
# test_mp = MazeworldProblem(test_maze10x10, (1, 4, 5, 6))

# test_maze40x40 = Maze("mazes/40x40.maz")
# test_mp = MazeworldProblem(test_maze40x40, (10 ,10, 2, 2))

# test_maze_wall = Maze("mazes/wall.maz")
# test_mp = MazeworldProblem(test_maze_wall, (2,2))

# test_maze_hallway = Maze("mazes/hallway.maz")
# test_mp = MazeworldProblem(test_maze_hallway, (1, 9, 1, 0))

# test_maze_inaccessible = Maze("mazes/inaccessible.maz")
# test_mp = MazeworldProblem(test_maze_inaccessible, (2, 2))

test_maze_blocked = Maze("mazes/blocked.maz")
test_mp = MazeworldProblem(test_maze_blocked, (7, 2, 6, 2))

# test_maze_two_path = Maze("mazes/two_path.maz")
# test_mp = MazeworldProblem(test_maze_two_path, (5, 1, 4, 1))

print(test_mp.get_successors(test_mp.start_state))

# this should explore a lot of nodes; it's just uniform-cost search
# start = time.time()
# result = astar_search(test_mp, null_heuristic)
# print(result)
# end = time.time()
# print("No heuristic time: " , end-start)

# start = time.time()
result = astar_search(test_mp, test_mp.euclidean_heuristic)
print(result)
# end = time.time()
# print("Euclidean heuristic time: " , end-start)

# start = time.time()
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
# end = time.time()
# print("Manhattan heuristic time: " , end-start)

test_mp.animate_path(result.path)
