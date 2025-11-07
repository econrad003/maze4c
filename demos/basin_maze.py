"""
demos.basin_maze - carve mazes in watershed basins
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Here we demonstrate how mazes can be carved directly in the basins
    produced by the Watershed class.

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

    usage: watershed_partial.py [-h] [-n SEEDS] [-s]

    Watershed demonstration with some land areas

    options:
      -h, --help        show this help message and exit

    watershed options:
      -n SEEDS, --seeds SEEDS
                        The number of seeds. (Default: 2)
      -s, --stack           Use stacks instead of queues.

    Output is to the console.
"""
import mazes
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.watershed import Watershed
from mazes.Algorithms.dfs_better import DFS
from mazes.Algorithms.bfs import BFS
from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.kruskal import Kruskal
from mazes.Queues.stack import Stack
from mazes.round_robin import RoundRobin

def make_grid(rows, columns) -> Maze:
    """returns a maze object that is ready for passage carving"""
    print("        # create a Maze instance")
    print("from mazes.Grids.oblong import OblongGrid")
    print("from mazes.maze import Maze")
    print(f"maze = Maze(OblongGrid({rows}, {columns}))")
    print(f"grid = maze.grid")
    return Maze(OblongGrid(rows, columns))

def seed_grid(maze:Maze, n:int=4):
    """get the seeds"""
    print(f"        # get {n} seed cells to use as pumps")
    print("from mazes import rng")
    print("seeds = rng.sample(list(maze.grid), n)")
    seeds = rng.sample(list(maze.grid), n)
    s = "["
    for seed in seeds:
        i, j = seed.index
        s += f"grid[{i},{j}], "
    s = s[:-2]
    s += "]"
    print(f"# --> seeds: {s}")
    return seeds

def round_robin(maze:Maze, seeds:list, use_stack:bool):
    """create a round robin watershed"""
    print("        # create a round robin watershed")
    print("from mazes.round_robin import RoundRobin")
    print("scheduler = RoundRobin()")
    scheduler = RoundRobin()
    if use_stack:
        print("from mazes.Queues.stack import Stack    # using a stack")
        print("watershed = Watershed(grid, seeds, QueueType=Stack,",
              "tournament=scheduler)")
        watershed = Watershed(maze.grid, seeds, QueueType=Stack, tournament=scheduler)
    else:
        print("watershed = Watershed(grid, seeds, tournament=scheduler)",
              "   # using a queue")
        watershed = Watershed(maze.grid, seeds, tournament=scheduler)
    return watershed

def unweighted_tournament(maze:Maze, seeds:list, use_stack:bool):
    """create an unweighted tournament watershed"""
    print("        # create an unweighted tournament watershed")
    if use_stack:
        print("from mazes.Queues.stack import Stack    # using a stack")
        print("watershed = Watershed(grid, seeds, QueueType=Stack)")
        watershed = Watershed(maze.grid, seeds, QueueType=Stack)
    else:
        print("watershed = Watershed(grid, seeds)    # using a queue")
        watershed = Watershed(maze.grid, seeds)
    return watershed

def weighted_tournament(maze:Maze, seeds:list, use_stack:bool, weights:list):
    """create a weighted tournament watershed"""
    print("        # create a weighted tournament watershed")
    tweights = dict()
    for i in range(len(weights)):
        tweights[i] = weights[i]
    print("weights =", tweights)
    if use_stack:
        print("from mazes.Queues.stack import Stack    # using a stack")
        print("watershed = Watershed(grid, seeds, QueueType=Stack,",
              "targs=weights)")
        watershed = Watershed(maze.grid, seeds, QueueType=Stack, targs=tweights)
    else:
        print("watershed = Watershed(grid, seeds,",
              "targs=weights)    # using a queue")
        watershed = Watershed(maze.grid, seeds, targs=tweights)
    return watershed

def build_basins(watershed:Watershed):
    """build the basins"""
    print("        # map the basins (coding loop)")
    print("passes = 1")
    print("while watershed.round_robin():")
    print("    passes += 1")
    passes = 1
    while watershed.round_robin():
        passes += 1
    print(f"# --> completed after {passes=}.")

