"""
tests.tetris1 - simple test of tetris module
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
from mazes.maze import Maze
from mazes.console_tools import unicode_str
from mazes.Grids.oblong import OblongGrid
from mazes.tetris.tile import Tile
from mazes.tetris.tetris import shapes, configs, create_tile

maze = Maze(OblongGrid(8, 16))
grid = maze.grid
labels = ('O', 'T', 'L', 'M', 'I', 'Z', 'S')

assert len(shapes) == 7

occupied = set()
n = 0
for i in range(7):
    shape = shapes[i]
    label = labels[i]
    descriptor = rng.choice(shape)
    # print(label, descriptor)
    tile = create_tile(descriptor)
    assert type(tile) == Tile
    x = 4 * (i // 2) + tile.zero
    y = 4 * (i % 2)
    placements = [grid[y+1,x], grid[y,x]]
    print("placement = ", (y,x), descriptor[0], labels[i])
    if tile.drop(placements, occupied):
        n += 4
        if len(placements) == 0:
            print("\tmisplaced!")
        m = len(occupied)
        if m != n:
            print(f"\toccupied cells accounting error; {m} cells, expected {n}")
        for(cell) in tile.cells:
            cell.label = labels[i]
        tile.carve(maze)
    else:
        print("\tnot placed")

descriptor = rng.choice(configs)
tile = create_tile(descriptor)
assert type(tile) == Tile
placements = [grid[5,12], grid[4,12]]
print("placement = ", (y,x), descriptor[0], "random")
if tile.drop(placements, occupied):
    n += 4
    if len(placements) == 0:
        print("\tmisplaced!")
    m = len(occupied)
    if m != n:
        print(f"\toccupied cells accounting error; {m} cells, expected {n}")
    for(cell) in tile.cells:
        cell.label = "?"
    tile.carve(maze)
else:
    print("\tnot placed")
print(unicode_str(maze))
