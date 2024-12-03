"""
mazes.Algorithms.growing_tree1 - a cell-based growing tree algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a cell-based maze carver which generalizes DFS, BFS, simplified
    Prim and vertex Prim.  It use generalize queuing queuing structure
    which we will simply call the queue.  The basic algorithm is follows:

        Push the start cell in the queue and mark it as visited
        Loop until the queue is empty:
            Consider the top cell in the queue;
            if the cell has an unvisited neighbor:
                carve a passage from the cell to the neighbor;
                mark the neighbor as visited
                place the neighbor in the queue;
            otherwise:
                jettison the cell from the queue

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
from mazes import rng, Algorithm
from mazes.gqueue import GeneralizedQueue

class VertexGrowingTree(Algorithm):
    """a cell-based growing tree algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Vertex Growing Tree"

        __slots__ = ("__q", "__visited", "__visit", '__pr')

                # QUEUE OPERATIONS

        def enter(self, cell):
            """push the data into the queue"""
            if self.__pr:
                self.__q.enter(cell, priority=self.__pr(cell))
            else:
                self.__q.enter(cell)

        def leave(self):
            """pop and return the first entry in the queue"""
            return self.__q.leave()

        def top(self):
            """return the first entry in the queue"""
            return self.__q.top()

        def jettison(self):
            """pop the top"""
            return self.__q.jettison()

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
            if not issubclass(QueueClass, GeneralizedQueue):
                raise ValueError("QueueClass must be a generalized queue type")
            super().parse_args()                # chain to parent
            self.__visit = self.visit_random if shuffle else self.visit_first
            self.__pr = priority

                # initialize the unvisited set and the queue
            if start_cell == None:
                unvisited = list(self.maze.grid)
                start_cell = rng.choice(unvisited)
            self.store_item("start cell", start_cell.index)
            self.__visited = {start_cell}       # hash
            qargs, qkwargs = init
            self.__q = QueueClass(*qargs, **qkwargs)
            self.enter(start_cell)              # one cell

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 1)         # the start cell
            self.store_item("passages", 0)

        @property
        def more(self):
            """returns True if the queue is not empty

            Overrides Algorithm.more.
            """
            return not self.is_empty

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def visit_first(self):
            """visit pass - unshuffled"""
            cell = self.top()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.link(cell, nbr)            # link to the first
                    self.__visited.add(nbr)
                    self.increment_item("cells")
                    self.enter(nbr)
                    return                          # new top of stack

            self.leave()                        # all done with this one

        def visit_random(self):
            """visit pass - shuffled

            We don't really shuffle... we choose at random
            """
            cell = self.top()
            nbrs = list()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    nbrs.append(nbr)

            if not nbrs:                        # done with this one
                self.jettison()                     # remove the selected cell
                return

            nbr = rng.choice(nbrs)              # random choice
            self.link(cell, nbr)                # link to it
            self.__visited.add(nbr)
            self.increment_item("cells")
            self.enter(nbr)                     # enlarge the queue

        def visit(self):
            """wrapper for __visit"""
            self.__visit()

# end module mazes.Algorithms.growing_tree1