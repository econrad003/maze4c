"""
mazes.misc.maze_group.py - set up the maze group
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module choses the maze crafting algorithm.

NOTES ON THE OPTIONS

    start - used by most algorithms for an optional starting cell;
        the default is to let the algorithm select a starting cell at
        random.

        The following algorithms _do NOT_ use starting cells:
            BFF (breadth-first forest)
            DFF (depth-first forest)
            Eller
            Inwinder
            MTRandomWalk
            OutwardEller
            RecursiveDivision
            Sidewinder
            BinaryTree (Simple)
            SPF (simplified Prim forest)
            VPF (vertex Prim forest)

    bias1 - used by the following algorithms for a coin flip:
            Eller
            Inwinder
            OutwardEller
            Outwinder
            Sidewinder
            BinaryTree (Simple)
        The default is a fair coin, i.e. a probability of 0.5 or 1/2.

    noshuffle - used by the following algorithms to suppress shuffling
        of neighborhoods:
            BFS
            BFF (breadth-first forest)
            DFS
            DFF (depth-first forest)
            Kruskal
            SimplifiedPrim
            SPF (simplified Prim forest)
        In general, runs will be faster if shuffling is suppressed, but
        the results will tend to exhibit more bias.  For example, DFS
        without shuffling tends to produce a maze with one extremely long
        passage with few turns.  (Actual results depend on the Python
        version and how dictionaries are implemented.)

    threads - used by the following algorithms:
            DFF (depth-first forest and relatives)
            MTRandomWalk
            WatershedDivision
        The following methods use the DFF algorithm class as their entry
        point:
                name                                method
            --------------------------------------- ------
            depth-first forest                      dff
            breadth-first forest                    bff
            simplified Prim forest                  spf
            vertex Prim forest                      vpf
            pure Prim forest                        ppf

    thread_weights - used by the following algorithms
            BFF (breadth-first forest)
            DFF (depth-first forest)
            MTRandomWalk
            SPF (simplified Prim forest)
            VPF (vertex Prim forest)
            WatershedDivision

        Used to set thread weights when the tournament scheduler is used.

    round_robin - used by the following algorithms:
            BFF (breadth-first forest)
            DFF (depth-first forest)
            MTRandomWalk
            SPF (simplified Prim forest)
            VPF (vertex Prim forest)
            WatershedDivision

        If True, the round robin scheduler will be used.  Otherwise the
        tournament scheduler will be used.

    eller_rate - a probability used in merging by Eller's algorithm;
        used by:
            Eller
            OutwardEller

    hcut - horizonal cut weight; used by:
            RecursiveDivision

    vcut - vertical cut weight; used by:
            RecursiveDivision

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
import math
def normal_round(n:float) -> int:
    """round half up"""
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)

import mazes
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.misc.maze_parser import MazeParser
from mazes.misc.oblong import twoD_grid_parser as grid_parser

def mode(a:int, b:int, mode:float) -> int:
    """triangular distribution range, if applicable"""
    assert type(a) == int and type(b) == int
    dz = b - a - 1
    if dz == 0:
        return a                            # trivial
    assert dz > 0
    da = normal_round(rng.triangular(mode=mode) * dz)
    assert 0 <= da <= dz
    return a + da                           # integer triangular

def aldous_broder(maze:"Maze", args:"Namespace"):
    """Aldous/Broder first entrance random walk"""
    from mazes.Algorithms.aldous_broder import AldousBroder
    return AldousBroder.on(maze, start_cell=args.start)

def bfs(maze:"Maze", args:"Namespace"):
    """breadth-first search"""
    from mazes.Algorithms.bfs import BFS
    return BFS.on(maze, start_cell=args.start, shuffle=not args.no_shuffle)

def bff(maze:"Maze", args:"Namespace"):
    """breadth-first forest"""
    from mazes.Algorithms.dff import DFF, Task
    from mazes.round_robin import RoundRobin
    from mazes.Queues.queue import Queue

    class TaskBFF(Task):
        """a wrapper for the task class"""

        def __init__(self, taskID:int):
            """constructor"""
            super().__init__(taskID, QueueType=Queue)

    class BFF(DFF):
        """wrapper for DFF class"""
        class Status(DFF.Status):
            """wrapper for DFF.Status class"""
            NAME = "Breadth-first Forest (BFF)"

    n = args.threads
    tasks = list()
    for i in range(n):
        tasks.append(TaskBFF(i))
    tasks = tuple(tasks)

    targs = tuple(args.thread_weights) if args.thread_weights else None
    if targs:
        if not args.quiet:
            print("thread weights =", tuple(targs))

    if args.round_robin:
        return BFF.on(maze, *tasks, Scheduler=RoundRobin,
                      shuffle=not args.no_shuffle)
    else:
        return BFF.on(maze, *tasks, weights=targs,
                      shuffle=not args.no_shuffle)

def dfs(maze:"Maze", args:"Namespace"):
    """depth-first search"""
    from mazes.Algorithms.dfs_better import DFS
    return DFS.on(maze, start_cell=args.start, shuffle=not args.no_shuffle)

def dff(maze:"Maze", args:"Namespace"):
    """depth-first forest"""
    from mazes.Algorithms.dff import DFF
    from mazes.round_robin import RoundRobin

    targs = tuple(args.thread_weights) if args.thread_weights else None
    if targs:
        if not args.quiet:
            print("thread weights =", tuple(targs))
    if args.round_robin:
        return DFF.on(maze, args.threads, Scheduler=RoundRobin,
                      shuffle=not args.no_shuffle)
    else:
        return DFF.on(maze, args.threads, weights=targs,
                      shuffle=not args.no_shuffle)

def eller(maze:"Maze", args:"Namespace"):
    """Eller's algorithm"""
    from mazes.Algorithms.eller import Eller, coin_toss
    return Eller.on(maze, flip1=(coin_toss, (), {"bias":args.bias1}),
                    flip2=(coin_toss, (), {"bias":args.eller_rate}))

