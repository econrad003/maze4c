"""
mazes.Grids.upsilon - upsilon grids
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An upsilon grid is a rectangular lattice where cells alternate both
    horizontally and vertically between square and octagonal cells.

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
from mazes.Grids.oblong import SquareCell, OblongGrid
from mazes.Grids.oblong8 import OctagonalCell

EAST, NORTH, WEST, SOUTH = ("east", "north", "west", "south")
SE, NE, NW, SW = ("southeast", "northeast", "northwest", "southwest")

class UpsilonGrid(OblongGrid):

    CELL = (SquareCell, OctagonalCell)

    __slots__ = ("__parity", )

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, rows:int, cols:int, parity=False):
        """argument parser

        POSITIONAL ARGUMENTS

            rows, cols - the number of rows and columns

        KEYWORD ARGUMENTS

            parity - if parity is False (default, even), then even cells
                are octagonal and odd cells are square; if parity is
                True (odd), then odd cells are octagonal and even cells
                are square.  The parity of a cell is the parity of the
                sum of its indices, for example (2,2) and (3,3) are both
                even and (2,3) and (3,2) are both odd.
        """
        self.__parity = parity
        super()._parse_args(rows, cols)

    @property
    def grid_parity(self) -> bool:
        """return the grid's parity"""
        return self.__parity

    @staticmethod
    def parity(i:int, j:int) -> bool:
        """determine the parity of ab index"""
        return bool((i+j) % 2)

    def newcell(self, *args, parity:bool=False, **kwargs):
        """called by initialize to create cells"""
        if parity == self.grid_parity:
            return OctagonalCell(self, *args, **kwargs)
        else:
            return SquareCell(self, *args, **kwargs)

    def _initialize(self):
        """initialization

        The cells alternate according to parity.
        """
        for i in range(self.m):
            for j in range(self.n):
                index = (i, j)                  # pack
                parity = self.parity(i, j)
                self[index] = self.newcell(index, parity=parity)

    def _configure(self):
        """configure the neighborhood"""
                # configure the orthogonal neighbors
        super()._configure()
                # configure the diagonal neighbors
        self._configure_diagonals()

    def _configure_diagonals(self):
        """configure the diagonal neighbors"""
        for cell in self:
            if not isinstance(cell, OctagonalCell):
                continue
            if cell.north:
                if cell.north.west:
                    cell.northwest = cell.north.west
                if cell.north.east:
                    cell.northeast = cell.north.east
            if cell.south:
                if cell.south.west:
                    cell.southwest = cell.south.west
                if cell.south.east:
                    cell.southeast = cell.south.east

            # TOPOLOGY (NEIGHBORHOOD)

    def diagonals(self, principal:bool, reverse:bool=False, fold:int=0):
        """generator for the diagonals

        ARGUMENTS

            principal - if True, the diagonals run southwest to
                northeast; if False, they run southeast to
                northwest.
        """
        seq = []
        if principal:
            i, j = 0, self.n-1
            while j > 0:
                seq.append([(i, j), NE])
                j -= 1
            while i < self.m:
                seq.append([(i, j), NE])
                i += 1
        else:
            i, j = 0, 0
            while j < self.n-1:
                seq.append([(i, j), NW])
                j += 1
            while i < self.m:
                seq.append([(i, j), NW])
                i += 1
        assert len(seq) == self.m + self.n - 1
        fold = fold % len(seq)
        if fold:
            seq = seq[fold:] + seq[:fold]
        if reverse:
            seq.reverse()
        for diag in seq:
            yield diag

    def _diagonal(self, diag:list, reverse:bool=False, fold:int=0) -> list:
        """returns the cells in a given diagonal"""
        index, direction = diag
        assert direction in {NE, NW}
        cell = self[index]
        i, j = index
        k = 1 if direction == NE else -1
        seq = []
        for j in self.columns(reverse=reverse, fold=fold):
            cell = self[i, j]
            if not cell.hidden:
                seq.append(cell)
        fold = fold % len(seq)
        if fold:
            seq = seq[fold:] + seq[:fold]
        if reverse:
            seq.reverse()
        return seq

    def diagonal(self, diag:list, reverse:bool=False, fold:int=0) -> list:
        """generator for the unmasked cells in a given diagonal"""
        seq = self._diagonal(diag, reverse, fold)
        for cell in seq:
            if not cell.hidden:
                yield cell

    def __str__(self):
        """string representation"""
        leader = self.format("leader")
        s = leader
        post = "+"
        for i in self.rows(reverse=True):
            for cell in self._row(i):
                if cell[NW] and cell.is_linked(cell[NW]):
                    if post == "/":
                        s += "X"                # crossing passages
                    else:
                        s += "\\"
                else:
                    s += post
                if cell.north and cell.is_linked(cell.north):
                    s += "   "
                else:
                    s += "---"
                if cell[NE] and cell.is_linked(cell[NE]):
                    post = "/"
                else:
                    post = "+"
            s += post + "\n" + leader
            cell = self[i, 0]
            if cell.west and cell.is_linked(cell.west):
                s += " "
            else:
                s += "|"
            for cell in self._row(i):
                s += ' ' + cell.char + ' '
                if cell.east and cell.is_linked(cell.east):
                    s += " "
                else:
                    s += "|"
            s += "\n" + leader
                # south fence
        post = "+"
        for cell in self._row(0):
            if cell[SE] and cell.is_linked(cell[SE]):
                if post == "\\":
                    s += "X"                # crossing passages
                else:
                    s += "/"
            else:
                s += post
            if cell.south and cell.is_linked(cell.south):
                s += "   "
            else:
                s += "---"
            if cell[SW] and cell.is_linked(cell[SW]):
                post = "\\"
            else:
                post = "+"
        s += post
        return s

# end module mazes.Grids.upsilon
