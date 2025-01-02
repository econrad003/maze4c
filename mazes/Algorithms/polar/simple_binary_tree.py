"""
mazes.Algorithms.polar.simple_binary_tree - a simple binary tree algorithm
    for theta mazes
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In the simple binary tree algorithm, cells (in principle) are processed
    in parallel. In each cell where there is a choice, a coin is tossed.  If
    the coin is a head, the rule is to carve a passage northward.  If the
    toss is a tail, the result is carving eastward.

    In the polar version, the eastard movement is replaced by clockwise or
    counterclockwise movement and the northward movement is replaced by
    outward movement.  (Outward movement is okay as the number of cells
    in a ring does not decrease as the radial distance (from center) increases.)

    In each ring, we identify a direction of flow (either clockwise or
    anticlockwise) and a privileged cell.  In the privileged cell, we cannot
    carve in the direction of flow.  In the outermost ring, we cannot carve
    outward.  In the outermost privileged cell, we cannot carve an exit.

    In cells where we have a choice, we flip a coin to decide what to do.
    With a head, we carve outward. If there is an outward split, we choose the
    last outward exit in the direction of flow.  With a tail, we carve an exit
    in the direction of flow.

    In privileged cells, the coin always returns a head.

IMPLEMENTATION

    Two classes are implemented here:

        BinaryTree - a subclass of Algorithm.

        BinaryTree.Status - a subclass of Algorithm.Status

    The following default coin flip method is defined:

        result = cointoss(_, bias=0.5, **kwargs)

    The return value is a boolean, True for a head or false for a Tail.  The
    cell argument is ignored.  If a uniformly random value (rng.random()) is
    less than the bias, the result is a head.  The first parameter depends on
    where the flip is used, but is not referenced in the method.

    The following range selection method is implemented:

        k = randint(_, n:int, **kwargs)

    The return value is a uniformly random integer in range(n), i.e.
        0 <= k < n.

    Two additional methods have been supplied which can be substituted for
    method cointoss:

        tf = true(*args, **kwargs)
        tf = false(*args, **kwargs)

    The first always returns True and the second False.

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
from mazes.tools.coin_tossing import cointoss
from mazes.tools.coin_tossing import all_heads as true
from mazes.tools.coin_tossing import all_tails as false

def randint(ring:int, n:int, **kwargs) -> int:
    """choose an integer in range(n)"""
    return rng.randrange(n)

class BinaryTree(Algorithm):
    """the simple binary tree maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Simple Binary Tree (Theta Maze)"

        __slots__ = ("__flip", "__bias", "__kwargs",
                     "__flows", "__privileged", "__iter")

        def parse_args(self,
                       flip1:callable=cointoss, bias1:float=0.5, kwargs1={},
                       flip2:callable=cointoss, bias2:float=0.5, kwargs2={},
                       randint:callable=randint, kwargs3={}):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - an uncarved theta maze, handled by __init__ in the
                    base class.

            KEYWORD ARGUMENTS

                flip1 - a True/False function of two arguments.  The calling
                    sequence flip1(cell, bias=bias1, **kwargs1).  The default is
                    a coin toss with a probability p=bias1 of heads.  This
                    function determines whether we carve outward (head) or
                    onward (tail) from a non-privileged cell.

                bias1 - a Bernoulli probability (default 0.5) passed as a
                    keyword argument ('bias') to flip1

                kwargs1 - keyword arguments (as a dictionary) for flip1

                flip2 - a True/False function of two arguments.  The calling
                    sequence flip2(ring, bias=bias2, **kwargs1).  The default is
                    a coin toss with a probability p=bias2 of heads.  This
                    function determines the direction of flow for the given
                    ring.

                    Also accepted are the strings "cw" and "ccw".

                bias1 - a Bernoulli probability (default 0.5) passed as a
                    keyword argument ('bias') to flip2

                kwargs2 - keyword arguments (as a dictionary) for flip2

                randint - a function randint(ring, n, **kwargs3) which
                    determines the privileged cell for a given ring by
                    selecting an integer in range(n).  The default is a
                    random selection with equal probability.

                kwargs3 - keyword arguments (as a dictionary) for randint
            """
            super().parse_args()            # chain to parent
            if not callable(flip1):
                raise TypeError("'flip1' is a cointoss function")
            self.__flip = flip1
            self.__bias = float(bias1)
            self.__kwargs = kwargs1
            if isinstance(flip2, str):
                if flip2.lower() == "cw":
                    flip2 = false
                elif flip2.lower == "ccw":
                    flip2 == true
            if not callable(flip2):
                raise TypeError("'flip2' is a cointoss function")
            if not callable(randint):
                raise TypeError("'randint' is a random range function")
            self.__flows = list()
            self.__privileged = set()
            grid = self.maze.grid
            for ring in range(grid.m):
                n = grid.n(ring)
                self.__flows.append(flip2(ring, bias=bias2, **kwargs2))
                j = randint(ring, n, **kwargs3)
                self.__privileged.add(grid[ring, j])

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 0)
            self.store_item("passages", 0)
                # set up the iteration
            self.__iter = iter(self.grid)
            self.more = True

        def outward(self, cell):
            """outward neighbor?"""
            i, j = cell.index
            split = cell.split
            flow = self.__flows[i]
            nbr = cell.outward(split-1) if flow else cell.outward(0)
            return nbr if nbr and not nbr.hidden else None

        def onward(self, cell):
            """onward neighbor?"""
            if cell in self.__privileged:
                return None
            i, j = cell.index
            flow = self.__flows[i]
            nbr = cell.counterclockwise if flow else cell.clockwise
            return nbr if nbr and not nbr.hidden else None

        def link(self, cell, nbr):
            """carve a passage"""
            self.increment_item("passages")
            self.maze.link(cell, nbr)

        def flip_in(self, cell) -> bool:
            """flip a coin in a cell"""
            return self.__flip(cell, bias=self.__bias, **self.__kwargs)

        def visit_cell(self, cell):
            """process the cell"""
            self.increment_item("cells")
            onward = self.onward(cell)
            outward = self.outward(cell)
            if bool(onward):
                if bool(outward):
                    if self.flip_in(cell):                  # head
                        self.link(cell, outward)
                    else:                                   # tail
                        self.link(cell, onward)
                else:
                    self.link(cell, onward)
            elif bool(outward):
                self.link(cell, outward)

        def visit(self):
            """visit or basic pass"""
            try:
                cell = next(self.__iter)
                self.visit_cell(cell)
            except StopIteration:
                self.more = False

        def __str__(self):
            """string representation"""
            bias = self.__bias
            self.store_item("bias", bias)
            return super().__str__()

# end module mazes.Algorithms.polar.simple_binary_tree