"""
mazes.Grids.oblong_rings - for iterating oblong grids using concentric rectangles
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    There are many ways of iterating through the cells of an oblong grid.  The
    first way is randomly -- shuffle the list of cells and iterate through the
    shuffled list.  For an m by n oblong grid, this yields
        (mn)! = (mn) (mn-1) (mn-2) ... (3) (2) (1) possible iterations,
    which, as the values of m and n grow, will soon exceed the possible
    shuffles produced by a pseudo-random number generator.  A 2x5 grid with 10
    cells has 10!=3,628,800 possible shuffles.  Moving to a grid with just twice
    as many cells (i.e. 20 cells: e.g. 4x5, 2x10), we have:
        20! = 2,432,902,008,176,640,000 shuffles
    or more than 2 quintillion (US; see note [a]).  Going up just 10 more cells
    (to 30 cells, e.g. 5x6, 3x10):
        30! = 265,252,859,812,191,058,636,308,480,000,000 shuffles
    (> 265 nonillion US; > 265 quintillion UK/FR).

    More practically, the usual approaches are row major or column major with
    rows and or columns taken in ascending or descending order.  These yield
    just 2x2x2=8 of the possible shuffles.  More shuffles can be obtained
    by varying the choice of direction (ascending/descending) in the inner
    tier.  For a 4x5 rectangle, we have:
        2 x 2^5 = 64 possibilities for row major shuffles
        2 x 2^4 = 32 possibilities for column major shuffles
    for a total of 96 shuflles.

    Now consider the following 4x5 matrix:

        4  5  6  7  8
        3 16 17 18  9
        2 15 20 19 10
        1 14 13 12 11

    Here the entries are arranged in two concentric rectangles.  Entries in the
    outer rectangle are numbered from 1 through 14 clockwise starting in the
    southwest corner.  The inner rectangle is numbered from 15 through 20
    clockwise from the southwest.  We could have let the numbers run
    counterclockwise, and the choice of the southwest corner was arbitrary.
    For the outer rectangle, we have:
        2 x 14 = 28 possible orderings
    For the inner rectangle, we have:
        2 x 6 = 12 possible ordering
    And we could order from inside outward for a total of:
        2 x (2 x (14+6)) = 80 possible shuffles.

    For example if we start in the inner rectangle (working outward) and
    number the inner rectangle counterclocwise from bottom center, and the
    outer rectangle clockwise from the southwest, as before, we have:

        10 11 12 13 14
         9  3  4  5 15
         8  2  1  6 16
         7 20 19 18 17

    This module implements concentric rectangular tiers.

NOTES

    [a] In the US, high order groups go up in threes:
            million, billion, trillion, quadrillion, quintillion, etc.
        In the UK and France, an older grouping of sixes is still (sometimes)
        in use:
            million/milliard; billion/billiard, trillion/trilliard, etc.
        Using the latter: 20! is between 2 and 3 trillion.
        Either way, that's a lot of shuffles. [see note b]

    [b] For a standard deck of 52 cards (4 suits, 13 ranks, no jokers) there are:
            52! = 80,658,175,170,943,878,571,660,636,856,403,766,
                     975,289,505,440,883,277,824,000,000,000,000
        distinct shuffles.  In about 5 centuries of playing cards, we aren't
        even close to achieving that many games.
        A standard year is 31,556,952 seconds. Let's round that up to 32,000,000.
        If each of 7 billion-US people played a game of solitaire every second
        for 500 years, we would have:
            7,000,000,000 x 500 x 32,000,000 = 1120 x 1,000,000,000,000,000
                = 1,120,000,000,000,000,000 games.
        Not even close!  Not even a drop in a bucket!

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

import mazes
from mazes.Grids.oblong import OblongGrid, SquareCell
from mazes.Grids.oblong import NORTH, SOUTH, EAST, WEST

class InnermostTierError(Warning):
    """This exception is raised in _pathmaker:
        if the smaller dimension is odd, then _pathmaker won't properly
        map the innermost tier
    """

class ConcentricOblongs(object):

    __slots__ = ("__grid", "__oblongs")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, grid:OblongGrid, *args, **kwargs):
        """constructor"""
        self.__grid = grid
        self.__oblongs = list()
        self._parse_args(*args, **kwargs)
        self._initialize()
        self._configure()

    def _parse_args(self):
        """argument parser for ConcentricOblong class (stub)"""
        pass

    def _initialize(self):
        """initialization"""
        m, n = self.__grid.m, self.__grid.n
        bbox = (0, 0, m-1, n-1)             # lower left, upper right
        done = False
        while not done:
            self.__oblongs.append(bbox)
            i0, j0, i1, j1 = bbox
            i0 += 1
            j0 += 1
            i1 -= 1
            j1 -= 1
            bbox = (i0, j0, i1, j1)         # next bounding box
            done = i0 > i1 or j0 > j1

    def _configure(self):
        """configuration (stub)"""

    @property
    def bounding_boxes(self) -> tuple:
        """returns the sequence of bounding boxes from outside inward"""
        return tuple(self.__oblongs)

    def __len__(self) -> int:
        """returns the number of rings"""
        return len(self.__oblongs)

    def tier_for(self, cell:(SquareCell, tuple)) -> int:
        """determine which concentric rectangle contains the cell or index"""
        i, j = cell.index if isinstance(cell, SquareCell) else cell
        m, n = self.__grid.m, self.__grid.n
        dw, de = j, n-j-1       # distances from the vertical walls
        ds, dn = i, m-i-1       # distances from the horizontal walls
        return min(dw, ds, de, dn)

    @staticmethod
    def is_inside(cell:SquareCell, bbox:tuple):
        """determine whether the cell is strictly inside the given bounding box"""
        i0, j0, i1, j1 = bbox
        i, j = cell.index
        return i0 < i < i1 and j0 < j < j1

    @staticmethod
    def is_outside(cell:SquareCell, bbox:tuple):
        """determine whether the cell is strictly outside the given bounding box"""
        i0, j0, i1, j1 = bbox
        i, j = cell.index
        return (i < i0 or i > i1 or j < j0 or j > j1) \
             and i0 <= i1 and j0 <= j1

    @staticmethod
    def is_on(cell:SquareCell, bbox:tuple):
        """determine whether the cell is on the boundary of the given bounding box"""
        i0, j0, i1, j1 = bbox
        i, j = cell.index
        return (i in {i0, i1} and j0 <= j <= j1 \
            or (j in {j0, j1} and  i0 <= i <= i1)) \
            and i0 <= i1 and j0 <= j1

    def site_for(self, cell:SquareCell) -> set:
        """determine which part of the tier the cell may be found

        The result is a list of runs or rises.  For example, the SW corner cell
        of a tier yields {south, west}.
        """
        result = set()
        tier = self.tier_for(cell)
        i, j = cell.index
        m, n = self.__grid.m, self.__grid.n
        if j == tier:
            result.add(WEST)
        if i == tier:
            result.add(SOUTH)
        if j == n - tier - 1:
            result.add(EAST)
        if i == m - tier - 1:
            result.add(NORTH)
        return result

    def _clockwise(self, index:tuple) -> tuple:
        """find the next clockwise index

        WARNING!
            This doesn't handle the innermost ring correctly when either
            the number of rows or the number of columns is odd.
        """
        i, j = index
        tier = self.tier_for(index)
        m, n = self.__grid.m, self.__grid.n
        if i == tier:                       # south wall
            if j > tier:
                return (i, j-1)
            return (i+1, j)                     # SW corner
        if j == tier:                       # west wall
            if i < m - tier - 1:
                return (i+1, j)
            return (i, j+1)                      # NW corner
        if i == m - tier - 1:               # north wall
            if j < n - tier - 1:
                return (i, j+1)
            return (i-1, j)                     # NE corner
                                            # east wall
        if i > tier:
            return (i-1, j)
        return (i, j-1)                         # SE corner

    def clockwise(self, cell):
        """returns the clockwise neighbor, if not hidden"""
        index0 = cell.index
        index1 = self._clockwise(index)
        if self.tier_for(index) != self.tier_for(index0):       # required!
            return None
        nbr = self.grid[index1]
        if nbr and not nbr.hidden:
            return nbr
        return None

    def _counterclockwise(self, index:tuple) -> tuple:
        """find the next counterclockwise index

        WARNING!
            This doesn't handle the innermost ring correctly when either
            the number of rows or the number of columns is odd.
        """
        i, j = index
        tier = self.tier_for(index)
        m, n = self.__grid.m, self.__grid.n
        if i == tier:                       # south wall
            if j < n - tier - 1:
                return (i, j+1)
            return (i+1, j)                     # SE corner
        if j == n - tier - 1:               # east wall
            if i < n - tier - 1:
                return (i+1, j)
            return (i, j-1)                      # NE corner
        if i == m - tier - 1:               # north wall
            if j > tier:
                return (i, j-1)
            return (i-1, j)                     # NW corner
                                            # west wall
        if i > tier:
            return (i-1, j)
        return (i, j+1)                         # SW corner

    def counterclockwise(self, cell):
        """returns the counterclockwise neighbor, if not hidden"""
        index0 = cell.index
        index1 = self._counterclockwise(index)
        if self.tier_for(index) != self.tier_for(index0):       # required!
            return None
        nbr = self.grid[index1]
        if nbr and not nbr.hidden:
            return nbr
        return None

    def _pathmaker(self, tier:int) -> list:
        """given a tier, return the clockwise path starting in the SW corner

        The path is a list of indices starting in the SW corner of the tier,
        proceeding clockwise, normally ending in the cell to the immediate
        right of the SW corner.

        If the tier number is negative or too large, a ValueError exception
        is raised.

        If the smaller dimension is odd, then this construction fails for the
        innermost tier.
        """
        if not isinstance(tier, int): raise TypeError
        if 0 > tier or tier >= len(self.__oblongs): raise ValueError
        if tier == len(self.__oblongs) - 1:         # innermost
            m, n = self.__grid.m, self.__grid.n
            if min(m, n) % 2 == 1:
                    # Houston! We have a problem
                    #   if the smaller dimension is odd, then the
                    #   innermost tier will be a chain
                raise InnermostTierError("pathmaker won't work here!")
        start = (tier, tier)
        path = [start]
        curr = self._clockwise(start)
        while curr != start and self.tier_for(curr) == tier:
            path.append(curr)
            curr = self._clockwise(curr)
        return path

    def pathmaker(self, tier:int) -> list:
        """constructs a path for the tier

        The path starts in the lower left corner.  If the last entry in the
        path is the constant None, then the path cannot be rotated.  (It can
        still be reversed.)
        """
        try:
            return self._pathmaker(tier)
        except InnermostTierError:
            pass

            # innermost tier when smaller dimension is odd!
        i, j = curr = (tier, tier)
        m, n = self.__grid.m, self.__grid.n
        path = []
        k, h = (0, 1) if m < n else (1, 0)
        while self.tier_for(curr) == tier:
            path.append(curr)
            i += k
            j += h
            curr = (i, j)
        path.append(None)
        return path

    @staticmethod
    def is_vertex(path:list, i:int):
        """determines whether a cell in a path is a vertex

        The path should be produced by pathmaker. Note that if the path
        is degenerate (single point or several points in a single line),
        then i should be in range(1, len(path)-1).  For a normal oblong
        path, the value of i should be in range(1, len(path)).  The
        inner tier is the only tier which produces degenerate paths.
        """
        if path[-1] == None:
            return None in {path[i-1], path[i+1]}       # endpoint
        n = len(path)
        i1, j1 = path[i-1]
        i2, j2 = path[(i+1) % n]            # careful! might need to rotate
        return i1!=i2 and j1!=j2

    @staticmethod
    def transform(path, reverse=False, rotate:int=0) -> list:
        """transforms a path

        Note that a degenerate path can be reversed, but not rotated.

        Rotation takes place before reversal.  The rotate argument
        is the index of the new starting point.  If the path is degenerate,
        then this argument is ignored.
        """
        if path[-1] == None:            # degenerate path
            rotate = 0
        if rotate:
            path = path[rotate:] + path[:rotate]
        if reverse:
            if path[-1] == None:
                path.pop()
                path = list(reversed(path))
                path.append(None)
            else:
                path = list(reversed(path))
        return path

    def classify(self, cell:SquareCell) -> dict:
        """classify the cell's neighbors

        In the dictionary that is returned, the values for each cell are
            -1: the neighbor is in the immediately outward tier
             0: the neighbor is in the same tier
            +1: the neighbor is in the immediately inward tier
        The value is a difference -- the tier of the cell minus the tier
        of the neighbor.  In a standard Von Neumann (N/S/E/W) neighborhood
        or in a Moore neighborhood (N/S/E/W + NE/NW/SE/SW), this difference
        will always be 0, 1 or -1.  If the cell's neighborhood is more
        complicated, for example, if the cell is a portal, then the difference
        might exceed 1 in absolute value.
        """
        result = dict()
        tier0 = self.tier_for(cell)
        for nbr in cell.neighbors:
            tier1 = self.tier_for(nbr)
            result[nbr] = tier1 - tier0
        return result

# end module mazes.Grids.oblong_rings
