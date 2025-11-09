"""
mazes.Algorithms.recursive_division - recursive division as a wall builder
Eric Conrad
Copyright ©2024-2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is our wall-building implementation of the recursive division
    algorithm.

    Here we implement the algorithm on a rectangular grid as a passage
    carver.  The following pseucode encapsulates the essentials:

        def divide(bbox, params):
            if bbox is larger than 1 cell:
                bbox1, params1, bbox2, params2 = subdivide(bbox, params)
                divide(bbox1, params1)
                divide(bbox2, params2)
                separate the two subdivisions with a wall with a door

IMPLEMENTATION

    The class RecursiveDivision is built on the Algorithm class in the usual
    way.  Run the implementation as:
        status = RecursiveDivision.on(maze)
    See method parse_args() in RecursiveDivision.Status for optional arguments.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 55-60, 249.

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

MODIFICATION HISTORY

    15 August 2025 - EC
        1) simpliflied the carve_room method in class Subgrid
"""
import mazes
from mazes.Grids.oblong import OblongGrid, EAST, NORTH
from mazes.maze import Maze
from mazes import rng
from mazes.algorithm_wb import AlgorithmWB

ROOM_LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    # UTILITY ROUTINES
    #       These are for 4-connected rectangular (oblong) mazes.
    #       These might be useful elsewhere.

class Subgrid(object):
    """bounding box for rectangular grids (wall builder)"""

    def __init__(self, maze:Maze,
                 lower_left:tuple=None,
                 upper_right:tuple=None):
        """initialization"""
        self.maze = maze
        self.grid = maze.grid
        if not isinstance(self.grid, OblongGrid):
            raise TypeError
        self.i1, self.j1 = lower_left if lower_left \
            else (0,0)                          # southwest corner
        self.i2, self.j2 = upper_right if upper_right \
            else self.grid.northeastmost        # northeast corner

    @property
    def bbox(self):
        """bounding box coordinates (row major)

        Returns ((SW row, SW column), (NE row, NE column)).
        """
        return ((self.i1, self.j1), (self.i2, self.j2))

    def __str__(self):
        """representation"""
        return "Subgrid" + str(self.bbox)

    @property
    def rows(self):
        """returns the number of rows in the subgrid"""
        return self.i2 + 1 - self.i1

    @property
    def cols(self):
        """returns the number of columns in the subgrid"""
        return self.j2 + 1 - self.j1

    @property
    def cells(self):
        """returns the number of cells in the subgrid"""
        return self.rows * self.cols

    def erect_wall_east(self):
        """erect an east separating wall (leaving one passage)"""
        door = rng.randrange(self.i1, self.i2+1)
        n = 0
        for i in range(self.i1, self.i2+1):
            if i != door:
                wall_panel = self.grid[i, self.j2]
                n += 1
                join = self.maze[frozenset([wall_panel, wall_panel.east])]
                self.maze.unlink(join)
        return n        # number of wall panels

    def erect_wall_north(self):
        """erect a north separating wall (leaving one passage)"""
        door = rng.randrange(self.j1, self.j2+1)
        n = 0
        for j in range(self.j1, self.j2+1):
            if j != door:
                wall_panel = self.grid[self.i2, j]
                n += 1
                join = self.maze[frozenset([wall_panel, wall_panel.north])]
                self.maze.unlink(join)
        return n        # number of wall panels

    def can_divide_horizontally(self, minwidth:int) -> bool:
        """is a horizontal division permissible?"""
        if minwidth < 2:
            minwidth = 2
        return self.cols >= minwidth

    def can_divide_vertically(self, minheight:int) -> bool:
        """is a vertical division permissible?"""
        if minheight < 2:
            minheight = 2
        return self.rows >= minheight

    def divide_horizontally(self, cutter:callable):
        """divide the subgrid horizontally

        DESCRIPTION

            Divides the subgrid into a left subgrid and a right subgrid and
            carves a door between them.

        RETURN VALUE

            ((subgrid1, subgrid2), unlinks) where:
                subgrid1 and subgrid2 are the subdivisions;
                unlinks is the number of wall panels erected

        EXCEPTIONS

            A RuntimeError exception is raised if subdividing is not
            possible.
        """
        if self.cols < 2:
            raise RuntimeError("Cannot subdivide horizontally")

        cut = int(cutter(self.j1, self.j2))
        assert self.j1 <= cut < self.j2
        cls = self.__class__
        subgrid1 = cls(self.maze, (self.i1, self.j1), (self.i2, cut))
        subgrid2 = cls(self.maze, (self.i1, cut+1), (self.i2, self.j2))
        n = subgrid1.erect_wall_east()
        return (subgrid1, subgrid2), n

    def divide_vertically(self, cutter:callable):
        """divide the subgrid vertically

        DESCRIPTION

            Divides the subgrid into a bottom subgrid and a top subgrid and
            carves a door between them.

        RETURN VALUE

            ((subgrid1, subgrid2), unlinks) where:
                subgrid1 and subgrid2 are the subdivisions;
                unlinks is the number of wall panels erected

        EXCEPTIONS

            A RuntimeError exception is raised if subdividing is not
            possible.
       """
        if self.rows < 2:
            raise RuntimeError("Cannot subdivide vertically")

        cut = int(cutter(self.i1, self.i2))
        assert self.i1 <= cut < self.i2
        cls = self.__class__
        subgrid1 = cls(self.maze, (self.i1, self.j1), (cut, self.j2))
        subgrid2 = cls(self.maze, (cut+1, self.j1), (self.i2, self.j2))
        n = subgrid1.erect_wall_north()
        return (subgrid1, subgrid2), n

    def divide(self, minheight:int, minwidth:int,
               cutterv:callable, cutterh:callable):
        """divide a subgrid, if possible

        RETURN VALUE

            ((subgrid1, subgrid2), links) where:
                subgrid1 and subgrid2 are the subdivisions;
                links is the number of doors carved (links=1)

            If no further subdivision is possible, then the return value
            is ((), 0).
        """
        if self.can_divide_horizontally(minwidth):
            if self.can_divide_vertically(minheight):
                if self.rows > self.cols:
                    return self.divide_vertically(cutterv)
                else:
                    return self.divide_horizontally(cutterh)
            else:
                return self.divide_horizontally(cutterh)
        else:
            if self.can_divide_vertically(minheight):
                return self.divide_vertically(cutterv)
            else:
                return (tuple(), 0)

