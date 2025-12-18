"""
mazes.Algorithms.kruskal - Kruskal's algorithm and variants
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Kruskal's algorithm, like Prim's algorithm, is a minimum weight spanning
    tree algorithm.  Like the more general growing tree family of algorithms,
    Kruskal's algorithm has variants that also produce spanning trees for
    connected graphs. When the initial graph is not connected, Kruskal's
    algorithms and its variants produce maximal spanning forests (with
    spanning trees in each component).

BASIC ALGORITHM

    Given: an edge weight map.

    Initialization:
       Place the edges in a priority queue.
       Number the components.  (Initially, the maze [or graph]) is emmpty, so
            each component is an isolated cell [or vertex].)

    Loop:
        While the queue is not empty:
            remove an edge from the queue; [this will be a lowest weight edge]
            if the edge is incident to two components:
                carve the associated passage
                    [this will join the two components]
                (merge the components)
            otherwise:
                do nothing

    Notes:

        (a) If k0 is the number of cells (or more generally, the number of
        components at start, then the loop can terminate as soon as k-1 edges
        have been added.

        (b) The algorithm can be used to extend a disconnected subgraph to a
        minimally connected subgraph by adding edges of minimal total weight.

        (c) If we don't care about edge weights, we can use any type of queue.

        (d) Growing tree algorithms are related to search processes.  Kruskal's
        algorithm and its variants are connected to sorting processes.

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

MODIFICATION

    18 Dec 2025 - EC
        correct some of the verbage, plus make sure that __q.enter is only
        called in Kruskal.enter.  (This insures that the prioririty is
        passed correctly.)
"""
import mazes
from mazes import rng, Algorithm
from mazes.gqueue import GeneralizedQueue
from mazes.Queues.priority_queue import PriorityQueue
from mazes.components import ComponentRegistry, MazeComponents

        # Initialization options (scatter, collect)

def scatter(maze:'Maze') -> ComponentRegistry:
    """ignore all existing passages

    returns a registry containing one cell per component
    """
    registry = ComponentRegistry()
    for cell in maze.grid:
        registry.register(cell)
    return registry

def collect(maze:'Maze') -> ComponentRegistry:
    """collect the cells into existing components

    returns a registry containing the components of an existing maze
    """
    components = MazeComponents(maze)
    return components.registry

    # setup procedure aliases
setups = {"collect":collect, "scatter":scatter}

class Kruskal(Algorithm):
    """Kruskal's algorithm and some variants"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Kruskal"

        __slots__ = ("__registry", "__q", '__pr', "__k")

                # QUEUE OPERATIONS (enter/leave/empty)

        @property
        def components(self):                       # 1 Sep 2025
            """return the number of components"""
            return self.__k

        def enter(self, edge):
            """push the data into the queue"""
            if self.__pr:
                self.__q.enter(edge, priority=self.__pr(frozenset(edge)))
            else:
                self.__q.enter(edge)

        def leave(self):
            """pop and return the first entry in the queue"""
            return self.__q.leave()

        @property
        def is_empty(self):
            """condition for termination"""
            return self.__q.is_empty

                # INITIALIZATION

        def parse_args(self, setup:(str, callable)="collect",
                       shuffle:bool=False,
                       QueueClass:object=PriorityQueue,
                       priority:callable=None,
                       init:tuple=(tuple(), dict())):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

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

                priority - a lookup function which maps an edge {cell, nbr} to a
                    priority.  If this is provided, the priority will be passed
                    to enter using the keyword priority, e.g.:
                        q.enter(cell, nbr, priority=priority({cell, nbr}))

                init -- arguments to be used in initializing QueueClass.
                    These take the form of a list or a tuple consisting of a
                    tuple and a dictionary, i.e. (args, kwargs).  The queue
                    class is then initialized as:
                        q = QueueClass(*args, **kwargs)
            """
            if not issubclass(QueueClass, GeneralizedQueue):
                raise ValueError("QueueClass must be a generalized queue type")
            super().parse_args()                # chain to parent

                    # initialize the component registry
            if isinstance(setup, str):
                setup = setups[setup]
            if not callable(setup):
                raise ValueError("setup must be callable")
            self.__registry = setup(self.maze)
            if not isinstance(self.__registry, ComponentRegistry):
                raise TypeError("setup return type error")

                    # initialize the queuing options
            self.__pr = priority

                # initialize the queuing class
            qargs, qkwargs = init
            self.__q = QueueClass(*qargs, **qkwargs)

                # fill the queue
            if bool(shuffle):
                self.enter_shuffled()
            else:
                self.enter_raw()

        def enter_shuffled(self):
            """here we use an auxiliary queue"""
            visited = set()         # to avoid entering loops and return arcs
            component_for = self.__registry.component_for
            q = list()

                    # add each grid edge (not arc!) to the auxiliary queue
            for cell in self.maze.grid:
                visited.add(cell)
                for nbr in cell.neighbors:
                    if nbr in visited:
                        continue
                    if component_for(cell) != component_for(nbr):
                        edge = (cell, nbr)
                        q.append(edge)

                    # sort the auxiliary
            rng.shuffle(q)

                    # move stuff into the queue
            while q:
                self.enter(q.pop())

        def enter_raw(self):
            """here we do not use an auxiliary queue"""
            visited = set()         # to avoid entering loops and return arcs
            component_for = self.__registry.component_for
                    # add each grid edge (not arc!) to the auxiliary queue
            for cell in self.maze.grid:
                visited.add(cell)
                for nbr in cell.neighbors:
                    if nbr in visited:
                        continue
                    if component_for(cell) != component_for(nbr):
                        edge = (cell, nbr)
                        self.enter(edge)            # 18 Dec 2025

        def configure(self):
            """configuration"""
                # set up the statistics
            self.__k = len(self.__registry)
            self.store_item("components (init)", self.__k)
            self.store_item("queue length (init)", len(self.__q))
            self.store_item("cells", len(self.maze.grid))
            self.store_item("passages", 0)

        @property
        def more(self):
            """returns True if the queue is not empty or k>1

            Overrides Algorithm.more.
            """
            if self.__k <= 1:
                return False
            return not self.is_empty

        def end_visit(self, cell1, cell2):
            """for derived classes

            This should be called if the edge is otherwise permissible.

            If the cells are in different components, then the edge is carved.

            If the cells are in the same component, then the edge is not carved.
            """
            registry = self.__registry
            k1 = registry.component_for(cell1)
            k2 = registry.component_for(cell2)
            if k1 != k2:
                        # carve a passage"""
                self.maze.link(cell1, cell2)
                self.increment_item("passages")
                registry.merge(k1, k2)
                self.__k -= 1

        def visit(self):
            """pop an edge; if it joins two components, carve it"""
            cell, nbr = self.leave()
            registry = self.__registry
            k1 = registry.component_for(cell)
            k2 = registry.component_for(nbr)
            if k1 != k2:
                        # carve a passage"""
                self.maze.link(cell, nbr)
                self.increment_item("passages")
                registry.merge(k1, k2)
                self.__k -= 1

        def __str__(self):
            """string representation"""
            s = super().__str__()
            when = "curr" if self.more else "final"
            indent2 = ' ' * self.format("indent2")
            fmt = "%30s  %7d"
            s += "\n" + indent2
            stat = "components (%s)" % when
            s += fmt % (stat, self.__k)
            s += "\n" + indent2
            stat = "queue length (%s)" % when
            s += fmt % (stat, len(self.__q))
            return s

# end module mazes.Algorithms.kruskal
