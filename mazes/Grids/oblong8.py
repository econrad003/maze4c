"""
mazes.Grids.oblong8 - rectangular grids with 8-neighborhoods
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An oblong-8 grid (or Moore grid) is a rectangular lattice where
    each interior cell has its eight Moore neighbors.

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

EAST, NORTH, WEST, SOUTH = ("east", "north", "west", "south")
SE, NE, NW, SW = ("southeast", "northeast", "northwest", "southwest")

class OctagonalCell(SquareCell):
    """cells with Moore neighborhoods"""

    @property
    def southeast(self):
        """southeast getter"""
        return self[SE]

    @southeast.setter
    def southeast(self, cell:Cell):
        """southeast setter"""
        self[SE] = cell                         # 8 Sep 2025

    @property
    def northeast(self):
        """northeast getter"""
        return self[NE]

    @northeast.setter
    def northeast(self, cell:Cell):
        """northeast setter"""
        self[NE] = cell

    @property
    def northwest(self):
        """northwest getter"""
        return self[NW]

    @northwest.setter
    def northwest(self, cell:Cell):
        """northwest setter"""
        self[NW] = cell

    @property
    def southwest(self):
        """southwest getter"""
        return self[SW]

    @southwest.setter
    def southwest(self, cell:Cell):             # 8 Sep 2025
        """southwest setter"""
        self[SW] = cell

class MooreGrid(OblongGrid):

    CELL = OctagonalCell                        # basic cell type

    __slots__ = tuple()

        # CONSTRUCTION AND INITIALIZATION

    def _configure(self):
        """configure the neighborhood"""
                # configure the orthogonal neighbors
        super()._configure()
                # configure the diagonal neighbors
        self._configure_diagonals()

    def _configure_diagonals(self):
        """configure the diagonal neighbors"""
        for cell in self:
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
                if cell.northwest and cell.is_linked(cell.northwest):
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
                if cell.northeast and cell.is_linked(cell.northeast):
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
            if cell.southwest and cell.is_linked(cell.southwest):
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
            if cell.southeast and cell.is_linked(cell.southwest):
                post = "\\"
            else:
                post = "+"
        s += post
        return s

# end module mazes.Grids.oblong8
