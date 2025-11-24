"""
mazes.Wallbuilders.basic_wallbuilder - erecting walls by breaking circuits
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Let M be a maze with ε passages, υ cells and κ components.  If its Euler
    characteristic χ = ε-υ+κ > 0, then M has a circuit C.  Let e be a passage
    in circuit C.  Let M\e be the maze obtained from M by deleting edge e.
    Then M\e has ε-1 passages, υ cells and κ components.  For its Euler
    characteristic:
        χ = (ε-1) - υ + κ ≥ 0
    M\e has the same number of components and the same number of cells.

    A simple wallbuilder can be built from almost any algorithm which
    locates circuits in a maze.  If we allow disconnections, then the
    algorithm must also detect the absence of a circuit.

    The wallbuilder here assumes no precondictions for connectivity.
    When the algorithm completes, the resulting maze has the same number
    of connected components.

    The algorithm may fail in one or more ways if the maze contains directed
    arcs.

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
from mazes import Algorithm
from mazes.Algorithms.qs_circuit_locator import CircuitFinder
from mazes.gqueue import GeneralizedQueue

class BasicWallbuilder(Algorithm):
    """a simple wallbuilding algorithm to use with a circuit locator"""

    class Status(Algorithm.Status):
        """where all the work is done"""

        __slots__ = ("__more", "__shuffle", "__start",
                     "__qType", "__qargs", "__qkwargs")

        @property
        def MyCircuitFinder(self):
            """returns the circuit finder class"""
            return CircuitFinder

        @property
        def locator_name(self):
            """get a name for the locator"""
            Locator = self.MyCircuitFinder
            return getattr(Locator.Status, "NAME", Locator.__name__)

        def find_edge(self) -> "Edge":
            """wrapper for the circuit locator

            returns either an edge or None
            """
            status = self.MyCircuitFinder.on(self.maze, shuffle=self.__shuffle, \
                         start_cell=self.__start, QueueType=self.__qType, \
                         qargs=self.__qargs, qkwargs=self.__qkwargs) \
                if self.__qType else \
                     self.MyCircuitFinder.on(self.maze, shuffle=self.__shuffle, \
                         start_cell=self.__start)
            self["finder passes"] += status["visits"]
            if status.result:
                _1, edge, _2 = status.result
                return edge
            return None

        def unlink(self, edge:"Edge"):
            """unlink an edge"""
            self["unlinks"] += 1
            self.maze.unlink(edge)

        @property
        def more(self):
            """is there more to be done?"""
            return self.__more

        def visit(self):
            """visit cycle"""
            edge = self.find_edge()
            if edge:
                self.unlink(edge)
            else:
                self.__more = False

        def parse_args(self, shuffle:bool=True, start_cell:'Cell'=None,
                       QueueType:"class"=None, qargs=tuple(), qkwargs=dict()):
            """parse the setup arguments

            REQUIRED ARGUMENTS

                maze - a maze object in which walls need to be erected

            KEYWORD ARGUMENTS

                shuffle (default: True) - if False, a cell's neighbors will
                    be traversed in dictionary order.  If true, the neighborhood
                    will be shuffled.

                start_cell (default: None) - if a starting cell is supplied,
                    all circuit location passes will start there.

                    If the maze is disconnected, the search will always start
                    in the component containing the start cell.  For the
                    remaining components, the search will start in a random cell.

                QueueType (default: None) - if None, then the queuing class will
                    be the default, if any, for the CircuitFinder class.  (This
                    will normally be a stack.)  If a class is specified, then the
                    queue will be set up as:
                        q = QueueType(*qargs, **qkwargs)

                    The default for qargs, an empty tuple, results in queue setup
                    as:
                        q =QueueType(**qkwargs)

                    The default for qkwargs, an empty dictionary, results in queue
                    setup as:
                        q =QueueType(*qargs)

                    If the default is taken for both qargs and qkwargs, the setup
                    is:
                        q =QueueType()

                qargs - see QueueType

                qkwargs - see QueueType
            """
            self["locator"] = self.locator_name
            super().parse_args()
            self.__shuffle = shuffle
            if QueueType != None:
                if not issubclass(QueueType, GeneralizedQueue):
                    raise TypeError("QueueType must be derived from GeneralizedQueue")
            if start_cell != None:
                self["start cell"] = start_cell.index
            self.__start = start_cell
            self.__qType = QueueType
            self.__qargs = qargs
            self.__qkwargs = qkwargs

        def initialize(self):
            """initialization"""
            super().initialize()
            self["finder passes"] = 0
            self["unlinks"] = 0
            self.__more = True

# END mazes.Wallbuilders.basic_wallbuilder
