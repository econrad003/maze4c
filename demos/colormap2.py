"""
tests.colormap2 - color gradient for a maze
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This demo produces distance-colored mazes.  It is more versatile than its
    unnumbered counterpart.

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
from matplotlib.colors import to_rgb

import mazes
from mazes import rng
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.dijkstra import test
from mazes.tools.distance_map import DistanceColoring

    # the new improved daddy long legs (23 Dec 2024)
from mazes.Graphics.oblong1 import Pholcidae

CARVER = (Wilson, (), {})
ALGORITHMS = "The available algorithms are:"
OPTIONS = "Options by algorithm:"

        # SIMPLE BINARY TREE

def sbt(args):
    """simple binary tree"""
    from mazes.Algorithms.simple_binary_tree import BinaryTree

    title = "Simple Binary Tree"
    pargs = ()
    kwargs = {}
    if args.bias != None:
        kwargs["bias"] = args.bias
        pct = args.bias * 100
        title += " (bias %.2f%%)" % pct
    if not args.title:
        args.title = title
    return (BinaryTree, pargs, kwargs)

ALGORITHMS += " '1' or 'sbt' - simple binary tree"
OPTIONS += " 1) sbt: uses --bias"

        # SIDEWINDER AND ITS VARIANTS

def sw(args):
    """sidewinder"""
    from mazes.Algorithms.sidewinder import Sidewinder

    title = "Sidewinder"
    pargs = ()
    kwargs = {}
    if args.bias != None:
        kwargs["bias"] = args.bias
        pct = args.bias * 100
        title += " (bias %.2f%%)" % pct
    if args.which != None:
        kwargs["which"] = args.which
    if not args.title:
        args.title = title
    return (Sidewinder, pargs, kwargs)

ALGORITHMS += "; '2' or 'sw' - sidewinder"
OPTIONS += "; 2) sw: uses --bias and --which"

def iw(args):
    """inwinder"""
    from mazes.Algorithms.inwinder import Inwinder

    title = "Inwinder"
    pargs = ()
    kwargs = {}
    if args.bias != None:
        kwargs["bias"] = args.bias
        pct = args.bias * 100
        title += " (bias %.2f%%)" % pct
    if args.which != None:
        kwargs["which"] = args.which
    if not args.title:
        args.title = title
    return (Inwinder, pargs, kwargs)

ALGORITHMS += "; '3' or 'iw' - inwinder"
OPTIONS += "; 3) iw: uses --bias and --which"

def ow(args):
    """sidewinder"""
    from mazes.Algorithms.outwinder import Outwinder

    title = "Outwinder"
    pargs = ()
    kwargs = {}
    if args.bias != None:
        kwargs["bias"] = args.bias
        pct = args.bias * 100
        title += " (bias %.2f%%)" % pct
    if args.which != None:
        kwargs["which"] = args.which
    if not args.title:
        args.title = title
    return (Outwinder, pargs, kwargs)

ALGORITHMS += "; '4' or 'ow' - outwinder"
OPTIONS += "; 4) ow: uses --bias and --which"

        # Depth-first search

def dfs(args):
    """depth-first search"""
    from mazes.Algorithms.dfs_better import DFS

    title = "Depth-first search"
    pargs = ()
    kwargs = {}
    if args.no_shuffle == True:
        kwargs["shuffle"] = False
        title += " (neighbors: FC/FS)"
    if not args.title:
        args.title = title
    return (DFS, pargs, kwargs)

ALGORITHMS += "; '5' or 'dfs' - depth-first search"
OPTIONS += "; 5) dfs: uses --no-shuffle"

        # Breadth-first search

def bfs(args):
    """breadth-first search"""
    from mazes.Algorithms.bfs import BFS

    title = "Breadth-first search"
    pargs = ()
    kwargs = {}
    if args.no_shuffle == True:
        kwargs["shuffle"] = False
        title += " (neighbors: FC/FS)"
    if not args.title:
        args.title = title
    return (BFS, pargs, kwargs)

ALGORITHMS += "; '6' or 'bfs' - breadth-first search"
OPTIONS += "; 6) bfs: uses --no-shuffle"

        # ELLER's ALGORITHM and VARIANTS

def ell(args):
    """Eller"""
    from mazes.Algorithms.eller import Eller, coin_toss

    title = "Eller's algorithm"
    pargs = ()
    kwargs = {}
    biases = []
    if args.bias != None:
        kwargs["flip1"] = (coin_toss, (), {"bias":args.bias})
        pct = args.bias * 100
        biases.append("rise bias %.2f%%" % pct)
    if args.merge != None:
        p, q = args.merge
        kwargs["flip2"] = (coin_toss, (), {"bias":p/q})
        biases.append("run bias %d/%d" % (p,q))
    if biases:
        title += " (" + ", ".join(biases) + ")"
    if not args.title:
        args.title = title
    return (Eller, pargs, kwargs)

ALGORITHMS += "; '7' or 'ell' - Eller's algorithm"
OPTIONS += "; 7) ell: uses --bias and --merge"

def oell(args):
    """outward Eller"""
    from mazes.Algorithms.outward_eller import OutwardEller, coin_toss

    title = "Outward Eller"
    pargs = ()
    kwargs = {}
    biases = []
    if args.bias != None:
        kwargs["flip1"] = (coin_toss, (), {"bias":args.bias})
        pct = args.bias * 100
        biases.append("rise bias %.2f%%" % pct)
    if args.merge != None:
        p, q = args.merge
        kwargs["flip2"] = (coin_toss, (), {"bias":p/q})
        biases.append("run bias %d/%d" % (p,q))
    if biases:
        title += " (" + ", ".join(biases) + ")"
    if not args.title:
        args.title = title
    return (OutwardEller, pargs, kwargs)

ALGORITHMS += "; '8' or 'oell' - outward Eller"
OPTIONS += "; 8) oell: uses --bias and --merge"

def iell(args):
    """inward Eller"""

###############################################################
    print("Inward Eller remains to be implemented")
    import sys
    sys.exit(1)
###############################################################

    from mazes.Algorithms.inward_eller import InwardEller, coin_toss

    title = "Inward Eller"
    pargs = ()
    kwargs = {}
    biases = []
    if args.bias != None:
        kwargs["flip1"] = (coin_toss, (), {"bias":args.bias})
        pct = args.bias * 100
        biases.append("rise bias %.2f%%" % pct)
    if args.merge != None:
        p, q = args.merge
        kwargs["flip2"] = (coin_toss, (), {"bias":p/q})
        biases.append("run bias %d/%d" % (p,q))
    if biases:
        title += " (" + ", ".join(biases) + ")"
    if not args.title:
        args.title = title
    return (OutwardEller, pargs, kwargs)

ALGORITHMS += "; '9' or 'iell' - inward Eller"
OPTIONS += "; 9) iell: uses --bias and --merge"

ALGORITHMS += " (not yet implemented)"

        # ALDOUS/BRODER

def ab(args):
    """Aldous/Broder"""
    from mazes.Algorithms.aldous_broder import AldousBroder

    title = "Aldous/Broder (first entrance random walk)"
    pargs = ()
    kwargs = {}
    if not args.title:
        args.title = title
    return (AldousBroder, pargs, kwargs)

ALGORITHMS += "; '10' or 'ab' - Aldous/Broder"
# OPTIONS += "; 10) ab: uses"       # NO OPTIONS

        # REVERSE ALDOUS/BRODER

def rab(args):
    """reverse Aldous/Broder"""
    from mazes.Algorithms.reverse_aldous_broder import ReverseAldousBroder

    title = "reverse Aldous/Broder (last exit random walk)"
    pargs = ()
    kwargs = {}
    if not args.title:
        args.title = title
    return (ReverseAldousBroder, pargs, kwargs)

ALGORITHMS += "; '11' or 'rab' - reverse Aldous/Broder"
# OPTIONS += "; 11) ab: uses"       # NO OPTIONS

        # WILSON

def wil(args):
    """Wilson"""
    from mazes.Algorithms.wilson import Wilson

    title = "Wilson (circuit-eliminated random walk)"
    pargs = ()
    kwargs = {}
    if not args.title:
        args.title = title
    return (Wilson, pargs, kwargs)

ALGORITHMS += "; '12' or 'wil' or 'wilson' - Wilson"
# OPTIONS += "; 12) wil: uses"       # NO OPTIONS

        # HOUSTON's ALGORITHM

def hou(args):
    """Houston's algorithm"""
    from mazes.Algorithms.houston import Houston

    title = "Houston's algorithm"
    pargs = ()
    kwargs = {}
    biases = []
    if args.cutoff != None:
        kwargs["cutoff_rate"] = args.cutoff
        pct = args.cutoff * 100
        biases.append("cutoff rate %.2f%%" % pct)
    if args.failures != None:
        kwargs["failure_rate"] = args.failures
        pct = args.failures * 100
        biases.append("failure rate %.2f%%" % pct)
    if biases:
        title += " (" + ", ".join(biases) + ")"
    if not args.title:
        args.title = title
    return (Houston, pargs, kwargs)

