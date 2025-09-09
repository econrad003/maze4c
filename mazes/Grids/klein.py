"""
mazes.Grids.klein - Klein bottle grid implementation
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A Klein bottle grid is an oblong grid (Von Neumann neighborhood) in
    which one of the opposite pairs of sides has been joined in the same
    direction (like a cylinder) and the other pair in the opposite
    direction (like a Moebius strip).  This construction cannot be
    realized topologically in three-dimensional space.

    (There are sculptures sold commercially as "Klein bottles", but
    these are only 3D models, not true Klein bottles.)

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] "Klein bottle" in Wikipedia. 22 Jun. 2025. Web.
        Accessed 24 Aug. 2025.
            https://en.wikipedia.org/wiki/Klein_bottle

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
from mazes.console_tools import unicode_str

class KleinGrid(OblongGrid):

    __slots__ = ("__parity", "__format")

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, *args, parity:bool=False,
                    fmt:str='N', **kwargs):
        """argument parser for CylinderGrid class

        ARGUMENTS

            rows, cols - for the OblongGrid constructor

        KEYWORD ARGUMENTS

            parity - if True, the oppositely directed boundaries are N/S
                instead of E/W.

            fmt (default: "N")
                the format to use in the string representation.  The
                permissible values are "N", "A", "U" or None.

        The additional arguments are discarded, for now.
        """
        super()._parse_args(*args, **kwargs)
        self.__parity = bool(parity)
        self.fmt = fmt

    @property
    def fmt(self) -> (str, None):
        """format getter"""
        return self.__format

    @fmt.setter
    def fmt(self, value:(str, None)):
        """format setter

        Changes the console display format.  Permitted values are "A",
        "N", "U", or None.

            A - Use alphabetic labels only (Unicode block chars)
            N - Use numeric labels for the rows (Unicode block chars)
            U - Use Unicode block characters without labels
            None - ASCII only, no labels
        """
        if value in {"A", "N", "U", None}:
            self.__format = value
        else:
            raise NotImplementedError("Unknown format type")

    def __str__(self):
        """string representation"""
        if self.__format == None:
            return super().__str__()
        if self.__format == "N":
            if self.__parity:
                return unicode_str(self, h="N", s="A", n="R")
            else:
                return unicode_str(self, w="N", e="NR", v="A")
        if self.__format == "A":
            if self.__parity:
                return unicode_str(self, h="A", s="A", n="R")
            else:
                return unicode_str(self, w="A", e="AR", v="A")
        if self.__format == "U":
            return unicode_str(self)
        raise NotImplementedError("Unknown format type")

    def _configure(self):
        """configuration"""
        super()._configure()                    # configure parent
        if self.__parity:
            self.__configure_NS_twist()
            self.__configure_EW()
        else:
            self.__configure_NS()
            self.__configure_EW_twist()

    def __configure_EW(self):
        """E/W sides are similary directed"""
        last = self.n - 1                       # eastmost column
        for i in range(self.m):
            westmost = self[i, 0]
            eastmost = self[i, last]
            westmost.west = eastmost
            eastmost.east = westmost

    def __configure_EW_twist(self):
        """E/W sides are oppositely directed"""
        last = self.n - 1                       # eastmost column
        for i in range(self.m):
            westmost = self[i, 0]
            twist = self.m - i - 1
            eastmost = self[twist, last]
            westmost.west = eastmost
            eastmost.east = westmost

    def __configure_NS(self):
        """N/S sides are similary directed"""
        last = self.m - 1                       # northmost row
        for j in range(self.n):
            southmost = self[0, j]
            northmost = self[last, j]
            southmost.south = northmost
            northmost.north = southmost

    def __configure_NS_twist(self):
        """N/S sides are oppositely directed"""
        last = self.m - 1                       # northmost row
        for j in range(self.n):
            southmost = self[0, j]
            twist = self.n - j - 1
            northmost = self[last, twist]
            southmost.south = northmost
            northmost.north = southmost

# end module mazes.Grids.torus
