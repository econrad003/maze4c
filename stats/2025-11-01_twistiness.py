"""
stats.twistiness - twistiness statistics
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This program gathers twistiness statistics for a number of
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
from mazes.misc.maze_group import main

n = 100                                 # 100 runs
rows, cols = (39, 39)
center = (19, 19)

def analyze(*args, **kwargs):
    """call the maze maker and analyze the result"""
    args = list(args)
    args.append("-d")
    args.append(str(rows))
    args.append(str(cols))
    for kw in kwargs:
        args.append("--" + kw)
        opt = kwargs[kw]
        if isinstance(opt, (list, tuple)):
            for item in opt:
                args.append(str(item))
        elif opt == None:
            pass
        else:
            args.append(str(opt))
    args.append("--quiet")
    maze = main(list(args))
    # print(maze)
    results = dict()
    results["errors"] = 0
    results["dead ends"] = 0
    results["turns"] = 0
    results["straight N/S"] = 0
    results["straight E/W"] = 0
    results["3-way"] = 0
    results["4-way"] = 0
    results["sum degrees"] = 0
    results["v"] = 0
    results["e"] = len(maze)
    for cell in maze.grid:
        results["v"] += 1
        d = len(list(cell.passages))
        results["sum degrees"] += d
        if d == 1:
            results["dead ends"] += 1
        elif d == 2:
            if cell.is_linked(cell.north) and cell.is_linked(cell.south):
                results["straight N/S"] += 1
            elif cell.is_linked(cell.east) and cell.is_linked(cell.west):
                results["straight E/W"] += 1
            else:
                results["turns"] += 1
        elif d == 3:
            results["3-way"] += 1
        elif d == 4:
            results["4-way"] += 1
        else:
            results["errors"] += 1
    if 2 * results["e"] != results["sum degrees"]:
        print("Euler counting error: Σd ≠ 2e",
              f"(Σd={results['sum degrees']}, e={results['e']})")
        raise RuntimeError("Euler counting error")
    if results["errors"] > 0:
        print(f"{results['errors']} degree errors")
        raise RuntimeError("degree error")
    return results

def ab(**kwargs):
    """Aldous/Broder"""
    results = analyze("-a", "ab", **kwargs)
    # print(results)
    return results

def bfs(**kwargs):
    """breadth-first search"""
    results = analyze("-a", "bfs", **kwargs)
    # print(results)
    return results

def dfs(**kwargs):
    """depth-first search"""
    results = analyze("-a", "dfs", **kwargs)
    # print(results)
    return results

def eller(**kwargs):
    """Eller's algorithm"""
    results = analyze("-a", "e", **kwargs)
    # print(results)
    return results

def houston(**kwargs):
    """Houston's algorithm"""
    results = analyze("-a", "h", **kwargs)
    # print(results)
    return results

def hk(**kwargs):
    """hunt and kill algorithm"""
    results = analyze("-a", "hk", **kwargs)
    # print(results)
    return results

def iw(**kwargs):
    """inwinder"""
    results = analyze("-a", "iw", **kwargs)
    # print(results)
    return results

def kruskal(**kwargs):
    """Kruskal's algorithm"""
    results = analyze("-a", "k", **kwargs)
    # print(results)
    return results

def mrw(**kwargs):
    """multithreaded random walk"""
    results = analyze("-a", "mrw", **kwargs)
    # print(results)
    return results

def outw_eller(**kwargs):
    """outward Eller"""
    results = analyze("-a", "oe", **kwargs)
    # print(results)
    return results

def ow(**kwargs):
    """outwinder"""
    results = analyze("-a", "ow", **kwargs)
    # print(results)
    return results

def rd(**kwargs):
    """recursive division"""
    results = analyze("-a", "rd", **kwargs)
    # print(results)
    return results

def rab(**kwargs):
    """reverse Aldous/Broder"""
    results = analyze("-a", "rab", **kwargs)
    # print(results)
    return results

def sw(**kwargs):
    """sidewinder"""
    results = analyze("-a", "sw", **kwargs)
    # print(results)
    return results

def sbt(**kwargs):
    """simple binary tree"""
    results = analyze("-a", "sbt", **kwargs)
    # print(results)
    return results

def sPrim(**kwargs):
    """simplified Prim"""
    results = analyze("-a", "sp", **kwargs)
    # print(results)
    return results

def w(**kwargs):
    """Wilson"""
    results = analyze("-a", "w", **kwargs)
    # print(results)
    return results

def wd(**kwargs):
    """watershed division"""
    results = analyze("-a", "wd", **kwargs)
    # print(results)
    return results

