"""
mazes.Algorithms.dihedral - symmetry group for rectangle or square
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A geometric symmetry of a shape is a continuous bijection
    which maps the shape to itself.  For example rotating the plane
    about the center of a circle through an arbitary angle is a
    symmetry of the circle:
        1) it is a continous mapping of the plane;
        2) it is one-to-one and onto the plane; and
        3) the image of the circle in the mapping is the circle
            itself.

    If we instead rotate the plane through 45 degrees about some
    point other than the center of the circle, we end up with
    a continuous bijection which fails point 3: the image of the
    circle is not the circle itself.  (It happens to be another
    circle, but that doesn't qualify.)

    This module applies symmetries of a rectangle (or a square)
    to a rectangular maze (or a square maze).
 
    A square has four rotational symmetries and four additional
    reflection symmetries.  These eight symmetries form the
    dihedral group for the square.

    A non-square rectangle has two rotational symmetries and two
    additional reflection symmetries.  These four symmetries form the
    group of symmetries for the rectangle.

REFERENCES

    Any introduction to group theory should talk about the dihedral
    groups.  The symmetries of a rectangle are often included in the
    discussion or in the related exercises.

    [1] "Dihedral group." in Wikipedia. 22 Sep. 2025. Web. 
        Accessed 25 Sep. 2025.
            https://en.wikipedia.org/wiki/Dihedral_group

    Here is a discussion of the symmetries of the rectangle:

    [2] "The Group of Symmetries of a Rectangle" in WikiDot. Web.
        Accessed 25 Sep. 2025.
            http://mathonline.wikidot.com/the-group-of-symmetries-of-a-rectangle

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

from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze

class DihedralGroup(object):
    """the dihedral group for the maze, as a set"""

    def __init__(self, maze:Maze, *args, debug:bool=False, **kwargs):
        """constructor

        POSITIONAL ARGUMENTS

            maze - the base maze

            *args - additional positional arguments
                (arguments other than rows and columns to be passed
                to the constructor)

        KEYWORD ARGUMENTS

            debug - if True, a message will be displayed before and
                after each member of the group is created

            **kwargs - additional keyword arguments for the
                constructor 
        """
        self.maze = maze
        self.grid = maze.grid
        self.args = args
        self.debug = debug
        self.kwargs = kwargs
        self.symmetries = [self.maze]
        self.validate()
        if debug:
            print("__init__:")
            print(maze)

    def validate(self):
        """checks to make sure the basic maze meets the requirements"""
        if not isinstance(self.maze.grid, OblongGrid):
            raise TypeError("base class must be OblongGrid")

    @staticmethod
    def rotate_1(index, m, n):
        """rotate left"""
        i, j = index
        return (j, m-i-1)

    @staticmethod
    def rotate_2(index, m, n):
        """rotate halfway"""
        i, j = index
        return (m-i-1, n-j-1)

    @staticmethod
    def rotate_3(index, m, n):
        """rotate right"""
        i, j = index
        return (n-j-1, i)

    @staticmethod
    def reflect_0(index, m, n):
        """reflect horizontally"""
        i, j = index
        return (i, n-j-1)

    @staticmethod
    def reflect_1(index, m, n):
        """rotate left, then reflect"""
        i, j = index
        return (j, i)

    @staticmethod
    def reflect_2(index, m, n):
        """rotate halfway, then reflect"""
        i, j = index
        return (m-i-1, j)

    @staticmethod
    def reflect_3(index, m, n):
        """rotate right, then reflect"""
        i, j = index
        return (n-j-1, m-i-1)

    SYMMETRIES = {}         # except the identity

    def create_maze(self, rotate:int, reflect:bool):
        """create a symmetrical copy of the maze

        ARGUMENTS

            rotate - an integer indicating the number of 90-degree
                rotations:
                    0 - no rotation
                    1 - 90 degree ccw rotation
                    2 - 180 degree rotation
                    3 - 90 degree cw rotation
                1 and 3 are only valid for square mazes

            reflect - reflect horizontally if True

        RETURN VALUE

            returns the new maze

        EXCEPTIONS

            Raises a ValueError exception under the following
            conditions:
                a) if rotate is 0 and reflect is False; or
                b) if rotate is odd and the base maze is not square.
        """
        rotate = rotate % 4
        reflect = bool(reflect)
        if self.debug:
            print(f"create_maze: {rotate=}, {reflect=}")

        if rotate == 0 and not reflect:
            raise ValueError("Identity symmetry is not permitted")
        rows, cols = self.grid.m, self.grid.n
        if rotate % 2 == 1 and rows != cols:
            raise ValueError("90 degree rotation requires square")

        GridClass = self.grid.__class__
        args, kwargs = self.args, self.kwargs
        maze = Maze(grid := GridClass(rows, cols, *args, **kwargs))
        edges = list(self.maze)
        transform = self.SYMMETRIES[rotate, reflect]
        for edge in edges:
            cell1, cell2 = edge
            index1, index2 = cell1.index, cell2.index
            index3 = transform(index1, rows, cols)
            index4 = transform(index2, rows, cols)
            cell3, cell4 = grid[index3], grid[index4]
            maze.link(cell3, cell4)

        if self.debug:
            print(maze)
        return maze
            
    def build_table(self):
        """build the table of symmetries"""
        rows, cols = self.grid.m, self.grid.n
        if rows == cols:
            rotations = [1, 2, 3]
            reflections = [0, 1, 2, 3]
        else:
            rotations = [2]
            reflections = [0, 2]
        for rotate in rotations:
            maze = self.create_maze(rotate, False)
            self.symmetries.append(maze) 
        for rotate in reflections:
            maze = self.create_maze(rotate, True) 
            self.symmetries.append(maze)
        if self.debug:
            print(len(self.symmetries), "mazes in orbit")

DihedralGroup.SYMMETRIES[1,False] = DihedralGroup.rotate_1
DihedralGroup.SYMMETRIES[2,False] = DihedralGroup.rotate_2
DihedralGroup.SYMMETRIES[3,False] = DihedralGroup.rotate_3
DihedralGroup.SYMMETRIES[0,True] = DihedralGroup.reflect_0
DihedralGroup.SYMMETRIES[1,True] = DihedralGroup.reflect_1
DihedralGroup.SYMMETRIES[2,True] = DihedralGroup.reflect_2
DihedralGroup.SYMMETRIES[3,True] = DihedralGroup.reflect_3

