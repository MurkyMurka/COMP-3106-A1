# Name this file to assignment1.py when you submit

"""
assignment1.py
By Adam, Mark, and Nico.

Performs A* search on a configured filepath to a CSV grid.
Assumes there are:
    exactly one start square,
    at least one goal square,
    at least 0 wall squares,
    at least 0 regular squares
and that regular squares are represented by an integer <= 0
"""

import math, heapq, itertools

START_SQUARE = 'S'
GOAL_SQUARE = 'G'
WALL_SQUARE = 'X'
GOAL_TREASURES = 5

class StateNode:
    # represents a state, with pointers to parent and neighbours
    def __init__(self, grid, row, col, treasure_locations, collected_treasures, goal_locations, parent=None, g=0):
        self.grid = grid
        self.row = row
        self.col = col
        self.treasure_locations = treasure_locations
        self.collected_treasures = collected_treasures[:]
        self.goal_locations = goal_locations
        self.parent = parent
        self.g = g

    def get_num_treasures(self):
        # returns the total value of treasures collected in this state
        return sum(int(self.grid[r][c]) for r, c in self.collected_treasures)

    def is_goal(self):
        # returns true if state has enough treasures and is on a goal square
        return self.grid[self.row][self.col] == GOAL_SQUARE and self.get_num_treasures() >= GOAL_TREASURES

    def update_treasures(self):
        # update treasures in case this state finds itself on a treasure
        if (self.row, self.col) in self.treasure_locations and (self.row, self.col) not in self.collected_treasures:
            self.collected_treasures.append((self.row, self.col))

    def get_neighbours(self):
        # find and returns the neighbours given that they are in bound and not walls
        neighbours = []
        # check each direction
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = self.row + dr, self.col + dc
            if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
                if self.grid[nr][nc] != WALL_SQUARE:
                    neighbour = StateNode(self.grid, nr, nc, self.treasure_locations, self.collected_treasures, self.goal_locations, parent=self, g=self.g+1)
                    neighbour.update_treasures()
                    neighbours.append(neighbour)
        return neighbours

def heuristic(node, goals):
    # use Euclidean distance from nearest goal
    return min(math.sqrt((node.row - gr)**2 + (node.col - gc)**2) for gr, gc in goals)

def same_state(n1, n2):
    # return True if two nodes are at the same position with the same collected treasures
    return n1.row == n2.row and n1.col == n2.col and sorted(n1.collected_treasures) == sorted(n2.collected_treasures)

def pathfinding(filepath):
    # read grid and parse into [row][column] 2D list
    grid = [line.strip().split(",") for line in open(filepath)]
    
    # find start squares, goal square(s), treasure square(s)
    goals = []
    treasures = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == START_SQUARE:
                start_row, start_col = r, c
            if grid[r][c] == GOAL_SQUARE:
                goals.append((r,c))
            if grid[r][c].isdigit() and int(grid[r][c]) > 0:
                treasures.append((r,c))

    # commence the A* search
    start_node = StateNode(grid, start_row, start_col, treasures, [], goals)
    frontier = []
    counter = itertools.count() # used as tiebreaker of equal priority states
    heapq.heappush(frontier, (heuristic(start_node, goals), next(counter), start_node))
    explored = []
    num_explored = 0

    while frontier:
        # pop current state
        _, _, current = heapq.heappop(frontier)

        # skip explored states
        if any(same_state(current, node) for node in explored):
            continue

        # mark state as explored
        explored.append(current)
        num_explored += 1

        # check if state is a goal
        if current.is_goal():
            # rebuild path and return
            path = []
            node = current
            while node:
                path.append((node.row, node.col))
                node = node.parent
            path.reverse()
            return path, current.g, num_explored

        # add neighbours to frontier
        for neighbour in current.get_neighbours():
            heapq.heappush(frontier, (neighbour.g + heuristic(neighbour, goals), next(counter), neighbour))
    
    # if the code gets here, it means that no solution could be found :(
    return None

# USER: change value of fp to match grid filepath
fp = "grid.txt"
# print the (1) optimal path, (2) cost of optimal path, (3) number of states explored
toPrint = pathfinding(fp)
for line in toPrint:
    print(line)