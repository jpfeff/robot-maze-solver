# Modified by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/2/2021

from Maze import Maze
from time import sleep

class SensorlessProblem:

    def __init__(self, maze):
        self.maze = maze
        self.start_state = self.find_start_state(maze)

    def __str__(self):
        string =  "Blind robot problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = self.set_to_tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = self.set_to_tuple(state)
            sleep(1)

            print(str(self.maze))
    
    # converts a set of tuples to a single tuple
    def set_to_tuple(self, state):
        result = []
        # loops over set, appending each item to a list
        for x_y in state:
            result.append(x_y[0])
            result.append(x_y[1])
        # converts the list to a tuple and returns it
        return tuple(result)
    
    # returns a list of all belief states
    def find_start_state(self, maze):
        start_state = set()

        for x in range(maze.width):
            for y in range(maze.height):
                if maze.is_floor(x,y):
                    start_state.add((x,y))
        
        return frozenset(start_state)

    # returns the transition cost from one state to another -- here, always 1
    def get_transition_cost(self, current_state, successor_state):
        return 1
    
    # goal test function; returns true if current state is the goal state (i.e., if there is only one belief state)
    def goal_test(self, state):
        return len(state) == 1
    
    # caculates the heuristic of a state (here, simply the number of belief states remaining)
    def sensorless_heuristic(self, state):
        return len(state)

    # function that returns a list of all possible next states from a given state
    def get_successors(self, state):
        successor_list = []

        # store north as a set, initially the same as the state
        north = set(state.copy())

        # for each belief state in the state
        for belief_state in state:
            # store x and y coordinates of the belief state
            x_coord = belief_state[0]
            y_coord = belief_state[1]
            belief_state_below = False

            # if there is a floor directly above the belief state
            if self.maze.is_floor(x_coord, y_coord+1):
                # turns bool to true if there is a belief state in the column below the belief state we are checking
                for y in range(0, y_coord):
                    if (x_coord,y) not in state:
                        continue
                    else: 
                        belief_state_below = True
                        break

                # if there are no belief states below or there is a wall/out of bounds directly below
                if not belief_state_below or not self.maze.is_floor(x_coord,y_coord - 1):
                    # eliminate belief state
                    north.remove(belief_state)
            
            # if there is a floor directly above any belief state
            if self.maze.is_floor(x_coord, y_coord + 1):
                # that floor now becomes a belief state
                north.add((x_coord, y_coord + 1))
        
        successor_list.append(frozenset(north))

        # store south as a set, initially the same as the state
        south = set(state.copy())
        
        # for each belief state in the state
        for belief_state in state:
            # store x and y coordinates of the belief state
            x_coord = belief_state[0]
            y_coord = belief_state[1]
            belief_state_above = False

            # if there is a floor directly below the belief state
            if self.maze.is_floor(x_coord, y_coord - 1):
                # if the belief state is not on the upper row of the map (avoids out of bounds)
                if y_coord != self.maze.height - 1:
                    # turns bool to true if there is a belief state in the column above the one we are checking
                    for y in range(y_coord + 1, self.maze.height):
                        if (x_coord,y) not in state:
                            continue
                        else: 
                            belief_state_above = True
                            break
                
                # if there are no belief states above or there is a wall/out of bounds directly above
                if not belief_state_above or not self.maze.is_floor(x_coord,y_coord + 1):
                    # eliminate belief state
                    south.remove(belief_state)

            # if there is a floor directly below any belief state
            if self.maze.is_floor(x_coord, y_coord - 1):
                # that floor now becomes a belief state
                south.add((x_coord, y_coord - 1))

        successor_list.append(frozenset(south))

        # store east as a set, initially the same as the state
        east = set(state.copy())

        # for each belief state in the state
        for belief_state in state:
            # store x and y coordinates of the belief state
            x_coord = belief_state[0]
            y_coord = belief_state[1]
            belief_state_left = False

            # if there is a floor directly to the right of the belief state
            if self.maze.is_floor(x_coord + 1, y_coord):
                # turns bool to true if there is a belief state to the left in the row of the one we are checking
                for x in range(0, x_coord):
                    if (x,y_coord) not in state:
                        continue
                    else: 
                        belief_state_left = True
                        break

                # if there are no belief states to the left or there is a wall/out of bounds directly to the left
                if not belief_state_left  or not self.maze.is_floor(x_coord - 1,y_coord):
                    # eliminate belief state
                    east.remove(belief_state)
                    
            # if there is a floor directly to the right of any belief state
            if self.maze.is_floor(x_coord + 1, y_coord):
                # that floor now becomes a belief state
                east.add((x_coord + 1, y_coord))

        successor_list.append(frozenset(east))

        # store west as a set, initially the same as the state
        west = set(state.copy())

        # for each belief state in the state
        for belief_state in state:
            # store x and y coordinates of the belief state
            x_coord = belief_state[0]
            y_coord = belief_state[1]
            belief_state_right = False

            # if there is a floor directly to the left of the belief state
            if self.maze.is_floor(x_coord - 1, y_coord):
                # if the belief state is not on the rightmost column of the map (avoids out of bounds)
                if x_coord != self.maze.width - 1:
                    # turns bool to true if there is a belief state to the right in the row of the one we are checking
                    for x in range(x_coord + 1, self.maze.width):
                        if (x,y_coord) not in state:
                            continue
                        else: 
                            belief_state_right = True
                            break

                # if there are no belief states to the right or there is a wall/out of bounds directly to the right
                if not belief_state_right  or not self.maze.is_floor(x_coord + 1,y_coord):
                    # eliminate belief state
                    west.remove(belief_state)

            # if there is a floor directly to the left of any belief state
            if self.maze.is_floor(x_coord - 1, y_coord):
                # that floor now becomes a belief state
                west.add((x_coord - 1, y_coord))

        successor_list.append(frozenset(west))

        return successor_list    
                        

## A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
    print(test_problem.get_successors(test_problem.start_state))

