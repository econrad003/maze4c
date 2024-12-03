"""
demos.arcPrim_isnt_prim - demonstrate that arc Prim is not a minimum weight
    spanning tree algorithm
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

from mazes.AGT.primic import primic, init_maze

def make_weights1(maze=None):
    indices = [(0,0), (0,1), (1,0), (1,1)]
    cells = list(maze.grid[index] for index in indices) \
        if maze!=None else ['A', 'B', 'C', 'D']
    A, B, C, D = cells
    w = {}
    w[A,B] = 1
    w[B,A] = 100
    w[frozenset([A,C])] = 10
    w[frozenset([B,D])] = 20
    w[frozenset([C,D])] = 40
    return w

def make_weights2(maze=None):
    indices = [(0,0), (0,1), (1,0), (1,1)]
    cells = list(maze.grid[index] for index in indices) \
        if maze!=None else ['A', 'B', 'C', 'D']
    A, B, C, D = cells
    w = {}
    w[frozenset([A,B])] = 1
    w[frozenset([A,C])] = 10
    w[frozenset([B,D])] = 20
    w[frozenset([C,D])] = 40
    return w

def make_weights3(maze=None):
    indices = [(0,0), (0,1), (1,0), (1,1)]
    cells = list(maze.grid[index] for index in indices) \
        if maze!=None else ['A', 'B', 'C', 'D']
    A, B, C, D = cells
    w = {}
    w[frozenset([A,B])] = 100
    w[frozenset([A,C])] = 10
    w[frozenset([B,D])] = 20
    w[frozenset([C,D])] = 40
    return w

def demo1(start, maker):
    """a 2x2 demo showing that arcPrim depends on the start location"""
    maze = init_maze(2, 2)
    grid = maze.grid
    cell1, cell2, cell3, cell4 = grid[0,0], grid[0,1], grid[1,0],  grid[1,1]
    cell1.label, cell2.label, cell3.label, cell4.label = 'A', 'B', 'C', 'D'
    w = maker(maze)
    cell0  = cell1 if start == 1 else cell2
    print(f"Starting in {cell0.char}:")
    status = primic(maze, start_cell=cell0, pr_map=w)
    # print(status)
    print(maze)

def display_weights(maker):
    w = maker(None)
    s = ""
    for key in w:
        b1, b2 = ('{', '}') if type(key) == frozenset else ('(', ')')
        a1, a2 = list(key)
        s += b1 + a1 + ',' + a2 + b2
        s += "->" + str(w[key]) + ", "
    s = s[:-2]
    print("weights =", s)

print("     ", "="*10, "ArcPrim", "="*10)
display_weights(make_weights1)
print("If we start in A, we must take AB(1), AC(10), BD(20) in that order.",
    "Total 31")
demo1(1, make_weights1)
print("If we start in B, we must take BD(20), DC(40), CA(10) in that order.",
    "Total 70")
demo1(2, make_weights1)
print("The choice of starting cell matters in arcPrim, but not in Prim.")

print()
print("     ", "="*10, "Prim (Edge Weights)", "="*10)
display_weights(make_weights2)
print("If we start in A, we must take AB(1), AC(10), BD(20) in that order.",
    "Total 31")
demo1(1, make_weights2)
print("If we start in B, we must take BA(1), AC(10), BD(20) in that order.",
    "Total 31")
demo1(2, make_weights2)

print()
print("     ", "="*10, "Prim (Edge Weights)", "="*10)
display_weights(make_weights3)
print("If we start in A, we must take AC(10), CD(30), DB(20) in that order.",
    "Total 70")
demo1(1, make_weights3)
print("If we start in B, we must take BD(20), DC(40), CA(10) in that order.",
    "Total 70")
demo1(2, make_weights3)

print()
print("We can get different mazes with Prim,",
      "but we always get the same total weight.")

# end module demos.arcPrim_isnt_Prim