def houston(maze:"Maze", args:"Namespace"):
    """Houston's algorithm"""
    from mazes.Algorithms.houston import Houston
    cutoff, failure = args.houston_rates
    return Houston.on(maze, start_cell=args.start,
                      cutoff_rate=cutoff, failure_rate=failure)

def hunt_and_kill(maze:"Maze", args:"Namespace"):
    """hunt and kill"""
    from mazes.Algorithms.hunt_kill import HuntKill
    return HuntKill.on(maze, start_cell=args.start)

def inwinder(maze:"Maze", args:"Namespace"):
    """inwinder"""
    from mazes.Algorithms.inwinder import Inwinder
    return Inwinder.on(maze, bias=args.bias1)

def kruskal(maze:"Maze", args:"Namespace"):
    """Kruskal's algorithm"""
    from mazes.Algorithms.kruskal import Kruskal
    return Kruskal.on(maze, shuffle=not args.no_shuffle)

def mt_random_walk(maze:"Maze", args:"Namespace"):
    """multithreaded first entry random walk algorithm"""
    from mazes.Algorithms.mt_random_walk import MTRandomWalk
    from mazes.round_robin import RoundRobin

    targs = list()
    if args.thread_weights:
        for item in args.thread_weights:
            targs.append(tuple([item]))
        if not args.quiet:
            print("thread weights =", tuple(targs))
    if args.round_robin:
        return MTRandomWalk.on(maze, args.threads, scheduler=RoundRobin())
    else:
        return MTRandomWalk.on(maze, args.threads, task_args=targs)

def outward_eller(maze:"Maze", args:"Namespace"):
    """Eller's algorithm"""
    from mazes.Algorithms.outward_eller import OutwardEller, coin_toss
    return OutwardEller.on(maze, flip1=(coin_toss, (), {"bias":args.bias1}),
                  flip2=(coin_toss, (), {"bias":args.eller_rate}))

def outwinder(maze:"Maze", args:"Namespace"):
    """outwinder"""
    from mazes.Algorithms.outwinder import Outwinder
    return Outwinder.on(maze, bias=args.bias1)

def prim(maze:"Maze", args:"Namespace"):
    """Prim's algorithm"""
    from mazes.Algorithms.growing_tree2 import ArcGrowingTree as AGT
    from mazes.Queues.priority_queue import PriorityQueue

    priorities = dict()
    edges = set()
    for cell in maze.grid:
        for nbr in cell.neighbors:
            edge = frozenset([cell, nbr])
            edges.add(edge)
    edges = list(edges)
    rng.shuffle(edges)
    for i in range(len(edges)):
        edge = edges[i]
        priorities[edge] = i
    pr = lambda cell, nbr: priorities[frozenset([cell, nbr])]

    return AGT.on(maze, start_cell=args.start, shuffle=False,
                  QueueClass=PriorityQueue, priority=pr)

