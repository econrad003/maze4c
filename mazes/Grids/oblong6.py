"""
mazes.Grids.oblong6 - rectangular grids with 6-neighborhoods
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An oblong-6 grid (or hexagonal grid, or hex grid [for short]) is a
    rectangular lattice where each interior cell has its four Von
    Neumann neighbors and two diagonal neighbors on the same diagonal
    line.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

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

from mazes.grid import Cell, Grid
from mazes.Grids.oblong8 import OctagonalCell, MooreGrid

EAST, NORTH, WEST, SOUTH = ("east", "north", "west", "south")
SE, NE, NW, SW = ("southeast", "northeast", "northwest", "southwest")

class HexagonalCell(OctagonalCell):
    """cells with hexagonal neighborhoods"""
    pass

class HexagonalGrid(MooreGrid):

    CELL = HexagonalCell                        # basic cell type

    __slots__ = ("__slope", )

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, *args, slope:int=1, **kwargs):
        """parse the constructor arguments"""
        err = "The slope must be 1 or -1"
        if not isinstance(slope, int):
            raise TypeError(err)
        if slope not in {-1, 1}:
            raise ValueError(err)
        self.__slope = slope
        super()._parse_args(*args, **kwargs)

    def _configure_diagonals(self):
        """configure the diagonal neighbors"""
        for cell in self:
            if cell.north:
                if self.__slope == 1:
                    if cell.north.east:
                        cell.northeast = cell.north.east
                else:
                    if cell.north.west:
                        cell.northwest = cell.north.west
            if cell.south:
                if self.__slope == 1:
                    if cell.south.west:
                        cell.southwest = cell.south.west
                else:
                    if cell.south.east:
                        cell.southeast = cell.south.east

            # TOPOLOGY (NEIGHBORHOOD)

    def diagonals(self, reverse:bool=False, fold:int=0):
        """generator for the diagonals"""
        kwargs = dict()
        kwargs["principle"] = self.__slope == 1
        kwargs["reverse"] = reverse
        kwargs["fold"] = fold
        for diag in super().diagonals(**kwargs):
            yield diag

# end module mazes.Grids.oblong6
