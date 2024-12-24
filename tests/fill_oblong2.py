"""
tests.fill_oblong2 - color gradient using the fill method in graphics.oblong1
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This test uses a path length-based color gradient to color a maze.

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
# from matplotlib.colors import to_hex
import mazes
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.dijkstra import test

    # the new improved daddy long legs (23 Dec 2024)
from mazes.Graphics.oblong1 import Phocidae

def gradient(hot:'rgb', cold:'rgb', d:int, dmax:int) -> 'rgb':
    """compute the interpolated color"""
    rgb = []
    for i in range(3):
        t0, t1 = hot[i], cold[i]
        t = t0 + (t1-t0) * d / dmax
        rgb.append(t)
    return tuple(rgb)

def main(rows:int, cols:int, hot:'rgb', cold:'rgb', zero:'rgb', Carver=Wilson):
    """color a maze using a color gradient"""
        # create the maze
    #maze = Maze(OblongGrid(21, 34))
    maze = Maze(OblongGrid(rows, cols))
    print(Carver.on(maze))

        # create the gradients
    dijkstra = test(maze)
    diameter = dijkstra.distance(dijkstra.farthest)
    gradients = {}
    for i in range(diameter+1):
        gradients[i] = gradient(hot, cold, i, diameter)
    # for i in gradients:
    #    print(i, gradients[i])

        # create the fill color array
    gradients[0] = zero
    fills = {}
    for cell in maze.grid:
        # print(f"cell={cell.index}, source={dijkstra.source.index},",
        #      f"distance={dijkstra.distance(cell)}")
        fills[cell] = gradients[dijkstra.distance(cell)]
        # print(fills[cell])

    return maze, fills

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
    args = parser.parse_args()
    if args.zero.lower() in {'', 'none'}:
        args.zero = args.hot
    print(args)
    hot, cold, zero = to_rgb(args.hot), to_rgb(args.cold), to_rgb(args.zero)
    print(f" {hot=}")
    print(f"{cold=}")
    print(f"{zero=}")
    rows, cols = args.dim
    return main(rows, cols, hot, cold, zero)

if __name__ == "__main__":
    import sys
    maze, fills = parse_args(sys.argv[1:])
        # plot the maze
    spider = Phocidae(maze)
    spider.setup(fillcolors=fills)
    spider.draw_maze()
    spider.show()

# end module tests.fill_oblong2