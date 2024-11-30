"""
mazes.Algorithms.dfs_better - the depth-first search maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a better implementation of the depth-first search maze carver.
    The basic algorithm is follows:

        Push the start cell on the stack and mark it as visited
        Loop until the stack is empty:
            Consider the cell at the top of the stack;
            if the cell has an unvisited neighbor:
                carve a passage from the cell to the neighbor;     [*]
                mark the neighbor as visited
                push the neighbor onto the stack;
            otherwise:
                pop the cell from the stack

    This is the algorithm that was used in the Ruby implementation of
    recursive backtracker found in [1].  It minimizes the growth of the
    stack.  It is implicitly edge-based. but see the note that follows.

    [*] If, instead of carving a passage from the cell to the selected
        neighbor, we carve a passage from the neighbor to one of the neighbor's
        visited neighbors, we have a frontier-based version of the algorithm.

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

class DFS(Algorithm):
    """the depth-first search maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Depth-first Search (DFS)"

        __slots__ = ("__stack", "__maxlen", "__visited", "__visit")

                # STACK OPERATIONS

        def push(self, cell):
            """push the data onto the stack"""
            self.__stack.append(cell)
            if len(self.__stack) > self.__maxlen:
                self.__maxlen = len(self.__stack)
                self.store_item("maximum stack depth", self.__maxlen)

        def pop(self):
            """pop and return the top of the stack"""
            return self.__stack.pop()

        def top(self):
            """return the top of the stack"""
            return self.__stack[-1]

        @property
        def is_empty(self):
            """condition for termination"""
            return len(self.__stack) == 0

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
            self.__visit = self.visit_random if shuffle else self.visit_first

                # initialize the unvisited set and the stack
            if start_cell == None:
                unvisited = list(self.maze.grid)
                start_cell = rng.choice(unvisited)
            self.store_item("start cell", start_cell.index)
            self.__visited = {start_cell}       # hash
            self.__stack = list()
            self.__maxlen = 0
            self.push(start_cell)               # one cell

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

        def visit_first(self):
            """visit pass - unshuffled"""
            cell = self.top()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.link(cell, nbr)            # link to the first
                    self.__visited.add(nbr)
                    self.increment_item("cells")
                    self.push(nbr)
                    return                          # new top of stack

            self.pop()                          # all done with this one

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
                self.pop()
                return

            nbr = rng.choice(nbrs)              # random choice
            self.link(cell, nbr)                # link to it
            self.__visited.add(nbr)
            self.increment_item("cells")
            self.push(nbr)

        def visit(self):
            """wrapper for __visit"""
            self.__visit()

# end module mazes.Algorithms.dfs_better