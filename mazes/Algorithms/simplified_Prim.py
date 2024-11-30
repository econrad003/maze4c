"""
mazes.Algorithm.simplified_Prim - a growing tree algorithm that is
    superficially similar to Prim's algorithm.
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The algorithm is described on pages 179-181 of the Jamis Buck book.  It
    is a growing tree algorithm that is sometimes incorrectly called Prim's
    algorithm.

    The basic algorithm is follows:

        Mark the start cell as active and visited.
        Loop until there are no active cells:
            choose a random active cell;
            if the cell has an unvisited neighbor:
                carve a passage from the cell to the neighbor;
                mark the neighbor as active and visited;
            otherwise:
                remove the cell from the active list.

    The similarities between this algorithm, DFS, and BFS striking.  All three
    along with Prim's algorithm (the real Prim's algorithm) are growing tree
    algorithms.  The name is appropriate as we start with a single cell and
    expand the maze like a tree's root system.  (We might also call them
    mycelial network algorithms as they grow a maze much like the growth of
    a mycelial network that supports a fungus.)

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
from mazes.active_list import ActiveList

class NotPrim(Algorithm):
    """a growing tree algorithm that isn't really Prim's algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = 'Simplified "Prim"'

        __slots__ = ("__active", "__maxlen", "__visited", "__visit")

                # STACK OPERATIONS

        def push(self, cell):
            """push the cell onto the active list"""
            self.__active.push(cell)
            if len(self.__active) > self.__maxlen:
                self.__maxlen = len(self.__active)
                self.store_item("maximum list length", self.__maxlen)

        def fetch(self, index):
            """fetch a cell from the active list"""
            return self.__active[index]

        def jettison(self, index):
            """remove a cell (by index) from the active list"""
            del self.__active[index]

        def random(self) -> int:
            """choose a random entry in the active list

            An index is returned.
            """
            return rng.randrange(len(self.__active))

        @property
        def more(self):
            """condition for looping"""
            return len(self.__active) > 0

                # INITIALIZATION

        def parse_args(self, start_cell:'Cell'=None, shuffle:bool=True):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                shuffle - if False, neighbors are processed first come,
                    first served.
            """
            super().parse_args()                # chain to parent
            self.__visit = self.visit_random if shuffle \
                else self.visit_in_order

                # initialize the visited set and the active list
            unvisited = list(self.maze.grid)
            if start_cell == None:
                start_cell = rng.choice(unvisited)
            self.store_item("start cell", start_cell.index)
            self.__visited = {start_cell}
            self.__active = ActiveList()
            self.__maxlen = 0
            self.push(start_cell)               # one cell

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 1)         # the starting cell
            self.store_item("passages", 0)

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def visit_in_order(self):
            """visit a cell"""
            index = self.random()
            cell = self.fetch(index)            # get an active cell
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.link(cell, nbr)
                    self.__visited.add(nbr)
                    self.push(nbr)
                    self.increment_item("cells")
                    return                      # successful visit
            self.jettison(index)            # unsuccessful visit

        def visit_random(self):
            """visit a cell"""
            index = self.random()
            cell = self.fetch(index)            # get an active cell
            nbrs = list()
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    nbrs.append(nbr)

            if not nbrs:                        # unsuccessful visit
                self.jettison(index)
                return

            nbr = rng.choice(nbrs)              # successful visit
            self.link(cell, nbr)
            self.__visited.add(nbr)
            self.push(nbr)
            self.increment_item("cells")

        def visit(self):
            """visit or basic pass"""
            self.__visit()

# end module mazes.Algorithms.simplified_Prim