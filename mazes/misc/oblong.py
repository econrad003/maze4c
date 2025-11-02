"""
mazes.misc.oblong.py - argument group for Von Neumann rectangular grids
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module provides a parser for maze making.

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
from mazes.misc.maze_parser import MazeParser

def grid_parser(parser:MazeParser) -> "parser.group":
    """set up the parser"""
    gridgrp = parser.parser.add_argument_group("grid arguments", \
        description="These arguments set up the grid.")
    parser.groups["grid"] = gridgrp
    return gridgrp

def grid_dim(gridgrp, dim=(8, 13)):
    """set up the grid dimensions"""
    if type(dim) != tuple or len(dim) != 2:
        raise TypeError("default dimension must a tuple with two entries")
    if type(dim[0]) != int or type(dim[1]) != int:
        raise TypeError("default dimension entries must be integers")
    gridgrp.add_argument("-d", "--dim", nargs=2, type=int, default=dim, \
        metavar=("ROWS", "COLS"), help="the numbers of rows and columns")

def twoD_grid_parser(parser:MazeParser, dim=(8, 13)) -> "parser.group":
    """set up a parser for a 2D rectangular maze"""
    gridgrp = grid_parser(parser)
    grid_dim(gridgrp, dim)
    return gridgrp

def make_maze(args:"Namespace", *pargs, GridClass:"class"=OblongGrid,
              **kwargs) -> Maze:
    """create the empty maze"""
    rows, cols = args.dim
    grid = GridClass(rows, cols, *pargs, **kwargs)
    return Maze(grid)

def main(argv):
    """main entry point"""
    DESCR = "Create an ordinary rectangular maze."
    EPILOG = ""
    parser = MazeParser(DESCR, EPILOG)
    gridgrp = twoD_grid_parser(parser)
        #   MORE STUFF GOES HERE
        #       algorithm selection
        #       plotter
    args = parser.parser.parse_args(argv)
    maze = make_maze(args)
        #   MORE STUFF GOES HERE
        #       algorithm
        #       plot
    print(maze)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
