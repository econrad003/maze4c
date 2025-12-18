"""
tests.minweight1 - spanning tree weight demo
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This demonstration checks several minimum weight spanning tree
    algorithms by comparing them with a number of other spanning tree
    algorithms.

    This demo may be expanded in the future.

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
from mazes import rng, Grid
from mazes.maze import Maze
from mazes.edge import Edge

def check_grid(grid:Grid):
    """verify that the grid is symmetric

    If there are parallel arcs, a warning is issued.  If there are loops,
    a warning is also issued.  If the grid is not symmetric, a ValueError
    exception is raised.

    A sparse adjacency matrix is returned.  (All entries are positive
    integers and count the number of times the target cell appears in
    the source neighborhood.)
    """
    print("Build and verify the adjacency matrix...")
        # create an adjacency matrix
    arcs = dict()
    for cell in grid:
        for nbr in cell.neighbors:
            arc = (cell, nbr)
            arcs[arc] = arcs[arc] + 1 if arc in arcs else 1
        # make sure that it is symmetric
    loops = 0
    mismatches = 0
    multiples = 0
    for arc in arcs:
        cell, nbr = arc
        if cell is nbr:
            loops += 1
            continue
        coarc = (nbr, cell)
        if arcs[arc] > 1:
            multiples += 1          # parallel arcs
        if arcs[arc] != arcs[coarc]:
            mismatches += 1         # symmetry violations
        # report the problems
    if loops:
        print(f"{loops} loops were found in the grid. (WARNING)")
    if multiples:
        print(f"{multiples} parallel arcs were found in the grid. (WARNING)")
    if mismatches:
        print(f"{mismatches} symmetry violations were found.")
        raise ValueError("The grid is not symmetric")
    return arcs                     # the adjacency matrix

def edge_set(adjacencies:dict):
    """builds the edge set for the grid

    Parallel edges are removed, but loops are retained.
    """
    print("Build the edge set...")
    edges = set()
    for arc in adjacencies:
        edge = frozenset(arc)
        edges.add(edge)
    return edges

def costs(edges:set, epsilon:float=1e-5):
    """build the weight matrix

    The value epsilon is the smallest positive weight increase.  The
    actual weight increase is the maximum of epsilon and random (0,1)
    deviate.  This insures that the increase is always positive and
    the weight matrix is an injection.  (In other words, different
    edges have different weights.)

    If epsilon is less than or equal to zero, the weight matrix cannot
    be guaranteed to be injective.  If epsilon is greater than or equal
    to 1, then the weights will always exceed by 1 some multiple of epsilon,
    (ignoring errors due to floating point rounding).
    """
    edges = list(edges)
    rng.shuffle(edges)
    weights = dict()
    weight = 1                  # the smallest weight
    for edge in edges:
        weights[edge] = weight
        weight += max(epsilon, rng.random())
    return weights

def check(maze):
    """verify the maze (return False for failure or True for success)"""
    v = len(maze.grid)
    e = len(maze)
    if v - e != 1:
        print(f"\tERROR: the maze is not a perfect maze! ({v=}, {e=})")
        return False
    unvisited = set(maze.grid)
    cell = list(maze.grid)[0]
    stack = [cell]
    while stack:                # depth-first search
        cell = stack.pop()
        if cell in unvisited:
            unvisited.remove(cell)
            for nbr in cell.neighbors:
                stack.append(nbr)
    if unvisited:
        print(f"\tERROR: the maze is not connected")
        return False
    for join in maze:
        if not isinstance(join, Edge):
            print("\tERROR: the maze has a passage which is not an edge.")
    return True

def weigh(maze, weights):
    """determine the total cost"""
    cost = 0
    for join in maze:
        edge = frozenset(join)
        weight = weights[edge]
        cost += weight
    print(f"{cost=}")
    return cost

from mazes.Algorithms.boruvka import Boruvka
from mazes.Algorithms.kruskal import Kruskal

from mazes.Algorithms.wilson import Wilson
from mazes.Algorithms.bfs import BFS
from mazes.Algorithms.dfs_better import DFS
from mazes.Algorithms.dff import DFF
from mazes.Algorithms.hunt_kill import HuntKill
from mazes.Algorithms.growing_tree2 import ArcGrowingTree as AGT

from mazes.Queues.priority_queue import PriorityQueue

carvers = dict()
carvers["Borůvka"] = (Boruvka, tuple(), dict(), "edge_weights", dict)
carvers["Kruskal"] = (Kruskal, tuple(), dict(), "priority", "edge")
carvers["Prim"] = (AGT, tuple(), {"QueueClass":PriorityQueue}, "priority", "edge2")
carvers["Wilson"] = (Wilson, tuple(), dict(), None, None)
carvers["breadth-first search"] = (BFS, tuple(), dict(), None, None)
carvers["depth-first search"] = (DFS, tuple(), dict(), None, None)
carvers["depth-first forest"] = (DFF, tuple(), dict(), None, None)
carvers["hunt & kill"] = (HuntKill, tuple(), dict(), None, None)

results = list()

def carve(maze, carver, weights):
    """simple passage carvers"""
    print(f"{carver=}: ", end="")
    maze.unlink_all()
    Carver, args, kwargs, warg, wargtype = carvers[carver]
    if wargtype == dict:
        kwargs[warg] = weights
    elif wargtype == "edge":
        kwargs[warg] = lambda edge: weights[edge]
    elif wargtype == "edge2":
        kwargs[warg] = lambda cell, nbr: weights[frozenset([cell,nbr])]
    status = Carver.on(maze, *args,**kwargs)
    ok = check(maze)
    if ok:
        cost = weigh(maze, weights)
        result = (cost, carver, "passage carver")
        results.append(result)
    return status

from mazes.Grids.oblong import OblongGrid

def test1():
    maze = Maze(OblongGrid(5, 8))
    weights = costs(edge_set(check_grid(maze.grid)))
    for carver in carvers:
        status = carve(maze, carver, weights)
        print(status)
        print(maze)
    sorted_results = sorted(results)
    print("Summary of Costs:")
    n = 0
    for result in sorted_results:
        n += 1
        cost, name, kind = result
        print(n, "\t%10.3f" % cost, name, kind)
        if n == 3:
            print("\t", "-"*50)
    print("Borůvka, Kruskal and Prim should have the lowest cost!")
    print("They will always produce identical mazes!")
    print("Floating point rounding errors create small differences.")
    sys.exit()

test1()

# END tests.minweight1
