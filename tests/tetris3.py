"""
tests.tetris3 - simple test of tetris drops (all configurations)
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
from mazes import rng, Cell
from mazes.maze import Maze
from mazes.console_tools import unicode_str
from mazes.Grids.oblong import OblongGrid
from mazes.tetris.tile import Tile
from mazes.tetris.tetris import configs, create_tile

rows, cols = 8, 15
maze = Maze(OblongGrid(8, 15))
grid = maze.grid
all_shapes = list(configs)

columns = list()
for j in range(cols):
    placements = list()
    for i in range(rows-1, -1, -1):
        cell = grid[i,j]
        assert isinstance(cell, Cell), f"{(i,j)}" 
        placements.append(cell)
    columns.append(tuple(placements))

occupied = set()
c = 0
while len(all_shapes) > 0:
    s = rng.randrange(len(all_shapes))
    shape = all_shapes[s]                     #pick a shape
    tile = create_tile(shape)
    width, height = tile.bbox
    zero = tile.zero
    j = rng.randrange(cols)
    drop = False
    sequence = list(range(j, cols)) + list(range(j))
    for j in sequence:                      # columns to choose from
        if j + width - zero > cols:
            continue                        # tile won't fit here
        if j - zero < 0:
            continue                        # tile won't fit here
        places = list()
        for cell in columns[j]:
            if cell not in occupied:
                places.append(cell)
        columns[j] = tuple(places)
        if len(places) == 0:
            continue                        # tile won't fit here
        drop = tile.drop(places, occupied)
        if drop:                            # successful drop
            tile.carve(maze)
            for cell in tile.cells:
                cell.label = chr(c + ord('0'))
            c += 1
            break
    if not drop:                        # unsuccessful drop
        del all_shapes[s]

print(unicode_str(maze))
print(c, "shapes placed")
