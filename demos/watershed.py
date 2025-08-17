"""
demos.watershed - create a watershed
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Here we demonstrate a simple application of the Watershed class.

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

USAGE

    usage: watershed.py [-h] [-d ROWS COLS] [-n SEEDS] [-s]

    Watershed demonstration

    options:
      -h, --help        show this help message and exit
      -d ROWS COLS, --dim ROWS COLS
                        the numbers of rows and columns in the maze. (Default:
                        (8, 13).)

    watershed options:
      -n SEEDS, --seeds SEEDS
                        The number of seeds. (Default: 2)
      -s, --stack           Use stacks instead of queues.

    Output is to the console.
"""
import mazes
from mazes import rng
from mazes.grid import Grid
from mazes.maze import Maze
from mazes.watershed import Watershed
from mazes.Algorithms.aldous_broder import AldousBroder
from mazes.Grids.oblong import OblongGrid
from mazes.Queues.stack import Stack

def make_grid(rows, columns) -> Maze:
    """returns a maze object that is ready for passage carving"""
    print(f"OblongGrid({rows}, {columns})")
    return Maze(OblongGrid(rows, columns))

def main(rows:int, cols:int, n:int, use_stack:bool):
    """the main entry point"""
    maze = make_grid(rows, cols)
    seeds = rng.choices(list(maze.grid), k=n)
    indices = list(seed.index for seed in seeds)
    print("Seed cells:", indices)

    if use_stack:
        print(f"Watershed(grid, seeds, QueueType=Stack)")
        watershed = Watershed(maze.grid, seeds, QueueType=Stack)
    else:
        print(f"Watershed(grid, seeds)  # default: QueueType=Queue)")
        watershed = Watershed(maze.grid, seeds)

    print("Beginning the round robin...")
    passes = 1
    while watershed.round_robin():
        passes += 1
    print(f"\tcompleted after {passes} passes.")

    print("Creating the component maze...")
    cmaze = watershed.initialize_maze()
    print(f"\t{len(cmaze.grid)} cells, expected {n}")
    assert len(cmaze.grid) == n

    print("\trunning Aldous/Broder...")
    print("\t\t(should be quick, but there are no guarantees)")
    AldousBroder.on(cmaze)
    print(f"\t{len(cmaze)} joins")

    print("Carving the floodgates:")
    gates = watershed.doors(cmaze)
    for gate in gates:
        assert isinstance(gate, set)
        cell1, cell2 = gate
        print(f"\tfloodgate: {cell1.index, cell2.index}")
        maze.link(cell1, cell2)

    watershed.label()
    print(maze)
        
def parse_args(argv):
    """parse the command line arguments"""
    import argparse

    DESC = "Watershed demonstration"
    EPI = "Output is to the console."
    default_dim = (8, 13)
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    parser.add_argument('-d', '--dim', type=int, nargs=2, \
        default=default_dim, metavar=('ROWS', 'COLS'), \
        help='the numbers of rows and columns in the maze.' \
        + f'  (Default: {default_dim}.)')

    shed = parser.add_argument_group('watershed options')
    shed.add_argument('-n', '--seeds', type=int, default=2, \
        help='The number of seeds.' \
        + f'  (Default: 2)')
    shed.add_argument('-s', '--stack', action="store_true", \
        help='Use stacks instead of queues.')
    args = parser.parse_args(argv)

    rows, cols = args.dim
    if args.seeds < 2:
        raise ValueError("Minimum is two seeds.")
    main(rows, cols, args.seeds, args.stack)

if __name__ == "__main__":
    import sys
    parse_args(sys.argv[1:])

# end module demos.watershed