ALGORITHMS += "; '13' or 'hou' or 'houston' - Houston's algorithm"
OPTIONS += "; 13) hou: uses --cutoff and --failures"

        # HUNT and KILL ALGORITHM

def hk(args):
    """Hunt & kill algorithm"""
    from mazes.Algorithms.hunt_kill import HuntKill

    title = "Hunt & Kill algorithm"
    pargs = ()
    kwargs = {}
    if not args.title:
        args.title = title
    return (HuntKill, pargs, kwargs)

ALGORITHMS += "; '14' or 'hk' - Hunt & kill algorithm"
# OPTIONS += "; 14) hk: uses"       # NO OPTIONS

        # KRUSKAL's ALGORITHM and VARIANTS

def kr(args):
    """Kruskal's algorithm"""
    from mazes.Algorithms.kruskal import Kruskal

    title = "Kruskal's algorithm"
    pargs = ()
    kwargs = {}
    if not args.title:
        args.title = title
    return (Kruskal, pargs, kwargs)

ALGORITHMS += "; '15' or 'kr' or 'kruskal' - Kruskal's algorithm"
# OPTIONS += "; 16) krs: uses"       # NO OPTIONS

def krq(args):
    """Kruskal's algorithm with a random queue"""
    from mazes.Algorithms.kruskal import Kruskal
    from mazes.Queues.random_queue import RandomQueue

    title = "Kruskal's algorithm (RandomQueue)"
    pargs = ()
    kwargs = {"QueueClass":RandomQueue}
    if not args.title:
        args.title = title
    return (Kruskal, pargs, kwargs)

