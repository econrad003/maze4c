"""
demos.minweight - Prim's algorithm and minimum weight spanning trees
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

LICENSE
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from mazes import rng
from mazes.AGT.primic import primic, init_maze

# a 3x5 oblong grid has how many edges?
#   Each cell has 2, 3 or 4 neighbors.  There are 15 cells
#   The interior cells form a 1x3 grid      3 cells x 4 neighbors = 12 arcs
#   There are four corner cells...          4 cells x 2 neighbors =  8 arcs
#   There are 8 more cells...               8 cells x 3 neighbors = 24 arcs
#                                          ========                 =======
#                                          15 cells                 44 arcs
#   Each edge is two arcs                                           22 edges

# 2**22-1 == 4194303 -- the largest 23 digit binary number, not a problem!

m, n = 3, 5                     # dimensions
e = 22                          # number of grid edges

# Under the scheme that follows, there is a bijection from the the numbers
# from 0 through 2**22-1 into the set of simple mazes. 0 is the maze with
# no passages and 2**22-1 is the complete maze (with a passage along every
# grid edge. Not all these mazes are trees.  If we know the weight of the
# the maze and we know the weight matrix, then the binary representation
# of the weight is enough to recover the maze.

# For example, suppose the weight is 39.  In binary, we have:
#       39 = 32 + 4 + 2 + 1 or 100,111 in binary notation.
# That tells us that the maze contains the edges with weights 32, 4, 2 and 1.

# In a recent run, Prim's algorithm return a maze with weight 102,399. Since
# there are 15 cells, there should be 14 edges.  Let's find the weights:
#       N           Even or Odd?            N/2         Edge Weight
#   102,399             1                 51,199            1           1
#    51,199             1                 25,599            2           2
#    25,599             1                 12,799            4           3
#    12,799             1                  6,399            8           4
#     6,399             1                  3,199           16           5
#     3,199             1                  1,599           32           6
#     1,599             1                    799           64           7
#       799             1                    399          128           8
#       399             1                    199          256           9
#       199             1                     99          512          10
#        99             1                     49         1024          11
#        49             1                     24         2048          12
#        24             0                     12        (4096)
#        12             0                      6        (8192)
#         6             0                      3       (16384)
#         3             1                      1        32768          13
#         1             1                      0        65536          14
#
# The weights of the 12 smallest edges sum to 4096-1=4095.  Adding this to
# the two remaining edges, we have:
#       65,536 + 32,768 + 4095 = 102,399.
# In binary, reading up:
#		11,000,111,111,111,111
#
# In another run, Prim found a spanning tree of weight 45055.  I leave it
# as an exercise to find the weights of the edges in that spanning tree.
# (There should be exactly 14 edges.)
#
# And finally, using this weighting scheme, the smallest possible weight
# of a tree is 16383.  Your task is to exaplain why that's true.
#
# Incidentally, I haven't implemented Kruskal's algorithm yet...
# (Time now: 20:40 [8:40 PM] 2 December 2024 US-EST.)
# But Kruskal's algorithm will give the same values as a correct
# implementation of Prim's algorithm.

weights = list()
weights.append(1)
for i in range(e-1):
    weights.append(weights[-1]*2)
#print(weights)
rng.shuffle(weights)

    # symmetric weight matrix
w = 0
W = {}
maze = init_maze(3, 5)
for cell in maze.grid:
    for nbr in cell.neighbors:
        pair1 = (cell.index, nbr.index)
        if pair1 in W:
            continue            # already processed
        pair2 = (nbr.index, cell.index)
        W[pair1] = W[pair2] = weights[w]
        # print(pair1, w)
        w += 1
assert w == e

def weight(cell1, cell2):
    """determine the weight of an edge"""
    index1 = cell1.index
    index2 = cell2.index
    return W[index1, index2]

def net_weight(maze):
    """determine the weight of the maze"""
    net = 0
    for join in maze:
        cell1, cell2 = join
        net += weight(cell1, cell2)
    return net

        # Time to create some mazes
results = {}

print("Prim's algorithm using the given weights...")
prim_maze = maze
grid = maze.grid
pr_map = {}
for key in W:
    cell1 = grid[key[0]]
    cell2 = grid[key[1]]
    pr_map[frozenset([cell1, cell2])] = W[key]
status = primic(prim_maze, pr_map=pr_map, cache=False)
#print(status)
print(maze)
winner = ("Prim", net_weight(prim_maze))
print(winner)
    # if it's a tree, then #{edges} + 1 = #{vertices}
assert len(maze) == len(maze.grid) - 1

maze = init_maze(m, n)
status = primic(maze)
loser = ("ArcPrim/cache", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

pr_map = {}
maze = init_maze(m, n)
for cell in maze.grid:
    pr_map[cell] = rng.random()
status = primic(maze, pr_map=pr_map)
loser = ("VertexPrim/arc", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.VGT.vprim import vprim
maze = init_maze(m, n)
status = vprim(maze)
loser = ("VertexPrim/cell", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.VGT.sprim import sprim
maze = init_maze(m, n)
status = sprim(maze)
loser = ("SimplifiedPrim/cell", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.Algorithms.simple_binary_tree import BinaryTree
maze = init_maze(m, n)
status = BinaryTree.on(maze)
loser = ("BinaryTree/EN", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

maze = init_maze(m, n)
status = BinaryTree.on(maze, onward="north", upward="east")
loser = ("BinaryTree/NE", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

maze = init_maze(m, n)
status = BinaryTree.on(maze, onward="south", upward="west")
loser = ("BinaryTree/SW", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.Algorithms.sidewinder import Sidewinder
maze = init_maze(m, n)
status = Sidewinder.on(maze)
loser = ("Sidewinder/EN", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

maze = init_maze(m, n)
status = Sidewinder.on(maze, onward="north", upward="east")
loser = ("Sidewinder/NE", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

maze = init_maze(m, n)
status = Sidewinder.on(maze, onward="south", upward="west")
loser = ("Sidewinder/SW", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.Algorithms.inwinder import Inwinder
maze = init_maze(m, n)
status = Inwinder.on(maze)
loser = ("Inwinder", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.Algorithms.dfs import DFS
maze = init_maze(m, n)
status = DFS.on(maze)
loser = ("DFS/naive", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

from mazes.Algorithms.dfs_better import DFS
maze = init_maze(m, n)
status = DFS.on(maze)
loser = ("DFS", net_weight(maze))
print(loser)
assert len(maze) == len(maze.grid) - 1
assert loser[1] >= winner[1]

#################################################################
# All that follows was added after 20:40 2 December 2024 US-EST #
#################################################################

# end module demos.minweight