def recursive_division(maze:"Maze", args:"Namespace"):
    """recursive division"""
    from mazes.Algorithms.recursive_division import RecursiveDivision
    if args.hmode >= 0 and args.hmode <= 1:
        if not args.quiet:
            print(f"  horizontal cut mode={args.hmode}")
        hrand = lambda a, b: mode(a, b, args.hmode)
    else:
        hrand = rng.randrange
    if args.vmode >= 0 and args.vmode <= 1:
        if not args.quiet:
            print(f"   vertical cut mode={args.vmode}")
        vrand = lambda a, b: mode(a, b, args.vmode)
    else:
        vrand = rng.randrange
    return RecursiveDivision.on(maze, horizontal_cutter=hrand,
                                vertical_cutter=vrand)

def reverse_aldous_broder(maze:"Maze", args:"Namespace"):
    """reverse Aldous/Broder last exit random walk"""
    from mazes.Algorithms.reverse_aldous_broder import ReverseAldousBroder
    return ReverseAldousBroder.on(maze, start_cell=args.start)

def sidewinder(maze:"Maze", args:"Namespace"):
    """sidewinder"""
    from mazes.Algorithms.sidewinder import Sidewinder
    return Sidewinder.on(maze, bias=args.bias1)

def simple_binary_tree(maze:"Maze", args:"Namespace"):
    """simple_binary tree"""
    from mazes.Algorithms.simple_binary_tree import BinaryTree
    return BinaryTree.on(maze, bias=args.bias1)

def simplified_Prim(maze:"Maze", args:"Namespace"):
    """Breadth-first search"""
    from mazes.Algorithms.simplified_Prim import NotPrim
    return NotPrim.on(maze, start_cell=args.start, shuffle=not args.no_shuffle)

def spf(maze:"Maze", args:"Namespace"):
    """simplified Prim forest"""
    from mazes.Algorithms.dff import DFF, Task
    from mazes.round_robin import RoundRobin
    from mazes.Queues.priority_queue import PriorityQueue

    class TaskSPF(Task):
        """a wrapper for the task class"""

        def __init__(self, taskID:int):
            """constructor"""
            pr = lambda cell: 1
            super().__init__(taskID, QueueType=Queue, priority=pr)

    class SPF(DFF):
        """wrapper for DFF class"""
        class Status(DFF.Status):
            """wrapper for DFF.Status class"""
            NAME = "Simplified Prim Forest (SPF)"

    n = args.threads
    tasks = list()
    for i in range(n):
        tasks.append(TaskSPF(i))
    tasks = tuple(tasks)

    targs = tuple(args.thread_weights) if args.thread_weights else None
    if targs:
        if not args.quiet:
            print("thread weights =", tuple(targs))

    if args.round_robin:
        return SPF.on(maze, *tasks, Scheduler=RoundRobin,
                      shuffle=not args.no_shuffle)
    else:
        return SPF.on(maze, *tasks, weights=targs,
                      shuffle=not args.no_shuffle)

def vertex_Prim(maze:"Maze", args:"Namespace"):
    """vertex Prim"""
    from mazes.Algorithms.growing_tree1 import VertexGrowingTree as VGT
    from mazes.Queues.priority_queue import PriorityQueue

    priorities = dict()
    cells = list(maze.grid)
    rng.shuffle(cells)
    for i in range(len(cells)):
        priorities[cells[i]] = i
    pr = lambda cell: priorities[cell]

    return VGT.on(maze, start_cell=args.start, shuffle=False,
                  QueueClass=PriorityQueue, priority=pr)

def vpf(maze:"Maze", args:"Namespace"):
    """vertex Prim forest"""
    from mazes.Algorithms.dff import DFF, Task
    from mazes.round_robin import RoundRobin
    from mazes.Queues.priority_queue import PriorityQueue

    priorities = dict()
    cells = list(maze.grid)
    rng.shuffle(cells)
    for i in range(len(cells)):
        priorities[cells[i]] = i
    pr = lambda cell: priorities[cell]

    class TaskVPF(Task):
        """a wrapper for the task class"""

        def __init__(self, taskID:int):
            """constructor"""
            super().__init__(taskID, QueueType=PriorityQueue, priority=pr)

    class VPF(DFF):
        """wrapper for DFF class"""
        class Status(DFF.Status):
            """wrapper for DFF.Status class"""
            NAME = "Vertex Prim Forest (BFF)"

    n = args.threads
    tasks = list()
    for i in range(n):
        tasks.append(TaskVPF(i))
    tasks = tuple(tasks)

    targs = tuple(args.thread_weights) if args.thread_weights else None
    if targs:
        if not args.quiet:
            print("thread weights =", tuple(targs))

    if args.round_robin:
        return VPF.on(maze, *tasks, Scheduler=RoundRobin, shuffle=False)
    else:
        return VPF.on(maze, *tasks, weights=targs, shuffle=False)

