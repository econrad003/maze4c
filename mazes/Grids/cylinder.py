"""
mazes.Grids.cylinder - cylindrical grid implementation
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A cylindrical grid is an oblong grid (Von Neumann neighborhood) in
    which the westmost cells have east-west grid connections with the
    eastmost cells.  One can visualize this by taping opposite ends of a
    strip of newspaper without twisting the strip.

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

class CylinderGrid(OblongGrid):

    __slots__ = ("__parity", )

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, *args, parity:bool=False, **kwargs):
        """argument parser for CylinderGrid class

        ARGUMENTS

            rows, cols - for the OblongGrid constructor

        KEYWORD ARGUMENTS

            parity - if True, the taped boundaries are N/S instead of
                E/W.

        The additional arguments are discarded, for now.
        """
        super()._parse_args(*args, **kwargs)
        self.__parity = bool(parity)

    def _configure(self):
        """configuration"""
        super()._configure()                    # configure parent
        if self.__parity:
            self.__configure_NS()
        else:
            self.__configure_EW()

    def __configure_EW(self):
        """even parity - E/W sides are taped"""
        last = self.n - 1                       # eastmost column
        for i in range(self.m):
            westmost = self[i, 0]
            eastmost = self[i, last]
            westmost.west = eastmost
            eastmost.east = westmost

    def __configure_NS(self):
        """odd parity - N/S sides are taped"""
        last = self.m - 1                       # northmost row
        for j in range(self.n):
            southmost = self[0, j]
            northmost = self[last, j]
            southmost.south = northmost
            northmost.north = southmost

    @property
    def parity(self):
        """parity getter"""
        return self.__parity

# end module mazes.Grids.cylinder
