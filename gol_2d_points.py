# Game of Life 2D method
# Copyright (C) 2024 Yan Peng <pydeoxy@gmail.com>

# This code is for a GhPython Script component in Grasshopper with Rhino 7.
# To use this code, just copy the whole content into a GhPython Script component,
# and to change the INPUTs and OUTPUTs according to the Args and Returns.
# Or, just use the gol_2d_points_example.gh file. 

# This file is to generate a group of 2d x*y array of 0s and 1s,
# representing the generations of dead and living cells based on the rules of Conway's Game of Life.
# The first 2d array is the starting generation.
# The total number of generations is z.
# The output is converted into a single string, to be solved to match with Hops data structure.

"""
Conway's Game of Life.
    Rules:
    1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    2. Any live cell with two or three live neighbors lives on to the next generation.
    3. Any live cell with more than three live neighbors dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

Args:
    x: The number of rows in the 2D array.
    y: The number of columns in the 2D array.
    z: The number of generations developed.
    n1: The total number of 1s in the first generation.    
    seed: seed of random to generate the 1s in the first generation.

Returns:
    status: 0s and 1s showing the status of each cell.
    status of all generations are recorded.
    
"""

__author__ = "yan.peng"
__version__ = "2024.02.25"

ghenv.Component.Name = "gol_2d"
ghenv.Component.NickName = 'game_of_life_2d'

import rhinoscriptsyntax as rs
import random
import ghpythonlib.treehelpers as th

def create_array(x, y, n, seed=None):
  """
  Creates a 2D x * y array with values 0 or 1, where the total number of 1s is n.
  """
  if seed is not None:
    random.seed(seed)
  if n > x*y:
    raise ValueError('n must be smaller than x*y')

  # Create an empty array
  array = [[0 for _ in range(y)] for _ in range(x)]

  # Fill the array with 1s randomly until n 1s are placed
  count = 0
  while count < n:
    i = random.randint(0, x - 1)
    j = random.randint(0, y - 1)
    if array[i][j] == 0:
      array[i][j] = 1
      count += 1

  return array
  
def add_zeros_around(array):
  """
  Adds 0s around a given 2D array.
  """

  # Get the dimensions of the input array
  x, y = len(array), len(array[0])

  # Create a new array with 0s around the input array
  new_array = [[0 for _ in range(y + 2)] for _ in range(x + 2)]

  # Copy the input array into the center of the new array
  for i in range(x):
    for j in range(y):
      new_array[i + 1][j + 1] = array[i][j]

  return new_array

def extract_sub_array(array, i, j):
  """
  Extracts a 3x3 sub-array from the given array at index (i, j).  
  """

  # Check if the given index is on the edge
  x, y = len(array), len(array[0])
  if i * j == 0 or (x-1-i) * (y-1-j) == 0:
    extend = add_zeros_around(array)
    sub_array = [
      row[j  : j + 3] for row in extend[i  : i + 3]
    ]
  else:
    sub_array = [
      row[j - 1 : j + 2] for row in array[i - 1 : i + 2]
    ]

  return sub_array

def cell_next_generation(array,i,j):
  """
  Calculate the cell's value of next generation from the given array at index (i, j).
  """

  # Get the sub-array with neighbors
  sub = extract_sub_array(array, i, j)

  sum_arr = sum(sum(row) for row in sub)
  neighbors = sum_arr-array[i][j]

  if array[i][j] == 1:
    if neighbors < 2:
      return 0
    elif 2 <= neighbors <= 3:
      return 1
    else:
      return 0
  else:
    if neighbors == 3:
      return 1
    else:
      return 0
      
def next_generation(array):
  """
  Calculate the array's value of next generation based on the rules from Conway's Game of Life.
  """
  new_arr = [[0 for _ in range(len(array[0]))] for _ in range(len(array))]

  for i in range(len(array)):
    for j in range(len(array[0])):
      new_arr[i][j] = cell_next_generation(array,i,j)

  return new_arr

def generations(array,n):
  """
  Calculate the array's value for the next n generations based on the rules from Conway's Game of Life.
  """
  generations = [array]  
  if n < 1:
    raise Exception("n must be at least 1")
  elif n > 1:
    for i in range(1,n):
      arr_i = next_generation(generations[i-1])      
      generations.append(arr_i)      
  return generations

def generations_str(gens):
    """
    String the status of generations for easier view.
    """
    gens_str = []
    for gen in gens:
        gen_str = []
        for row in gen:
            row_str = ''
            for item in row:
                row_str += str(item)
            gen_str.append(row_str) 
        # reverse the list to match with points coordinations
        gen_str.reverse()
        gens_str.append(gen_str) 
    return gens_str
  
def gen_points(gens):
    """
    Generate points based on the status of generations.
    """
    points0 = []
    points1 = []
    for k in range(len(gens)):
        points0_gen = []
        points1_gen = []
        for j in range(len(gens[k])):
            for i in range(len(gens[k][j])):            
                point = rs.CreatePoint(i,j,k)
                if gens[k][j][i] == 0:
                    points0_gen.append(point)
                else:
                    points1_gen.append(point)      
        points0.append(points0_gen)
        points1.append(points1_gen)

    return (points0,points1)

# Main function to generate outputs

arr = create_array(x, y, n1,seed)
gens = generations(arr,z)
all_points = gen_points(gens)

status = th.list_to_tree(gens)
status_str = th.list_to_tree(generations_str(gens))
points0 = th.list_to_tree(all_points[0])
points1 = th.list_to_tree(all_points[1])
