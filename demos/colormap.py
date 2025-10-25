"""
tests.colormap - color gradient for a maze
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This demo produces distance-colored mazes.

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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.dijkstra import test
from mazes.tools.distance_map import DistanceColoring

    # the new improved daddy long legs (23 Dec 2024)
from mazes.Graphics.oblong1 import Pholcidae

CARVER = (Wilson, (), {})

def make_maze(rows:int, cols:int, carver):
    """color a maze using a color gradient"""
        # create the maze
    maze = Maze(OblongGrid(rows, cols))
    Carver, carve_args, carve_kwargs = carver
    status = Carver.on(maze, *carve_args, **carve_kwargs)
    return status

def make_colormap(maze, hot, cold, zero, source):
    """create a color map"""
    coloring = DistanceColoring(maze, hot, cold, zero, source)
    return coloring.gradients

def make_sketch(maze, hot, cold, zero, source):
    """sketch the maze"""
    fills = make_colormap(maze, hot, cold, zero, source)
    spider = Pholcidae(maze)
    spider.setup(fillcolors=fills)
    spider.draw_maze()
    return spider

def main(rows:int, cols:int, hot:'rgb', cold:'rgb', zero:'rgb',
         source:str='', carver=CARVER):
    """color a maze using a color gradient"""

        # create the maze
    status = make_maze(rows, cols, carver)
    print(status)
    maze = status.maze

        # source cell
    source = source.lower()
    if source == "sw":
        source = maze.grid[0,0]
    elif source == "se":
        source = maze.grid[0,cols-1]
    elif source == "ne":
        source = maze.grid[rows-1,cols-1]
    elif source == "nw":
        source = maze.grid[rows-1,0]
    elif source == "c":
        source = maze.grid[rows//2,cols//2]
    else:
        source=None

        # create the sketch
    spider = make_sketch(maze, hot, cold, zero, source)
    return spider

def parse_args(argv):
    """get arguments using argparse"""
    import argparse
    from matplotlib.colors import to_rgb

    DESCR = "fill maze with path-length gradient"
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument("hot", type=str, nargs='?', default="crimson", \
        help="the name of the zero distance color (crimson)")
    parser.add_argument("cold", type=str, nargs='?', default="skyblue", \
        help="the name of the maximum distance color (skyblue)")
    parser.add_argument("-z", "--zero", type=str, default="goldenrod", \
        help="the name of the source cell color (goldenrod).  'none' will" \
        + " set this to the hot color")
    parser.add_argument("-d", "--dim", type=int, nargs=2, default=(13,21), \
        metavar = ("ROWS", "COLS"), \
        help="the dimensions of the maze (13, 21)")
    parser.add_argument("-s", "--source", type=str, default='', \
        help="one of the corners ('sw', 'se', 'ne', 'nw')) or 'c' for" \
        + " center. Default will use longest path computation.")
    args = parser.parse_args()
    if args.zero.lower() in {'', 'none'}:
        args.zero = args.hot
    print(args)
    hot, cold, zero = to_rgb(args.hot), to_rgb(args.cold), to_rgb(args.zero)
    print(f" {hot=}")
    print(f"{cold=}")
    print(f"{zero=}")
    rows, cols = args.dim
    return main(rows, cols, hot, cold, zero, source=args.source)

if __name__ == "__main__":
    import sys
    spider = parse_args(sys.argv[1:])
    spider.show()

# end module demos.colormap
