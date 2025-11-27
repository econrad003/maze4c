"""
mazes.Wallbuilders.pq_wallbuilder - erecting walls by breaking circuits
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

NOTE ON EFFICIENCY

    This algorithm will generally not be practical for trimming grids
    with large numbers of passages.  In short, it tends to require far more
    time than a practical algorithm.

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
from numbers import Real

from mazes import rng
from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
from mazes.Algorithms.pq_circuit_locator import CircuitFinder
from mazes.Queues.priority_queue import PriorityQueue

class PQWallbuilder(BasicWallbuilder):
    """basic wallbuilding using a BFS circuit locator"""

    class Status(BasicWallbuilder.Status):
        """almost all the work is done is done in the parent class"""

        slots = ("__start", "__shuffle", "__pr", "__prtype", "__qtype")

        @property
        def MyCircuitFinder(self):
            """returns the circuit finder class"""
            return CircuitFinder

        def find_edge(self) -> "Edge":
            """replacement for find_edge

            returns either an edge or None
            """
            status = self.MyCircuitFinder.on(self.maze, shuffle=self.__shuffle, \
                         start_cell=self.__start, pr=self.__pr, \
                         prtype=self.__prtype, qtype=self.__qtype, \
                         cached=False)
            self["finder passes"] += status["visits"]
            if status.result:
                _1, edge, _2 = status.result
                return edge
            return None

        def parse_args(self, shuffle:bool=True, start_cell:'Cell'=None,
                       pr:(callable, dict)=dict(), prtype="edge",
                       qtype:str="unstable"):
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

                pr - a priority function or dictionary

                prtype = "vertex", "edge" (default), or "arc"

                qtype = "stable", "unstable" (default) or "antistable"
            """
            self.__shuffle = shuffle
            self.__start = start_cell
            pr1 = lambda x: pr.get(x, None)                 # one operand
            pr2 = lambda x, y: pr.get((x,y), None)          # two operands
            if prtype == "vertex":
                self.__pr = self.set_vertex_pr(self.prfunction(pr, pr1))
            elif prtype == "edge":
                self.__pr = self.set_edge_pr(self.prfunction(pr, pr1))
            elif prtype == "arc":
                self.__pr = self.set_arc_pr(self.prfunction(pr, pr2))
            else:
                raise ValueError("'prtype' must be 'vertex', 'edge' or 'arc'")
            self.__prtype = prtype
            self.__qtype = qtype
            super().parse_args(shuffle, start_cell, QueueType=PriorityQueue)

        @staticmethod
        def prfunction(pr, lambda_pr):
            """decide which one is to be used"""
            if isinstance(pr, dict):
                return lambda_pr
            if callable(pr):
                return pr
            raise TypeError("the priority map must be a function or a dictionary")

        def set_vertex_pr(self, pr:callable) -> dict:
            """assigns a priority to all cells"""
            new_pr = dict()
            for cell in self.maze.grid:
                z = pr(cell)
                if not isinstance(z, Real):
                    z = rng.random()
                new_pr[cell] = z
            return new_pr

        def set_edge_pr(self, pr:callable) -> dict:
            """assigns a priority to all edges"""
            new_pr = dict()
            for join in self.maze:
                z = pr(join)
                if not isinstance(z, Real):
                    z = rng.random()
                new_pr[join] = z
            return new_pr

        def set_arc_pr(self, pr:callable) -> dict:
            """assigns a priority to all joins"""
            new_pr = dict()
            for join in self.maze:
                for cell in join.cells:
                    z = pr(cell, join)
                    if not isinstance(z, Real):
                        z = rng.random()
                    new_pr[cell, join] = z
            return new_pr

# END mazes.Wallbuilders.pq_wallbuilder