def wilson(maze:"Maze", args:"Namespace"):
    """Wilson (circuit-eliminated random walk)"""
    from mazes.Algorithms.wilson import Wilson
    return Wilson.on(maze, start_cell=args.start)

def watershed_division(maze:"Maze", args:"Namespace"):
    """watershed division"""
    from mazes.Algorithms.watershed_division import WatershedDivision
    from mazes.round_robin import RoundRobin

    min_cells, pumps = args.watershed
    targs = dict()
    if args.thread_weights:
        for i in range(len(args.thread_weights)):
            targs[i] = (tuple([args.thread_weights[i]]))
        if not args.quiet:
            print("thread weights =", tuple(targs))
    return WatershedDivision.on(maze, min_cells, pumps)

    # additional arguments for the maze group

def noshuffle(mazegrp:"parser group"):
    """the no-shuffle option"""
    mazegrp.add_argument("--no_shuffle", action="store_true", \
        help="Algorithms that traverse neighborhoods normally shuffle" \
        + "the neighborhood in order to traverse the neighbors in" \
        + " random order.  Turning off shuffling is usually faster," \
        + " but less random.  This option turns off shuffling.")

def bias1(mazegrp:"parser group"):
    """coin toss bias"""
    mazegrp.add_argument("-b", "--bias1", type=float, default=0.5, \
        metavar="BIAS", help="a coin toss probability (default: 0.5)")

def eller_bias(mazegrp:"parser group"):
    """Eller's algorithm bias"""
    mazegrp.add_argument("--eller_rate", type=float, default=1/3, \
        metavar="BIAS", help="a probability for Eller's algorithm '(default: 0.333)")

def houston_rates(mazegrp:"parser group"):
    """Houston's algorithm rates"""
    mazegrp.add_argument("--houston_rates", type=float, nargs=2,
        default=(2/3, 0.9), metavar=("CUTOFF", "FAILURE"),
        help="percentage rates for Houston's algorithm (default: 0.667, 0.9)")

def threads(mazegrp:"parser group"):
    """threading arguments"""
    mazegrp.add_argument("--threads", type=int, default=2, metavar="N",
        help="number of threads for multi-threading (default: 2)")

def round_robin(mazegrp:"parser group"):
    """scheduler"""
    mazegrp.add_argument("--round_robin", action="store_true",
        help="set this option to use the round robin scheduler for multithreading")

def thread_weights(mazegrp:"parser group"):
    """thread weights"""
    mazegrp.add_argument("--thread_weights", type=int, nargs="*",
        default=list(), metavar="WGT",
        help="thread weights (one per thread, if used)")

def hmode_arg(mazegrp:"parser group"):
    """horizontal cut mode"""
    mazegrp.add_argument("--hmode", type=float, default=-1, metavar="WGT",
        help="horizontal mode value for recursive division")

def vmode_arg(mazegrp:"parser group"):
    """vertical cut mode"""
    mazegrp.add_argument("--vmode", type=float, default=-1, metavar="WGT",
        help="vertical mode value for recursive division")

def watershed(mazegrp:"parser group"):
    """watershed minimum and pumps"""
    mazegrp.add_argument("--watershed", type=int, nargs=2,
        default=(2, 3), metavar=("MIN", "PUMPS"),
        help="(default: 2 3) two integers -- the first is the minimum" \
        + " number of cells in a watershed; the second is the number of" \
        + " pumps to use.  (If the number of pumps exceeds he number of" \
        + " cells in the watershed, then each cell is a basin.  Otherwise" \
        + " the number of basins is the number of pumps.)" )

    # Algorithms table
    #   code -> (name, caller)
