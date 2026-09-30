"""
mazes.demos.tetris - create a maze using the Tetris tile drop algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The algorithm performs a series of tile drops onto an empty
    rectangular maze.

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
from mazes.Algorithms.tetris import Tetris
from mazes.Algorithms.kruskal import Kruskal
from mazes.console_tools import unicode_str as U

DESCRIPTION = "create a maze using the Tetris tile drop algorithm"

def positive_int(n):
    """check that the argument is a positive integer"""
    n = int(n)                      # type check and conversion
    if n < 1:
        raise ValueError(f"{n} is not a positive integer.")
    return n

def create_grid(args:"Namespace"):
    m, n = args.dim
    return Maze(OblongGrid(m, n))

def drop_tiles(args:"Namespace", tiles=None):
    """Tetris tile drops"""
    maze = create_grid(args)
    status = Tetris.on(maze, tiles=tiles, debug=args.debug)
    return maze, status

def main(argv:list, description=DESCRIPTION):
    """parse arguments"""
    import argparse

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-d", "--dim", type=positive_int, nargs=2, \
        default=(8,13), help="maze dimensions (default: 8,13)",
        metavar=("ROW", "COL"))
    parser.add_argument("-T", "--tetris_only", action="store_true", \
        help="set this option to suppress the run of Kruskal's algorithm")
    parser.add_argument("-D", "--debug", action="store_true", \
        help="set this option to display state messages")
    parser.add_argument("-N", "--no_display", action="store_true", \
        help="set this suppress printing")
    args = parser.parse_args(argv)
    print("args =", args)

    my_print = lambda msg: (None if args.no_display else print(msg))
    maze, status = drop_tiles(args)
    my_print(status)
    if args.debug:
        my_print("\t\t --- Occupied cells ---")
        my_print(U(maze))
        for cell in maze.grid:
            cell.label = " " if cell in status.occupied else "X"
        my_print("\t\t --- Unoccupied cells ---")
    my_print(U(maze))
    if not args.tetris_only:
        my_print(Kruskal.on(maze))
        my_print(U(maze))
    return maze

if __name__ == "__main__":
    import sys
    argv = sys.argv[1:]
    # argv.append("-h")
    # argv.append("-N")
    main(argv)
