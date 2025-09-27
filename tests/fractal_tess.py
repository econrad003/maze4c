"""
mazes.tests.fractal_tess - test the fractal tessellation maze carver
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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.kruskal import Kruskal
from mazes.Algorithms.fractal_tess import FractalTessellation

def banner(msg):
    """print the banner for the test"""
    i = (72 - len(msg) - 2) // 2
    left = ("=" * i) + " "
    right = " " + ("=" * i)
    msg = left + msg + right
    while len(msg) < 72:
        msg += "="
    print(msg) 


def test1():
    """test a single pass with no symmetry"""
    banner("TEST 1")
    print(test1.__doc__)
    carver = FractalTessellation()
    GridType, m, n = carver.single_pass(test=True)
    print(f"test_pass from (1,1): {GridType.__name__}, {m=}, {n=}")
    assert m==2 and n==2 and GridType==OblongGrid
    seed = Maze(OblongGrid(3, 4))
    Kruskal.on(seed)
    GridType, m, n = carver.single_pass(seed, test=True)
    print(f"test_pass from (3, 4): {GridType.__name__}, {m=}, {n=}")
    assert m==6 and n==8 and GridType==OblongGrid
    print("seed:  3 rows, 4 columns")
    print(seed)
    print("maze:  6 rows, 8 columns")
    maze = carver.single_pass(seed)
    print(maze)
    print(carver)
    print("Manually verify that the maze contains four copies of the seed.")
    assert len(maze) == 47  # 47 passages
    print("ok.")

def test2():
    """test a single pass with symmetry"""
    banner("TEST 2")
    print(test2.__doc__)
    symmetries = {}
    symmetries[0,0] = 0
    symmetries[0,1] = 1
    symmetries[1,1] = 2
    symmetries[1,0] = 3
    carver = FractalTessellation(symmetries=symmetries)
    seed = Maze(OblongGrid(3, 4))
    Kruskal.on(seed)
    print("seed:  3 rows, 4 columns")
    print(seed)
    print("maze:  6 rows, 8 columns")
    maze = carver.single_pass(seed)
    print(maze)
    print(carver)
    print("Manually verify that the maze contains the orbit of the seed",
          "in D(2).")
    print("The seed is the lower left entry.")
    print("Proceeding counterclockwise: rotate 180, flip H, flip/rotate.")
    assert len(maze) == 47  # 47 passages
    print("ok.")

def test3():
    """test two passes with symmetry"""
    banner("TEST 3")
    print(test3.__doc__)
    symmetries = {}
    symmetries[0,0] = 0
    symmetries[0,1] = 1
    symmetries[0,2] = 2
    symmetries[1,2] = 3
    symmetries[2,2] = 4
    symmetries[2,1] = 5
    symmetries[2,0] = 6
    symmetries[1,0] = 7
    symmetries[1,1] = 8         # 8 % 8 = 0
    carver = FractalTessellation(rows=3, cols=3, symmetries=symmetries)
    print("pass 1 seed:  1 rows, 1 column")
    print(carver.maze)
    print("pass 1 maze:  3 rows, 3 columns")
    maze = carver.single_pass()
    print(maze)
    print(carver)
    assert len(maze) == 8       # 8 passages
    assert len(maze.grid) == 9  # 9 cells
    carver.maze = maze          # change the carver's seed
    print("pass 2 maze:  9 rows, 9 columns")
    maze = carver.single_pass()
    print(maze)
    print(carver)
    print("Manually verify that the maze contains the orbit of",
          "the 3×3 maze in D(4).")
    print("The 3×3 maze is the lower left and center entries.")
    print("Proceeding counterclockwise: rotate 90, 180, 270,",
          "flip H, and 3 flip/rotates.")
    assert len(maze) == 80      # 80 passages
    assert len(maze.grid) == 81 # 81 cells
    assert maze.grid.m == maze.grid.n == 9
    print("ok.")

def test4():
    """join 4 arbitrary 5x5 mazes to form a 10x10 maze"""
    banner("TEST 4")
    print(test4.__doc__)
    from mazes.Algorithms.simple_binary_tree import BinaryTree
    from mazes.Algorithms.bfs import BFS
    from mazes.Algorithms.dfs_better import DFS
    from mazes.Algorithms.recursive_division import RecursiveDivision

    mazes = []
    for i in range(4):
       mazes.append(Maze(OblongGrid(5, 5)))
    mazes = tuple(mazes)

        # carve the mazes to be patched together
    BinaryTree.on(mazes[0])

    start = mazes[1].grid[2,2]              # center cell
    BFS.on(mazes[1], start_cell=start)

    start = mazes[2].grid[0,0]              # lower left cell
    DFS.on(mazes[2], start_cell=start)

    RecursiveDivision.on(mazes[3])

        # prepare the composite
    symmetries = {}
    symmetries[0,0] = 0
    symmetries[0,1] = 1
    symmetries[1,1] = 2
    symmetries[1,0] = 3

    carver = FractalTessellation(symmetries=symmetries)
    maze = carver.single_pass(*mazes)

        # label key cells
    sbtroot = maze.grid[4,4]
    sbtroot.label = "R"
    bfsstart = maze.grid[2,7]
    bfsstart.label = "C"
    dfsstart = maze.grid[5,5]
    dfsstart.label = "S"

    print(maze)
    print(carver)
    print("Manually verify that the maze contains the four",
          "prepared mazes.")
    print("Proceeding counterclockwise from lower left:")
    print("   (0,0) simple binary tree with root R")
    print("   (0,1) BFS tree with start C")
    print("   (1,1) DFS tree with start S")
    print("   (1,0) Recursive division")
    assert len(maze) == 99          # 99 passages
    assert len(maze.grid) == 100    # 100 cells
    assert maze.grid.m == maze.grid.n == 10
    print("ok.")

def test5():
    """join 4 symmetries of a given 5x5 maze to form a 10x10 maze"""
    banner("TEST 5")
    print(test5.__doc__)
    from mazes.Algorithms.sidewinder import Sidewinder
    maze = Maze(OblongGrid(5, 5))
    Sidewinder.on(maze)
    print("seed:  5 rows, 5 columns")
    print(maze)

    carver = FractalTessellation(symmetries=True)
    maze = carver.single_pass(maze)
    print("maze:  10 rows, 10 columns")
    print(maze)
    print(carver)

    print("Manually verify that the maze contains four",
          "random symmetries of the seed.")
    print("There may be repetitions.")
    assert len(maze) == 99          # 99 passages
    assert len(maze.grid) == 100    # 100 cells
    assert maze.grid.m == maze.grid.n == 10
    print("ok.")

def test6():
    """run three passes of the carver for an 8x8 maze"""
    banner("TEST 6")
    print(test6.__doc__)
    carver = FractalTessellation(symmetries=True)
    maze = carver.on()              # 3 passes from scratch
    print(maze)
    print(carver)
    assert len(maze) == 63
    assert len(maze.grid) == 64
    print("ok.")

def test7():
    """run three passes of the carver for an 8x8 Moore grid maze"""
    banner("TEST 7")
    print(test7.__doc__)
    from mazes.Grids.oblong8 import MooreGrid

    maze = Maze(MooreGrid(1,1))
    carver = FractalTessellation(symmetries=True)
    carver.maze = maze              # sneak in a Moore grid maze
    maze = carver.on()              # 3 passes from scratch
    print(maze)
    print(carver)
    assert len(maze) == 63
    assert len(maze.grid) == 64
    print("ok.")
    


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()

