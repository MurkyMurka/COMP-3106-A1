# Name this file to assignment1.py when you submit
import math, heapq, itertools

# constants for grid
START_SQUARE = 'S'
GOAL_SQUARE = 'G'
WALL_SQUARE = 'X'
GOAL_COINS = 5

class State_Node:
  def __init__(self, grid, curr_row, curr_col, coin_locations, collected_coins, goal_locations, parent_state_node=None):
    self.grid                   = grid              # accessible by [row][col]
    self.curr_row               = curr_row          # current row position
    self.curr_col               = curr_col          # current column position
    self.coin_locations         = coin_locations    # list of all coin positions as (row, col)
    self.collected_coins        = collected_coins   # list of collected coins positions as (row, col)
    self.goal_locations         = goal_locations    # list of all goal positions as (row, col)
    self.parent_state_node      = parent_state_node # parent state node

    self.neighbour_state_nodes  = []                # list of neighbour state nodes; to be determined

  def __str__(self):
    # format: "Pos:(row col), Coins:[(r1,c1),(r2,c2)...] (Total:n), Parent:parent_state_node"
    return f"Pos:({self.curr_row} {self.curr_col}), Coins:{self.collected_coins} (Total:{self.get_num_coins()}), Parent:{self.parent_state_node}"
  
  def get_num_coins(self):
    # returns the number of coins collected so far
    num_coins = 0
    for coin in self.collected_coins:
      num_coins += int(self.grid[coin[0]][coin[1]])
    return num_coins

  def is_goal_state(self):
    # returns true if is a goal state, false otherwise
    if self.grid[self.curr_row][self.curr_col] == GOAL_SQUARE and self.get_num_coins() >= GOAL_COINS:
      return True
    else:
      return False
    
  def update_coins(self):
    # update the coin list if current position has a coin
    if (self.curr_row, self.curr_col) in self.coin_locations and (self.curr_row, self.curr_col) not in self.collected_coins:
      self.collected_coins.append((self.curr_row, self.curr_col))

  def get_neighbour_states(self):
    # create one neighbour state for each adjacent square
    neighbours = []
    directions = [(-1,0), (1,0), (0,1), (0,-1)]
    for dr, dc in directions:
      nr, nc = self.curr_row + dr, self.curr_col + dc
      if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
        if self.grid[nr][nc] != WALL_SQUARE:
          # copy collected coins so far
          new_collected = self.collected_coins[:]
          neighbour = State_Node(self.grid, nr, nc, self.coin_locations, new_collected, self.goal_locations, self)
          neighbour.update_coins()
          neighbours.append(neighbour)
    self.neighbour_state_nodes = neighbours
    return neighbours

def calcH(node, goals):
  # calculation for heuristic using the minimum Euclidean distance to any goal
  return min(
    math.sqrt((node.curr_row - gr)**2 + (node.curr_col - gc)**2)
    for gr, gc in goals
  )

def priority(g, thisPos,goalPos):
  # calculation for priority function f(n) = g(n) + h(n)
  return g + calcH(thisPos, goalPos)

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  # filepath is the path to a CSV file containing a grid 
  # finds the optimal path using A* search

  def construct_grid(filepath):
    # construct a 2D array (list of lists) to represent the grid
    grid = []
    with open(filepath) as file:
      for line in file:
        row = line.strip().split(",")
        grid.append(row)
    return grid
  
  def start_search(grid):
    # performs the search for the optimal path
    # assumes that exactly one Start square exists, and at least one Goal square exists
    # returns optimal path, optimal path cost, number of states explored

    # find goals and coin positions as [row][col]
    goal_squares = []
    coin_squares = []
    for r in range(len(grid)):
      for c in range(len(grid[0])):
        if grid[r][c] == START_SQUARE:
          start_r = r
          start_c = c
        if grid[r][c] == GOAL_SQUARE:
          goal_squares.append((r,c))
        if grid[r][c].isdigit() and int(grid[r][c]) > 0:
          coin_squares.append((r,c))

    # build start node
    start_node = State_Node(grid, start_r, start_c, coin_squares, [], goal_squares)

    # A* search
    counter = itertools.count()  # used to break ties in heapq
    frontier = []
    explored = set()  # explored set of signatures

    # initial state signature
    start_sig = (start_node.curr_row, start_node.curr_col, tuple(sorted(start_node.collected_coins)))
    heapq.heappush(frontier, (0, next(counter), start_node))
    g_score = {start_sig: 0}
    num_states_explored = 0

    while frontier:
      _, _, current = heapq.heappop(frontier)
      sig = (current.curr_row, current.curr_col, tuple(sorted(current.collected_coins)))

      # skip if current state has already been explored
      if sig in explored:
        continue

      # mark as current state explored
      explored.add(sig)
      num_states_explored += 1

      # goal state is found
      if current.is_goal_state():
        # reconstruct path
        # return path as list of (row, col) tuples, path cost, number of states explored
        path = []
        node = current
        while node is not None:
          path.append((node.curr_row, node.curr_col))
          node = node.parent_state_node
        path.reverse()
        return path, g_score[sig], num_states_explored

      # explore neighbours
      for neighbour in current.get_neighbour_states():
        neighbour_sig = (neighbour.curr_row, neighbour.curr_col, tuple(sorted(neighbour.collected_coins)))
        tentative_g = g_score[sig] + 1

        # only add neighbour to frontier if it's not explored or has a better g_score
        if neighbour_sig not in explored and (neighbour_sig not in g_score or tentative_g < g_score[neighbour_sig]):
          g_score[neighbour_sig] = tentative_g
          f = tentative_g + calcH(neighbour, goal_squares)
          heapq.heappush(frontier, (f, next(counter), neighbour))

  grid = construct_grid(filepath)
  return start_search(grid)

fp = 'grid.txt'
print(pathfinding(filepath=fp))