algorithms = dict()
algorithms["AB"] = ("Aldous/Broder (random walk, first exit)", aldous_broder)
algorithms["BFS"] = ("Breadth-first search", bfs)
algorithms["BFF"] = ("Breadth-first forest", bff)
algorithms["DFS"] = ("Depth-first search", dfs)
algorithms["DFF"] = ("Depth-first forest", dff)
algorithms["E"] = ("Eller's algorithm", eller)
algorithms["H"] = ("Houston's algorithm", houston)
algorithms["HK"] = ("hunt and kill", hunt_and_kill)
algorithms["IW"] = ("inwinder", inwinder)
algorithms["K"] = ("Kruskal's algorithm", kruskal)
algorithms["MRW"] = ("multithreaded random walk", mt_random_walk)
algorithms["OE"] = ("outward Eller's algorithm", outward_eller)
algorithms["OW"] = ("outwinder", outwinder)
algorithms["P"] = ("Prim's algorithm", prim)
algorithms["RD"] = ("recursive division", recursive_division)
algorithms["RAB"] = ("reverse Aldous/Broder (random walk, last exit)",
                      reverse_aldous_broder)
algorithms["SW"] = ("sidewinder", inwinder)
algorithms["SBT"] = ("simple binary tree", simple_binary_tree)
algorithms["SP"] = ("simplified 'Prim'", simplified_Prim)
algorithms["SPF"] = ("simplified Prim forest", bff)
algorithms["VP"] = ("vertex Prim", vertex_Prim)
algorithms["VPF"] = ("vertex Prim forest", vpf)
algorithms["W"] = ("Wilson (circuit-eliminated random walk)", wilson)
algorithms["WD"] = ("watershed division", watershed_division)

defaults = dict()
defaults["algorithm"] = "DFS"

def maze_parser(parser:MazeParser) -> "parser.group":
    """set up the parser"""
    mazegrp = parser.parser.add_argument_group("maze crafting arguments", \
        description="These arguments control the crafting of the maze.")
    parser.groups["maze"] = mazegrp
    alghelp = "This argument determines the maze crafting algorithm:"
    for item in algorithms:
        name = algorithms[item][0]
        alghelp += " " + item + "-" + name + ";"
    alghelp = alghelp[:-1] + "."
    mazegrp.add_argument("-a", "--algorithm", type=str, default="", help=alghelp)
    mazegrp.add_argument("--start", type=int, nargs=2, default=None, \
        help="optional start cell indices, where applicable")
    noshuffle(mazegrp)      # add shuffle option
    bias1(mazegrp)          # coin toss
    eller_bias(mazegrp)     # eller merge probability
    houston_rates(mazegrp)  # houston cutoff and failure rates
    threads(mazegrp)        # multithreaded algorithms
    round_robin(mazegrp)    #   ditto
    thread_weights(mazegrp) #   ditto
    hmode_arg(mazegrp)
    vmode_arg(mazegrp)
    watershed(mazegrp)
    return mazegrp

def twoD_grid_parser(parser:MazeParser, dim=(8, 13)) -> "parser.group":
    """set up a parser for a 2D rectangular maze"""
    gridgrp = grid_parser(parser)
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
    EPILOG = "Mode values, when used, should be between 0 and 1, inclusive." \
        + "  Values outside that interval, including the default (-1) will" \
        + " use randrange.  Values in the interval use a triangular " \
        + "distribution."
    parser = MazeParser(DESCR, EPILOG)
    parser.parser.add_argument("--quiet", action = "store_true",
        help="suppress console output")
    gridgrp = twoD_grid_parser(parser)
    mazegrp = maze_parser(parser)
        #   MORE STUFF GOES HERE
        #       plotter
    args = parser.parser.parse_args(argv)
    args.algorithm = args.algorithm.upper()
    if args.start:
        args.start = tuple(args.start)
    if not args.quiet:
        print(args)
    maze = make_maze(args, GridClass=OblongGrid)
    if args.start:
        args.start = maze.grid[args.start]
        if not args.quiet:
            print(f"{args.start=}")
        
    algtuple = algorithms.get(args.algorithm)
    if algtuple:
        name, alg = algtuple
        if not args.quiet:
            print(f"{name=}")
        status = alg(maze, args)
        if not args.quiet:
            print(status)
    else:
        print(parser.parser.print_help())
        print()
        print("ERROR:", "The algorithm selection (-a) is not defined",
                         f"({args.algorithm})")
        return
    
        #   MORE STUFF GOES HERE
        #       algorithm
        #       plot
    return maze

if __name__ == "__main__":
    import sys
    maze = main(sys.argv[1:])
    print(maze)
