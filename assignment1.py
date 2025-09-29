# Name this file to assignment1.py when you submit

# constants for grid
GOAL_SQUARE = 'G'

class State_Node:
  def __init__(self, grid, row_pos, col_pos, num_coins, cur_square):
    self.grid = grid # need to figure out how to store this; coins?
    self.row_pos = row_pos
    self.col_pos = col_pos
    self.num_coins = num_coins
    self.cur_square = cur_square
    self.parent_state_node = None
    self.neighbour_state_nodes = []

  def __str__(self):
    return f"Pos:({self.row_pos} {self.col_pos}), Coins:{self.num_coins}, Square:{self.cur_square}, Parent:{self.parent_state_node}"
  
  def is_goal_state(self):
    if self.cur_square == GOAL_SQUARE:
      return True
    else:
      return False
    
  def create_neighbour_states(self, grid):
    # create one neightbour state for each adjacent square

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  # filepath is the path to a CSV file containing a grid 

  def construct_grid(filepath):
    grid = []
    with open(filepath) as file:
      for line in file:
        line = line.replace("\n", "")
        line_characters = line.split(",")
        grid.append(line_characters)

    return grid

  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search
  return optimal_path, optimal_path_cost, num_states_explored