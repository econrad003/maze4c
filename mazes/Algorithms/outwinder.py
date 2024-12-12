"""
mazes.Algorithms.outwinder - the outwinder maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The outwinder algorithm, like its sibling inwinder, is a variation of
    the sidewinder algorithm.

    In sidewinder, we divide a row into runs and in each run, we carve
    one passage north to the next row. Of course, a symmetry argument
    indicates that we could instead carve southward from each run instead
    of northward.  Another symmetry argument tells us that we could
    divide a column into rises and from each rise, carve a passage eastward.

    Outwinder is an application of the same  algorithm.  As in inwinder, we
    divide the oblong grid into a sequence of rectangular rings, each ring
    being a fixed number of cells in taxicab distance from the perimeter of
    the oblong.  Again as in inwinder, we divide each ring into a sequence
    of consecutive runs.  From each run, we choose a cell to carve a passage
    outward.  (Note that with a corner cell, we have two outward neighbors to
    choose from.  The availability of outward neighbors from the corners
    makes outwinder a bit simpler than inwinder.)

IMPLEMENTATION

    Two classes are implemented here:

        Outwinder - a subclass of Algorithm.

        Outwinder.Status - a subclass of Algorithm.Status

    In addition, two default methods are defined.  The first is the following
    default coin flip method is defined:

        result = cointoss(cell, bias=0.5)

    The second method is a run choice method:

        cell, nbr = run_choice(run, which=None)

    These are identical to those defined in the sidewinder implementation.
    They are described below in method Outwinder.Status.parse_args.

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
from mazes import rng, Algorithm, Cell
from mazes.Grids.oblong_rings import ConcentricOblongs

def coin_toss(cell, bias=0.5) -> bool:
    """a simple coin toss simulation

    If a uniformly random value is less than the bias (default=0.5), then
    True is returned.  The cell argument is ignored.
    """
    return rng.random() < bias

def run_choice(run, which:(tuple, int, None)=None) -> tuple:
    """a choice function

    See the module documentation for details.

    Returns a cell, neighbor pair.
    """
    if isinstance(which, (tuple, list)):
        which = any if len(which) == 0 else rng.choice(which)
    if isinstance(which, int):
        try:
            result = run[which]
            return result
        except IndexError:
            pass
    return rng.choice(run)

class Outwinder(Algorithm):
    """the outwinder maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Outwinder Tree"

        __slots__ = ('__rings', '__tier', '__path', '__run',
                     '__flip', '__bias',
                     '__choose', '__which')

        def parse_args(self, *args,
                       flip:callable=coin_toss, bias=0.5,
                       choose_in_run:callable=run_choice, which=any,
                       **kwargs):
            """argument parser

            KEYWORD ARGUMENTS

                flip - the coin toss method

                    Flip takes cell a bias and returns a boolean: True or
                    False represents a head or a tail, respectively.  The
                    default is method 'coin_toss' defined above.  The cell
                    is ignored in the default method.

                bias - the probability of a head

                    The bias is passed as a keyword argument to the flip
                    method

                choose_in_run - the method used to choose a cell-neighbor
                    pair from a run.  It takes a run and 'which' and returns
                    an entry in the run.  The default is the method
                    'run_choice' defined above.

                which - a keyword parameter used to decide how the run choice
                    method picks an entry.  The default method 'run_choice'
                    admits three types of input:
                        (i) a tuple or list of integers:
                            one of these integers is chosen and used as in (ii)
                        (ii) a list index, so, for example, 0 represents the
                            first entry, 1 the second, -1 the last
                        (iii) anything that fails as a list integer, i.e. a
                            non-integer (e.g. None or any) or an integer
                            which raises an IndexError exception, results in
                            a uniform choice from the entire run.
            """
            super().parse_args(*args, **kwargs)
            self.__flip = flip              # coin toss
            self.__bias = bias
            self.__choose = choose_in_run   # run choice
            self.__which = which

        def initialize(self):
            """initialization"""
            self.__rings = ConcentricOblongs(self.grid)

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 0)
            self.store_item("passages", 0)
            self.store_item("tiers", 0)
            self.store_item("onward", 0)
            self.store_item("outward", 0)

                # set up the visits
            self.__tier = 0         # outermost tier
            self.__run = list()
            self.more = True

        def link(self, cell, nbr):
            """carve a passage"""
            self.increment_item("passages")
            self.maze.link(cell, nbr)

        def can_go_onward(self, i, cell) -> bool:
            """is the next cell ok?"""
            if cell.index == self.__path[-1]:
                return False            # last cell
            next_cell = self.grid[self.__path[i+1]]
            return next_cell in cell.neighbors

        def can_go_outward(self, i, cell) -> list:
            """return the outward neighbors"""
            nbrs = self.__rings.classify(cell)
            for nbr in nbrs:
                if nbrs[nbr] == -1:
                    self.__run.append((cell, nbr))
            return len(self.__run) > 0

        def last_in_tier(self, i, cell) -> bool:
            """is the the last in the ring?"""
            return cell == self.__path[-1]

        def carve_outward(self):
            """carve a passage outward"""
            self.increment_item("outward")
            chosen = self.__choose(self.__run, which=self.__which)
            self.link(*chosen)
            self.__run = list()

        def carve_onward(self, i, cell):
            """carve a passage onward"""
            self.increment_item("onward")
            nbr = self.grid[self.__path[i+1]]
            self.link(cell, nbr)

        def coin_toss(self, i, cell):
            """head -- go inward; tail -- go onward"""
            if self.__flip(cell, bias=self.__bias):
                    # HEAD
                # print("  HEAD")
                self.carve_outward()
            else:
                # print("  TAIL")
                    # TAIL
                self.carve_onward(i, cell)

        def visit_cell(self, i, cell):
            """process a cell"""
            # print(cell.index, self.__run)
            if self.can_go_onward(i, cell):
                if self.can_go_outward(i, cell):
                    self.coin_toss(i, cell)
                else:
                    # print("  forge onward")
                    self.carve_onward(i, cell)
            else:
                if self.can_go_outward(i, cell):
                    # print("  forge outward")
                    self.carve_outward()
                else:
                    # print("  the last cell (or so it seems)")
                    pass

        def visit_tier(self):
            """process a ring"""
            if self.__path[-1] == None:
                        # innermost tier is a chain
                self.__path.pop()
            else:
                        # rotate the path (don't need to reverse)
                rot = rng.randrange(len(self.__path))
                self.__path = self.__rings.transform(self.__path, rotate=rot)
            for i in range(len(self.__path)):
                self.increment_item("cells")
                cell = self.grid[self.__path[i]]
                assert isinstance(cell, Cell)
                self.visit_cell(i, cell)

        def visit(self):
            """visit or basic pass"""
            try:
                self.__path = self.__rings.pathmaker(self.__tier)
                self.increment_item("tiers")
                self.visit_tier()
                self.__tier += 1
            except ValueError:
                self.more = False

        def __str__(self):
            """string representation"""
            # bias = self.__bias
            # self.store_item("bias", bias)
            return super().__str__()

# end module mazes.outwinder