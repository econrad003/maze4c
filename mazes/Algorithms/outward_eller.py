"""
mazes.Algorithms.outward_eller - Eller's algorithm (ouward ring version)
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This variant of Eller's algorithm works outward using ringed tiers.  It
    generalizes outwinder, the outward variant of sidewinder.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 189-197, 250.

IMPLEMENTATION

    Two classes are implemented here:

        OutwardEller - a subclass of Eller.

        OutwardEller.Status - a subclass of Eller.Status

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
from mazes.Algorithms.eller import Eller, _MetaMethod, coin_toss, select_pair
from mazes.Grids.oblong_rings import ConcentricOblongs

OUTWARD = "outward"

        # the following orientations are all accepted...

        #   three are taken as the clockwise direction
CLOCK = "clockwise"
CW = "cw"
LEFT = "left"                       # left hand curves clockwise

        #   five are taken as the counterclockwise direction
CCLOCK = "counterclockwise"         # US
CCW = "ccw"
ACLOCK = "anticlockwise"            # UK
ACW = "acw"
RIGHT = "right"                     # right hand curves ccw/acw

class OutwardEller(Algorithm):
    """outward-Ellerish maze carving algorithm"""

    class Status(Eller.Status):
        """most of the work is done in Eller.Status"""

        NAME = "Outward Eller"

        VALID_DIRECTIONS = set([(CLOCK, OUTWARD), (CW, OUTWARD), \
            (CCLOCK, OUTWARD), (CW, OUTWARD), (ACLOCK, OUTWARD), \
            (ACW, OUTWARD), (LEFT, OUTWARD), (RIGHT, OUTWARD)])

        __slots__ = ("__rings")

                # Grid Management

        def make_row(self, onward):
            """create the row method"""
            def make_path(i, reverse=False, rings=None, grid=None):
                """turn a ring into a path"""
                path = rings.pathmaker(i)
                rot = rng.randrange(len(path)) if path[-1] else None
                path = rings.transform(path, reverse=reverse, rotate=rot)
                for index in path:
                    cell = grid[index]
                    if not cell.hidden:
                        yield cell

            ccw = onward not in {CLOCK, CW, LEFT}
            method =_MetaMethod(make_path, reverse=ccw,
                                rings=self.__rings, grid=self.maze.grid)
            super().make_row(method)

        def make_rows(self, outward):
            """create the rows method"""
            def ring_range():
                """from innermost to outermost"""
                return range(len(self.__rings)-1, -1, -1)

            super().make_rows(_MetaMethod(ring_range))

        def upward(self, cell) -> list:
            """return the cells in the outward direction"""
            nbrs = self.__rings.classify(cell)
            outward = []
            for nbr in nbrs:
                if nbrs[nbr] == -1:
                    outward.append(nbr)
            return outward

                # Initialization and configuration

        def parse_args(self, onward:str="clockwise",
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

                onward - clockwise (default) or counterclockwise

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
            super().parse_args(onward=onward, upward="outward",
                               flip1=flip1, flip2=flip2,
                               required_choice=required_choice,
                               debug=debug, labels=labels)

        def initialize(self):
            """initialization"""
            self.__rings = ConcentricOblongs(self.maze.grid)
            super().initialize()

# end module mazes.Algorithms.eller