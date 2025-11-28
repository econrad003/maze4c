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

HISTORY

    27 November 2025 - EC
        Consider a 5 by 5 maze.  In the BEFORE setup, the corners in the
        lower left ar diagonally adjacent in two ways:

                            N[1,0]
                            |
                            SW[0,0]--E[0,1]
                          /
               W[4,3]--NE[4,4]
                       |
                       S[3,4]
        The other two corners form a similar configuration.  In our 5 by 5
        maze, we have 21 cells with four distinct neghbors and 4 cells with
        just three distinct neighbors.  Geographic considerations suggest
        that is a problem.  In the AFTER configuration, we consider a pair
        of diagonally opposite cells to be the same cell.  So we have 23
        cells, each with exactly four neighbors.  To avoid problems with
        trivial we insist on at least three rows and at least three columns.
"""

from mazes.Grids.oblong import SquareCell, OblongGrid
from mazes.console_tools import unicode_str

class ProjectiveGrid(OblongGrid):

    __slots__ = ("__format", "__label_corners")

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, rows:int, cols:int, fmt:str='N',
                    label_corners:bool=False, **kwargs):
        """argument parser for CylinderGrid class

        ARGUMENTS

            rows, cols - for the OblongGrid constructor.  Both values
                must be at least three.

        KEYWORD ARGUMENTS

            fmt (default: "N")
                the format to use in the string representation.  The
                permissible values are "N", "A", "U" or None.

            label_corners (default: False)
                the four corners of the grid are especially confusing. If
                this is set, the four corners (just two cells) and their
                neighbors are labelled.  The cell occupying the bottom
                left and top right corners is labelled "O" (for "origin")
                and its four directed neighbors are labelled in capital
                letters with their respective compass directions.  The
                cell occupying the bottom right and top left corners is
                labelled "x" (to suggest a unit vector on the x-axis) and
                its four neighbors are labelled in minuscule with their
                respective compass directions.

        The additional arguments are discarded, for now.
        """
        if rows < 3 or cols < 3:
            raise ValueError("the grid must be 3×3 or larger")
        self.__label_corners = label_corners        # used by _configure()
        super()._parse_args(rows, cols, **kwargs)
        self.fmt = fmt

    def __getitem__(self, index):
        """get a cell"""
        cell = super().__getitem__(index)
        if cell == None:
            if index in {(self.m-1, 0), (self.m-1, self.n-1)}:
                new_index = (0, self.n - index[1] - 1)
                cell = super().__getitem__(new_index)
        return cell

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
            # merge the diagonally opposite corners
            #       SW, NE
        m, n = self.m, self.n
        SW, NE = self[0, 0], self[m-1, n-1]
        SW.south = NE.south
        NE.south.north = SW
        SW.west = NE.west
        NE.west.east = SW
            #       SE, NW
        SE, NW = self[0, n-1], self[m-1, 0]
        SE.south = NW.south
        NW.south.north = SE
        SE.east = NW.east
        NW.east.west = SE
            # remove the top corners
        del self[m-1, 0]
        del self[m-1, n-1]
            # debugging
        if self.__label_corners:
            self.label_corners()

    def label_corners(self):
        """label the corners for debugging"""
        SW, SE = self[0, 0], self[0, self.n-1]
        SW.label = "O"
        SW.north.label = "N"
        SW.south.label = "S"
        SW.east.label = "E"
        SW.west.label = "W"
        SE.label = "x"
        SE.north.label = "n"
        SE.south.label = "s"
        SE.east.label = "e"
        SE.west.label = "w"

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
