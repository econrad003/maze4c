"""
mazes.Grids.oblong3 - base class implementation for triangular square grids
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An triangular square grid is a rectangular lattice where each cell has
    three neighbors.

    In our implementation, there are two kinds of cells:

        +---+---+---+---+---+---+
        | 0   1   0   1   0   1 |       Type      Layout
        +---+   +---+   +---+   +
        | 1   0   1   0   1   0 |                 + N +
        +   +---+   +---+   +---+         0       W   E
        | 0   1   0   1   0   1 |                 +---+
        +---+   +---+   +---+   +
        | 1   0   1   0   1   0 |                 +---+
        +   +---+   +---+   +---+         1       W   E
        | 0   1   0   1   0   1 |                 + S +
        +---+---+---+---+---+---+

    The type 0 cells have grid arcs to the north, east and west,
    while type 1 cells have grid arcs to the south, east and west.
    Thus each row is grid-connected, but, in order to insure that
    the grid is connected, we need one of the following conditions
    to be satisfied:
        1) there is exactly one row; or
        2) there are exactly two cells in a single column; or
        3) the number of rows is even and there are at least two
           columns.
    The first two possibilities can be treated as trivial cases.  We
    thus require condition 3.

    Note that every perfect maze on this grid is a binary maze.  For
    a rooted binary tree, select a cell of degree 1 or 2 as the root.
    (All cells of degree 3 and cells of degree 2 other than the root
    are internal nodes in the rooted tree.  Cells of degree 1 other
    than the root cell are leaves.)

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

from mazes.Grids.oblong import SquareCell, OblongGrid

class TrigonalCell(SquareCell):
    """square cells with three neighbors"""

    __slots__ = ("__cell_type", )

    def _parse_args(self, cell_type:int):
        """parse arguments

        The argument identifies the kind of cell.  It is used by the
        TriangularGrid class when configuring the grid.
        """
        super()._parse_args()
        self.__cell_type = cell_type

    @property
    def cell_type(self):
        """returns the cell type"""
        return self.__cell_type

class TriangularGrid(OblongGrid):

    CELL = TrigonalCell

        # CONSTRUCTION AND INITIALIZATION

    def _initialize(self):
        """initialization"""
        assert self.m > 1 and self.n > 1, "trivial triangular grid"
        assert self.m % 2 == 0, "the number of rows must be even"
        for i in range(self.m):
            for j in range(self.n):
                index = (i, j)                  # pack
                ctype = (i+j)%2
                self[index] = self.newcell(index, ctype)

    def _config_if(self, cell, way, h, k):
        """create a grid arc"""
        i, j = cell.index
        nbr = self[i+h, j+k]
        if nbr:
            cell[way] = nbr

    def _config0(self, cell):
        """configure a northward (ctype 0) cell"""
        self._config_if(cell, "north", 1, 0)
        self._config_if(cell, "west", 0, -1)
        self._config_if(cell, "east", 0, 1)

    def _config1(self, cell):
        """configure a southward (ctype 1) cell"""
        self._config_if(cell, "south", -1, 0)
        self._config_if(cell, "west", 0, -1)
        self._config_if(cell, "east", 0, 1)

    def _configure(self):
        """configuration"""
        for cell in self:
            i, j = cell.index
            if cell.cell_type == 0:
                self._config0(cell)
            else:
                self._config1(cell)

        self.set_format("leader", "")

# end module mazes.Grids.oblong3
