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
from mazes.Algorithms.dfs_circuit_locator import CircuitFinder

class BasicWallbuilder(Algorithm):
    """a simple wallbuilding algorithm to use with a circuit locator"""

    class Status(Algorithm.Status):
        """where all the work is done"""

        __slots__ = ("__more", "__shuffle")

        def find_edge(self) -> "Edge":
            """wrapper for the circuit locator

            returns either an edge or None
            """
            status = CircuitFinder.on(self.maze, shuffle=self.__shuffle)
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

        def parse_args(self, shuffle:bool=True):
            """parse the setup arguments"""
            super().parse_args()
            self.__shuffle = shuffle

        def initialize(self):
            """initialization"""
            super().initialize()
            self["finder passes"] = 0
            self["unlinks"] = 0
            self.__more = True