ALGORITHMS += "; '16' or 'krq' - Kruskal's (RandomQueue)"
# OPTIONS += "; 16) krs: uses"       # NO OPTIONS

        # PRIM's ALGORITHM VARIANTS

def sprim(args):
    """simplified "Prim's" algorithm"""
    from mazes.Algorithms.simplified_Prim import NotPrim

    title = "Simplified \"Prim's\" algorithm"
    pargs = ()
    kwargs = {}
    if not args.title:
        args.title = title
    return (NotPrim, pargs, kwargs)

ALGORITHMS += "; '17' or 'sprim' - Simplified 'Prim'"
# OPTIONS += "; 17) sprim: uses"       # NO OPTIONS

def vprim(args):
    """vertex "Prim's" algorithm"""
    from mazes.Algorithms.growing_tree1 import VertexGrowingTree
    from mazes.Queues.priority_queue import PriorityQueue

    title = "Vertex \"Prim's\" algorithm"
    pargs = ()
    kwargs = {"QueueClass":PriorityQueue}
    if not args.title:
        args.title = title
    return (VertexGrowingTree, pargs, kwargs)

ALGORITHMS += "; '18' or 'vprim' - Vertex 'Prim'"
# OPTIONS += "; 18) vprim: uses"       # NO OPTIONS

