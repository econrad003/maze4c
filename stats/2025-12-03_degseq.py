"""
stats.deg_seq - degree sequence statistics
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This program gathers degree sequence statistics for a number of
    algorithms.

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
from math import sqrt

import mazes
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze

failed = {"isolates":0}

N = 100                                 # 100 runs
ROWS, COLS = 41, 41
MAX_DEGREE = 4                          # N/S/E/W grid

noargs = tuple()
nokwargs = dict()
noshuffle = {"shuffle":False}
southwest = {"shuffle":False, "start_cell":(0,0)}
west = {"shuffle":False, "start_cell":(20,0)}
centered = {"shuffle":False, "start_cell":(20,20)}
bias25 = {"bias":0.25}
bias75 = {"bias":0.75}

vtype = {"prtype":"vertex",}
vtypen = {"prtype":"vertex", "shuffle":False}
vtypesw = {"prtype":"vertex", "shuffle":False, "start_cell":(0,0)}
vtypec = {"prtype":"vertex", "shuffle":False, "start_cell":(10,17)}

atype = {"prtype":"arc",}
atypen = {"prtype":"arc", "shuffle":False}
atypesw = {"prtype":"arc", "shuffle":False, "start_cell":(0,0)}
atypec = {"prtype":"arc", "shuffle":False, "start_cell":(10,17)}

grids = OblongGrid, (ROWS, COLS), nokwargs

def run(algo, debug):
    """run the algorithm"""
    GridType, gargs, gkwargs = grids
    maze = Maze(GridType(*gargs, **gkwargs))
    Algo, args, kwargs = algorithms[algo]
    if is_wall_builder(Algo):
        maze.link_all()
    if debug:
        print(algo, args, kwargs)
    if "start_cell" in kwargs:
        kwargs = kwargs.copy()
        kwargs["start_cell"] = maze.grid[kwargs["start_cell"]]
    status = Algo.on(maze, *args, **kwargs)
    return maze

from mazes.Algorithms.aldous_broder import AldousBroder         # baseline
from mazes.Algorithms.dfs_better import DFS                     # baseline
from mazes.Algorithms.bfs import BFS                            # baseline
from mazes.Algorithms.wilson import Wilson                      # baseline
from mazes.Algorithms.binary_growing_tree1 import BinaryGrowingTree as GreedyBinaryTree
from mazes.Algorithms.binary_growing_tree2 import BinaryGrowingTree as FairBinaryTree
from mazes.Algorithms.simple_binary_tree import BinaryTree

def is_wall_builder(Algo) -> bool:
    """passage carver (False) or wall builder (True)"""
    return False

algorithms = {}
    # baseline algorithms
algorithms["DFS"] = DFS, noargs, nokwargs
algorithms["BFS"] = DFS, noargs, nokwargs
algorithms["Aldous/Broder"] = AldousBroder, noargs, nokwargs
algorithms["Wilson"] = Wilson, noargs, nokwargs

    # simple binary tree
algorithms["SBT E/N p=0.25"] = BinaryTree, noargs, bias25
algorithms["SBT E/N p=0.5"] = BinaryTree, noargs, nokwargs
algorithms["SBT E/N p=0.75"] = BinaryTree, noargs, bias75

    # queuing types
from mazes.Queues.queue import Queue
qtype = {"QueueType":Queue}

from mazes.Queues.random_queue import RandomQueue
rqtype = {"QueueType":RandomQueue}

from mazes.Queues.split_stack import SplitStack
sstype1 = {"QueueType":SplitStack, "qkwargs":{"target_length":1}}
sstype10 = {"QueueType":SplitStack}

from mazes.Queues.split_queue import SplitQueue
sqtype1 = {"QueueType":SplitQueue, "qkwargs":{"target_length":1}}
sqtype10 = {"QueueType":SplitQueue}

from mazes.Queues.priority_queue import PriorityQueue
pqtype = {"QueueType":PriorityQueue}

    # greedy binary tree
algorithms["GBT/DFS"] = GreedyBinaryTree, noargs, nokwargs
algorithms["GBT/DFS rand=N"] = GreedyBinaryTree, noargs, noshuffle
algorithms["GBT/DFS rand=N SW"] = GreedyBinaryTree, noargs, southwest
algorithms["GBT/DFS rand=N W"] = GreedyBinaryTree, noargs, west
algorithms["GBT/DFS rand=N C"] = GreedyBinaryTree, noargs, centered

algorithms["GBT/BFS"] = GreedyBinaryTree, noargs, qtype
algorithms["GBT/BFS rand=N"] = GreedyBinaryTree, noargs, {**noshuffle, **qtype}
algorithms["GBT/BFS rand=N SW"] = GreedyBinaryTree, noargs, {**southwest, **qtype}
algorithms["GBT/BFS rand=N W"] = GreedyBinaryTree, noargs, {**west, **qtype}
algorithms["GBT/BFS rand=N C"] = GreedyBinaryTree, noargs, {**centered, **qtype}

algorithms["GBT/SS TL=1"] = GreedyBinaryTree, noargs, sstype1
algorithms["GBT/SS TL=10"] = GreedyBinaryTree, noargs, sstype10
algorithms["GBT/SQ TL=1"] = GreedyBinaryTree, noargs, sqtype1
algorithms["GBT/SQ TL=10"] = GreedyBinaryTree, noargs, sqtype10
algorithms["GBT/PQ cache"] = GreedyBinaryTree, noargs, pqtype

    # fair binary tree
algorithms["FBT/DFS"] = FairBinaryTree, noargs, nokwargs
algorithms["FBT/DFS rand=N"] = FairBinaryTree, noargs, noshuffle
algorithms["FBT/DFS rand=N SW"] = FairBinaryTree, noargs, southwest
algorithms["FBT/DFS rand=N W"] = FairBinaryTree, noargs, west
algorithms["FBT/DFS rand=N C"] = FairBinaryTree, noargs, centered

algorithms["FBT/BFS"] = FairBinaryTree, noargs, qtype
algorithms["FBT/BFS rand=N"] = FairBinaryTree, noargs, {**noshuffle, **qtype}
algorithms["FBT/BFS rand=N SW"] = FairBinaryTree, noargs, {**southwest, **qtype}
algorithms["FBT/BFS rand=N W"] = FairBinaryTree, noargs, {**west, **qtype}
algorithms["FBT/BFS rand=N C"] = FairBinaryTree, noargs, {**centered, **qtype}

algorithms["FBT/SS TL=1"] = FairBinaryTree, noargs, sstype1
algorithms["FBT/SS TL=10"] = FairBinaryTree, noargs, sstype10
algorithms["FBT/SQ TL=1"] = FairBinaryTree, noargs, sqtype1
algorithms["FBT/SQ TL=10"] = FairBinaryTree, noargs, sqtype10

algorithms["FBT/RQ"] = FairBinaryTree, noargs, rqtype
algorithms["FBT/PQ cache"] = FairBinaryTree, noargs, pqtype

from mazes.Algorithms.dijkstra import Dijkstra

def diameter(maze):
    """diameter for a perfect maze"""
    start = maze.grid[0,0]
    dijkstra = Dijkstra(maze, start)
    source = dijkstra.farthest
    dijkstra.calculate(source)
    target = dijkstra.farthest
    return dijkstra.distance(target)

from mazes.edge import Edge

def capture_stats(algo, max_degree, debug=False):
    """capture the diameter and the degree sequence"""
    
    maze = run(algo, debug)
    stats = dict()
    for i in range(max_degree+1):
        stats[i] = 0
    stats["degsum"] = 0
    for cell in maze.grid:
        stats[len(list(cell.passages))] += 1
        stats["degsum"] += len(list(cell.passages))
    stats["v"] = len(maze.grid)
    stats["e"] = 0
    stats["a"] = 0
    for join in maze:
        if isinstance(join, Edge):
            stats["e"] += 1
        else:
            stats["a"] += 1
    if stats[0] == 0:
        stats["d"] = diameter(maze)
    else:
        stats["d"] = stats["v"]
        failed["isolates"] += 1
    stats["algo"] = algo
    stats["horiz"] = 0
    stats["vert"] = 0
    stats["turn"] = 0
    for cell in maze.grid:              # degree 2 analysis
        if len(list(cell.passages)) != 2:
            continue
        if cell.is_linked(cell.north) and cell.is_linked(cell.south):
            stats["vert"] += 1
            continue
        if cell.is_linked(cell.east) and cell.is_linked(cell.west):
            stats["horiz"] += 1
            continue
        stats["turn"] += 1
    return stats

def headings(max_degree):
    """column headings"""
    headers = list()
    indices = dict()
    def header(name, value):
        """set the heading and indices"""
        headers.append(name)
        indices[name] = value

    header("algorithm", "algo")
    header("isolates", 0)
    header("dead ends", 1)
    for i in range(2, max_degree+1):
        header(f"degree {i}", i)
    header("degree sum", "degsum")
    header("cells", "v")
    header("edges", "e")
    header("arcs", "a")
    header("diameter", "d")
    header("N--S", "vert")
    header("E--W", "horiz")
    header("turns", "turn")
    return headers, indices

def quick_csv(filename):
    """just run each algorithm once"""
    keys = list(algorithms.keys())
    headers, indices = headings(MAX_DEGREE)
    with open(filename, "w") as fout:
        fout.write(", ".join(headers) + "\n")
        for key in keys:
            stats = capture_stats(key, MAX_DEGREE, debug=True)
            stats2 = list()
            for header in headers:
                index = indices[header]
                stats2.append(str(stats[index]))
            fout.write(", ".join(stats2) + "\n")

def gather(algo, runs):
    """average of some runs"""
    print(algo, end="")
    stats = list()
    for i in range(runs):
        # print(algo, i)
        print(".", end="", flush=True)
        result = capture_stats(algo, MAX_DEGREE)
        del result["algo"]
        stats.append(result)
    print()
    sumX = dict()
    sumXX = dict()
    for key in stats[0]:
        sumX[key] = 0
        sumXX[key] = 0
    for line in stats:
        for key in line:
            sumX[key] += line[key]
            sumXX[key] += line[key] ** 2
    averages = dict()
    stddevs = dict()
    for key in sumX:
        mean = sumX[key] / runs
        averages[key] = mean
        meanXX = sumXX[key] / runs
        variance = meanXX - mean ** 2
        stddev = sqrt(variance)
        stddevs[key] = stddev
    averages["algo"] = algo
    stddevs["algo"] = "std deviation"
    return averages, stddevs

def gather_all(filename, runs):
    """averages of everything"""
    keys = list(algorithms.keys())
    headers, indices = headings(MAX_DEGREE)
    with open(filename, "w") as fout:
        fout.write(", ".join(headers) + "\n")
        for key in keys:
            # print(key, "...")
            means, stdevs = gather(key, runs)
            stats2 = list()
            for header in headers:
                index = indices[header]
                value = means[index]
                if type(value) == float:
                    value = "%5.3f" % value
                stats2.append(str(value))
            fout.write(", ".join(stats2) + "\n")
            stats2 = list()
            for header in headers:
                index = indices[header]
                value = stdevs[index]
                if type(value) == float:
                    value = "%5.3f" % value
                stats2.append(str(value))
            fout.write(", ".join(stats2) + "\n")

#foo = list(algorithms.keys())
#for bar in foo:
#    print(bar, capture_stats(bar, 4))

#quick_csv("output.csv")

#means, stdevs = gather("Wilson", 20)
#print(means)
#print(stdevs)

gather_all("output.csv", N)

if failed["isolates"] == 0:
    print("All runs terminated with spanning trees.")
else:
    print(failed["isolates"], "runs terminated without a spanning tree.")
    print("For these runs, the diameter was taken to be the number of cells.")
    print("These runs will have at least one isolated vertex.")

# end module mazes.stats.degseq
