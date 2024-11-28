"""
tests.simple_binary_tree - test the simple binary tree algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The simple binary tree algorithm is a passage carver based on a coin flip:
    head -- carve northward or tail -- carve eastward.

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
import mazes
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.sidewinder import Sidewinder

def testEN(rows:int, cols:int, which=None):
    """create an east/north sidewinder tree"""
    print(f"  east/north sidewinder tree with {which=}")
    maze = Maze(OblongGrid(rows, cols))
    maze.grid.set_format("leader", "    ")
    status = Sidewinder.on(maze, which=which)
    print(maze)
    print(status)
    assert status.fetch_item("visits") == len(maze.grid) + 1
    assert status.fetch_item("cells") == len(maze.grid)
    assert status.fetch_item("passages") == len(maze.grid) - 1
    assert len(maze) == len(maze.grid) - 1
    for cell in maze.grid:
        i, j = cell.index
        if i == rows - 1:           # top row
            assert not cell.north
            if j < cols - 1:        # all but last in row
                assert cell.is_linked(cell.east)
                assert cell.east.is_linked(cell)
        assert len(list(cell.passages)) >= 1

    print(f"  east/north ({which=})pass...")

def test1(rows:int, cols:int, onward:str, upward:str):
    """create a sidewinder tree"""
    print(f"  {onward}/{upward} sidewinder tree")
    if onward in {"north", "south"}:
        assert upward in {"east", "west"}
    else:
        assert onward in {"east", "west"}
        assert upward in {"north", "south"}
    toprow = rows-1 if "north" in {onward, upward} else 0
    lastcol = cols-1 if "east" in {onward, upward} else 0
    vertically = "north" if "north" in {onward, upward} else "south"
    horizontally = "east" if "east" in {onward, upward} else "west"
    print(f"    {vertically=}, {horizontally=}")
        
    maze = Maze(OblongGrid(rows, cols))
    maze.grid.set_format("leader", "    ")
    status = Sidewinder.on(maze, onward=onward, upward=upward)
    print(maze)
    print(status)
    assert status.fetch_item("visits") == len(maze.grid) + 1
    assert status.fetch_item("cells") == len(maze.grid)
    assert status.fetch_item("passages") == len(maze.grid) - 1
    assert len(maze) == len(maze.grid) - 1
    for cell in maze.grid:
        i, j = cell.index
        if i == toprow:             # top row
            assert not cell[vertically]
            if j != lastcol and upward in {"north", "south"}:   # all but last in row
                assert cell.is_linked(cell[horizontally])
                assert cell[horizontally].is_linked(cell)
        if j == lastcol:            # last column
            assert not cell[horizontally]
            if i != toprow and upward in {"east", "west"}:      # all but top in column
                assert cell.is_linked(cell[vertically])
                assert cell[vertically].is_linked(cell)
        assert len(list(cell.passages)) >= 1

    print(f"  {onward}/{upward} pass...")

def test2(rows:int, cols:int, bias:float, warnlow:float, warnhigh:float):
    """create an east/north sidewinder tree with a bias"""
    print(f"  east/north sidewinder tree with bias p={bias}")
    maze = Maze(OblongGrid(rows, cols))
    maze.grid.set_format("leader", "    ")
    status = Sidewinder.on(maze, bias=bias)
    print(maze)
    print(status)
    assert status.fetch_item("visits") == len(maze.grid) + 1
    assert status.fetch_item("cells") == len(maze.grid)
    assert status.fetch_item("passages") == len(maze.grid) - 1
    assert len(maze) == len(maze.grid) - 1
    northward = 0
    either = 0
    for cell in maze.grid:
        if cell.east and cell.north:
            either += 1
            if cell.is_linked(cell.north):
                northward += 1
    rate = northward / either
    print(f"    northward {bias=}, actual {rate=}")
    msg = "This might indicate an error or it might simply be bad luck in" \
        + "in the random sequence.  For the default 5x8 mazes, these warnings" \
        + "should occur occasionally.  (I haven't done a formal analysis of " \
        + "variance, so I won't give an estimate.)" \
        + " To reduce the variance, increase the numbers of rows and columns." \
        + " I get very nice results with 10x15 mazes.  If you want to see this" \
        + " message more often, reduce the number of rows and columns -- 3x4 " \
        + " increases the variance substantially!"
    if rate < warnlow:
        raise Warning(f"{bias=}, {rate=}<{warnlow}: {msg=}")
    if rate > warnhigh:
        raise Warning(f"{bias=}, {rate=}>{warnhigh}: {msg=}")
    print(f"  east/north with {bias=} pass...")


def tests(rows:int, cols:int):
    """entry point for tests"""
    import os
    print(f"tests.{os.path.basename(__file__)}:")
    testEN(rows, cols)
    testEN(rows, cols, which=(0, -1))               # cocktail shaker
    test1(rows, cols, "east", "north")
    test1(rows, cols, "north", "east")
    test1(rows, cols, "south", "east")
    test1(rows, cols, "south", "west")
    test1(rows, cols, "west", "south")
    test1(rows, cols, "west", "north")
    test2(rows, cols, 0.25, 0.1, 0.4)
    test2(rows, cols, 0.5, 0.35, 0.65)
    test2(rows, cols, 0.75, 0.6, 0.9)

def main(argv):
    """entry point for tests"""
    import argparse

    DESC = "test the sidewinder algorithm"
    EPI = "This module displays several mazes on the console.  It" \
        + " is suggested that the dimensions be kept small enough" \
        + " for these mazes to fit in a typical console window. For" \
        + " a 24x80 console window, a 10x15 oblong grid will fit."
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)
    parser.add_argument("-d", "--dimensions", type=int, nargs=2, \
        metavar=("ROWS", "COLUMNS"), default=(5, 8), \
        help="the numbers of rows and columns in the oblong (i.e. " \
        + "rectangular) maze [default: 5 rows, 8 columns]")
    args = parser.parse_args(argv)
    print(args)
    rows, cols = args.dimensions
    if rows < 2 or cols < 2: raise ValueError
    tests(rows, cols)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

# end module tests.simple_binary_tree
