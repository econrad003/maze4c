"""
mazes.Algorithms.rotation_subgroup - rotation group for rectangle or square
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The rotation group for a square consists of four rotations,
    including the identity, two ninety-degree rotations, and
    one reflection.  For a general rectangle, the two ninety-degree
    rotations are excluded as they don't map the rectangle onto
    itself.

REFERENCES

    Any introduction to group theory should talk about the dihedral
    groups.  The symmetries of a rectangle are often included in the
    discussion or in the related exercises.  The rotation subgroup
    of a dihedral group omit the reflections -- as the name indicates,
    only rotations are admitted.

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

from mazes.Algorithms.dihedral import DihedralGroup

class RotationGroup(DihedralGroup):
    """the rotation group for the maze, as a set"""

    def build_table(self):
        """build the table of symmetries"""
        rows, cols = self.grid.m, self.grid.n
        if rows == cols:
            rotations = [1, 2, 3]
        else:
            rotations = [2]
        for rotate in rotations:
            maze = self.create_maze(rotate, False)
            self.symmetries.append(maze) 

