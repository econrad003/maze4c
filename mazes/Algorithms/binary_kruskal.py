"""
mazes.Algorithms.binary_kruskal - a Kruskal's algorithm variant to carve binary trees
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Kruskal's algorithm, like Prim's algorithm, is a minimum weight spanning
    tree algorithm.  This variant creates binary spanning trees by restricting
    the degrees of cells as edges are processed.  It will sometimes fail to
    produce a tree.

    Using the "arity" option, other trees with a constraint on the degree can
    also be generated.  For example, "arity=3" generates ternary trees by
    guaranteeing that no cell has degree greater than four.  (Arity limits
    the number of children.  In addition, each node except the root node
    has a parent.)  As with the default (arity=2 for binary trees), the
    algorithm will sometimes fail to end with a tree.

    When the algorithm fails, the resulting maze is a forest (disconnected).
    All the components in the forest are trees of the specified "arity".

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
from mazes.Algorithms.kruskal import Kruskal

class BinaryKruskal(Kruskal):
    """a Kruskal's algorithm variant to create binary trees"""

    class Status(Kruskal.Status):
        """this is where most of the work is done"""

        NAME = "Binary Kruskal"

        __slots__ = ("__arity", )

                # INITIALIZATION

        def parse_args(self, *args, arity:int=2, **kwargs):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                arity (default: 2 for binary)
                    The maximum number of children for a cell.  This is
                    used to determine the maximum degree for a cell:
                        maximum degree = arity + 1  (one parent + the children)
                    constraints on trees are sufficient to guarantee the
                    existence of a root node.

                    -- The remaining arguments are passed on to Kruskal.Status.

                setup - a startup procedure.  This may be  one of the strings
                    'scatter' or 'collect', or a function whose input is a
                    maze and its return value is an instance of class
                    ComponentRegistry (defined in module mazes.components).
                    The default is 'collect'.

                        'scatter' - returns a registry in which each component
                            is a single cell.

                        'collect' - collects cells into connected components.
                            If the initialize maze has no passages, this is the
                            same as 'scatter'.

                shuffle - if False, grid edges are entered directly into the
                    queue without shuffling; if True, they are shuffled before
                    entry.  The default is False.

                QueueClass - a generalized queueing class defined
                    using class GeneralizedQueue from mazes.gqueue.
                    The default is PriorityQueue.

                priority - a lookup function which maps a cell to a
                    priority (e.g. for VertexPrim).  If this is provided,
                    the priority will be passed to enter using the keyword
                    priority, e.g.:
                        q.enter(cell, priority=priority(cell))

                init -- arguments to be used in initializing QueueClass.
                    These take the form of a list or a tuple consisting of a
                    tuple and a dictionary, i.e. (args, kwargs).  The queue
                    class is then initialized as:
                        q = QueueClass(*args, **kwargs)
            """
            if not isinstance(arity, int):
                raise TypeError("the arity must be an integer")
            if arity < 1:
                raise ValueError("the arity must be a positive integer")
            self.__arity = arity
            super().parse_args(*args, **kwargs)

        def configure(self):
            """configuration"""
                # set up the statistics
            super().configure()
            self["arity"] = arity = self.__arity
            names = {1:"Unary", 2:"Binary", 3:"Ternary",
                     4:"Quaternary", 5:"Quinary"}
            prefix = names.get(self.__arity, f"{self.__arity}-ary")
            self.name = prefix + " Kruskal's Algorithm"

                # VISIT OVERRIDE

        def visit(self):
            """pop an edge and check the arity"""
                    # seize control
            cell1, cell2 = self.leave()
                    # if the degree of either cell exceeds the arity, then it
                    # is saturated, i.e. if has a parent and the maximum number
                    # of children, 
            if len(list(cell1.passages)) > self.__arity:
                return
            if len(list(cell2.passages)) > self.__arity:
                return
                    # the cell is not saturated, so relinquish control
            self.end_visit(cell1, cell2)

# end module mazes.Algorithms.binary_kruskal
