"""
stats.deg_seq - degree sequence statistics
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This program gathers degree sequence statistics for a number of
    algorithms.

    This differs in the selection of algorithms.  In this sampling,
    emphasis is on four passes of fractal tessellation to produce
    a 16x16 rectangular maze.

    Some algorithms are omitted based on results from the samplings
    of 7 and 8 October 2025.  For uniform 16x16 mazes, we use Wilson's
    algorithm -- Aldous/Broder is slower, and limitations due to use
    of Python's pseudorandom module ("random") did not seem to create
    significant differences between the implementations of the two
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

n = 100                                 # 100 runs
noargs = tuple()
nokwargs = dict()

grids = OblongGrid, (16, 16), nokwargs, 4

# from mazes.Algorithms.aldous_broder import AldousBroder
from mazes.Algorithms.bfs import BFS
from mazes.Algorithms.dfs_better import DFS
# from mazes.Algorithms.dff import DFF
# from mazes.Algorithms.dff import Task as DFF_Task
from mazes.Algorithms.eller import Eller
# from mazes.Algorithms.houston import Houston
from mazes.Algorithms.hunt_kill import HuntKill
from mazes.Algorithms.inwinder import Inwinder
from mazes.Algorithms.kruskal import Kruskal
# from mazes.Algorithms.mt_random_walk import MTRandomWalk
from mazes.Algorithms.outward_eller import OutwardEller
from mazes.Algorithms.outwinder import Outwinder
# from mazes.Algorithms.recursive_division import RecursiveDivision
from mazes.Algorithms.sidewinder import Sidewinder
from mazes.Algorithms.simple_binary_tree import BinaryTree as BinaryTree1
from mazes.Algorithms.wilson import Wilson

# class BFF(object):
#    """breadth first forest"""
#    @classmethod
#    def on(cls, maze, n):
#        """filter for DFF"""
#        tasks = list()
#        for i in range(n):
#            task = DFF_Task(i, QueueType=Queue)
#            tasks.append(task)
#        return DFF.on(maze, *tasks)

class VertexPrim(object):
    """vertex Prim"""
    @classmethod
    def on(cls, maze):
        """filter for vprim"""
        from mazes.VGT.vprim import vprim
        return vprim(maze)

class SimplifiedPrim(object):
    """simplified Prim"""
    @classmethod
    def on(cls, maze):
        """filter for sprim"""
        from mazes.VGT.sprim import sprim
        return sprim(maze)

class Prim(object):
    """Prim's algorithm"""
    @classmethod
    def on(cls, maze):
        """filter for primic"""
        from mazes.AGT.primic import primic
        pr = dict()
        for cell in maze.grid:
            for nbr in cell.neighbors:
                edge = frozenset([cell, nbr])
                pr[edge] = rng.random()
        return primic(maze, pr_map=pr)           # a priori priorities

    # ADDED
from mazes.Algorithms.fractal_tess import FractalTessellation
from mazes.Algorithms.dihedral import DihedralGroup
from mazes.Algorithms.rotation_subgroup import RotationGroup

class FracTess(object):
    """filter for fractal tesselation"""
    @classmethod
    def on(cls, symmetries:bool, Group:callable=DihedralGroup):
        """create a 16x16 fractal maze"""
        tess = FractalTessellation(symmetries=symmetries)
        return tess.on(passes=4, SymmetryGroup=Group, verbose=False)

