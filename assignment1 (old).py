import heapq


# Name this file to assignment1.py when you submit

class Node:
  def __init__(self,r,c,char):
    if(char.isdigit()):
      self.value = int(char)
    else:
      self.value = 0
    self.position = (r,c)
    self.adjacency_list = []
    self.char = char
    self.is_visited = False
    self.parent = None

  def __str__(self):
    return f"{self.char} {self.position}, {self.value}"
  
  def get_neighbors_text(self):
    neighbors = []
    neighbors.append(self.char)
    for v in self.adjacency_list:
      neighbors.append(v.__str__())
    return neighbors

  def connect_with(self, other_node):
    # do not connect the nodes if one of them is a wall
    self.adjacency_list.append(other_node)
    other_node.adjacency_list.append(self)

def create_nodes(grid):
  m = len(grid) # number of rows
  n = len(grid[0]) # number of cols
  node_list = []
  for r in range(m):
    row = []
    for c in range(n):
      node = Node(r,c,grid[r][c])
      print(node)
      row.append(node)
    node_list.append(row)
  
  return node_list

# The pathfinding function must implement A* search to find the goal state
def pathfinding(filepath):
  # filepath is the path to a CSV file containing a grid 

  # optimal_path is a list of coordinate of squares visited (in order)
  # optimal_path_cost is the cost of the optimal path
  # num_states_explored is the number of states explored during A* search

  
  
  grid = construct_grid(filepath)
  node_list = create_nodes(grid=grid)
  #connect the each node to the one to the right of it and the one below it (if the node is not a wall)
  m = len(grid) # number of rows
  n = len(grid[0]) # number of cols
  for r in range(m-1):
    for c in range(n-1):
      node_list[r][c].connect_with(node_list[r][c+1])
      node_list[r][c].connect_with(node_list[r+1][c])

  for r in range(m):
    for c in range(n):
      print(node_list[r][c].get_neighbors_text())
  #return optimal_path, optimal_path_cost, num_states_explored


def construct_grid(filepath):
  grid = []
  with open(filepath) as file:
    for line in file:
      line = line.replace("\n", "")
      line_characters = line.split(",")
      grid.append(line_characters)

  return grid

def graph_search(graph, start_states, goal_states):
  frontier = start_states
  explored = []
  while True:
    if frontier == []:
      return False
    leaf = heapq.heappop(frontier)[1]
    if leaf in goal_states:
      return leaf 
    
    explored.append(leaf)
    for node in leaf.adjacency_list:
      curr_path_cost = leaf.path_cost + 1 ################
      if ((node not in frontier and node not in explored)
          or (node in frontier and curr_path_cost<node.pathcost)):
        node.parent = leaf
        node.path_cost = curr_path_cost
        frontier.headpush(f, node)
    
def recover_path(final_node):
  # check if start is always None
  path = []
  node = final_node
  while (node.parent != None):
    path.insert(0,node)
    node = node.parent
  path.insert(0,node)
  return path
    
  

# fp =r'C:\Users\adamm\OneDrive\Desktop\Year 4\COMP 3106\ass1\Examples\Example0\grid.txt'
fp ='grid-ex0.txt'
pathfinding(filepath=fp)