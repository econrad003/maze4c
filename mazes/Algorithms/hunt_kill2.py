"""
mazes.Algorithms.hunt_kill - the hunt and kill algorithm (scanning version)
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an alternate implementation of the hunt and kill maze carving
    algorithm, perhaps more in line with the description in [1].  The
    difference is in the hunting phase.  Instead of choosing a random frontier
    cell, the cells are scanned and the first frontier cell found is the
    result of the hunt.  The algorithm is as follows:

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
                scan for an unvisited cell that has a visited neighbor;
                carve a passage from the cell to a visited neighbor.
                now the cell is the current cell.

    There is less overhead as the algorithm does not maintain a frontier
    set, but the overhead reduction does entail a cost: the hunt potentially
    scans all unvisited cells.  How this change affects time complexity is
    hard to predict, as choosing a random frontier element requires converting
    a set into a list.

    (See [1], pages 67-71 and 251.)

NOTES

    If the grid is not connected, the algorithm will terminate with a
    tree in the starting component and isolated cells in the remaining
    components.

IMPLEMENTATION

    The class HuntKill is built on the Algorithm class in the usual way.
    Run the implementation as:
        status = HuntKill.on(maze)
    See method parse_args() in HuntKill.Status for optional arguments.

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
from mazes import rng, Algorithm, Cell

class HuntKill(Algorithm):
    """the hunt and kill maze carving algorithm (with scanning)"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Hunt/Scan and Kill"

        __slots__ = ("__unvisited", "__current_cell", "__hunt_failed")

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
            self.__unvisited = list(self.maze.grid)
            if self.__current_cell == None:
                self.__current_cell = rng.choice(self.__unvisited)
            self.__unvisited = set(self.__unvisited)
            self.__hunt_failed = False

        @property
        def unvisited(self) -> frozenset:
            """returns the unvisited set as a frozen set"""
            return frozenset(self.__unvisited)

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.maze.grid))
            self.store_item("passages", 0)
            self.store_item("hunt", 0)
            self.store_item("kill", 0)
            self.store_item("scans", 0)
            self.store_item("starting cell", self.__current_cell.index)
                # process the starting cell
            if self.__current_cell not in self.maze.grid:
                raise ValueError("The starting cell was not found.")
            self.__unvisited.remove(self.__current_cell)

        @property
        def more(self):
            """returns True if there are unvisited cells

            Overrides Algorithm.more.
            """
            return len(self.__unvisited) > 0 and not self.__hunt_failed

        def visited(self, cell:Cell):
            """returns True if the cell has been visited"""
            return cell not in self.__unvisited

        def hunt_failed(self):
            """log a hunt failure and return two nothings

            Called by scan if a frontier cell is not found.  Subclasses
            should call this in the event of a hunt failure.
            """
            self.__hunt_failed = True
            self["hunt failed"] = True
            return None, None

        def scan(self):
            """returns a frontier cell and a visited neighbor

            This scanning operation searches the unvisited region for
            a frontier cell.  Each access is counted in the "scans" status
            variable.

            Subclasses may redefine this.  See also property "unvisited" and
            method "hunt_failed".
            """
            for cell in self.__unvisited:
                for nbr in cell.neighbors:
                    self["scans"] += 1          # for status 
                    if nbr not in self.__unvisited:
                        return cell, nbr
                # failed hunt!
            return self.hunt_failed()

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def kill(self, cell, nbrs):
            """kill phase

            ARGUMENTS

                cell - the current cell

                nbrs - a non-empty list of unvisited neighbors
            """
            self.increment_item("kill")
            nbr = rng.choice(nbrs)
            self.link(cell, nbr)
            self.__unvisited.remove(nbr)
            self.__current_cell = nbr

        def hunt(self):
            """hunt phase"""
            self.increment_item("hunt")
            cell, nbr = self.scan()
            if cell == None:
                return                      # failed hunt
            self.link(cell, nbr)
            self.__unvisited.remove(cell)
            self.__current_cell = cell

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

# end module mazes.Algorithms.hunt_kill2
