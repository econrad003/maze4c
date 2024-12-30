"""
mazes.Grids.polar - base class implementation for theta (aka: polar) grids
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An theta (aka: polar) grid is a lattice on a circular disk where each cell
    may have neighbors directed inward towards the pole (aka: center),
    outwards away from the pole, or in either direction, clockwise or
    counterclockwise, along annuli centered at the pole.

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
from math import pi, ceil, isnan, sin, cos

from mazes import Cell, Grid

CW, CCW, INWARD, OUTWARD = ("cw", "ccw", "inward", "outward")

def xy(r, theta) -> tuple:
    """convert from polar to Cartesian"""
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y

class ThetaCell(Cell):
    """a cell in a theta (aka: polar) maze"""

    __INSET = 0.15

    @classmethod
    def change_inset(cls, inset:float):
        """sets the inset (this is a global attribute for ThetaCell)"""
        inset = float(inset)
        if 0.01 < inset < 0.31:
            cls.__INSET = inset
        else:
            raise ValueError("The inset must be strictly between 0.01 and 0.31")

    @classmethod
    def inset(cls):
        """returns the inset"""
        return cls.__INSET

    __slots__ = ("__r", "__theta", "__outward_split", "__pole")

    def _parse_args(self, r:int, theta:tuple, *args,
                    split:int=1, pole:bool=False, **kwargs):
        """parse additional arguments

        ADDITIONAL REQUIRED ARGUMENTS

            r (integer)
                starting from the pole as 0, annuli are numbered from 1 to m-1

            theta (ordered pair)
                starting with the eastward x-axis vector as 0, the
                counterclockwise wall is numbered from 0 to n-1.  The ordered
                pair theta is the pair (t, n) where the cells annular walls
                range in revolutions from t/n to (t+1)/n., as measured
                counterclockwise from an eastward vector situated at the pole.

                For pole cells, the value of theta is ignored.

        ADDITIONAL OPTIONAL ARGUMENTS

            split (integer, default 1)
                the number of outward neighbors

            pole (boolean, default False)
                if true, this is a single cell in the center of the maze
        """
        super()._parse_args(*args, **kwargs)
        self.__r = r
        self.__theta = theta
        self.__outward_split = split
        self.__pole = pole

    @property
    def pole(self) -> bool:
        return self.__pole

        # DIRECTIONS
        #
        #   Inward, clockwise, and counterclockwise work just like south, east
        #   and west, respectively, or like north, west, and east, respectively.
        #
        #   Outward is trickier as a cell may have more than one outward
        #   neighbor.

    @property
    def clockwise(self):
        """clockwise cell getter"""
        return self[CW]

    @clockwise.setter
    def clockwise(self, cell:Cell):
        """clockwise cell setter"""
        self[CW] = cell

    @property
    def counterclockwise(self):
        """counterclockwise cell getter"""
        return self[CCW]

    @counterclockwise.setter
    def counterclockwise(self, cell:Cell):
        """counterclockwise cell setter"""
        self[CCW] = cell

    @property
    def inward(self):
        """inward cell getter"""
        return self[INWARD]

    @inward.setter
    def inward(self, cell:Cell):
        """inward cell setter"""
        self[INWARD] = cell

    def outward(self, index:int):
        """outward cell getter"""
        return self[OUTWARD, index]

    def set_outward(self, index:int, cell:Cell):
        """outward cell setter"""
                # The topology is normally stable, so we do some checking
                # here.
        if not isinstance(index, int):
            raise TypeError("The outward index must be a non-negative integer")
        if index < 0:
            raise ValueError("The outward index may not be negative")
        if index >= self.__outward_split:
            raise ValueError("The outward index is too large" \
                + f"(maximum={self.__outward_split})")
        if not isinstance(cell, Cell):
            raise TypeError("The outward cell must be a cell")
        self[OUTWARD, index] = cell

    @property
    def r(self) -> int:
        """inner radius"""
        return self.__r

    @property
    def theta0(self) -> float:
        """counterclockwise wall angle in radians"""
        i, n = self.__theta
        return 2*pi*i/n

    @property
    def theta1(self) -> float:
        """clockwise wall angle in radians"""
        i, n = self.__theta
        return 2*pi*(i+1)/n

    @property
    def theta0_rev(self) -> tuple:
        """theta0 in revolutions, unreduced"""
        return self.__theta

    @property
    def theta1_rev(self) -> tuple:
        """theta0 in revolutions, unreduced"""
        i, n = self.__theta
        return i+1, n

    @property
    def split(self) -> int:
        """potential number of outward neighbors"""
        return self.__outward_split

    @property
    def doors(self) -> list:
        """returns the door guard locations for the cell in polar coordinates

        The inset must be a value between 0 and 1/2.

        The list starts with the clockwise wall and proceeds counterclockwise.
        """
        inset = self.inset()
        r0 = self.r
        r1 = r0 + 1
        r0s = r0 + inset
        r1s = r1 - inset
        doors = []

        t0 = self.theta0
        t1 = self.theta1
        dt = (t1 - t0) * inset
        split = self.__outward_split
        if (r1 == self.grid.m) or (split <= 1):
                    # this cell does not split
            t0s = t0 + dt
            t1s = t1 + dt
            door = ((r1s,t1s), (r0s,t1s))
            doors.append(door)
            door = ((r0s,t1s), (r0s, t0s))
            doors.append(door)
            door = ((r0s, t0s), (r1s, t1s))
            doors.append(door)
            door = ((r1s, t1s), (r1s,t1s))
            doors.append(door)
            return doors

                # this is cell splits
        du = dt / split                                 # dt > du
        door = ((r1s,t1-du/2),(r0s,t1-du/2))            # clockwise wall
        doors.append(door)
        door = ((r0s,t1-dt),(r0s,t0+dt))                # inward door
        doors.append(door)
        door = ((r0s,t0+du/2),(r1s,t0+du/2))            # counterclockwise wall
        doors.append(door)
        ds = (t1 - t0) / split
        for i in range(split):
            t1 = t0 + ds
            door = ((r1s,t0+du), (r1s, t1-du))
            doors.append(door)
            t0 = t1
        return doors

    def corners(self):
        """return a polar bounding box for the cell"""

class ThetaGrid(Grid):

    CELL = ThetaCell                           # basic cell type

        # EXPLANATION OF THE PARAMETERS
        #
        #   r - the radius of the grid
        #       The radius is the distance from the center point to the outward
        #       boundary of the grid
        #
        #   pole - the number of cells at the pole
        #       If this number is 1, then there is a single pole cell.  If it is
        #       greater than 1, the pole will consist of pie-shape wedges that
        #       cover the same angular distance.
        #
        #   split - the decision on when there is an outward split.  If this
        #       value is positive, outward splits occur when the outer arc
        #       length (i.e nΘ when where n is the distance from center to the
        #       outward arc and the Θ angular distance in radians) exceeds this
        #       threshold.  A value of zero prevents splitting.
        #
        #   rings - for each ring, this dictionary returns an ordered pair
        #       which tells how many cells are in the ring and how many
        #       outward neighbors each cell has.

    __slots__ = ("__r", "__pole", "__split", "__rings")

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, r:int, *args, pole:int=6, split=1, **kwargs):
        """argument parser for OblongGrid class"""
        self.__r = r
        self.__pole = pole
        self.__split = split
        self.__rings = {}

    def get_split(self, a:float):
        """determine the outward split value

        The input is the arc length.
        """
        if self.__split <= 0:
            return 1                    # no splitting
        return int(ceil(a / self.__split))

    def make_pole_cell(self, split):
        """make a single pole cell"""
        index = (0,0)
        cell = self.CELL(self, index, r=0, theta=(0,1), split=split, pole=True)
        self[index] = cell

    def make_other_cells(self, r, n, split):
        """make a range of pole cells"""
        for i in range(n):
            index = (r, i)
            theta = (i, n)          # i/n revolutions to ccw wall
            cell = self.CELL(self, index, r=r, theta=theta, split=split)
            self[index] = cell

    def _initialize(self):
        """initialization"""
                # validate a few things
        r, pole = self.__r, self.__pole
        rings = self.__rings
        if not isinstance(pole, int):
            raise TypeError("The number of pole cells must be an integer")
        if pole < 1:
            raise ValueError("The number of pole cells must be positive")
        if self.__split < 0:
            raise ValueError("The split value must be non-negative")
        if isnan(self.__split):
            raise ValueError("The split value must be finite")

                # create the polar disk
        a = 2*pi/pole                   # arc length (using radius=1)
        split = self.get_split(a)
        rings[0] = (pole, split)

        if pole == 1:
            self.make_pole_cell(split)
        else:
            self.make_other_cells(0, pole, split)
        assert pole == len(self)            # self-test

        for i in range(1, r):
            n, split = rings[i-1]
            n *= split                      # number of cells in this ring
            a = 2*pi*(i+1)/n                # arc length of cell
            split = self.get_split(a)
            rings[i] = (n, split)           # number of cells, outward split
            self.make_other_cells(i, n, split)

    def _configure(self):
        """configuration (stub)"""
        for cell in self:
            r = cell.r
            i, n = cell.theta0_rev
            split = cell.split
            assert cell.index == (r, i)     # self-check
            if n > 1:
                ccw = self[r, (i+1)%n]
                cell.counterclockwise = ccw
                ccw.clockwise = cell
            if r +1 == self.__r:                   # innermost ring
                continue
            p = i*split
            for j in range(split):
                outward = self[r+1, p+j]
                cell.set_outward(j, outward)
                outward.inward = cell

            # TOPOLOGY (NEIGHBORHOOD)

    @property
    def m(self):
        """the number of rings"""
        return self.__r

    def n(self, m:int):
        """the number of columns in a given ring"""
        n, _ = self.__rings[m]
        return n

    def splits(self, m:int):
        """the number of splits from a given ring into the next"""
        _, split = self.__rings[m]
        return split

    def rings(self, reverse:bool=False):
        """generator for the rings"""
        seq = range(self.__r-1,-1,-1) if reverse else range(self.__r)
        for i in seq:
            yield i

    def ring(self, i:int, reverse:bool=False, fold:int=0):
        """generator for ring i"""
        n = self.n(i)               # of cells
        seq = range(n-1,-1,-1) if reverse else range(n)
        for j in seq:
            k = (j + fold) % n
            cell = self[i, k]
            if not cell.hidden:
                yield cell

    def _ring(self, i:int, reverse:bool=False, fold:int=0):
        """generator for ring i, including hidden cells"""
        n = self.n(i)               # of cells
        seq = range(n-1,-1,-1) if reverse else range(n)
        for j in seq:
            k = (j + fold) % n
            yield self[i, k]

    def __str__(self):
        """string representation"""
        return "ϴ grid"

# end module mazes.Grids.polar