"""
mazes.VGT.vprim - "Vertex Prim" using the vertex growing tree module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module defines a method "vprim" which uses the vertex-growing tree
    module and a priority queue to carve a maze.  The priorities correspond to
    vertices in a grid.  The result is an algorithm called "Vertex Prim"
    because it is superficially similar to Prim's algorithm for finding a
    minimum weight spanning tree.

    Prim's algorithm assigns weight to edges in the grid.  If the grid is
    connected, then the result is a spanning tree whose total edge weight is
    always equal to the minimum total edge weight.  Note that if we use
    vertex weights instead of edge weights the total weight is a constant.
    Although vertex Prim does indeed produce a minimum vertex weight spanning
    tree, the same can be said for any correct spanning tree algorithm.
    Vertex Prim does, however, produce a reasonably random spanning tree
    without too much effort.

    The algorithm is implemented as a passage carver.

    In addition to method "vprim", the method "init_maze" is included to create
    an oblong grid set up for passage carving.  (The growing tree algorithm
    works on arbitrary grids.)

    Vertex Prim is discussed on pages 181 through 183 of the Jamis Buck
    book [1].  Although Buck calls the algorithm "TruePrims", he notes that
    it is not a correct implementation of Prim's algorithm.

REMARKS

    A. Prim's algorithm is discussed on pages 175 through 179.  (It is best
       implemented with an edge-based setup.)

`   B. We can either start with a map from cells to vertices or we can let the
       priority queue cache take care of that for us.

SUMMARY

    defined here:
        method vprim - carve a maze using vertex Prim
        method init_grid - create an oblong grid and set it up for carving

    Method vprim will work on any connected grid.

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
from mazes import Cell
from mazes.maze import Maze
from mazes.Algorithms.growing_tree1 import VertexGrowingTree as VGT
from mazes.Queues.priority_queue import PriorityQueue

def vprim(maze:Maze, start_cell:Cell=None,
          shuffle=True, cell_map:dict={},
          action="unstable", cache=True) -> VGT.Status:
    """a Prim-like algorithm using the vertex-growing tree module

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
        cell_map - a dictionary that maps a cell to a priority.  This
            dictionary can be empty or incomplete.  The priority queue
            class assigns uniformly distributed float values in the interval
            [0,1) for any missing entries.
        cache - (default: True) if this option is set to False, the priority
            queue cache will be disabled, and the cell_map must cover every
            cell.
    """
    pr = lambda cell: cell_map.get(cell, None)
    init = ((), {"action":action, "cache":cache})
    return VGT.on(maze, start_cell=start_cell,
                  QueueClass=PriorityQueue,
                  priority=pr, init=init)

def init_maze(rows:int, columns:int) -> Maze:
    """create an oblong grid set up for passage carving"""
    from mazes.Grids.oblong import OblongGrid
    return Maze(OblongGrid(rows, columns))

# end module mazes.AGT.primic