def prim(args):
    """Prim's algorithm"""
    from mazes.Algorithms.growing_tree2 import ArcGrowingTree
    from mazes.Queues.priority_queue import PriorityQueue

    lookup = {}
    rows, cols = args.dim
        # a symmetric priority lookup
    for i in range(rows):
        for j in range(cols):
            ix1 = (i, j)
            for k in range(rows):
                for l in range(cols):
                    ix2 = (k, l)
                    if (ix2, ix1) in lookup:
                        lookup[ix1, ix2] = lookup[ix2, ix1]
                    else:
                        lookup[ix1, ix2] = rng.random()
        # callable
    pr = lambda cell1, cell2: lookup[cell1.index, cell2.index]

    title = "Prim's algorithm"
    pargs = ()
    init = ((), {"cache":False})
    kwargs = {"QueueClass":PriorityQueue, "priority":pr, "init":init}
    if not args.title:
        args.title = title
    return (ArcGrowingTree, pargs, kwargs)

ALGORITHMS += "; '19' or 'prim' - Prim's algorithm"
# OPTIONS += "; 19) prim: uses"       # NO OPTIONS

def aprim(args):
    """arc "Prim's" algorithm"""
    from mazes.Algorithms.growing_tree2 import ArcGrowingTree
    from mazes.Queues.priority_queue import PriorityQueue

    title = "Arc \"Prim's\" algorithm"
    pargs = ()
    kwargs = {"QueueClass":PriorityQueue}
    if not args.title:
        args.title = title
    return (ArcGrowingTree, pargs, kwargs)

ALGORITHMS += "; '20' or 'aprim' - Arc 'Prim'"
# OPTIONS += "; 20) aprim: uses"       # NO OPTIONS

    # ADD NEW ALGORITHMS ABOVE THIS LINE

def choose_algorithm(args) -> tuple:
    """determine what algorithm to use

    Returns a triple (Algorithm, args, kwargs)

    If it can't figure out what algorithm to use, it returns (Wilson, (), {}).
    """
    alg = args.algorithm.lower()
    if args.algorithm in {"1", "sbt"}:
        return sbt(args)
    if args.algorithm in {"2", "sw"}:
        return sw(args)
    if args.algorithm in {"3", "iw"}:
        return iw(args)
    if args.algorithm in {"4", "ow"}:
        return ow(args)
    if args.algorithm in {"5", "dfs"}:
        return dfs(args)
    if args.algorithm in {"6", "bfs"}:
        return bfs(args)
    if args.algorithm in {"7", "ell"}:
        return ell(args)
    if args.algorithm in {"8", "oell"}:
        return oell(args)
    if args.algorithm in {"9", "iell"}:
        return iell(args)
    if args.algorithm in {"10", "ab"}:
        return ab(args)
    if args.algorithm in {"11", "rab"}:
        return rab(args)
    if args.algorithm in {"12", "wil", "wilson"}:
        return wil(args)
    if args.algorithm in {"13", "hou", "houston"}:
        return hou(args)
    if args.algorithm in {"14", "hk"}:
        return hk(args)
    if args.algorithm in {"15", "kr", "kruskal"}:
        return kr(args)
    if args.algorithm in {"16", "krq"}:
        return krq(args)
    if args.algorithm in {"17", "sprim"}:
        return sprim(args)
    if args.algorithm in {"18", "vprim"}:
        return vprim(args)
    if args.algorithm in {"19", "prim"}:
        return prim(args)
    if args.algorithm in {"20", "aprim"}:
        return aprim(args)

		# ADD SETUP CALLS ABOVE THIS LINE

		# One of the cookie companies set its automated machinery to add
		# more chocolate if something amiss was detected.  This was their
		# failsafe action.  Here, instead of adding chocolate, we call
		# Wilson's algorithm.  That's okay because I prefer vanilla to
		# chocolate.

    print("Not sure what you want! Running Wilson's algorithm instead...")
    args.title = "Wilson's algorithm (default)"
    return CARVER

ALGORITHMS += ". The default is Wilson's algorithm."
OPTIONS += "."

def make_maze(args):
    """color a maze using a color gradient"""
        # create the maze
    rows, cols = args.dim
    maze = Maze(OblongGrid(rows, cols))
    Carver, carve_args, carve_kwargs = choose_algorithm(args)
    status = Carver.on(maze, *carve_args, **carve_kwargs)
    return status

def make_colormap(maze, hot, cold, zero, source):
    """create a color map"""
    coloring = DistanceColoring(maze, hot, cold, zero, source)
    return coloring.gradients

