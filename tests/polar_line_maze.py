"""
tests.polar_line_maze - a simple test for theta grids
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This simple test creates.a theta maze (using recursive backtracker) on a
    theta grid and renders it as a line maze.  It is mainly intended to make
    sure that the grid was built correctly.

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
from mazes import Algorithm
from mazes.Grids.polar import ThetaGrid
from mazes.maze import Maze
from mazes.Algorithms.dfs_better import DFS
from mazes.Algorithms.wilson import Wilson
from mazes.Graphics.polar2 import SpiderWeb

class Kuratowski(Algorithm):
    """carves a complete maze"""

    class Status(Algorithm.Status):
        """make all possible edges"""

        def configure(self):
            """configuration"""
            super().configure()
            self.store_item("cells", len(self.maze.grid))
            self.store_item("edges carved", 0)
            for cell in self.maze.grid:
                for nbr in cell.neighbors:
                    if not cell.is_linked(nbr):
                        self.maze.link(cell, nbr)
                        self.increment_item("edges carved")
            self.store_item("edges", len(self.maze))

        @property
        def more(self):
            """That's all, folks!"""
            return False

def make_grid(rings:int, pole:int, split:float) -> ThetaGrid:
    """create a polar grid"""
    grid = ThetaGrid(rings, pole=pole, split=split)
    print(f"{str(grid)}.. {len(grid)=} ")
    return grid

def make_maze(grid:ThetaGrid, AlgorithmClass:callable, *args, **kwargs):
    """carve the maze"""
    maze = Maze(grid)
    print(AlgorithmClass.on(maze, *args, **kwargs))
    return maze

def make_sketch(maze:Maze, center:str='ro', nodes:str='go', **kwargs):
    """plot the maze"""
    spider = SpiderWeb(maze)
    spider.setup(**kwargs)
    if center:
        spider.ax.plot(0, 0, center)
    if nodes:
        for cell in maze.grid:
            x, y = spider.get_location_of(cell, 0, 0)
            spider.ax.plot(x, y, nodes)
    spider.draw_maze()
    return spider

def main(rings:int, pole:int, split:float, Alg:callable,
         show=True, center:str='ro', nodes:str='go'):
    """run the test"""
    grid = make_grid(rings, pole, split)
    maze = make_maze(grid, Alg)
    spider = make_sketch(maze, center=center)
    spider.title(f"Theta Maze ({Alg.__name__})")
    if show:
        spider.show()
    return spider

def parse_args(argv):
    """parse the command line arguments"""
    import argparse

    Algorithms = {}
    Algorithms['1'] = DFS
    Algorithms['dfs'] = DFS
    Algorithms['2'] = Wilson
    Algorithms['w'] = Wilson
    Algorithms['100'] = Kuratowski
    Algorithms['complete'] = Kuratowski

    helper = {}
    for s in Algorithms:
        A = Algorithms[s]
        if A in helper:
            helper[A] += " or " + s
        else:
            helper[A] = s
    algo_help = "One of the following:"
    separator = ""
    for A in helper:
        algo_help += separator + f" ({A.__name__}) {helper[A]}"
        separator = ";"
    algo_help += ". (default: dfs)"

    DESC = "polar line DFS maze generator"""
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-r", "--rings", type=int, default=5, \
        help="the number of rings in the maze (integer, default=5)")
    parser.add_argument("-p", "--pole", type=int, default=6, \
        help="the number of cells at the pole (integer, default=6)")
    parser.add_argument("-s", "--split", type=float, default=1, \
        help="the maximum arc length for a cell (float, default=1)")
    parser.add_argument("-a", "--algorithm", type=str, default="dfs", \
        help=algo_help)
    args = parser.parse_args(argv)
    print(args)
    alg = args.algorithm.lower()
    Alg = Algorithms[alg]
    main(args.rings, args.pole, args.split, Alg)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module tests.polar_line_maze