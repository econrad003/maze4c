"""
mazes.tetris.maze2tile - given a maze, create a tile
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

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
from mazes import Cell
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.tetris.tile import Tile

def WarningHandler(warning:bool, msg:str):
    if warning:
        print("Warning:", msg)
        print("         proceeding anyway") 
    else:
        raise Warning(msg)

def maze2tile(maze:Maze, start:Cell,
              bbox=None, zero=None, warning=False) -> Tile:
    """create a tile from a maze"""
    warning = bool(warning)
    grid = maze.grid
    if isinstance(grid, OblongGrid):
        if bbox == None:
            bbox = (grid.m, grid.n)
        else:
            msg = "bbox should not be supplied for a rectangular grid"
            WarningHandler(warning, msg)
        if zero == None:
            i, j = start.index
            zero = j
            if i != 0:
                msg = "start cell should be in th bottom row"
                WarningHandler(warning, msg)
        else:
            msg = "zero should not be supplied for a rectangular grid"
            WarningHandler(warning, msg)

    reachable = {}              # cells that can be reached from start
    vector = (-1, None, start)
    stack = [vector]            # depth-first search
    n = -1                      # cell number
    while stack:
        prev, way, cell = stack.pop()
        if cell in reachable:
            continue            # already processed
        n += 1
        reachable[cell] = (prev, way, n)
        for way in cell.ways:
            nbr = cell[way]
            if nbr in reachable:
                continue        # already processed
            if cell.is_linked(nbr):
                vector = (n, way, nbr)
                stack.append(vector)
    del reachable[start]
    shape = sorted(reachable.values())
    # print(shape)
    return Tile(n+1, shape, bbox=bbox, zero=zero)

if __name__ == "__main__":
    import os
    print(f"Simple test of {os.path.basename(__file__)}:")
    print("Creating T maze")
    maze = Maze(OblongGrid(2, 3))
    start = maze.grid[0,1]
    maze.link(start, start.north)
    maze.link(start.north, start.north.east)
    maze.link(start.north, start.north.west)
    start.label = start.north.label = start.north.east.label = start.north.west.label = "T"
    print("T maze:")
    print(maze)
    print("Creating T tile")
    tile = maze2tile(maze, start)
    print("If this is working, you should see the description of a T tile:")
    print("  shape:", tile.shape)
    print("   bbox:", tile.bbox, "\t-- (2 rows, 3 columns)")
    print("   zero:", tile.zero, "\t\t-- (column 1 of bottom row)")
    assert tile.bbox == (2, 3)
    assert tile.zero == 1
    v1 = (0, "north", 1)
    v2 = (1, "west", 2)
    v3 = (1, "east", 3)
    v4 = (1, "east", 2)
    v5 = (1, "west", 3)
    assert tile.shape in [{v1, v2, v3}, {v1, v4, v5}]
    print("SUCCESS!")
