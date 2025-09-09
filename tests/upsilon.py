"""
tests.upsilon - test the upsilon grid class
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module performs some rudimentary tests on the upsilon grid
    class.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

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

from mazes.Grids.upsilon import UpsilonGrid
from mazes.Grids.oblong import SquareCell
from mazes.Grids.oblong8 import OctagonalCell
from mazes.maze import Maze
from mazes.Algorithms.kruskal import Kruskal

def label_cells(grid:'Grid') -> 'Grid':
    """label the cells by type"""
    for cell in grid:
        if isinstance(cell, OctagonalCell):
            cell.label = 'O'
        elif isinstance(cell, SquareCell):
            cell.label = 'S'
    return grid

def link_all(grid:'Grid') -> Maze:
    """link all the neighbors"""
    maze = Maze(grid)
    for cell in grid:
        for nbr in cell.neighbors:
            if cell.is_linked(nbr):
                continue
            maze.link(cell, nbr)
    return maze

print("Creating an upsilon grid with even parity")
grid = label_cells(UpsilonGrid(8, 13))
print("The cells should alternate O in lower left with S...")
print("Empty maze:")
print(grid)
maze = link_all(grid)
print("Complete maze:")
print(maze)

print("Creating an upsilon grid with odd parity")
grid = label_cells(UpsilonGrid(8, 13, parity=True))
print("The cells should alternate S in lower left with O...")
print("Empty maze:")
print(grid)
maze = link_all(grid)
print("Complete maze:")
print(maze)

print("Testing maze creation using Kruskal's algorithm")
print("Even parity")
maze = Maze(label_cells(UpsilonGrid(8, 13)))
print(Kruskal.on(maze))
print(maze)

print("Odd parity")
maze = Maze(label_cells(UpsilonGrid(8, 13, parity=True)))
print(Kruskal.on(maze))
print(maze)

# end tests.upsilon
