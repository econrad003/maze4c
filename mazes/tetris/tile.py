"""
mazes.tetris.tile - base class implementation for tiles of cells
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A tile is a group of (preferably neighboring) cells in a maze.

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

from mazes import Cell
from mazes.maze import Maze

class Tile(object):
    """a tile, such as one used in Tetris

    PROTECTED DATA

        dropped (boolean) -- a flag indicates whether the tile has
            found its place in the maze.  A dropped tile is locked in
            place.

        n (positive integer) -- the number of cells in the tile.  Cells
            are numbered from 0 through n-1.

        shape (set of 3-tuples) -- the shape description of the tile.
            It is a set consisting of exactly n-1 3-tuples.  Each
            3-tuples has the following form:
                    (C1, D12, C2)
            where C1 and C2 are the numbers of two cells in the tile and
            D12 is the grid direction in the tile from cell C1 to C2.
            In each 3-tuple C1<C2, so C2 cannot be 0 and C1 cannot be
            be n-1.  In addition, each C2 is unique, guaranteeing that
            the tile is a small perfect maze.  (It is internally
            represented as a tuple instead of a set.)

        cells (set of cells) - the cells in the maze that were covered
            by the tile.  This is only defined for dropped tiles.

        bbox - bounding box coordinates for the tile (optional)

        zero - location of the zero in the bounding box (optional)

    SHAPE EXAMPLE

       Consider the following Tetris tile:
                                    +---+
                                    | 3 |
                                +---+---+---+
                                | 0 | 1 | 2 |
                                +---+---+---+

        For a 4-connected grid, the tile's shape description is essentially
        unique:
            {(0, "east", 1), (1, "east", 2), (1, "north", 3)}

        For an 8-connected grid, the tile's shape description may vary:
            {(0, "east", 1), (1, "east", 2), (1, "north", 3)}
            {(0, "east", 1), (0, "northeast", 3), (1, "east", 2)}
            {(0, "east", 1), (1, "east", 2), (2, "northwest", 3)}
    """

    __slots__ = ("__dropped", "__n", "__shape", "__carved",
                 "__cells", "__bbox", "__zero")

    def __init__(self, *args, **kwargs):
        """constructor

        Subclasses should override methods parse_args, initialize,
        and configure.
        """
        self.parse_args(*args, **kwargs)
        self.initialize()
        self.configure()

    def parse_args(self, n:int, shape:set, bbox=None, zero=None, verify=True):
        """parse the tile description (base)

        The dropped flag is set to False.  The shape information for
        the cell is parsed and stored.

        If bbox and/or zero are supplied (i.e. not equal to None),
        they are stored.  They are not validated.  (They are intended
        for application use as needed.)

        If verify is False, checks to insure that the shape descriptor
        represents a perfect maze (connected and circuit-free) are not
        done.  Some applications may fail if the shape is not connected.
        """
        self.__n = n
        self.__dropped = False
        self.__carved = False
        self.__shape = tuple(sorted(shape))
        if bbox != None:
            self.__bbox = bbox
        if zero != None:
            self.__zero = zero
        if verify:
            self.__verify_shape()

    def __verify_shape(self):
        """verify that the shape vector is well-formed.

        DESCRIPTION

            Checks that the tile represents a perfect maze

        BUGS

            The direction label is not checked.  (This is handled
            in the drop routine.

        EXCEPTIONS

            Raises a ValueError if the shape vector is not well-formed.
            The error message provides a clue to the problem
        """
        m = self.__n - 1
        if len(self.__shape) != m:
            raise ValueError(f"Imperfect tile shape; expected {m} entries")
        destinations = set()
        for i in range(m):
            arc = self.__shape[i]
            c1, di2, c2 = arc
            if not (isinstance(c1, int) and isinstance(c2, int)):
                raise TypeError("Shape arc {arc}: require int for C1 and C2")
                    # Note: the inequality c1<c2 catches c1==m or c2==0
            if c1 < 0 or c1 > m:
                raise ValueError("Shape arc {arc}: require C1 in [0,{m-1}]")
            if c2 < 0 or c2 > m:
                raise ValueError("Shape arc {arc}: require C2 in [1,{m}]")
            if c1 >= c2:
                raise ValueError(f"Shape arc {arc} in shape: expect C1 < C2")
            if c2 in destinations:
                raise ValueError(f"Shape arc {arc}: duplicate destination {c2}")
            destinations.add(c2)

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    @property
    def dropped(self) -> bool:
        """returns True if the tile has been placed, and False otherwise"""
        return self.__dropped

    @property
    def n(self) -> int:
        """returns the number of cells in the tile"""
        return self.__n

    @property
    def shape(self) -> set:
        """returns the shape vector as a set"""
        return set(self.__shape)

    @property
    def cells(self) -> tuple:
        """returns the cells covered by the tile

        EXCEPTIONS

            raises a RuntimeError exception if the tile has not
            been dropped.
        """
        if self.__dropped:
            return self.__cells
        raise RuntimeError("The tile has not dropped.")

    @property
    def bbox(self):
        """bounding box, if defined"""
        return self.__bbox

    @property
    def zero(self):
        """zero location, if defined"""
        return self.__zero

    def drop(self, places:list, occupied:set) -> bool:
        """attempt to drop a tile into a grid

        ARGUMENTS

            places -- the cells to try as cell number 0; the
                first successful placement wins.  The list is
                processed as a stack, last in, first out.
                (This is a destructive operation!)  The cells
                in this list may not be occupied.

            occupied -- cells that are already occupied - if the
                placement is successful, this will be updated

        RETURN VALUE

            True if the placement is successful, False otherwise.
        """
        while len(places) > 0:
            place = places.pop()
            if place in occupied:
                raise RuntimeError("drop: cannot place cell 0 in occupied cell")
            # print(place.index)
            cells = {0: place}
            for arc in self.__shape:
                c1, d12, c2 = arc
                cell1 = cells[c1]
                cell2 = cell1[d12]
                if cell2 and (cell2 not in occupied):
                    cells[c2] = cell2
                    continue
                break
            if len(cells) == self.__n:      # successful placement
                self.__dropped = True
                self.__cells = tuple(cells[i] for i in range(self.__n))
                occupied.update(self.__cells)
                return True
        return False                        # unsuccessful, all places tried

    def carve(self, maze:Maze) -> int:
        """carve the tile in the maze - once only!

        Returns the number of carved links.
        """
        if not self.__dropped:
            raise ValueError("carve: the tile hasn't dropped")
        if self.__carved:
            raise RuntimeError("carve: the tile has already been carved")
        n = 0
        cells = self.__cells
        for i in range(self.__n-1):
            arc = self.__shape[i]
            c1, d12, c2 = arc
            cell1 = cells[c1]
            cell2 = cells[c2]
            # print("link", cell1.index, "--", cell2.index)
            maze.link(cell1, cell2)
            n += 1
        return n

# end module tetris.tile
