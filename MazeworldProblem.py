# Modified by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/2/2021

from Maze import Maze
from time import sleep
import math

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        robot_locations = list(maze.robotloc)
        robot_locations.insert(0,0)
        self.start_state = tuple(robot_locations)
        
        self.goal_locations = goal_locations
        self.num_robots = len(goal_locations)/2
        self.maze = maze

    def __str__(self):
        string =  "Mazeworld problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    # returns the transition cost from one state to another  
    def get_transition_cost(self, current_state, successor_state):
        # if the robot did not move, the cost is 0
        if current_state[1:] == successor_state[1:]:
            return 0
        # otherwise the cost is 1
        else:
            return 1
        
    # function to calculate total manhattan distance from each robot to its goal
    def manhattan_heuristic(self, state):
        robot_locations = state[1:]
        goal_locations = self.goal_locations
        heuristic_sum = 0

        # loops over robot locations in state
        for k in range(0, len(goal_locations) - 1, 2):
            x_cur = robot_locations[k]
            y_cur = robot_locations[k + 1]

            x_goal = goal_locations[k]
            y_goal = goal_locations[k + 1]

            # plug current x, current y, goal x, and goal y into manhattan distance formula, cumulatively adding to sum
            heuristic_sum += abs(x_goal - x_cur) + abs(y_goal - y_cur)

        return heuristic_sum
    
    # function to calculate total euclidean distance from each robot to its goal
    def euclidean_heuristic(self, state):
        robot_locations = state[1:]
        goal_locations = self.goal_locations
        heuristic_sum = 0

        # loops over robot locations in state
        for k in range(0, len(goal_locations) - 1, 2):
            x_cur = robot_locations[k]
            y_cur = robot_locations[k + 1]

            x_goal = goal_locations[k]
            y_goal = goal_locations[k + 1]

            # plug current x, current y, goal x, and goal y into euclidean distance formula, cumulatively adding to sum
            heuristic_sum += math.sqrt((x_goal - x_cur)**2 + (y_goal - y_cur)**2)

        return heuristic_sum

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))
    
    # function that returns a list of all possible next states from a given state
    def get_successors(self, state):
        # update the maze to reflect robot locations of the current state
        self.maze.robotloc = state[1:]

        # store state (a tuple) as a list for east modification of elements
        state = list(state)
        # initalize empty successor list
        successor_list = []
        # initialize empty list of possible next states to be passed to validate_state
        possible_nextstates = []

        # store the number of the robot whose turn it is
        robot_turn_number = state[0]

        # if the robot is the last one, it becomes the 0th robot's turn
        if robot_turn_number == self.num_robots-1:
            next_robot_turn_number = 0
        else:
            # otherwise it is the next robot's turn
            next_robot_turn_number = robot_turn_number + 1

        # set 5 next possible states to current state
        next_state1 = state.copy()
        next_state2 = state.copy()
        next_state3 = state.copy()
        next_state4 = state.copy()
        next_state5 = state.copy()
        
        # set the last integer of next state (which holds the number of the robot whose turn it is) to the number of the next robot in line
        next_state1[0] = next_robot_turn_number
        next_state2[0] = next_robot_turn_number
        next_state3[0] = next_robot_turn_number
        next_state4[0] = next_robot_turn_number
        next_state5[0] = next_robot_turn_number

        # store the position of the x and y coordinates of the robot whose turn it is 
        x_coord = robot_turn_number*2 + 1
        y_coord = robot_turn_number*2 + 2

        # next_state1: robot does not move
        # this state will always be valid, so no need to pass to validate_state
        successor_list.append(tuple(next_state1))

        # next_state2: robot moves N (adjust y coordinate up 1)
        next_state2[y_coord] += 1
        possible_nextstates.append(next_state2) 

        # next_state3: robot moves E (adjust x coordinate up 1)
        next_state3[x_coord] += 1
        possible_nextstates.append(next_state3)

        # next_state4: robot moves W (adjust x coordinate down 1)
        next_state4[x_coord] -= 1
        possible_nextstates.append(next_state4)

        # next_state5: robot moves S (adjust y coordinate down 1)
        next_state5[y_coord] -= 1
        possible_nextstates.append(next_state5)

        # loop over states in possible_nextstates, passing them through validate_state
        for cur_state in possible_nextstates:
            if self.validate_state(cur_state, robot_turn_number, x_coord, y_coord):
                # add states that passed validate_state as tuples to successor_list
                successor_list.append(tuple(cur_state))

        return successor_list

    #TODO: maybe dont use maze here to check if another robot in same location if maze doesnt get updated after each get_succ

    # returns true if the state is possible (no robots out of bounds, on top of each other, on walls, etc), false otherwise
    def validate_state(self, state, robot_turn_number, x_coord, y_coord):
        # if the spot just moved into is a floor
        if Maze.is_floor(self.maze, state[x_coord],state[y_coord]):
            # and there is not another robot on that floor
            if not Maze.has_robot(self.maze, state[x_coord],state[y_coord]):
                return True
        return False

    # returns true if the robot locations of the current state match the goal locations, false otherwise
    def goal_test(self, state):
        # change state and goal locations to a lists instead of tuples for easier comparison
        # discard the first element of the state, which hold the number of the robot whose turn it is
        goal_locations = list(self.goal_locations)
        state = list(state[1:])

        # loop over robot locations in the state, making sure they match robot locations in goal_locations 
        for loc in range(len(goal_locations)):
            if state[loc] != goal_locations[loc]:
                return False
        return True
        
## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((1, 1, 0, 1, 2, 2, 1)))