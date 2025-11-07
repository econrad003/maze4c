"""
mazes.Algorithms.simple_binary_tree - the simple binary tree maze carving
    algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In the simple binary tree algorithm, cells (in principle) are processed
    in parallel. In each cell where there is a choice, a coin is tossed.  If
    the coin is a head, the rule is to carve a passage northward.  If the
    toss is a tail, the result is carving eastward.

    The result on an oblong grid is a rooted binary tree with the northeast
    corner as an obvious root.  There is a continuous east-west corridor along
    the north boundary wall and a continuous north-south corridor along the
    east boundary wall.  To find a path between two cells, simply go north or
    east from each cell to eventuall arrive in the northeast corner -- follow
    one of these paths until the two paths meet, and then trace the second path
    back to its source.

IMPLEMENTATION

    Two classes are implemented here:

        BinaryTree - a subclass of Algorithm.

        BinaryTree.Status - a subclass of Algorithm.Status

    In addition, the following default coin flip method is defined:

        result = cointoss(cell, bias=0.5, **kwargs)

    The return value is a boolean, True for a head or false for a Tail.  The
    cell argument is ignored.  If a uniformly random value (rng.random()) is
    less than the bias, the result is a head.

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
from mazes import rng, Algorithm

def cointoss(cell, bias=0.5, **kwargs) -> bool:
    """a simple coin toss simulation

    If a uniformly random value is less than the bias (default=0.5), then
    True is returned.  The cell argument is ignored.
    """
    return rng.random() < bias

class BinaryTree(Algorithm):
    """the simple binary tree maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Simple Binary Tree"

        __slots__ = ("__onward", "__upward", "__flip", "__kwargs",
                     "__iter", "__grid")

        def parse_args(self, onward:str="east", upward:str="north",
                       flip:callable=cointoss, randomize:bool=False,
                       **kwargs):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                onward - the onward direction (tail). The default is "east".

                upward - the upward direction (head). The default is "north".

                flip - a function which takes a cell and some keyword arguments
                    as input and returns a boolean value: True for a head and
                    False for a tail.  The default is method 'cointoss' defined
                    above.

            KEYWORD ARGUMENTS

                name - handled by __init__ in the base class.

                bias - the probability of a head.  The default is 0.5 in
                    'cointoss'.  This argument is passed to flip, if present.

                randomize (default False) - if True, the grid is shuffled
                    to get a new iteration order. (This option is primarily
                    for demonstation purposes.)

                **kwargs
                    all other keyword arguments are passed to the coin flip
                    subroutine.
            """
            super().parse_args()            # chain to parent
            self.__onward = onward
            self.__upward = upward
            self.__flip = flip
            self.__kwargs = kwargs
            self.__grid = list(self.grid)
            if randomize:
                rng.shuffle(self.__grid)

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 0)
            self.store_item("passages", 0)
                # set up the iteration
            self.__iter = iter(self.__grid)
            self.more = True

        def upward(self, cell):
            """upward neighbor?"""
            nbr = cell[self.__upward]
            return nbr if nbr and not nbr.hidden else None

        def onward(self, cell):
            """onward neighbor?"""
            nbr = cell[self.__onward]
            return nbr if nbr and not nbr.hidden else None

        def link(self, cell, nbr):
            """carve a passage"""
            self.increment_item("passages")
            self.maze.link(cell, nbr)

        def flip_in(self, cell) -> bool:
            """flip a coin in a cell"""
            return self.__flip(cell, **self.__kwargs)

        def visit_cell(self, cell):
            """process the cell"""
            self.increment_item("cells")
            onward = self.onward(cell)
            upward = self.upward(cell)
            if bool(onward):
                if bool(upward):
                    if self.flip_in(cell):                  # head
                        self.link(cell, upward)
                    else:                                   # tail
                        self.link(cell, onward)
                else:
                    self.link(cell, onward)
            elif bool(upward):
                self.link(cell, upward)

        def visit(self):
            """visit or basic pass"""
            try:
                cell = next(self.__iter)
                self.visit_cell(cell)
            except StopIteration:
                self.more = False

        def __str__(self):
            """string representation"""
            self.store_item("onward", self.__onward)
            self.store_item("upward", self.__upward)
            bias = self.__kwargs["bias"] if "bias" in self.__kwargs \
                else 0.5
            self.store_item("bias", bias)
            return super().__str__()

# end module mazes.Algorithms.simple_binary_tree
