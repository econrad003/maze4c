"""
mazes.Algorithms.houston - a hybrid random walk algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an implementation of a hybrid random walk maze carver, which
    Jamis Buck refers to this in [3] as Houston's algorithm .  The algorithm
    was suggested in Buck's blog in a response by Robin Houston dated 20
    January 2011.  From the followup the next day, it is not known whether
    the resulting maze is uniform.

    The basic algorithm is as follows:

        Use first-entrance Aldous/Broder until the size of the unvisited area
        falls below a given threshold;  then use Wilson's algorithm to complete
        the maze.

NOTES

    If the grid is not connected, the algorithm (and its implementation here)
    will not terrminate,

    Even if the grid is connected, the algorithm (and its implementation here)
    might not terminate.  The actual probability of this is quite low.
    (The probability for the algorithm is zero.  Whether it can actually happen
    with this implementation is unknown.)  There is no practical way of
    distinguishing between a very slow run and a run that will never terminate.

    Houston's algorithm takes advantage of ALdous/Broder's initial quick
    capture of are and Wilson's algorithm speedy finish when most of the maze
    is complete.

IMPLEMENTATION

    The class Houston is built on the Algorithm class in the usual way.
    Run the implementation as:
        status = Houston.on(maze)
    See method parse_args() in Wilson.Status for optional arguments.

    Most of the code here was lifted from my implementation of the
    Aldous/Broder and Wilson classes.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 60-65, 255.

    [2] Jamis Buck.  "Maze Generation: Wilson's algorithm" in the Buckblog.
        Web.  Accessed 21 January 2024.
            http://weblog.jamisbuck.org/2011/1/20/ -
                maze-generation-wilson-s-algorithm.html
        See the responses by Robin Houston that are dated 20 and 21 January,
        2011.

    [3] Jamis Buck.  Maze Algorithms.  Web.  Accessed 21 December 2024.
        https://www.jamisbuck.org/mazes/

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

class Houston(Algorithm):
    """the hybrid random walk maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Hybrid Random Walk (Houson)"

        __slots__ = ("__unvisited", "__current_cell", "__path",
                     "__wilson", "__threshold", "__frate", "__fails")

        def parse_args(self, start_cell:'Cell'=None,
                       cutoff_rate=2/3,
                       failure_rate=0.9):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                start_cell - an optional starting cell

                cutoff_rate - switches to Wilson if the ratio of unvisited
                    cells to all cells falls below the cutoff rate.  With
                    the default (2/3) and a grid with 100 cells, the algorithm
                    seitches to Wilson when the unvisited area falls down to
                    66 cells (since 67 >= 2/3(100) > 66).

                failure_rate - switches to Wilson if the ratio of consecutive
                    failures (i.e. visits of already visited cells) to
                    unvisited cells exceeds this value.  If the unvisited area
                    has 100 cells, then 91 consecutive visits of already
                    visited cells will trigger this threshold.
            """
            super().parse_args()                # chain to parent
            self.__current_cell = start_cell
            self.__threshold = cutoff_rate
            self.__frate = failure_rate

        def initialize(self):
            """initialization"""
            unvisited = list(self.maze.grid)
            self.__unvisited = set(unvisited)
            if self.__current_cell == None:
                self.__current_cell = rng.choice(unvisited)
            self.__path = None
                    # switching controls
            self.__wilson = False
            self.__threshold = int(self.__threshold * len(unvisited))
            self.__fails = 0

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.__unvisited))
            self.store_item("passages", 0)
            self.store_item("cuttoff threshold", self.__threshold)
            self.store_item("failure rate", self.__frate)
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

                # WILSON'S ALGORITHM

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

        def wilson_visit(self):
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

                # ALDOUS/BRODER

        def ab_visit(self, cell, unvisited):
            """a single pass -- this is as simple as it gets"""
            nbr = rng.choice(list(cell.neighbors))
            if nbr in unvisited:
                self.link(cell, nbr)
                unvisited.remove(nbr)
                self.__fails = 0
            else:
                self.__fails += 1
            self.__current_cell = nbr

                # HYBRID

        def visit(self):
            """decide what to do"""
            if self.__wilson:
                self.wilson_visit()
                return
            self.ab_visit(self.__current_cell, self.__unvisited)

                # ARE WE READY TO SWITCH?
            if len(self.__unvisited) <= self.__threshold:
                self.store_item("trigger", "cutoff threshold")
                self.__wilson = True
            elif self.__fails > self.__frate * len(self.__unvisited):
                self.store_item("trigger", "failure threshold")
                self.__wilson = True

# end module mazes.Algorithms.houston