"""
demos.maximally_eulerian - create maximally Eulerian oblong mazes
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Creates 4-connected oblong grids and carves passages to form maximally
    Eulerian mazes.  These mazes are not random.

NOTE

    The general problem of finding a maximal spanning Eulerian subgraph
    apparently does not have a known deterministic polynomial time
    solution.  (WARNING: This conclusion was based on a quick search
    of preprints on arxiv.org and could easily be a misunderstanding
    on my part.  This is my first foray into this particular area.)

    The claim here is that the mazes produced here satisfy the following
    constraints:

        (1) They are spanning mazes, i.e., every cell in the grid is
            also a cell in the maze, and every passage in the maze is
            an edge in the grid.  (The cell sets are the same, and the
            passage set is a subset of the edges in the grid.)

        (2) They are connected subsets.

        (3) Every cell in the maze has an even number of incident passages.

        (4) They are maximal in the following sense: The complement in
            the grid of the maze does not contain any (simple) circuits.

    I believe (at this point without proof!) that they are also maximal
    in a stronger sense:

        (5) For each of the supported grids, there aren't any spanning
            Eulerian mazes with more passages.

    The grids here are rectangular with planar Von Neumann (N/S/E/W)
    neighborhoods.  There are some restrictions on grids with either
    an odd number of rows or an odd number of columns.  See the
    documentation for more details.

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
import sys

import argparse

from mazes.Grids.eulerian_oblong import maximally_Eulerian

DESC = "create maximally Eulerian oblong mazes"

def make_maze(rows:int, cols:int, constrain=True)-> "Maze":
    """create the maze"""
    print(f"make_maze({rows=}, {cols=}, {constrain=})")
    maze = maximally_Eulerian(rows, cols, constrain=constrain)
    return maze

def main(argv:list):
    """main routine"""
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-d", "--dim", type=int, nargs=2, \
        default=(8,10), metavar=("ROWS", "COLS"), \
        help="the dimensions of the grid")
    parser.add_argument("-N", "--no_constraints", \
        action="store_true", \
        help="allow creation on incompatible grids (for debugging)")
    args = parser.parse_args(argv)
    print(args)
    rows, cols = args.dim
    maze = make_maze(rows, cols, constrain=not args.no_constraints)
    print(maze)

if __name__ == "__main__":
        # PARSER
    main(sys.argv[1:])
