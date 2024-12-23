"""
mazes.Algorithms.aldous_broder - the first entrance random walk algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of the first entrance random walk maze carver,
    or (simply) Aldous/Broder.  The algorithm is as follows:

        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;
            the starting cell is now the current cell.

        Loop until every cell has been visited:
            choose a random neighbor of the current cell;
            if this neighbor has not been visited:
                (this is a first entrance!)
                remove the neighbor from the unvisited set
                carve a passage from the current cell to the neighbor;
            now the neighbor is the current cell.

    The algorithm is named after David Aldous and Andrei Broder who
    independently discovered the algorithm.  If the random choices are
    uniformly random, then the result is a uniformly random spanning tree.
    There is a more precise way of saying this:

        Let T be the set of all spanning trees of a connected grid G and let
        t be any member of T.  Given a spanning tree s resulting from a
        completed run of Aldous/Broder:
            P(s=t) = 1 / |T|.

    There are some assumptions here, The first (explicitly stated!) is that
    the algorithm terminates (or "completes").  With a bad random sequence, the
    algorithm will never finish.  For example, on a rectangular grid with more
    than one row, if the random neighbor is always east or west of the current
    cell, then the algorithm won't terminate.  Of course, the probability that
    this is the is the given random sequence is zero, i.e.,
            P(neighbor is always east or west) = 0
    But zero probability is not the same as impossible.

    The second assumption (not explicitly stated above) is that the random
    neighbor generator is a uniformly random sequence,  For example, if we use
    a periodic pseudo-random sequence (such as the sequence produced by
    Python's random.choice() method), then all bets are off.  For a
    sufficiently large grid, the number of spanning trees of the grid will
    exceed the period of the sequence.

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
        Book (978-1-68050-055-4).  Pages 55-60, 249.

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

class AldousBroder(Algorithm):
    """the first entrance random walk maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "First Entrance Random Walk (Aldous/Broder)"

        __slots__ = ("__unvisited", "__current_cell")

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
                self.link(cell, nbr)
                unvisited.remove(nbr)
            return nbr

        def visit(self):
            """a single pass -- wrapper for _visit"""
            self.__current_cell = self._visit(self.__current_cell,
                                              self.__unvisited)

# end module mazes.Algorithms.aldous_broder