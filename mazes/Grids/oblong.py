"""
mazes.Grids.oblong - base class implementation for oblong (aka: rectangular) grids
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An oblong grid is a rectangular lattice where each cell has its Von Neumann
    neighbors (north, south, east, and west).

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

MODIFICATIONS

    11 November 2025 - EC
        Tag the hidden cells in the str() interface with '█'.
"""

from mazes import Cell, Grid

EAST, NORTH, WEST, SOUTH = ("east", "north", "west", "south")

class SquareCell(Cell):
    """cells with Von Neumann neighborhoods"""

    @property
    def east(self):
        """east getter"""
        return self[EAST]

    @east.setter
    def east(self, cell:Cell):
        """east setter"""
        self[EAST] = cell

    @property
    def north(self):
        """north getter"""
        return self[NORTH]

    @north.setter
    def north(self, cell:Cell):
        """north setter"""
        self[NORTH] = cell

    @property
    def west(self):
        """west getter"""
        return self[WEST]

    @west.setter
    def west(self, cell:Cell):
        """west setter"""
        self[WEST] = cell

    @property
    def south(self):
        """south getter"""
        return self[SOUTH]

    @south.setter
    def south(self, cell:Cell):
        """south setter"""
        self[SOUTH] = cell

class OblongGrid(Grid):

    CELL = SquareCell                           # basic cell type

    __slots__ = ("__rows", "__cols")

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, rows:int, cols:int, *args, **kwargs):
        """argument parser for OblongGrid class

        The additional arguments are discarded, for now.
        """
        self.__rows = rows
        self.__cols = cols

    def _initialize(self):
        """initialization"""
        for i in range(self.__rows):
            for j in range(self.__cols):
                index = (i, j)                  # pack
                self[index] = self.newcell(index)

    def _configure(self):
        """configuration"""
        def set_if(cell, way, nbr):
            """set the neighbor if it exists"""
            if nbr: cell[way] = nbr

        for cell in self:
            i, j = cell.index
            set_if(cell, EAST, self[i, j+1])
            set_if(cell, NORTH, self[i+1, j])
            set_if(cell, WEST, self[i, j-1])
            set_if(cell, SOUTH, self[i-1, j])

        self.set_format("leader", "")

            # TOPOLOGY (NEIGHBORHOOD)

    @property
    def m(self):
        """the number of rows"""
        return self.__rows

    @property
    def n(self):
        """the number of columns"""
        return self.__cols

    def rows(self, reverse:bool=False, fold:int=0):
        """generator for the rows"""
        seq = list((fold + i) % self.__rows for i in range(self.__rows))
        for i in seq:
            if reverse:
                yield self.__rows - i - 1
            else:
                yield i

    def columns(self, reverse:bool=False, fold:int=0):
        """generator for the columns"""
        seq = list((fold + j) % self.__cols for j in range(self.__cols))
        for j in seq:
            if reverse:
                yield self.__cols - j - 1
            else:
                yield j

    def row(self, i:int, reverse:bool=False, fold:int=0):
        """generator for row i"""
        for j in self.columns(reverse=reverse, fold=fold):
            cell = self[i, j]
            if not cell.hidden:
                yield cell

    def _row(self, i:int, reverse:bool=False, fold:int=0):
        """generator for row i, including hidden cells"""
        for j in self.columns(reverse=reverse, fold=fold):
            yield self[i, j]

    def column(self, j:int, reverse:bool=False, fold:int=0):
        """generator for column j"""
        for i in self.rows(reverse=reverse, fold=fold):
            cell = self[i, j]
            if not cell.hidden:
                yield cell

    def _column(self, j:int, reverse:bool=False, fold:int=0):
        """generator for column j, including hidden cells"""
        for i in self.rows(reverse=reverse, fold=fold):
            yield self[i, j]

    def __str__(self):
        """string representation

        Masking is ignored.  (See also: OblongGrid.mask_to_str property)
        """
        leader = self.format("leader")
        s = leader
        for i in self.rows(reverse=True):
            s += "+"
            for cell in self._row(i):
                if cell.north and cell.is_linked(cell.north):
                    s += "   +"
                else:
                    s += "---+"
            s += "\n" + leader
            cell = self[i, 0]
            if cell.west and cell.is_linked(cell.west):
                s += " "
            else:
                s += "|"
            for cell in self._row(i):
                if cell.hidden:
                    if cell.char == ' ':
                        s += "███"
                    else:
                        s += '█' + cell.char + '█'
                else:
                    s += ' ' + cell.char + ' '
                if cell.east and cell.is_linked(cell.east):
                    s += " "
                else:
                    s += "|"
            s += "\n" + leader
        s += "+"
        for cell in self._row(0):
            if cell.south and cell.is_linked(cell.south):
                s += "   +"
            else:
                s += "---+"
        return s

    @property                       # added 11 Aug 2025
    def northeastmost(self):                        
        """coordinates of the northeast corner"""
        return self.m - 1, self.n - 1

# end module mazes.Grids.oblong