def build_floodgates(maze, n, watershed:Watershed):
    """carve the floodgates"""
    print("        # carve the floodgates separating the basins")
    print("cmaze = watershed.initialize_maze()    # simplified basin map")
    cmaze = watershed.initialize_maze()
    print(f"# --> {len(cmaze.grid)} cells in map, expected {n}")
    print("from mazes.Algorithms.kruskal import Kruskal  # floodgate carver")
    print("print(Kruskal.on(cmaze))")
    print(Kruskal.on(cmaze))
    print("gates = watershed.doors(cmaze)   # now carving")
    gates = watershed.doors(cmaze)
    print("#   connecting the gates (loop)")
    print("for gate in gates:")
    print("    cell1, cell2 = gate")
    print("    maze.link(cell1, cell2)")
    s = "floodgate indices: "
    for gate in gates:
        assert isinstance(gate, set)
        cell1, cell2 = gate
        i, j = cell1.index
        c1 = f"({i},{j})" 
        i, j = cell2.index
        c2 = f"({i},{j})"
        s += "{" + f"{c1},{c2}" + "}, "
        maze.link(cell1, cell2)
    s = s[:-2]
    print(f"# --> {s}")

def label_basins(watershed:Watershed):
    """label the basins"""
    print("        # labelling the basins...")
    print("watershed.label()")
    watershed.label()

def carve_basins(maze:Maze, watershed:Watershed):
    """carve mazes in the basins"""
    print("        # carve mazes in the basins (loop)")
    print("from mazes.Algorithms.dfs_better import DFS")
    print("from mazes.Algorithms.bfs import BFS")
    print("from mazes.Algorithms.wilson import Wilson")
    print("algorithms = [Wilson, BFS, DFS]")
    print("for basin in watershed.basins:")
    print("    cells = set(watershed.basins[basin])")
    print("    for cell in grid._cells:        # all the cells")
    print("        if cell in cells:")
    print("            cell.reveal()")
    print("        else:")
    print("            cell.hide()")
    print("    Carver = algorithms.pop() if algorithms else Kruskal")
    print("    print(f'{basin=}:', Carver.on(maze))")
    print("for cell in grid._cells:        # all the cells")
    print("    cell.reveal()")
    print("# " + "-" * 30 + " CARVING RESULTS " + "-" * 30)
    algorithms = [Wilson, BFS, DFS]
    for basin in watershed.basins:
        cells = set(watershed.basins[basin])
        for cell in maze.grid._cells:
            if cell in cells:
                cell.reveal()
            else:
                cell.hide()
        Carver = algorithms.pop() if algorithms else Kruskal
        print(f"{basin=}:", Carver.on(maze))
    for cell in maze.grid._cells:
        cell.reveal()
    print("# " + "-" * 77)
    print(f"#    number of cells = {len(maze.grid)}")
    print(f"# number of passages = {len(maze)}")

def main(rows, cols, n:int=4, use_stack:bool=False, use_rr:bool=False,
         weights:list=None) -> Maze:
    """the main entry point"""
    maze = make_grid(rows, cols)
    seeds = seed_grid(maze, n)
    if use_rr:
        watershed = round_robin(maze, seeds, use_stack)
    elif weights:
        watershed = weighted_tournament(maze, seeds, use_stack, weights)
    else:
        watershed = unweighted_tournament(maze, seeds, use_stack)
    build_basins(watershed)
    build_floodgates(maze, n, watershed)
    label_basins(watershed)
    carve_basins(maze, watershed)
    return maze
        
def parse_args(argv) -> Maze:
    """parse the command line arguments"""
    import argparse

    DESC = "Watershed demonstration with mazes carved in the basins."
    EPI = "Output is to the console.  The basin carving algorithms are" \
        + " respectively DFS, BFS, Wilson, and Kruskal.  Kruskal will" \
        + " be used whenever there are four or more basins." 
    parser = argparse.ArgumentParser(description=DESC, epilog=EPI)

    shed = parser.add_argument_group('watershed options')
    shed.add_argument("-d", "--dim", type=int, nargs=2, \
        default=(8, 13), metavar=("ROWS", "COLS"), \
        help="the dimensions of the underlying grid.")
    shed.add_argument('-n', '--seeds', type=int, default=4, \
        help='The number of pumps.' \
        + f'  (Default: 4)')
    shed.add_argument("--round_robin", action="store_true", \
        help='use a round robin scheduler.')
    shed.add_argument('-s', '--stack', action="store_true", \
        help='Use stacks instead of queues.')
    shed.add_argument("--task_args", type=int, nargs="*", default=list(), \
        metavar="WGT", help="tournament task weights.")
    args = parser.parse_args(argv)

    if args.seeds < 2:
        raise ValueError("Minimum is two seeds.")
    print(args)
    return main(*args.dim, n=args.seeds, use_stack=args.stack,
                use_rr=args.round_robin, weights=args.task_args)

if __name__ == "__main__":
    import sys
    maze = parse_args(sys.argv[1:])
    print("#        display the result")
    print("print(maze)")
    print(maze)

# end module demos.watershed_partial
