"""
tests.polar_eller - a simple demo of the polar version of Eller's algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Eller's algorithm is a generalization of the sidewinder algorithm for
    generating mazes.  In a rectangular setting using two orthogonal compass
    directions, for example North and East, or West and South, the
    algorithm has essentially one imlementation.  In a polar setting where
    the four directions are essentially inbound or outbound, and clockwise or
    counterclockwise, the rotational direction being the major direction,
    and the central direction is minor. Because the annulular rings have a
    different number of cells, there are some significant differences
    between the handling of the inbound and outbound minor cases.  The
    rotational direction is actually arbitrary.

    The differences between inbound polar Eller and outbound polar Eller are
    analogous to the differences between inbound sidewinder (i.e. inwinder)
    and outbound sidewinder (i.e. outwinder).

    This demo runs the both versions of the algorithm.

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
import argparse

import mazes
from mazes import rng
from mazes.Grids.polar import ThetaGrid
from mazes.maze import Maze
from mazes.tools.distance_map import DistanceColoring
from mazes.Algorithms.polar.eller import PolarEller, INWARD, OUTWARD, coin_toss

def make_grid(r:int, pole:int, split:(float, int)) -> Maze:
    """create a grid object"""
        # TRACING
    params = f"radius={r}, pole cells={pole}, split={split}"
    print(f"  creating the grid ({params})...")

        # VALIDATE ARGUMENTS
    if type(r) == int:
        if r < 1:
            raise ValueError("The grid radius must be positive.")
    else:
        raise TypeError("The grid radius must be an integer.")

    if type(r) == int:
        if r < 1:
            raise ValueError("The grid radius must be positive.")
    else:
        raise TypeError("The grid radius must be an integer.")

    if isinstance(split, (float, int)):
        if split <= 0:
            raise ValueError("The arc split length must be positive.")
    else:
        raise TypeError("The arc split length must be a float or an int.")

        # CREATE THE MAZE OBJECT
    return Maze(ThetaGrid(r, pole=pole, split=split))

def carve_maze(maze:Maze, outbound:bool, flip:float, toss:float, debug:int=0):
    """carve the maze"""
        # TRACING
    params = f"outbound={outbound}, flip={flip}, toss={toss}"
    print(f"  carving the maze ({params})...")

        # VALIDATE ARGUMENTS
    if type(outbound) != bool:
        raise TypeError("The outbound flag must be a boolean.")

    if isinstance(flip, (float, int)):      # int values 0, 1 are permitted
        if flip < 0 or flip > 1:
            raise ValueError("Coin toss probability must be in [0,1].")
    else:
        raise TypeError("The coin toss probability must be a float.")

    if isinstance(toss, (float, int)):      # int values 0, 1 are permitted
        if toss < 0 or toss > 1:
            raise ValueError("Dice toss probability must be in [0,1].")
    else:
        raise TypeError("Dice toss probability must be a float.")

        # CARVE THE MAZE OBJECT
    upward = OUTWARD if outbound else INWARD
    flip1 = (coin_toss, (), {"bias":flip})
    flip2 = (coin_toss, (), {"bias":toss})
    status = PolarEller.on(maze,
                           upward=upward, flip1=flip1, flip2=flip2,
                           debug=debug)
    print(status)
    return status

def title(args:argparse.Namespace):
    """create a custom title"""
    if args.title:
        return args.title
    parms = f"flip={args.flip:.4f}, toss={args.toss:.4f}"
    if args.outbound:
        return f"Eller's Algorithm (outbound, {parms})"
    return f"Eller's Algorithm (inbound, {parms})"

def draw_maze(maze, title:str, colors:bool, output:str):
    """sketch the maze"""
    from mazes.Graphics.polar1 import Phocidae
    spider = Phocidae(maze)
    if colors:
        RED = (1.0, 0, 0)
        BLUE = (0, 0, 1.0)
        distances = DistanceColoring(maze, RED, BLUE, RED, maze.grid[0,0])
        spider.setup(fillcolors=distances.gradients)
    else:
        spider.setup()
    spider.title(title)
    spider.draw_maze()
    if output:
        print("Saving image as:", output)
        spider.save_image(output)
    spider.show()

def parse_args(argv:list):
    """argument parser"""
    DESC = "Eller's algorithm on a polar (theta) grid"
    parser = argparse.ArgumentParser(description=DESC)
    ggroup = parser.add_argument_group('grid arguments')
    ggroup.add_argument("-r", "--radius", type=int, default=5, \
        help="the number of rings (including the pole) [default: 5]")
    ggroup.add_argument("-p", "--pole_cells", type=int, default=6, \
        help="the number of cells at the pole [default: 6]")
    ggroup.add_argument("-s", "--split", type=float, default=1, \
        help="the arc length for an outward split [default: 1]")

    agroup = parser.add_argument_group('algorithm arguments')
    agroup.add_argument("-o", "--outbound", action="store_true",
        help="if this option is set, the direction is outward")
    agroup.add_argument("-f", "--flip", type=float, default=0.5, \
        help="coin toss probability of a head [default: 0.5]")
    agroup.add_argument("-t", "--toss", type=float, default=1/3, \
        help="dice toss probability [default: 0.333...]")
    agroup.add_argument("--debug", action="store_true", \
        help="display debugging information")

    dgroup = parser.add_argument_group('sketching properties')
    dgroup.add_argument("--title", type=str, default="", \
        help="an optionl title fo the sketch")
    dgroup.add_argument("--color", action="store_true", \
        help="if set, color all cells accessible from cell(0,1)")
    dgroup.add_argument("--output", type=str, default="", \
        help="if set, the graph will be saved to a file")


    args = parser.parse_args(argv)
    print(args)
    return args

def process(args:argparse.Namespace):
    """process the arguments"""
    debug = 100 if args.debug else 0
    maze = make_grid(args.radius, args.pole_cells, args.split)
    status = carve_maze(maze, args.outbound, args.flip, args.toss, debug)
    draw_maze(maze, title(args), args.color, args.output)

if __name__ == "__main__":
    import sys

    # print(sys.argv)         # echo command line
    process(parse_args(sys.argv[1:]))

# end module tests.polar_eller
