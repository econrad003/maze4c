"""
mazes.Algorithms.dfs - the depth-first search maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is also known as 'recursive backtracker', but a recursive
    implementation is not practical because of restrictions the size of
    Python's runtime stack.

    The basic algorithm is follows:

        Push the start cell on the stack
        Loop until the stack is empty or every cell has been visited:
            pop a cell from the stack;
            if the cell hasn't been visited:
                carve a passage from the cell to the visited area;
                mark the cell as visited;
            push the cell's unvisited neighbors onto the stack.

    There are a number of different ways of doing this.  The key ambiguity is
    in the command 'carve a passage from the visited area'.  Two ways of
    implementing this are:

        (1) edge-based

            When we push a cell (other than the start cell) onto the stack,
            we keep track of its already visited neighbor.  When we carve
            the passage, we carve it from the cell to its known neighbor.

        (2) frontier-based

            When we are ready to carve a passage, we choose a visited neighbor,
            perhaps randomly, perhaps simply the first one we encounter.

IMPLEMENTATION

    We have implemented several variations:

        edge-based
            unshuffled neighborhood
            shufffled neighborhood

        frontier-based
            unshuffled neighborhood
            shufffled neighborhood

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

        __slots__ = ("__stack", "__maxlen", "__unvisited", "__shuffle")

                # STACK OPERATIONS

        def push(self, *args):
            """push the data onto the stack"""
            self.__stack.append(args)           # pack and append
            if len(self.__stack) > self.__maxlen:
                self.__maxlen = len(self.__stack)
                self.store_item("maximum stack depth", self.__maxlen)

        def pop(self):
            """pop and return the top of the stack"""
            return self.__stack.pop()

        @property
        def is_empty(self):
            """condition for termination"""
            return len(self.__stack) == 0 or len(self.__unvisited) == 0

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None,
                       edge_based:bool=True, shuffle:bool=True):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                edge_based - if False, then frontier-based.

                shuffle - if False, neighbors are processed first come,
                    first served.  (Being pushed onto the stack counts
                    as being served, so "the first shall be last" and
                    "the last shall be first".)
            """
            super().parse_args()                # chain to parent
            self.__shuffle = shuffle

                # initialize the unvisited set and the stack
            unvisited = list(self.maze.grid)
            if start_cell == None:
                start_cell = rng.choice(unvisited)
            self.store_item("start cell", start_cell.index)
            self.__unvisited = set(unvisited)   # hash
            self.__stack = list()
            self.__maxlen = 0
            if edge_based:
                self.push(None, start_cell)     # two cells
            else:
                self.push(start_cell)           # one cell

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 0)
            self.store_item("passages", 0)
                # set up the iteration
            self.more = True

        def link(self, cell, nbr):
            """carve a passage"""
            if cell != None:
                self.maze.link(cell, nbr)
                self.increment_item("passages")

        def push_edges_in_order(self, cell):
            """push the edges in neighborhood order onto the stack"""
            for nbr in cell.neighbors:
                if nbr in self.__unvisited:
                    self.push(cell, nbr)

        def push_edges(self, cell):
            """push the edges after shuffling them"""
            nbrs = list()
            for nbr in cell.neighbors:
                if nbr in self.__unvisited:
                    nbrs.append(nbr)
            if len(nbrs) == 0:
                return
            rng.shuffle(nbrs)
            for nbr in nbrs:
                self.push(cell, nbr)

        def visit_edge(self, nbr, cell):
            """visit and edge"""
            if cell in self.__unvisited:
                self.link(nbr, cell)
                self.__unvisited.remove(cell)
                self.increment_item("cells")

            if not self.__shuffle:
                    # first come, first served (into the stack)
                self.push_edges_in_order(cell)
            else:
                    # shuffle
                self.push_edges(cell)

        def visit_cell(self, cell):
            """visit and edge"""
                    # classify the neighborhood
            visited = list()
            unvisited = list()
            for nbr in cell.neighbors:
                if nbr in self.__unvisited:
                    if nbr != cell:             # guard against loops!
                        unvisited.append(nbr)
                else:
                    visited.append(nbr)

                    # visit the cell if
            if cell in self.__unvisited:
                if visited:                     # not the starting cell
                    nbr = rng.choice(visited)
                    self.maze.link(nbr, cell)
                self.__unvisited.remove(cell)
                self.increment_item("cells")

                    # process the unvisited neighbors
            if not unvisited:
                return
            if self.__shuffle:
                rng.shuffle(unvisited)          # shuffle in place
            for nbr in unvisited:
                self.push(cell, nbr)

        def visit(self):
            """visit or basic pass"""
            if self.is_empty:
                self.more = False
                return
            package = self.pop()
            if len(package) == 2:
                self.visit_edge(*package)
            else:
                self.visit_cell(*package)

# end module mazes.Algorithms.dfs
