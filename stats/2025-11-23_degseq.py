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

n = 100                                 # 100 runs
noargs = tuple()
nokwargs = dict()
noshuffle = {"shuffle":False}
southwest = {"shuffle":False, "start_cell":(0,0)}
centered = {"shuffle":False, "start_cell":(10,17)}

vtype = {"prtype":"vertex",}
vtypen = {"prtype":"vertex", "shuffle":False}
vtypesw = {"prtype":"vertex", "shuffle":False, "start_cell":(0,0)}
vtypec = {"prtype":"vertex", "shuffle":False, "start_cell":(10,17)}

atype = {"prtype":"arc",}
atypen = {"prtype":"arc", "shuffle":False}
atypesw = {"prtype":"arc", "shuffle":False, "start_cell":(0,0)}
atypec = {"prtype":"arc", "shuffle":False, "start_cell":(10,17)}

grids = OblongGrid, (21, 34), nokwargs, 4

def make_grid(GridType:"Grid", *args, **kwargs) -> Maze:
    """make a grid"""
    return Maze(GridType(*args, **kwargs))

def run(algo, debug):
    """run the algorithm"""
    GridType, gargs, gkwargs, _ = grids
    maze = make_grid(GridType, *gargs, **gkwargs)
    Algo, time_str, args, kwargs = algorithms[algo]
    if is_wall_builder(Algo):
        maze.link_all()
    if debug:
        print(algo, time_str, args, kwargs)
    if "start_cell" in kwargs:
        kwargs = kwargs.copy()
        kwargs["start_cell"] = maze.grid[kwargs["start_cell"]]
    status = Algo.on(maze, *args, **kwargs)
    t = status[time_str]
    return t, maze

from mazes.Algorithms.aldous_broder import AldousBroder         # baseline
from mazes.Algorithms.dfs_better import DFS                     # baseline
from mazes.Algorithms.wilson import Wilson                      # baseline
from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
from mazes.WallBuilders.bfs_wallbuilder import BFSWallbuilder
from mazes.WallBuilders.pq_wallbuilder import PQWallbuilder

def is_wall_builder(Algo) -> bool:
    """passage carver (False) or wall builder (True)"""
    if Algo in {AldousBroder, DFS, Wilson}:
        return False
    return True

algorithms = {}
algorithms["Aldous/Broder"] = AldousBroder, "visits", noargs, nokwargs
algorithms["DFS"] = DFS, "visits", noargs, nokwargs
algorithms["Wilson"] = Wilson, "cells visited", noargs, nokwargs

algorithms["WB/DFS shuffle"] = BasicWallbuilder, "finder passes", noargs, nokwargs
algorithms["WB/DFS seq"] = BasicWallbuilder, "finder passes", noargs, noshuffle
algorithms["WB/DFS seq SW"] = BasicWallbuilder, "finder passes", noargs, southwest
algorithms["WB/DFS seq center"] = BasicWallbuilder, "finder passes", noargs, centered

algorithms["WB/BFS shuffle"] = BFSWallbuilder, "finder passes", noargs, nokwargs
algorithms["WB/BFS seq"] = BFSWallbuilder, "finder passes", noargs, noshuffle
algorithms["WB/BFS seq SW"] = BFSWallbuilder, "finder passes", noargs, southwest
algorithms["WB/BFS seq center"] = BFSWallbuilder, "finder passes", noargs, centered

algorithms["WB/PQ(e) shuffle"] = PQWallbuilder, "finder passes", noargs, nokwargs
algorithms["WB/PQ(e) seq"] = PQWallbuilder, "finder passes", noargs, noshuffle
algorithms["WB/PQ(e) seq SW"] = PQWallbuilder, "finder passes", noargs, southwest
algorithms["WB/PQ(e) seq center"] = PQWallbuilder, "finder passes", noargs, centered

algorithms["WB/PQ(v) shuffle"] = PQWallbuilder, "finder passes", noargs, vtype
algorithms["WB/PQ(v) seq"] = PQWallbuilder, "finder passes", noargs, vtypen
algorithms["WB/PQ(v) seq SW"] = PQWallbuilder, "finder passes", noargs, vtypesw
algorithms["WB/PQ(v) seq center"] = PQWallbuilder, "finder passes", noargs, vtypec

algorithms["WB/PQ(a) shuffle"] = PQWallbuilder, "finder passes", noargs, atype
algorithms["WB/PQ(a) seq"] = PQWallbuilder, "finder passes", noargs, atypen
algorithms["WB/PQ(a) seq SW"] = PQWallbuilder, "finder passes", noargs, atypesw
algorithms["WB/PQ(a) seq center"] = PQWallbuilder, "finder passes", noargs, atypec

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
    
    t, maze = run(algo, debug)
    stats = dict()
    stats["time"] = t
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
    stats["d"] = diameter(maze)
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
    header("time", "time")
    return headers, indices

def quick_csv(filename):
    """just run each algorithm once"""
    keys = list(algorithms.keys())
    max_degree = grids[3]
    headers, indices = headings(max_degree)
    with open(filename, "w") as fout:
        fout.write(", ".join(headers) + "\n")
        for key in keys:
            stats = capture_stats(key, max_degree, debug=True)
            stats2 = list()
            for header in headers:
                index = indices[header]
                stats2.append(str(stats[index]))
            fout.write(", ".join(stats2) + "\n")

def gather(algo, runs):
    """average of some runs"""
    max_degree = grids[3]
    print(algo, end="")
    stats = list()
    for i in range(runs):
        # print(algo, i)
        print(".", end="", flush=True)
        result = capture_stats(algo, max_degree)
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
    max_degree = grids[3]
    headers, indices = headings(max_degree)
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

gather_all("output.csv", n)

# end module mazes.stats.degseq
