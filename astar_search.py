# Modified by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# 10/2/2021

from SearchSolution import SearchSolution
from heapq import heapify, heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0, f=0):
        # variables to hold state, parent, heuristic, transition cost, and f(=heuristic+transition cost)
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.transition_cost = transition_cost
        self.f = f

        # used to mark a node as removed from the priority queue
        self.removed = False

    def priority(self):
        # priority is lowest f = cost + heuristic
        return self.f

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()

# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        # if backchaining in a SensorlessProblem, convert from frozenset to set before adding to path
        if isinstance(current.state,frozenset):
            set_state = set(current.state)
            result.append(set_state)
        else:
            result.append(current.state)
        current = current.parent

    result.reverse()
    return result

def astar_search(search_problem, heuristic_fn):
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # store state and cheapest cost to visit
    visited_cost = {}
    visited_cost[start_node.state] = 0

    # while the priority queue is not empty
    while pqueue:
        # pop the node with the smallest f value off the priority queue
        current_node = heappop(pqueue)

        # until it finds a node that has not been marked as removed, keep trying to get a new one
        while current_node.removed:
            current_node = heappop(pqueue)

        # increment nodes visited to be returned in the solution
        solution.nodes_visited += 1

        # store the path and return the solution
        if search_problem.goal_test(current_node.state):
            solution.path = backchain(current_node)
            solution.cost = visited_cost[current_node.state] + current_node.transition_cost
            return solution

        # store its successors
        successors = search_problem.get_successors(current_node.state)

        for successor_state in successors:
            # get the transition cost (calculated differently depending on the search problem)
            transition_cost = search_problem.get_transition_cost(current_node.state, successor_state)
            
            # store the path cost to the successor
            cost_to_successor = visited_cost[current_node.state] + transition_cost

            # store the heuristic of the successor node
            heuristic = heuristic_fn(successor_state)

            # f = cumulative cost to node + heuristic of the node
            f = cost_to_successor + heuristic

            # pack successor attributes into a node
            successor_node = AstarNode(successor_state, heuristic, current_node, transition_cost, f)

            # if node has not been visited
            if successor_state not in visited_cost:
                # store the cost to visit it
                visited_cost[successor_state] = cost_to_successor
                # add it to the priority queue
                heappush(pqueue, successor_node)
                heapify(pqueue)

            else:
                # store the current cheapest path to the successor node
                current_cost = visited_cost[successor_state]
                # if the new cost is lower than the current cost
                if cost_to_successor < current_cost:
                    # replace the current cost with the new one
                    visited_cost[successor_state] = cost_to_successor
                    # find the index of the old successor node entry in the priority queue
                    index_in_pqueue = get_index(successor_node, pqueue)
                    # if the entry was found
                    if index_in_pqueue != None: 
                        # mark it as removed
                        pqueue[index_in_pqueue].removed = True
                    # add the new successor node to the priority queue
                    heappush(pqueue, successor_node)
                    heapify(pqueue)
    
    return solution

def get_index(node, pqueue):
    # loop over the priority queue
    for k in range(len(pqueue)):
        # if the state matches the parameter, return that index
        if pqueue[k].state == node.state:
            return k
    return None



        
        