def make_sketch(maze, hot, cold, zero, source):
    """sketch the maze"""
    fills = make_colormap(maze, hot, cold, zero, source)
    spider = Pholcidae(maze)
    spider.setup(fillcolors=fills)
    spider.draw_maze()
    return spider

def main(args):
    """color a maze using a color gradient"""
    print(args)

        # create the maze
    status = make_maze(args)
    print(status)
    maze = status.maze

    if args.zero.lower() in {'', 'none'}:
        args.zero = args.hot
    print(args)
    hot, cold, zero = to_rgb(args.hot), to_rgb(args.cold), to_rgb(args.zero)
    print(f" {hot=}, {cold=}, {zero=}")

        # source cell
    source = args.source.lower()
    rows, cols = args.dim
    if source == "sw":
        source = maze.grid[0,0]
    elif source == "se":
        source = maze.grid[0,cols-1]
    elif source == "ne":
        source = maze.grid[rows-1,cols-1]
    elif source == "nw":
        source = maze.grid[rows-1,0]
    elif source == "c":
        source = maze.grid[rows//2,cols//2]
    else:
        source=None

        # create the sketch
    spider = make_sketch(maze, hot, cold, zero, source)
    if args.title:
        spider.title(args.title)
    return spider

def parse_args(argv):
    """get arguments using argparse"""
    import argparse

    DESCR = "fill maze with path-length gradient"
    parser = argparse.ArgumentParser(description=DESCR)
    parser.add_argument("hot", type=str, nargs='?', default="crimson", \
        help="the name of the zero distance color (crimson)")
    parser.add_argument("cold", type=str, nargs='?', default="skyblue", \
        help="the name of the maximum distance color (skyblue)")
    parser.add_argument("-z", "--zero", type=str, default="goldenrod", \
        help="the name of the source cell color (goldenrod).  'none' will" \
        + " set this to the hot color")
    parser.add_argument("-d", "--dim", type=int, nargs=2, default=(13,21), \
        metavar = ("ROWS", "COLS"), \
        help="the dimensions of the maze (13, 21)")
    parser.add_argument("-s", "--source", type=str, default='', \
        help="one of the corners ('sw', 'se', 'ne', 'nw')) or 'c' for" \
        + " center. Default will use longest path computation.")
    parser.add_argument("-a", "--algorithm", type=str, default="0", \
        help=ALGORITHMS)
    parser.add_argument("--title", type=str, default=None, \
        help="a title for the plot")

    special = parser.add_argument_group("specialized arguments", \
        "The following arguments are options for some of the maze carving" \
        + " algorithms.")

    special.add_argument('-p', "--bias", type=float, default=None, \
        help="the probability of a head in a coin toss." \
        + "  The default is a fair coin. (default None)")
    special.add_argument("--which", type=int, nargs='+', default=None, \
        help="controls selection from a run, for example (0, -1) always" \
        + " selects the first or the last element of the run. The default "\
        + "is to randomly choose an element from each run. (default None)")
    special.add_argument("--no-shuffle", action="store_true", \
        help= "if this is set, some algorithms will process neighbors" \
        + " on a first-come first-served basis instead of shuffling the" \
        + " neighborhoods. For most Python distributions, setting this" \
        + "option will result in a directional bias.")
    special.add_argument("--merge", type=int, nargs=2, default=None, \
        metavar=("P", "Q"), \
        help="the probability P/Q of a run merge in Eller's algorithm." \
        + "  The default probability is 1/3.  (default None)")
    special.add_argument("--cutoff", type=float, default=None, \
        help="when the this cutoff proportion is reached, the." \
        + "algorithm switches. (default None)")
    special.add_argument("--failures", type=float, default=None, \
        help="when the failure rate is reached, the." \
        + "algorithm switches. (default None)")

        # dummy argument group follows 'special'
    parser.add_argument_group("usage of specialized arguments", OPTIONS)

    args = parser.parse_args()
    return main(args)

if __name__ == "__main__":
    import sys
    spider = parse_args(sys.argv[1:])
    spider.show()

# end module demos.colormap2
