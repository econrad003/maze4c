"""
mazes.tetris.pentris_generator - generates most the pentomino Python code
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    All of the pentominos are generated.  Comments are generated in
    order to help understand the pentominos.

    Not generated:
        (a) prologue comments (i.e. the main __doc__ information);
        (b) import of the random number generator; and
        (c) epilogue code (routines for extracting sample shapes.

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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.tetris.maze2tile import maze2tile
from mazes.Algorithms.kruskal import Kruskal
from mazes.console_tools import unicode_str as U

S, E, N, W = 'south', 'east', 'north', 'west'

print()
print("n = 5                           # each tile has five cells")
print()
print("    # directions on the 4-connected rectangular grid")
print("S, E, N, W = 'south', 'east', 'north', 'west'")
print()
print("# ---------- SHAPE DEFINITIONS GO HERE ----------")

def leftsquare(grid, m):
    """For the 3x2 mazes"""
    v = [((1,0),E), ((0,0),E), ((0,1),N)]
    index, way = v[m]
    return square(grid, index, way)

def rightsquare(grid, m):
    """For the 3x2 mazes"""
    v = [((1,1),E), ((0,1),E), ((0,2),N)]
    index, way = v[m]
    return square(grid, index, way)

def square(grid, index, way):
    """create base square"""
    maze = Maze(grid)
    for cell in grid:
        if cell[E] and not cell[E].hidden:
            if cell.index != index or way != E:
                maze.link(cell, cell[E])
        if cell[N] and not cell[N].hidden:
            if cell.index != index or way != N:
                maze.link(cell, cell[N])
    return maze

def my_str(maze):
    """display a maze"""
    grid = maze.grid
    for i in range(grid.m):
        for j in range(grid.n):
            cell = grid[i,j]
            if cell.hidden:             # mark the hidden cells
                cell.label = "█"
    return U(maze)

def to_shape(grid, name=None, start=(0,0)):
    """turn a grid into a tile shape"""
    maze = Maze(grid)
    status = Kruskal.on(maze)
    if name:
        s = my_str(maze)
        lines = s.splitlines()
        print()
        print("#   base shape:")
        for line in lines:
            print(f"#           {line}")
        print(f"{name} = list()")
    tile = maze2tile(maze, grid[start])
    shape = tuple(sorted(tile.shape))
    bbox = tile.bbox
    zero = tile.zero
    result = (shape, (bbox[0], bbox[1], zero))
    return result

def maze_to_shape(maze, name=None, start=(0,0), m=0):
    """turn a maze into a tile shape"""
    if name:
        s = my_str(maze)
        lines = s.splitlines()
        if m == 0:
            print()
            print("#   base shape:")
        else:
            print(f"#   move the wall ({m}):")
        for line in lines:
            print(f"#           {line}")
        if m == 0:
            print(f"{name} = list()")
    tile = maze2tile(maze, maze.grid[start])
    shape = tuple(sorted(tile.shape))
    bbox = tile.bbox
    zero = tile.zero
    result = (shape, (bbox[0], bbox[1], zero))
    return result

def display_result(result, name):
    """show the shape"""
    result = str(result)
    result = result.replace("'north'", "N")
    result = result.replace("'south'", "S")
    result = result.replace("'east'", "E")
    result = result.replace("'west'", "W")
    print(f"{name}.append({result})")

def hide(grid):
    """hide all the upper cells"""
    for i in range(1, grid.m):
        for j in range(grid.n):
            cell = grid[i,j]
            cell.hide()

def rot90(grid):
    """rotate this grid counterclockwise"""
    grid2 = OblongGrid(grid.n, grid.m)
    for i in range(grid.m):
        for j in range(grid.n):
            if grid[i,j].hidden:
                h = j
                k = grid.m - i - 1
                grid2[h,k].hide()
    return grid2

def rot_maze(maze):
    """rotate this maze counterclockwise"""
    grid = maze.grid
    grid2 = rot90(grid)
    maze2 = Maze(grid2)
    for cell in grid:
        if cell.hidden:
            continue
        i, j = cell.index
        h = j
        k = grid.m - i - 1
        cell2 = grid2[h,k]
        if cell[E] and cell.is_linked(cell[E]):
            maze2.link(cell2, cell2[N])
        if cell[N] and cell.is_linked(cell[N]):
            maze2.link(cell2, cell2[W])
    # print(maze2)
    return maze2

suffixes = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# longest side = 5

display_result(to_shape(OblongGrid(1,5), name="sA"), "sA")
display_result(to_shape(OblongGrid(5,1)), "sA")

# longest side = 4

p = 1
for j in range(4):
    suffix = suffixes[p]
    name = "s" + suffix
    grid = OblongGrid(2,4)
    hide(grid)
    grid[1,j].reveal()
    display_result(to_shape(grid, name), name)
    for n in range(1,4):
        grid = rot90(grid)
        for j in range(grid.n):
            if not grid[0,j].hidden:
                break
        shape = to_shape(grid, start=(0,j))
        display_result(shape, name)
    p += 1                              # next prefix

# longest side = 3, shortest = 2 (messy!)

j = 0                               # square on right
suffix = suffixes[p]
name = "s" + suffix
for m in range(3):
    grid = OblongGrid(2,3)
    grid[1,j].hide()
    maze = rightsquare(grid, m)
    display_result(maze_to_shape(maze, name, m=m), name)
    for n in range(1,4):
        maze = rot_maze(maze)
        for k in range(maze.grid.n):
            if not maze.grid[0,k].hidden:
                break
        shape = maze_to_shape(maze, start=(0,k))
        display_result(shape, name)
p += 1                              # next prefix

j=1
suffix = suffixes[p]
name = "s" + suffix
grid = OblongGrid(2,3)
grid[1,j].hide()
display_result(to_shape(grid, name), name)
for n in range(1,4):
    grid = rot90(grid)
    for k in range(grid.n):
        if not grid[0,k].hidden:
            break
    shape = to_shape(grid, start=(0,k))
    display_result(shape, name)
p += 1                              # next prefix

j=2                                 # square on left
suffix = suffixes[p]
name = "s" + suffix
for m in range(3):
    grid = OblongGrid(2,3)
    grid[1,j].hide()
    maze = leftsquare(grid, m)
    display_result(maze_to_shape(maze, name, m=m), name)
    for n in range(1,4):
        maze = rot_maze(maze)
        for k in range(maze.grid.n):
            if not maze.grid[0,k].hidden:
                break
        shape = maze_to_shape(maze, start=(0,k))
        display_result(shape, name)
p += 1                              # next prefix


# 3 square (L and T shapes)

for j in range(3):
    suffix = suffixes[p]
    grid = OblongGrid(3,3)
    hide(grid)
    grid[1,j].reveal()
    grid[2,j].reveal()
    name = "s" + suffix
    display_result(to_shape(grid, name), name)
    for n in range(1,4):
        grid = rot90(grid)
        for k in range(grid.n):
            if not grid[0,k].hidden:
                break
        shape = to_shape(grid, start=(0,k))
        display_result(shape, name)
    p += 1                              # next prefix

print()
print("# ---------- SHAPE DEFINITIONS END HERE ----------")

# catalogue the shapes

print()
print("# ---------- LIST ALL THE SHAPE CLASSES ----------")
print()
s = "shape_lists = ["
for i in range(p-1):
    if len(s) > 68:
        s += " \\"
        print(s)
        s = "              "
    s += "s" + suffixes[i] + ", "
if len(s) > 68:
    s += " \\"
    print(s)
    s = "              "
s += "s" + suffixes[p-1] + "]"
print(s)
print()
print("# ---------- CHOOSE YOUR POISON ----------")
print()
