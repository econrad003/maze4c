"""
mazes.Algorithms.wilson - the circuit-eliminated random walk algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of the circuit-eliminated random walk maze
    carver, or (simply) Wilson's algorithm.  The algorithm is as follows:

        Preparation:
            get a list of cells to be visited;
            choose a starting cell and remove it from the unvisited set;

        Loop until every cell has been visited:
            choose a random cell in the unvisited area as the current cell;
            the walk := [cell]
                    (the random walk)
            while the current cell has not been visited:
                choose one of its neighborsl
                if the neighbor has not been visited:
                    if the neighbor is in the walk:
                                (circuit elimination)
                        remove all cells added since the neighbor was added;
                    otherwise:
                        add the neighbor to the walk
                now the neighbor is the current cell
            add the walk to the maze

    The algorithm is named after David Wilson who discovered the algorithm.
    If the random choices are uniformly random, then the result is a uniformly
    random spanning tree.

NOTES

    If the grid is not connected, the algorithm (and its implementation here)
    will not terrminate,

    Even if the grid is connected, the algorithm (and its implementation here)
    might not terminate.  The actual probability of this is quite low.
    (The probability for the algorithm is zero.  Whether it can actually happen
    with this implementation is unknown.)  There is no practical way of
    distinguishing between a very slow run and a run that will never terminate.

    Unlike Aldous/Broder, Wilson's algorithm tends to be slow at first and
    to speed up as more cells are visited.

    In [1], circuits are referred to as loops.  We reserve the term "loop" for
    a trivial circuit.  Terminology varies.  There is no point in arguing over
    it.  Just get used to the fact.

IMPLEMENTATION

    The class Wilson is built on the Algorithm class in the usual way.
    Run the implementation as:
        status = Wilson.on(maze)
    See method parse_args() in Wilson.Status for optional arguments.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 60-65, 255.

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

class Wilson(Algorithm):
    """the circuit-eliminated random walk maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Circuit-Eliminated Random Walk (Wilson)"

        __slots__ = ("__unvisited", "__current_cell", "__path")

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
            self.__path = None

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.__unvisited))
            self.store_item("passages", 0)
            self.store_item("paths constructed", 0)
            self.store_item("cells visited", 0)
            self.store_item("circuits", 0)
            self.store_item("markers placed", 0)
            self.store_item("markers removed", 0)
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

        def begin_walk(self):
            """begin the circuit-eliminated random walk"""
            self.increment_item("paths constructed")
            self.increment_item("cells visited")
            current = self.__current_cell = rng.choice(list(self.__unvisited))
            self.__path = {current:None}

        def step_forward(self) -> 'Cell':
            """the next step in the walk"""
            cell = self.__current_cell
            nbr = rng.choice(list(cell.neighbors))
            self.increment_item("cells visited")
            if nbr in self.__path:
                self.increment_item("circuits")
                while cell != nbr:
                    doomed = cell
                    cell = self.__path[doomed]
                    del self.__path[doomed]
                    self.increment_item("markers removed")
            else:
                    # mark the path
                self.__path[nbr] = cell
                self.increment_item("markers placed")
            self.__current_cell = nbr
            return nbr

        def end_walk(self):
            """engrave the path from finish back to start"""
            cell = self.__current_cell
            nbr = self.__path[cell]
            while nbr != None:
                self.link(cell, nbr)
                self.__unvisited.remove(nbr)
                cell, nbr = nbr, self.__path[nbr]
            self.__path = None

        def visit(self):
            """construct a path from the unvisited area to the visited region

            This is a circuit-eliminated random walk.  The idea is that as
            we try to find a way out of the desert into civilization,
            we leave a trail which tells us when we have gone around in a
            circle.  As our supply of markers is limited, we remove markers in
            the circuit and the continue our search from that point.
            """
            self.begin_walk()
            while self.step_forward() in self.__unvisited:
                pass
            self.end_walk()

# end module mazes.Algorithms.wilson