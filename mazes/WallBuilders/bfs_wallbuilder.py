"""
mazes.Wallbuilders.bfs_wallbuilder - erecting walls by breaking circuits
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
from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
from mazes.Algorithms.bfs_circuit_locator import CircuitFinder

class BFSWallbuilder(BasicWallbuilder):
    """basic wallbuilding using a BFS circuit locator"""

    class Status(BasicWallbuilder.Status):
        """all the work is done is done in the parent class"""

        @property
        def MyCircuitFinder(self):
            """returns the circuit finder class"""
            return CircuitFinder

        def parse_args(self, shuffle:bool=True, start_cell:'Cell'=None):
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
            """
            super().parse_args(shuffle, start_cell)

# END mazes.Wallbuilders.bfs_wallbuilder
