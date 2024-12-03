"""
mazes.AGT.primic - Prim-like algorithms using the arc growing tree module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

FAQ

    Q: Why "primic"?
    A: Because we're mimicking Prim's algorithm.

DESCRIPTION

    This module defines a method "primic" which uses the arc-growing tree
    module and a priority queue to carve a maze.  The priorities correspond to
    arcs in a grid.  The result is an algorithm called "Arc Prim" because it
    is similar to Prim's algorithm for finding a minimum weight spanning tree.
    If the priority function is symmetric, then "Arc Prim" reduces to Prim's
    algorithm, so "Arc Prim" is actually a generalization of Prim's algorithm.

    Prim's algorithm assigns weight to edges in the grid.  If the grid is
    connected, then the result is a spanning tree whose total edge weight is
    always equal to the minimum total edge weight.  Arc Prim assigns weights to
    arcs instead of edges, so the priority function is not necessarily
    symmetric.

    The algorithm is implemented as a passage carver.

    In addition to method primic, this module defines an oblong grid
    initializer called "make_maze" and several different priority functions.

REMARKS

    Prim's algorithm is discussed on pages 175 through 179 of [1].

SUMMARY

    defined here:
        method primic - carve a maze using arc growing tree and a priority
            queue
        method init_grid - create an oblong grid and set it up for carving

    Method primic will work on any connected grid.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

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
import mazes
from mazes import rng, Cell
from mazes.maze import Maze
from mazes.Algorithms.growing_tree2 import ArcGrowingTree as AGT
from mazes.Queues.priority_queue import PriorityQueue

def primic(maze:Maze, start_cell:Cell=None,
          shuffle=True, pr_map:dict={},
          action="unstable",
          cache=True) -> AGT.Status:
    """vertex Prim using the arc-growing tree module

    In addition to the maze, an optional starting cell, and a flag to use or
    not choose neighbors randomly ("shuffle"), we have two parameters for
    the priority queue:

        action - "stable", "antistable", or "unstable" (default)
            This three-way flag sets the protocol for handling equal
            priority cells:
                "stable" - first in, first out
                "antistable" - last in, first out
                "unstable" - random
            The first letter is sufficient.  For example 's', 'S', 'Superman',
            and 'supercalifragilisticexpialidocious' are all treated as
            'stable'.  Similarly, 'Ultraman' and 'Underdog' are 'unstable';
            'Aquaman' and 'antimony' are 'antistable'; and 'Batman' and
            'Robin' both raise ValueError exceptions.
        pr_map - a dictionary that maps arcs to a priority.  This
            dictionary can be empty or incomplete.  The priority queue
            class assigns uniformly distributed float values in the interval
            [0,1) for any missing entries.  The keys can take several forms:
                "const" - the value is a constant
                cell - the value is the priority of the destination
                edge (frozenset) - the value is the priority of an edge as
                    in Prim's algorithm
                arc (tuple) - the value is the priority of an arc
            priorities are tried in order from specfic (arc) to general
        cache - set this to false if the priority queue cache should not be
            used.
    """
    def pr(cell1, cell2):
        """search in the cell map"""
        arc = (cell1, cell2)
        pr = pr_map.get(arc, None)                # arc Prim
        if pr == None:
            edge = frozenset([cell1, cell2])
            pr = pr_map.get(edge, None)           # Prim
        if pr == None:
            pr = pr_map.get(cell2, None)          # vertex Prim
        if pr == None:
            pr = pr_map.get("const", None)        # simplified Prim
        return pr

    init = ((), {"action":action, "cache":cache})
    return AGT.on(maze, start_cell=start_cell,
                  QueueClass=PriorityQueue,
                  priority=pr, init=init)

def init_maze(rows:int, columns:int) -> Maze:
    """create an oblong grid set up for passage carving"""
    from mazes.Grids.oblong import OblongGrid
    return Maze(OblongGrid(rows, columns))

# end module mazes.AGT.primic