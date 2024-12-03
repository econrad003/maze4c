"""
tests.spider_web - test the SpiderWeb driver in mazes.Graphics.oblong2
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Oblong grids are drawn linewise.

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
import os
thisfilename = os.path.basename(__file__)

import mazes
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.simple_binary_tree import BinaryTree
from mazes.Graphics.oblong2 import SpiderWeb

def test_graphics(maze, title):
    """run the graphics driver"""
    print("Check that the sketch agrees with the maze displayed above...")
    web = SpiderWeb(maze)
    web.setup()
    web.title(title)
    web.draw_maze()
    web.show()

def test1():
    """this makes sure a basic maze has a valid linewise representation"""
        # create a binary tree maze
    maze = Maze(OblongGrid(3, 5))
    BinaryTree.on(maze)
        # display it on the console
    print(maze)
        # graphics
    test_graphics(maze, f"tests/{thisfilename}: test1()")

def test2():
    """this gives a better indication of how the sketch should appear"""
        # create a specific binary tree maze
    maze = Maze(OblongGrid(3, 5))
    grid = maze.grid
    for i in range(3):
        for j in range(5):
            cell = grid[i, j]
            if i == 2:
                if j < 4: maze.link(cell, cell.east)
            elif j == 4:
                maze.link(cell, cell.north)
            elif (i+j) % 2:
                maze.link(cell, cell.east)
            else:
                maze.link(cell, cell.north)
    print("Cellwise diagram:")
    print(maze)
        # This gives a better idea
    print("Linewise diagram:")
    print("   ---+-----+--+")
    print("      |     |  |")
    print("   +--+  +--+  |")
    print("   |     |     |")
    print("   |  ---+  ---+")
        # graphics
    test_graphics(maze, f"tests/{thisfilename}: test2()")

def test3():
    """Similar to test2 except we have arrows going east and north"""
        # create a specific binary tree maze
    maze = Maze(OblongGrid(3, 5))
    grid = maze.grid
    for i in range(3):
        for j in range(5):
            cell = grid[i, j]
            if i == 2:
                if j < 4: maze.link(cell, cell.east, directed=True)
            elif j == 4:
                maze.link(cell, cell.north, directed=True)
            elif (i+j) % 2:
                maze.link(cell, cell.east, directed=True)
            else:
                maze.link(cell, cell.north, directed=True)
    print("Cellwise diagram:")
    print(maze)
        # This gives a better idea
    print("Linewise diagram:")
    print("   --->-->--+--+")
    print("      |     |  |")
    print("   ^-->  ^-->  ^")
    print("   |     |     |")
    print("   |  --->  --->")
        # graphics
    test_graphics(maze, f"tests/{thisfilename}: test3()")

def test4():
    """Similar to test3 with arrows in opposite direction"""
        # create a specific binary tree maze
    maze = Maze(OblongGrid(3, 5))
    grid = maze.grid
    for i in range(3):
        for j in range(5):
            cell = grid[i, j]
            if i == 2:
                if j < 4: maze.link(cell.east, cell, directed=True)
            elif j == 4:
                maze.link(cell.north, cell, directed=True)
            elif (i+j) % 2:
                maze.link(cell.east, cell, directed=True)
            else:
                maze.link(cell.north, cell, directed=True)
    print("Cellwise diagram:")
    print(maze)
        # This gives a better idea
    print("Linewise diagram:")
    print("   <--<--<--<--+")
    print("      |     |  |")
    print("   <--v  <--v  v")
    print("   |     |     |")
    print("   v  <--v  <--v")
        # graphics
    test_graphics(maze, f"tests/{thisfilename}: test4()")

def unlink_relink(maze, bias=2/3):
    """random replace edges by arcs"""
    to_be_replaced = list()
    j1 = len(maze)                      # number of joins
    for edge in maze:
        if rng.random() < bias:         # head
            to_be_replaced.append(edge)
    print(f"Replacing {len(to_be_replaced)} edges with arcs...")
    for edge in to_be_replaced:
        cell1, cell2 = edge
        maze.unlink(edge)
        if rng.random() < 1/2:          # fair coin head
            maze.link(cell1, cell2, directed=True)
        else:
            maze.link(cell2, cell1, directed=True)
    j2 = len(maze)                      # number of joins
    assert j1 == j2, f"{len(maze.grid)=}, {j1=}, {j2=}"

def test5():
    """this tests arcs and edges"""
        # create a binary tree maze
    maze = Maze(OblongGrid(8, 13))
    BinaryTree.on(maze)
        # display it on the console
    print("Before edges get replaced by arcs")
    print(maze)
    unlink_relink(maze)
        # graphics
    test_graphics(maze, f"tests/{thisfilename}: test5()")

if __name__ == "__main__":
    import argparse

    DESC = "test the SpiderWeb class in mazes.Graphics.oblong2"
    EPI = "Tests: 1) test with a simple binary tree maze; " \
        + "2) supplies a console line diagram for comparison; " \
        + "3) like (2) with arcs instead of edges; " \
        + "4) like (3) with arrows going the other way; " \
        + "5) a larger binary maze with some edge replaced by arcs."
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)
    parser.add_argument("test", type=int, nargs='?', default=1, \
        help="the test number 1, 2, 3, 4 or 5. (Default: 1)")
    args=parser.parse_args()
    tests = {1:test1, 2:test2, 3:test3, 4:test4, 5:test5}
    print("Running:", tests[args.test].__name__)
    tests[args.test]()

# end module tests.spider_web