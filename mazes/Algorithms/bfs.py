"""
mazes.Algorithms.bfs - the breadth-first search maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of the breadth-first search maze carver.
    The basic algorithm is follows:

        Place the start cell in the queue and mark it as visited
        Loop until the queue is empty:
            Consider the cell in the front of the queue;
            if the cell has an unvisited neighbor:
                carve a passage from the cell to the neighbor;     [*]
                mark the neighbor as visited
                place the neighbor in the end of the queue;
            otherwise:
                remove the cell from the queue

    Apart from using a queue instead of a stack, this is the same algorithm as
    the more elegant and efficient form of depth-first search.  Note that once
    a cell reaches the front of the queue, it stays in front until it is
    removed from the queue.  So we can incorporate a couple of small
    enhancements:

        Place the start cell in the queue and mark it as visited
        Loop until the queue is empty:
            remove the cell from the front of the queue
            while this cell has an unvisited neighbor:
                carve a passage from the cell to the neighbor;     [*]
                mark the neighbor as visited
                place the neighbor in the end of the queue;

    [*] If, instead of carving a passage from the cell to the selected
        neighbor, we carve a passage from the neighbor to one of the neighbor's
        visited neighbors, we have a frontier-based version of the algorithm.

REMARKS

    A breadth first implementation of the naïve implementation of DFS in
    Algorithms.dfs is not feasible as the queue grow exponentially.

    On an oblong grid, there is not much difference in the output between
    shuffling and taking cells in dictionary order.

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
from collections import deque

import mazes
from mazes import rng, Algorithm

class BFS(Algorithm):
    """the breadth-first search maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Breadth-first Search (BFS)"

        __slots__ = ("__queue", "__maxlen", "__visited", "__visit")

                # QUEUE OPERATIONS

        def enter(self, cell):
            """place a cell in the queue"""
            self.__queue.append(cell)
            if len(self.__queue) > self.__maxlen:
                self.__maxlen = len(self.__queue)
                self.store_item("maximum queue length", self.__maxlen)

        def leave(self):
            """remove the cell in the front of the queue and return it"""
            return self.__queue.popleft()

        @property
        def is_empty(self):
            """condition for termination"""
            return len(self.__queue) == 0

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)
            """
            super().parse_args()                # chain to parent
            self.__visit = self.visit_shuffled if shuffle \
                else self.visit_in_order

                # initialize the unvisited set and the stack
            if start_cell == None:
                unvisited = list(self.maze.grid)
                start_cell = rng.choice(unvisited)
            self.store_item("start cell", start_cell.index)
            self.__visited = {start_cell}       # hash
            self.__queue = deque()
            self.__maxlen = 0
            self.enter(start_cell)               # one cell

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 1)         # the start cell
            self.store_item("passages", 0)

        @property
        def more(self):
            """returns True if the stack is empty

            Overrides Algorithm.more.
            """
            return not self.is_empty

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def visit_in_order(self):
            """visit pass - unshuffled"""
            cell = self.leave()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.link(cell, nbr)            # link to the first
                    self.__visited.add(nbr)
                    self.increment_item("cells")
                    self.enter(nbr)

        def visit_shuffled(self):
            """visit pass - shuffled"""
            cell = self.leave()
            nbrs = list()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    nbrs.append(nbr)
            if not nbrs:
                return                              # nothing to do

            rng.shuffle(nbrs)
            for nbr in nbrs:
                if nbr in self.__visited:
                    continue                # parallel grid edges
                self.link(cell, nbr)                # link to it
                self.__visited.add(nbr)
                self.increment_item("cells")
                self.enter(nbr)

        def visit(self):
            """wrapper for __visit"""
            self.__visit()

# end module mazes.Algorithms.bfs