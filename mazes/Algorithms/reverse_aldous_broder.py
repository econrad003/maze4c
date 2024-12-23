"""
mazes.Algorithms.reverse_aldous_broder - the last exit random walk algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of the last exit random walk maze carver,
    or (simply) reverse Aldous/Broder.  The algorithm is as follows:

        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;
            the starting cell is now the current cell;
            initialize an asssociative array "tentative exits".

        Loop until every cell has been visited:
            choose a random neighbor of the current cell;
            if this neighbor has not been visited:
                (this is a first entrance!)
                remove the neighbor from the unvisited set
            set the tentative exit from the current cell to the neighbor;
            now the neighbor is the current cell.

        Loop through all cells in the tentative exit list:
            carve a passage from the cell to its neighbor in the list.

    The algorithm is a modified version of the Aldous/Broder first entrance
    random walk.  If the random choices are uniformly random, then the result
    is also a uniformly random spanning tree.

    When implemented as a passage carver (as described above), the algorithm
    has some extra overhead, but it's time complexity is asymptoticly the
    same as for its first entrance counterpart.

NOTES

    If the grid is not connected, the algorithm (and its implementation here)
    will not terrminate,

    Even if the grid is connected, the algorithm (and its implementation here)
    might not terminate.  The actual probability of this is quite low.
    (The probability for the algorithm is zero.  Whether it can actually happen
    with this implementation is unknown.)  There is no practical way of
    distinguishing between a very slow run and a run that will never terminate.

IMPLEMENTATION

    The class ReverseAldousBroder is built on the Algorithm class with a small
    modification.  Run the implementation in the usual way as:
        status = ReverseAldousBroder.on(maze)
    See method parse_args() in ReverseAldousBroder.Status for optional
    arguments.

    The "on" classmethod in the algorithm has been modified to include an after
    action ("afterwards") that takes place after the last "visit".

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 55-60, 249.

    [2] Yiping Hu, Russell Lyons and Pengfei Tang.  A reverse Aldous/Broder
        algorithm.  Preprint.  Web: arXiv.org.  24 Jul 2019.
            http://arxiv.org/abs/1907.10196v1

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

class ReverseAldousBroder(Algorithm):
    """the last exit random walk maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Last Exit Random Walk (Reverse Aldous/Broder)"

        __slots__ = ("__unvisited", "__current_cell", "__last_exit")

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
            unvisited = list(self.maze.grid)
            self.__unvisited = set(unvisited)
            if self.__current_cell == None:
                self.__current_cell = rng.choice(unvisited)
            self.__last_exit = dict()

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.__unvisited))
            self.store_item("passages", 0)
            self.store_item("starting cell", self.__current_cell.index)
                # process the starting cell
            if self.__current_cell not in self.__unvisited:
                raise ValueError("The starting cell was not found.")
            self.__unvisited.remove(self.__current_cell)

        @property
        def more(self):
            """returns True if there are unvisited cells

            Overrides Algorithm.more.
            """
            return bool(self.__unvisited)

        def link(self, cell, nbr):
            """carve a passage"""
            self.maze.link(cell, nbr)
            self.increment_item("passages")

        def _visit(self, cell, unvisited):
            """a single pass -- this is as simple as it gets"""
            nbr = rng.choice(list(cell.neighbors))
            if nbr in unvisited:
                unvisited.remove(nbr)
            self.__last_exit[cell] = nbr
            return nbr

        def visit(self):
            """a single pass -- wrapper for _visit"""
            self.__current_cell = self._visit(self.__current_cell,
                                              self.__unvisited)

        def afterwards(self):
            """carve the maze"""
                # at this point, no passages have been carved.  The following
                # loop carves the passages.
            for cell in self.__last_exit:
                nbr = self.__last_exit[cell]
                self.link(cell, nbr)

    @classmethod
    def on(cls, maze:'Maze', *args, status=None, **kwargs):
        """algorithm execution -- including an afterwards action"""
        if status == None:
            status = cls.Status(maze, *args, **kwargs)

        while status.more:
            status.increment_item("visits")
            status.visit()

        status.afterwards()             # added action

        return status

# end module mazes.Algorithms.reverse_aldous_broder