class RecursiveDivision(AlgorithmWB):
    """the basic recursive division algorithm (wall builder)"""

    class Status(AlgorithmWB.Status):
        """this is where most of the work is done"""

        NAME = "Recursive Division (Wall Builder)"

        __slots__ = ("__Subgrid", "__stack", "__min_rows", "__min_cols",
                     "__cutterh", "__cutterv", "__debug", "__label_rooms",
                     "__room_id")

        @property
        def debug(self) -> bool:
            """for debugging"""
            return self.__debug

        @property
        def min_rows(self) -> int:
            """the smallest number of rows"""
            return self.__min_rows

        @property
        def min_cols(self) -> int:
            """the smallest number of columns"""
            return self.__min_cols

        @property
        def cutterv(self) -> callable:
            """return the vertical cutter"""
            return self.__cutterv

        @property
        def cutterh(self) -> callable:
            """return the horizontal cutter"""
            return self.__cutterh

        def label(self, subgrid):
            """label a room"""
            (i1, j1), (i2, j2) = subgrid.bbox
            grid = self.maze.grid
            theLabel = ROOM_LABELS[self.__room_id]
            self.__room_id = (self.__room_id + 1) % len(ROOM_LABELS)
            for i in range(i1, i2+1):
                for j in range(j1, j2+1):
                    cell = grid[i, j]
                    cell.label = theLabel

        def divide(self):
            """divide the current subdivision

            This is an iterative formulation using a stack.  Don't call this
            if the stack is empty
            """
            subgrid = self.pop()
            subgrids, unlinks = subgrid.divide(self.min_rows, self.min_cols,
                                             self.cutterv, self.cutterh)

            self.increment_item("wall panels", unlinks)
            self.increment_item("walls")

            for subgrid in subgrids:
                self.push(subgrid)
                if self.__label_rooms:
                    self.label(subgrid)

        def parse_args(self, min_rows:int=2, min_cols:int=2,
                       debug:bool=False, SubgridType:object=Subgrid,
                       vertical_cutter:callable=rng.randrange,
                       horizontal_cutter:callable=rng.randrange,
                       label_rooms:bool=False):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                min_rows (default=2)
                    the minimum height for a subdividable room
                min_cols (default=2)
                    the minimum width for a subdividable room
                debug (default=False)
                    set to True for detailed stack analysis
                SubgridType (default=Subgrid defined above)
                    can be modified to change the way the algorithm
                    recursively subdivides the grid.
                horizontal_cutter (default=randrange)
                    finds the horizontal cut column
                vertical_cutter (default=randrange)
                    finds the horizontal cut row
                label_rooms (default=False)
                    if true, the cells in a subgrid will be labelled.
                    The labels will only be displayed in console displays,
                    not in graphic objects.

            The cutter functions take two arguments, namely a starting
            row or column, and an ending row or column.  These will be
            taken from the southwest and northeast corners.  Like
            randrange, the function returns an integer which is
            not less than the start value and strictly less than the
            stop value.
            """
            super().parse_args()                # chain to parent
            self.__min_rows = max(min_rows, 2)
            self.__min_cols = max(min_cols, 2)
            self.__Subgrid = SubgridType
            self.__debug = debug
            self.__cutterv = vertical_cutter
            self.__cutterh = horizontal_cutter
            self.__label_rooms = label_rooms
            self.__room_id = 0
            self.__stack = []

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", len(self.maze.grid))
            self.store_item("walls", 0)
            self.store_item("wall panels", 0)
            self.store_item("max stack", 0)
            subgrid = self.__Subgrid(self.maze)
            self.__stack.append(subgrid)

        def push(self, subgrid):
            """push data onto the stack"""
            if self.__debug:
                print("PUSH:", subgrid)
            self.__stack.append(subgrid)
            if len(self.__stack) > self.fetch_item("max stack"):
                self.store_item("max stack", len(self.__stack))

        def pop(self):
            """push data onto the stack"""
            result = self.__stack.pop()
            if self.__debug:
                print("POP:", result)
            return result

        def top(self):
            """push data onto the stack"""
            return self.__stack[-1]

        @property
        def more(self):
            """returns True if there are stack entries

            Overrides Algorithm.more.
            """
            if len(self.__stack) > 0:
                return True
            self["passages"] = len(self.maze)
            return False

        def visit(self):
            """a single pass -- wrapper for _visit"""
            self.divide()

# end module mazes.Wallbuilders.recursive division
