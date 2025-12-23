"""
mazes.Metrics.oblong - sample metrics for a rectangular grid
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DEFINITIONS

    A metric on a set X is a real-valued function d:X²→R which
    satisfies the following constraints:
        a) d is positive definite, i.e., for each x and y in X,
             1) d(x, y) ≥ 0; and
             2) d(x, y) = 0 if and only if x = y;
        b) d is symmetric, i.e., for each x and y in X,
                d(x, y) = d(y, x); and
        c) d satisfies the triangle inequality, i.e., for each x, y, z
            in X,
                d(x, y) + d(y, z) ≥  d(x, z).

    A metric space is a pair (X, d) where X is a set and d is a metric
    on X.

STANDARD EXAMPLES

    Let X be the Cartesian plane with the usual right-handed (x,y) coordinate
    system.

    The Pythagorean metric (or distance) between two points is given by:
            d((x,y), (s,t)) = √((x-s)² + (y-t)²).

    The Manhattan metric (or taxicab distance) is given by: 
            d((x,y), (s,t)) = |(x-s)| + |(y-t)|

    The uniform metric (or maximum metric) is given by:
            d((x.y), (s,t)) = max(|(x-s)|, |(y-t)|)

USAGE

    Step 1) Select your metric, for example Metric for the Pythagorean
        distance.

                from mazes.Metrics.oblong import Metric
                maze = Maze(OblongGrid(34, 55))
                metric = Metric(maze)        # or metric = Metric(grid)

    Step 2) Choose your course of action:

        a) To calculate distances between cells:
                d = metric.d(Cell1, Cell2)

        b) To calculate distances from a fixed cell:
                d = metric.distances(FixedCell)
                d[Cell]         # distance from FixedCell to Cell

IMPLEMENTED METRICS

    Metric  - Pythagorean (or as the crow flies) distance
        this is the base class:
            redefine method "_d" to create a coordinate-based metric
    TaxicabMetric - Manhattan (or taxicab) distance
    UniformMetric - the uniform (or maximum or Chebyshev) metric
    KnightMetric - the knight's move metric

REFERENCES

        The following article was used in preparing the code for
        class KnightMetric:

    [1] Knight's Shortest Path on Chessboard, in StackOverflow.
        Note especially "Simon's answer".
        URL: https://stackoverflow.com/questions/2339101/ -
                knights-shortest-path-on-chessboard/41704071#41704071

        The following article inspired this module:

    [2] Herman Tulleken.  Algorithms for making more interesting mazes,
        in Game Developer Blog.
        URL: https://www.gamedeveloper.com/programming/ -
                algorithms-for-making-more-interesting-mazes

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
from math import sqrt

from mazes import Cell
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze

class Metric(object):
    """the Pythagorean metric"""

    __slots__ = ("__grid", )

    def __init__(self, grid:(OblongGrid, Maze)):
        """contructor"""
        if isinstance(grid, Maze):
            grid = grid.grid
        if not isinstance(grid, OblongGrid):
            raise TypeError("the grid must be rectangular")
        self.__grid = grid

    @property
    def grid(self) -> OblongGrid:
        """return the grid"""
        return self.__grid

    def is_corner(self, x, y) -> bool:
        m, n = self.__grid.m, self.__grid.n
        return x in (0, m-1) and y in (0, n-1)

    def _d(self, x1, y1, x2, y2) -> 'Real':
        """the Pythagorean distance"""
        return sqrt((x1-x2)**2 + (y1-y2)**2)

    def d(self, p:Cell, q:Cell) -> 'Real':
        """compute the metric

        In most cases, subclasses should override the method "_d".
        """
        if p == q:
            return 0
        y1, x1 = p.index
        y2, x2 = q.index
        return self._d(x1, y1, x2, y2)

    def distances(self, p:Cell) -> dict:
        """return a map of distances to each cell from a given cell"""
        d = dict()
        for q in self.__grid:
            d[q] = self.d(p, q)
        return d

class TaxicabMetric(Metric):
    """the Manhattan or taxicab metric"""

    def _d(self, x1, y1, x2, y2):
        """the taxicab distance"""
        return abs(x1-x2) + abs(y1-y2)

class UniformMetric(Metric):
    """the uniform or maximum metric

    This is the taxicab distance using the Moore neighborhood as diagonal
    moves are allowed.
    """

    def _d(self, x1, y1, x2, y2):
        """the uniform or maximum distance"""
        return max(abs(x1-x2), abs(y1-y2))

class KnightMetric(Metric):
    """a Chebyshev metric based on knight moves on a chessboard"""

    def _d(self, x1, y1, x2, y2):
        """the number of knight moves

        See reference [1].

        Note 1: The reference was apparently working on a fully infinite
            chessboard.  The (1,1) special case when the starting square
            is a corner wasn't mentioned, but is required for symmetry.
        """
        dx = abs(x1-x2)
        dy = abs(y1-y2)
        if dx < dy:
            dy, dx = dx, dy             # diagonal symmetry
        delta = dx - dy
                # corner cases
        if (dx, dy) == (1, 0):
            return 3
        if (dx, dy) == (2, 2):
            return 4
        if (dx, dy) == (1, 1) and self.is_corner(x1, y1):
            return 4                    # note 1 (symmetry)
                # general case
        if dy > delta:
            return delta - 2 * ((delta - dy) // 3)
        return delta - 2 * ((delta - dy) // 4)

# END mazes.Metrics.oblong