def to_csv(name, mean, variance):
    """output form for the stats"""
    def avg(item):
        """display average"""
        return f"{mean[item]:6.1f}"

    def stdev(item):
        """display standard deviation"""
        dev = sqrt(variance[item])
        return f"{dev:6.1f}"

    s = f"{name:30}"
    s += "," + avg("dead ends")
    s += "," + avg("turns")
    s += "," + avg("straight N/S")
    s += "," + avg("straight E/W")
    s += "," + avg("3-way")
    s += "," + avg("4-way")
    s += "\n"
    s += f"{'   standard deviation':30}"
    s += "," + stdev("dead ends")
    s += "," + stdev("turns")
    s += "," + stdev("straight N/S")
    s += "," + stdev("straight E/W")
    s += "," + stdev("3-way")
    s += "," + stdev("4-way")
    s += "\n"
    return s

def collect(alg, name, *args, **kwargs):
    """collect statistics"""
    print(f"{name=}")
    sumx = dict()
    sumx["dead ends"] = 0
    sumx["turns"] = 0
    sumx["straight N/S"] = 0
    sumx["straight E/W"] = 0
    sumx["3-way"] = 0
    sumx["4-way"] = 0
    sumxx = dict()
    sumxx["dead ends"] = 0
    sumxx["turns"] = 0
    sumxx["straight N/S"] = 0
    sumxx["straight E/W"] = 0
    sumxx["3-way"] = 0
    sumxx["4-way"] = 0
    for i in range(n):
        results = alg(*args, **kwargs)
        for item in sumx:
            x = results[item]
            sumx[item] += x
            sumxx[item] += x*x
    mean = dict()
    variance = dict()
    for item in sumx:
        mean[item] = sumx[item] / n
        variance[item] = sumxx[item] / n - mean[item] ** 2
    s = to_csv(name, mean, variance)
    return s

def headers():
    """get the headers"""
    s = " "*27 + ","
    s += "dead ends,"
    s += " turns,"
    s += "   N/S,"
    s += "   E/W,"
    s += " 3-way,"
    s += " 4-way\n"
    return s

with open("output.csv", "w") as fp:
    fp.write(headers())
    fp.write(collect(ab, "Aldous/Broder"))
    fp.write(collect(bfs, "breadth-first search"))
    #fp.write(collect(bfs, "breadth-first search (center)", start=center))
    fp.write(collect(dfs, "depth-first search"))
    #fp.write(collect(dfs, "depth-first search (sorted)", no_shuffle=None))
    fp.write(collect(eller, "Eller's algorithm"))
    #fp.write(collect(eller, "Eller (heads=75%)", bias1=0.75))
    #fp.write(collect(eller, "Eller (merge=2/3)", eller_rate=2/3))
    fp.write(collect(houston, "Houston's algorithm"))
    #fp.write(collect(houston, "Houston (cutoff=1/3)", houston_rates=(1/3, 0.9)))
    #fp.write(collect(eller, "Houston (failures=10%)", houston_rates=(2/3, 0.1)))
    fp.write(collect(hk, "hunt and kill"))
    fp.write(collect(iw, "inwinder"))
    #fp.write(collect(iw, "inwinder (heads=75%)", bias1=0.75))
    fp.write(collect(kruskal, "Kruskal's algorithm"))
    fp.write(collect(mrw, "2-thread random walk"))
    fp.write(collect(mrw, "3-thread random walk", threads=3))
    #fp.write(collect(mrw, "3-thread random walk (RR)", threads=3, round_robin=None))
    #fp.write(collect(mrw, "3-thread random walk (8 5 3)", threads=3,                   thread_weights=(8, 5, 3)))
    fp.write(collect(outw_eller, "outward Eller"))
    #fp.write(collect(outw_eller, "outward Eller (heads=75%)", bias1=0.75))
    #fp.write(collect(outw_eller, "outward Eller (merge=2/3)", eller_rate=2/3))
    fp.write(collect(ow, "outwinder"))
    #fp.write(collect(ow, "outwinder (heads=75%)", bias1=0.75))
    fp.write(collect(rd, "recursive division"))
    #fp.write(collect(rd, "recursive div (hmode=61.8%)", hmode=0.618))
    #fp.write(collect(rd, "recursive div (vmode=61.8%)", vmode=0.618))
    fp.write(collect(rab, "reverse Aldous/Broder"))
    fp.write(collect(sw, "sidewinder"))
    #fp.write(collect(sw, "sidewinder (heads=75%)", bias1=0.75))
    fp.write(collect(sbt, "simple binary tree"))
    #fp.write(collect(sbt, "simple binary tree (heads=75%)", bias1=0.75))
    fp.write(collect(sPrim, "simple Prim"))
    #fp.write(collect(sPrim, "simple Prim (sorted)", no_shuffle=None))
    fp.write(collect(w, "Wilson's algorithm"))
    fp.write(collect(wd, "2-pump watershed division", watershed=(2,2)))
    fp.write(collect(wd, "3-pump watershed division", watershed=(2,3)))

# dfs()
# dfs(start=[5, 5])

# end module mazes.stats.twistiness
