"""
mazes.Algorithms.growing_tree2 - an arc-based growing tree algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

PRIM'S ALGORITHM

    In [2], the algorithm is described informally as follows (quoting):

        1. Initialize the tree with a single vertex...
        2. Grow the tree by one edge: Of the edges that connect the tree to
           vertices not yet in the tree, find the minimum-weight edge, and
           transfer it to the tree.
        3. Repeat...

GENERALIZING PRIM'S ALGORITHM

    The goal is to generalize this, and of course there are many ways to do
    this.  For a vertex-based generalization, we consider only the case where
    edges have equal weight.  One result is the algorithm implemented in
        mazes.Algorithms.growing_tree1 (vertex-based)
    In that algorithm, we insure that vertices are enqueued once.  In effect
    vertices are weighted by their position in the queue.

    For an edge-based algorithm, we need to retain the notion of edge weight.
    But, as in the vertex-based case, this can be determined by the position
    of the edge in the queue.  If our queue is a priority queue, the result is
    Prim's Algorithm.

    In the specific case where we are using a priority queue, the efficiency
    will be very sensitive to the implementation of the priority queue.

HISTORY AND NOMENCLATURE

    Prim's algorithm was discovered by Vojtěch Jarník in 1930 and
    rediscovered by Robert Prim in 1957 and again by Edsger Dijkstra in 1959.
    It is accordingly known by various names, e.g. Prim's, Prim-Jarník,
    Jarník's, Prim-Dijkstra, and DJP.  In the United States, the most
    common name seems to be Prim's algorithm.

DESCRIPTION

    This is a cell-based maze carver which generalizes DFS, BFS, simplified
    Prim and vertex Prim.  It use generalize queuing queuing structure
    which we will simply call the queue.  The basic algorithm is follows:

        Pick a cell as the starting cell.
        Place its incident grid edges in the queue.
        Mark the start cell as visited
        Loop until the queue is empty:
            Pop an edge from the queue;
            (Note that at least one of its incident cells has been visited.)
            If one of its incident cells has not been visited:
                Mark that cell as visited
                Carve a passage along the edge
                For each grid edge incident to the cell:
                    If the edge is also incident to an unvisited cell,
                        then place it in the queue;
            Otherwise:
                Just pass.

    This may seem daunting but it is easier than it looks.

REMARKS

    Marking cells as visited insures that no edge is enqueued more than
    once.

    In practice, we can end early if all cells have been visited, or
    equivalently, if there are no unvisited cells.  If the queue is empty
    and there are unvisited cells, then the grid is not connected.

    Technically our implementation uses grid arcs rather than grid edges.
    Unless we are actually trying to implement Prim's algorithm on a grid,
    the distinction is just a technicality.  Given two grid arcs (cell1,
    cell2) and (cell2, cell1), just one of these will be encountered in a
    given run.  For example, if (cell1, cell2) is in the queue, then cell1
    has already been visited, so (cell2, cell1) cannot be added to the
    queue.

    For a correct implementation of Prim's algorithm, there are three
    conditions:
        1) an explicit priority function must be specified; and
        2) for each arc (cell1, cell2) in the grid:
            a) pr(cell1, cell2) is defined, i.e. the priority function is
               closed;
            b) pr(cell1, cell2) = pr(cell2, cell1), i.e. the priority
               function is symmetric; and
            c) there is a corresponding grid arc (cell2, cell1), i.e. the
               grid is symmetric.
        3) the queuing structure must be a min-priority queue.
    From the standpoint of a maze carving algorithm, much of this is really
    a technicality.  If we let our PriorityQueue structure create a partial
    priority function using its cache, we can easily extend this to a priority
    function that satisfies points (1), (2a) and (2b).

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4). Pages 175-179.

    [2] "Prim's algorithm." Wikipedia. 25 Oct. 2024. Web. Accessed 2 Dec. 2024.
        URL: https://en.wikipedia.org/wiki/Prim%27s_algorithm

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
from mazes import rng, Algorithm
from mazes.gqueue import GeneralizedQueue

class ArcGrowingTree(Algorithm):
    """a arc-based growing tree algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Arc Growing Tree"

        __slots__ = ("__q", "__unvisited", "__discover",
                     "__pr", "__start")

                # QUEUE OPERATIONS

        def enter(self, cell1, cell2):
            """push the data into the queue"""
            if self.__pr:
                self.__q.enter(cell1, cell2, priority=self.__pr(cell1, cell2))
            else:
                self.__q.enter(cell1, cell2)

        def leave(self):
            """pop and return the first entry in the queue"""
            return self.__q.leave()

        @property
        def is_empty(self):
            """condition for termination"""
            return self.__q.is_empty

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True,
                       QueueClass:object=None, priority:callable=None,
                       init:tuple=(tuple(), dict())):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)

                QueueClass - a generalized queueing class (required!) defined
                    using class GeneralizedQueue from mazes.gqueue.

                priority - a lookup function which maps two cells to a
                    priority (e.g. for Prim's algorithm).  If this is provided,
                    the priority will be passed to enter using the keyword
                    priority, e.g.:
                        q.enter(cell, priority=priority(cell))

                init -- arguments to be used in initializing QueueClass.
                    These take the form of a list or a tuple consisting of a
                    tuple and a dictionary, i.e. (args, kwargs).  The queue
                    class is then initialized as:
                        q = QueueClass(*args, **kwargs)
            """
            if not issubclass(QueueClass, GeneralizedQueue):
                raise ValueError("QueueClass must be a generalized queue type")
            super().parse_args()                # chain to parent
            self.__discover = self.discover_random if shuffle \
                else self.discover_in_order
            self.__pr = priority

                # initialize the unvisited set
            unvisited = list(self.maze.grid)
            self.__start = start_cell if start_cell else rng.choice(unvisited)
            self.store_item("start cell", self.__start.index)
            self.__unvisited = set(unvisited)   # hash

                # initialize the queue
            qargs, qkwargs = init
            self.__q = QueueClass(*qargs, **qkwargs)

        def initialize(self):
            """initialization"""
                # set up the statistics
            self.store_item("cells", 0)
            self.store_item("passages", 0)

        def configure(self):
            """configuration"""
                # get the ball rolling
            self.__discover(self.__start)

        @property
        def more(self):
            """returns False if the queue is empty or all cells are visited

            Overrides Algorithm.more.
            """
            return not self.is_empty and bool(self.__unvisited)

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def discover_in_order(self, cell):
            """visit pass - unshuffled"""
            self.increment_item("cells")
            self.__unvisited.remove(cell)

            for nbr in cell.neighbors:
                if nbr in self.__unvisited:
                    self.enter(cell, nbr)           # visited, unvisited

        def discover_random(self, cell):
            """visit pass - shuffled"""
            self.increment_item("cells")
            self.__unvisited.remove(cell)

            nbrs = list()
            for nbr in cell.neighbors:
                if nbr in self.__unvisited:
                    nbrs.append(nbr)

            if not nbrs:                        # done with this one
                return

            nbr = rng.shuffle(nbrs)             # reorder
            for nbr in nbrs:
                self.enter(cell, nbr)           # visited, unvisited

        def visit(self):
            """the main loop"""
            cell, nbr = self.__q.leave()
            if nbr in self.__unvisited:
                self.link(cell, nbr)
                self.__discover(nbr)

# end module mazes.Algorithms.growing_tree2