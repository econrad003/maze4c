"""
mazes.Grids.projective - real projective plane grid implementation
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A real projective plane grid is an oblong grid (Von Neumann
    neighborhood) in which both of the opposite pairs of sides have
    been joined in the opposite direction (like a Moebius strip). This
    construction cannot be realized topologically in three-dimensional
    space.  (This is not the same construction as deriving a Klein
    bottle from a rectangle!)

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

    [2] "Real projective plane" in Wikipedia. 20 Aug. 2025. Web.
        Accessed 24 Aug. 2025.
            https://en.wikipedia.org/wiki/Real_projective_plane

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

class ProjectiveGrid(OblongGrid):

    __slots__ = ("__format",)

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, *args, fmt:str='N', **kwargs):
        """argument parser for CylinderGrid class

        ARGUMENTS

            rows, cols - for the OblongGrid constructor

        KEYWORD ARGUMENTS

            fmt (default: "N")
                the format to use in the string representation.  The
                permissible values are "N", "A", "U" or None.

        The additional arguments are discarded, for now.
        """
        super()._parse_args(*args, **kwargs)
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
            return unicode_str(self, w="N", e="NR", s="A", n="R")
        if self.__format == "A":
            return unicode_str(self, w="A", e="R", s="A", n="R")
        if self.__format == "U":
            return unicode_str(self)
        raise NotImplementedError("Unknown format type")

    def _configure(self):
        """configuration"""
        super()._configure()                    # configure parent
        self.__configure_NS_twist()
        self.__configure_EW_twist()

    def __configure_EW_twist(self):
        """E/W sides are oppositely directed"""
        last = self.n - 1                       # eastmost column
        for i in range(self.m):
            westmost = self[i, 0]
            twist = self.m - i - 1
            eastmost = self[twist, last]
            westmost.west = eastmost
            eastmost.east = westmost

    def __configure_NS_twist(self):
        """N/S sides are oppositely directed"""
        last = self.m - 1                       # northmost row
        for j in range(self.n):
            southmost = self[0, j]
            twist = self.n - j - 1
            northmost = self[last, twist]
            southmost.south = northmost
            northmost.north = southmost

# end module mazes.Grids.projective
