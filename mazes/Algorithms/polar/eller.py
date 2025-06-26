"""
mazes.Algorithms.polar.eller - Eller's algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This variant of Eller's algorithm works in a polar grid.  It
    generalizes inwinder and outwinder, two ring-oriented variants of
    sidewinder.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 189-197, 250.

IMPLEMENTATION

    Two classes are implemented here:

        PolarEller - a subclass of Eller.

        PolarEller.Status - a subclass of Eller.Status

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

MODIFICATIONS

    23 December 2024 - EC
        Pop the None indicator from the path in make_row.  The error occurred
        in the innermost ring of mazes whose smaller dimension was odd.  Other
        rectangular mazes are not affected by the problem or by the fix.
"""
from random import randrange
import mazes
from mazes import rng, Algorithm
from mazes.Algorithms.eller import Eller, _MetaMethod, coin_toss, select_pair

INWARD = "inward"
OUTWARD = "outward"

        # orientation is counterclockwise...

CCW = "ccw"

class PolarEller(Algorithm):
    """Ellerish maze carving algorithm for the Θ grid"""

    class Status(Eller.Status):
        """most of the work is done in Eller.Status"""

        NAME = "Polar Eller"

        VALID_DIRECTIONS = ((CCW, INWARD), (CCW, OUTWARD))

        __slots__ = ("__rings", "__inward")

                # Grid Management

        def make_row(self, onward):
            """create the row method"""
            def make_path(i, grid=None):
                """turn a ring into a path"""
                k = randrange(self.grid.n(i))
                if self.debugging:
                    print(f"row={i}, length={grid.n(i)}, fold={k}")
                for cell in self.grid.ring(i, fold=k):
                    yield cell

            method =_MetaMethod(make_path, grid=self.maze.grid)
            super().make_row(method)

        def make_rows(self, outward):
            """create the rows method"""
            def ring_range():
                """from innermost to outermost"""
                return self.__rings

            super().make_rows(_MetaMethod(ring_range))

        def inward(self, cell) -> list:
            """return the inward cell (as a singleton list)"""
            if cell[INWARD]:
                return [cell[INWARD]]
            return []

        def outward(self, cell) -> list:
            outward_cells = []
            for j in range(cell.split):
                if cell.outward(j):
                    outward_cells.append(cell.outward(j))
            return outward_cells

        def upward(self, cell) -> list:
            """return the cells in the radial direction"""
            return self.inward(cell) if self.__inward \
                else self.outward(cell)

        def maybe_carve_upward(self, registry, registryp, cell, nbr):
            """proceed only if optional carve upward is allowed"""
            try:
                registryp.component_for(nbr)
            except KeyError:
                super().maybe_carve_upward(registry, registryp, cell, nbr)

                # Initialization and configuration

        def parse_args(self, upward=OUTWARD,
                       flip1 = (coin_toss, (), {"bias":0.5}),
                       flip2 = (coin_toss, (), {"bias":1/3}),
                       required_choice = (select_pair, (), {}),
                       debug = 0, labels=False):
            """parse constructor arguments

            USAGE

                The first argument, the uncarved maze, is passed as the
                first argument to the constructor (__init__ in class
                Algorithm.Status).  Method parse_args is called by the
                constructor with any remaining arguments.

                The remaining arguments are processed here.

            KEYWORD ARGUMENTS

                upward - inward (default) or outward

                flip1 - the coin toss handler for merging two adjacent cells
                    in the same row.  The default is a fair coin.

                flip2 - the coin toss handler for optional upward carving. The
                default is a head in 1 of 3 tosses, or equivalently 1:2 odds
                for head:tail.

                    The method handlers for flip1 and flip2.are provided with
                    two required arguments, namely the cells whose components
                    may be merged.  These, along with any optional arguments
                    and any keyword arguments except "bias", are ignored.

                required_choice - the handler for required upward carving.  The
                    method handler is provided a run consisting of (cell,nbr)
                    pairs with cell in the current row (or column, or more
                    generally: tier) and nbr its grid neighbor in the next tier.

                    The method handlers for flip1, flip2, and required choice
                    are triples (name, args, kwargs) consisting of:
                        name - a method name;
                        args - a tuple listing and additional named or
                            optional arguments;
                        kwargs - a dictionary which supplies keyword arguments.
                    The default method for flip1 and flip2 is the procedure
                    coin_toss defined immediately after the Eller module
                    docstring.  The default method for required_choice is
                    procedure select_pair defined after coin_toss.

                debug - display some informative messages indicating what
                    is going on.  If False or 0, no simply informative messages
                    are displayed.  If True or 1, messages tracking row state
                    are displayed.  Higher values will display additional
                    messages.  For example, a value of 5 will also trace merges
                    and a value of 10 will print all of the trace messages.

                    To suppress the warning messages as well as the informative
                    messages, use a value of -10.  The warnings detect
                    connectivity problems that can occur if the the grid is
                    configured in an unusual way or if some cells have been
                    masked.

                    (At this point in time, the author does not plan to use
                    Python's logging module for these messages.)

                labels - default is False; set to true for debugging
            """
            self.__inward = upward != OUTWARD
            super().parse_args(upward=upward, onward=CCW,
                               flip1=flip1, flip2=flip2,
                               required_choice=required_choice,
                               debug=debug, labels=labels)

        def initialize(self):
            """initialization"""
            print(f"Initializing: {self.__inward=}")
            self.__rings = list(self.maze.grid.rings(reverse=self.__inward))
            super().initialize()

# end module mazes.Algorithms.polar.eller