algorithms = {}
#algorithms["Aldous/Broder"] = AldousBroder, noargs, nokwargs
algorithms["Binary Tree/Simple"] = BinaryTree1, noargs, nokwargs
algorithms["Breadth-first search"] = BFS, noargs, nokwargs
#algorithms["Breadth-first forest/2 tasks"] = BFF, (2,), nokwargs
#algorithms["Breadth-first forest/3 tasks"] = BFF, (3,), nokwargs
algorithms["Depth-first search"] = DFS, noargs, nokwargs
#algorithms["Depth-first forest/2 tasks"] = DFF, (2,), nokwargs
#algorithms["Depth-first forest/3 tasks"] = DFF, (3,), nokwargs
algorithms["Eller"] = Eller, noargs, nokwargs
#algorithms["Houston"] = Houston, noargs, nokwargs
algorithms["Fractal Tess/ident"] = FracTess, (False,), nokwargs
algorithms["Fractal Tess/rotate"] = FracTess, (True, RotationGroup), nokwargs
algorithms["Fractal Tess/dihedral"] = FracTess, (True,), nokwargs
algorithms["Hunt & Kill"] = HuntKill, noargs, nokwargs
algorithms["Inwinder"] = Inwinder, noargs, nokwargs
algorithms["Kruskal"] = Kruskal, noargs, nokwargs
#algorithms["MT Randon Walk/2 tasks"] = MTRandomWalk, (2,), nokwargs
#algorithms["MT Random Walk/3 tasks"] = MTRandomWalk, (3,), nokwargs
algorithms["Outward Eller"] = OutwardEller, noargs, nokwargs
algorithms["Outwinder"] = Outwinder, noargs, nokwargs
algorithms["Prim"] = Prim, noargs, nokwargs
algorithms["Prim/Vertex"] = VertexPrim, noargs, nokwargs
algorithms["Prim/Simplified"] = SimplifiedPrim, noargs, nokwargs
#algorithms["Recursive Division"] = RecursiveDivision, noargs, nokwargs
algorithms["Sidewinder"] = Sidewinder, noargs, nokwargs
algorithms["Wilson"] = Wilson, noargs, nokwargs

def make_grid(GridType:"Grid", *args, **kwargs) -> Maze:
    """make a grid"""
    return Maze(GridType(*args, **kwargs))

def make_maze(maze:Maze, Algorithm:'Algorithm', *args, **kwargs):
    """carve a maze"""
    return Algorithm.on(maze, *args, **kwargs)

def carve(algo):
    """carve a maze"""
    if algorithms[algo][0] == FracTess:
        Algo, args, kwargs = algorithms[algo]
        maze = Algo.on(*args, **kwargs)
        status = "done"
    else:
        GridType, args, kwargs, _ = grids
        maze = make_grid(GridType, *args, **kwargs)
        Algo, args, kwargs = algorithms[algo]
        status = make_maze(maze, Algo, *args, **kwargs)
    return maze, status

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

def capture_stats(algo, max_degree):
    """capture the diameter and the degree sequence"""
    maze, status = carve(algo)
    stats = dict()
    for i in range(max_degree+1):
        stats[i] = 0
    stats["degsum"] = 0
    for cell in(maze.grid):
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
    stats["d"] = diameter(maze)
    stats["algo"] = algo
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
    return headers, indices

def quick_csv(filename):
    """just run each algorithm once"""
    keys = list(algorithms.keys())
    max_degree = grids[3]
    headers, indices = headings(max_degree)
    with open(filename, "w") as fout:
        fout.write(", ".join(headers) + "\n")
        for key in keys:
            stats = capture_stats(key, max_degree)
            stats2 = list()
            for header in headers:
                index = indices[header]
                stats2.append(str(stats[index]))
            fout.write(", ".join(stats2) + "\n")

def gather(algo, runs):
    """average of some runs"""
    max_degree = grids[3]
    stats = list()
    for i in range(runs):
        # print(algo, i)
        result = capture_stats(algo, max_degree)
        del result["algo"]
        stats.append(result)
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
    max_degree = grids[3]
    headers, indices = headings(max_degree)
    with open(filename, "w") as fout:
        fout.write(", ".join(headers) + "\n")
        for key in keys:
            print(key, "...")
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

#algorithms = {}
#algorithms["Fractal Tess/ident"] = FracTess, (False,), nokwargs
#algorithms["Fractal Tess/rotate"] = FracTess, (True,), {"Group":RotationGroup}
#algorithms["Fractal Tess/dihedral"] = FracTess, (True,), nokwargs
#algorithms["Sidewinder"] = Sidewinder, noargs, nokwargs
#for item in algorithms:
#    maze, status = carve(item)
#    print(item)
#    print(status)
#    print(maze)

#foo = list(algorithms.keys())
#for bar in foo:
#    print(bar, capture_stats(bar, 4))

#quick_csv("output.csv")

#means, stdevs = gather("Eller", 20)
#print(means)
#print(stdevs)

gather_all("output.csv", n)

# end module mazes.stats.degseq
