"""
mazes.Algorithms.hunt_kill - the hunt and kill algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of the hunt and kill maze carving algorithm.
    The algorithm is as follows:

        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;
            the starting cell is now the current cell.

        Loop until every cell has been visited:
            if the current cell has an unvisited neighbor:
                        (kill)
                choose a random unvisited neighbor of the current cell;
                carve a passage between the cell and this neighbor;
                now the neighbor is the current cell;
            otherwise:
                        (hunt)
                choose a random unvisited cell that has a visited neighbor;
                carve a passage from the cell to a visited neighbor.
                now the cell is the current cell.

    (See [1], pages 67-71 and 251.

NOTES

    If the grid is not connected, the algorithm (and its implementation here)
    will not terrminate,

    Even if the grid is connected, the algorithm (and its implementation here)
    might not terminate.  The actual probability of this is quite low.
    (The probability for the algorithm is zero.  Whether it can actually happen
    with this implementation is unknown.)  There is no practical way of
    distinguishing between a very slow run and a run that will never terminate.

IMPLEMENTATION

    The class AldousBroder is built on the Algorithm class in the usual way.
    Run the implementation as:
        status = AldousBroder.on(maze)
    See method parse_args() in AldousBroder.Status for optional arguments.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 67-71, 251.

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

class HuntKill(Algorithm):
    """the hunt and kill maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Hunt and Kill"

        __slots__ = ("__visited", "__frontier", "__current_cell")

        def parse_args(self, start_cell:'Cell'=None):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell
            """
            super().parse_args()                # chain to parent
            self.__current_cell = start_cell

        def initialize(self):
            """initialization"""
            self.__visited = set()
            if self.__current_cell == None:
                self.__current_cell = rng.choice(list(self.maze.grid))
            self.__frontier = {self.__current_cell}

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.maze.grid))
            self.store_item("passages", 0)
            self.store_item("hunt", 0)
            self.store_item("kill", 0)
            self.store_item("starting cell", self.__current_cell.index)
                # process the starting cell
            if self.__current_cell not in self.maze.grid:
                raise ValueError("The starting cell was not found.")
            self.update_frontier(self.__current_cell)

        @property
        def more(self):
            """returns True if there are unvisited cells

            Overrides Algorithm.more.
            """
            return bool(self.__frontier)

        def visited(self, cell):
            """returns True if the cell has been visited"""
            return cell in self.__visited

        @property
        def random_frontier_cell(self):
            """get a random cell from the frontier"""
            return rng.choice(list(self.__frontier))

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def update_frontier(self, cell):
            """update the frontier"""
            self.__visited.add(cell)
            self.__frontier.remove(cell)
            for nbr in cell.neighbors:
                if nbr not in self.__visited:
                    self.__frontier.add(nbr)
            self.__current_cell = cell

        def kill(self, cell, nbrs):
            """kill phase

            ARGUMENTS

                cell - the current cell

                nbrs - a non-empty list of unvisited neighbors
            """
            self.increment_item("kill")
            nbr = rng.choice(nbrs)
            self.link(cell, nbr)
            self.update_frontier(nbr)

        def hunt(self):
            """hunt phase"""
            self.increment_item("hunt")
            cell = self.random_frontier_cell
            nbrs = []
            for nbr in cell.neighbors:
                if self.visited(nbr):
                    nbrs.append(nbr)
            nbr = rng.choice(nbrs)          # nbrs is a non-empty list
            self.link(cell, nbr)
            self.update_frontier(cell)

        def _visit(self, cell):
            """hunt or kill?"""
            nbrs = []
            for nbr in cell.neighbors:
                if not self.visited(nbr):
                    nbrs.append(nbr)
            if nbrs:
                self.kill(cell, nbrs)
            else:
                self.hunt()

        def visit(self):
            """a single pass -- wrapper for _visit"""
            self._visit(self.__current_cell)

# end module mazes.Algorithms.hunt_kill