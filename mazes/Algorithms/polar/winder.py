"""
mazes.Algorithms.polar.winder - a sidewinder algorithm for theta mazes
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In the polar version of the simple binary tree algorithm, in most cells,
    we flip a coin.  If the coin lands face up (head/True), we carve an exit
    outward from the cell.  If it lands face down (tail/False), we instead
    carve a lateral exit.  (The lateral direction is fixed for each ring.)

    In each ring, in addition to direction of lateral flow (either clockwise
    or anticlockwise), we identify a privileged cell.  In a privileged cell,
    we cannot carve laterally.  In the outermost ring, where we cannot carve
    outward, we must carve an exit laterally -- in the outermost privileged
    cell, we simply cannot carve an exit.

    We can also adapt the sidewinder algorithm to work in a theta grid.  As
    with the simple binary tree algorithm, our rows are the circular rings.
    The analogy for columns is weaker, but we do have rises.  For the binary
    tree algorithm, our rises were forced outward towards the equator, but only
    because rises inward toward the pole would not necessarily preserve the
    binary aspect of the trees.  With the sidewinder algorithm, we aren't under
    pressure to form binary trees, so we can rise in either direction.

    If our rises are outward, we call the algorithm outwinder.  For inward
    rises the algorithm is inwinder.  Since we don't really have sides, we can
    simply refer to inwinder and outwinder as winder...

IMPLEMENTATION

    Five classes are implemented here:

        _WinderStatus - a subclass of Algorithm.Status, intended for use
            herein.  This is the class that actually does all the work.

        Inwinder - a subclass of Algorithm

        Inwinder.Status - a subclass of _WinderStatus

        Outwinder - a subclass of Algorithm

        Outwinder.Status - a subclass of _WinderStatus

    The calling sequence is either:

        status = Inwinder.on(maze, **kwargs)

    or:

        status = Outwinder.on(maze, **kwargs)

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

    Two additional methods have been supplied which can be substiuted for
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

def choose_from_run(ring:int, run:list, **kwargs) -> tuple():
    """choose an ordered pair from the run"""
    return rng.choice(run)

class _WinderStatus(Algorithm.Status):
    """this is where most of the work is done"""

    __slots__ = ("__flip", "__bias", "__kwargs",
                 "__choose", "__ckwargs",
                 "__flows", "__privileged",
                 "__ring", "__iter", "__run",
                 "__rise")

    def parse_args(self,
                   flip1:callable=cointoss, bias1:float=0.5, kwargs1={},
                   flip2:callable=cointoss, bias2:float=0.5, kwargs2={},
                   randint:callable=randint, kwargs3={},
                   choose:callable=choose_from_run, kwargs4={}):
        """parse constructor arguments

        POSITIONAL ARGUMENTS

            maze - an uncarved theta maze, handled by __init__ in the
                base class.

        KEYWORD ARGUMENTS

            flip1 - a True/False function of two arguments.  The calling
                sequence flip1(cell, bias1, **kwargs1).  The default is
                a coin toss with a probability p=bias1 of heads.  This
                function determines whether we carve outward (head) or
                onward (tail) from a non-privileged cell.

            bias1 - a Bernoulli probability (default 0.5) passed as the
                second argument to flip1

            kwargs1 - keyword arguments (as a dictionary) for flip1

            flip2 - a True/False function of two arguments.  The calling
                sequence flip2(ring, bias1, **kwargs1).  The default is
                a coin toss with a probability p=bias2 of heads.  This
                function determines the direction of flow for the given ring.

                Also accepted are the strings "cw" and "ccw".

            bias1 - a Bernoulli probability (default 0.5) passed as the
                second argument to flip2

            kwargs2 - keyword arguments (as a dictionary) for flip2

            randint - a function randint(ring, n, **kwargs3) which
                determines the privileged cell for a given ring by
                selecting an integer in range(n).  The default is a
                random selection with equal probability.

            kwargs3 - keyword arguments (as a dictionary) for randint

            choose - given a ring number and a list of rises (ordered pairs
                of cells), choose just one to carve a rise.

            kwargs4 - keyword arguments (as a dictionary) for choose
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
        self.__privileged = {}
        grid = self.maze.grid
        for ring in range(grid.m):
            n = grid.n(ring)
            self.__flows.append(flip2(ring, bias=bias2, **kwargs2))
            j = randint(ring, n, **kwargs3)
            self.__privileged[ring] = j
        if not callable(choose):
            raise TypeError("'choose' is a random choice function")
        self.__choose = choose
        self.__ckwargs = kwargs4
        self.__rise = None
        self.__run = []

    def configure(self):
        """configuration"""
            # set up the statistics
        self.store_item("cells", 0)
        self.store_item("passages", 0)
            # set up the iteration
        self.__ring = 0
        n = self.maze.grid.n(0)
        j = self.__privileged[0]
        flow = self.__flows[0]
        self.__privileged[0] = self.maze.grid[0, j]
        self.__iter = iter(range(j+1, j+n+1)) if flow \
            else iter(range(j-1, j-n-1, -1))

    @property
    def rise(self):
        """rise getter"""
        return self.__rise

    @rise.setter
    def rise(self, direction:str):
        """rise getter"""
        self.__rise = direction
        return direction

    @property
    def more(self):
        """more rows?"""
        return self.__ring < self.maze.grid.m

    def extend_run_outward(self, curr:'Cell'):
        """extend the run to include possible outward neighbors"""
        ring = self.__ring
        if ring + 1 >= self.maze.grid.m:
            return              # outermost ring, so nothing to do
        split = curr.split
        items = range(split) if self.__flows[ring] \
            else range(split-1, -1, -1)
        for j in items:
            nbr = curr.outward(j)
            if nbr and not nbr.hidden:
                self.__run.append((curr, nbr))
        return self.__run

    def extend_run_inward(self, curr:'Cell'):
        """extend the run to include possible inward neighbors"""
        ring = self.__ring
        if ring < 1:
            return              # innermost ring, so nothing to do
        nbr = curr.inward
        if nbr and not nbr.hidden:
            self.__run.append((curr, nbr))
        return self.__run

    def extend_run(self, curr:'Cell'):
        """try to extend the run"""
        if self.__rise == "outward":                # outwinder
            return self.extend_run_outward(curr)
        if self.__rise == "inward":                 # inwinder
            return self.extend_run_inward(curr)
        raise NotImplementedError("winder rise error")

    def onward(self, cell):
        """onward neighbor?"""
        if cell == self.__privileged[self.__ring]:
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

    def close_run(self):
        """close the current run"""
        if not self.__run:
            return                  # empty
        pair = self.__choose(self.__ring, self.__run, **self.__ckwargs)
        self.link(*pair)
        self.__run = []

    def visit_cell(self, cell):
        """process the cell"""
        self.increment_item("cells")
        onward = self.onward(cell)
        run = self.extend_run(cell)
        if bool(onward):
            if bool(run):
                if self.flip_in(cell):                  # head
                    self.close_run()
                else:                                   # tail
                    self.link(cell, onward)
            else:
                self.link(cell, onward)
        elif bool(run):
            self.close_run()

    def visit(self):
        """visit or basic pass"""
        grid = self.maze.grid
        try:
            j = next(self.__iter)
            curr = grid[self.__ring, j % grid.n(self.__ring)]
            if curr and not curr.hidden:
                self.visit_cell(curr)
            else:
                self.close_run()
        except StopIteration:
            self.close_run()
            self.__ring += 1
            ring = self.__ring
            if ring < grid.m:
                n = grid.n(ring)
                j = self.__privileged[ring]
                flow = self.__flows[ring]
                self.__privileged[ring] = self.maze.grid[ring, j]
                self.__iter = iter(range(j+1, j+n+1)) if flow \
                    else iter(range(j-1, j-n-1, -1))

    def __str__(self):
        """string representation"""
        bias = self.__bias
        self.store_item("rise direction", str(self.__rise))
        self.store_item("bias", bias)
        return super().__str__()

class Inwinder(Algorithm):
    """the inwinder algorithm for theta grids"""

    class Status(_WinderStatus):
        """the parent _WinderStatus does all the work"""

        NAME = "Polar Inwinder"

        def initialize(self):
            """initialization"""
            super().initialize()
            self.rise = "inward"

class Outwinder(Algorithm):
    """the outwinder algorithm for theta grids"""

    class Status(_WinderStatus):
        """the parent _WinderStatus does all the work"""

        NAME = "Polar Outwinder"

        def initialize(self):
            """initialization"""
            super().initialize()
            self.rise = "outward"

# end module mazes.Algorithms.polar.winder