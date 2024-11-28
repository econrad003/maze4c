"""
mazes.inwinder - the inwinder maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The inwinder algorithm is a variation of the sidewinder algorithm.
    In sidewinder, we divide a row into runs and in each run, we carve
    one passage north to the next row. Of course, a symmetry argument
    indicates that we could instead carve southward from each run instead
    of northward.  Another symmetry argument tells us that we could
    divide a column into rises and from each rise, carve a passage eastward.

    Inwinder is not a symmetry, but it is an application of the same
    algorithm.  We divide the oblong grid into a sequence of rectangular
    rings, each ring being a fixed number of cells in taxicab distance
    from the perimeter of the oblong.  As in sidewinder, we divide each ring
    into a sequence of consecutive runs.  From each run, we choose a cell (but
    not a corner cell) to carve a passage inward.

    The reason for not carving inward from a corner is straightforward:
    corner cell don't have inward neighbors.  Consequently, in our runs,
    we don't permit isolated corners.

IMPLEMENTATION

    Two classes are implemented here:

        Inwinder - a subclass of Algorithm.

        Inwinder.Status - a subclass of Algorithm.Status

    In addition, two default methods are defined.  The first is the following
    default coin flip method is defined:

        result = cointoss(cell, bias=0.5)

    The second method is a run choice method:

        cell, nbr = run_choice(run, which=None)

    These are identical to those defined in the sidewinder implementation.
    They are described below in method Inwinder.Status.parse_args.

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

class Inwinder(Algorithm):
    """the inwinder maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Inwinder Tree"

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
            self.store_item("inward", 0)
            self.store_item("backward", 0)

                # set up the visits
            self.__tier = 0
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

        def can_go_inward(self, i, cell) -> list:
            """return the inward neighbors"""
            nbrs = self.__rings.classify(cell)
            for nbr in nbrs:
                if nbrs[nbr] == 1:
                    self.__run.append((cell, nbr))
            return len(self.__run) > 0

        def last_in_tier(self, i, cell) -> bool:
            """is the the last in the ring?"""
            return cell == self.__path[-1]

        def carve_inward(self):
            """carve a passage inward"""
            self.increment_item("inward")
            chosen = self.__choose(self.__run, which=self.__which)
            self.link(*chosen)
            self.__run = list()

        def carve_onward(self, i, cell):
            """carve a passage onward"""
            self.increment_item("onward")
            nbr = self.grid[self.__path[i+1]]
            self.link(cell, nbr)

        def maybe_carve_backward(self, i, cell):
            """carve a passage backward

            This only happens under three simultaneous conditions:
                (i) the cell is the last cell in the ring;
                (ii) the cell is a corner cell (and thus has no inward
                    neighbors); and
                (iii) a HEAD was called in the previous cell.

            The decision procedure in visit_cell insures that this method
            is only called when the run has no inward neighbors.  This
            could happen either when the run is in the innermost ring or
            when this is a corner cell in some other ring.
            """
            if i+1 < len(self.__path):
                return              # not the last cell
            if self.__tier+1 == len(self.__rings):
                return              # innermost tier

                    # some weird stuff might happen if some cells are
                    # hidden.  The following checks are to cover that
                    # situation.  Of course the resulting maze might
                    # not be perfect.
            if i < 1:
                return              # no previous cell in path
            nbr = self.grid[self.__path[i-1]]
            if nbr not in cell.neighbors:
                return              # don't link
            # print("  go backward")
            self.increment_item("backward")
            self.link(cell, nbr)

        def coin_toss(self, i, cell):
            """head -- go inward; tail -- go onward"""
            if self.__flip(cell, bias=self.__bias):
                    # HEAD
                # print("  HEAD")
                self.carve_inward()
            else:
                # print("  TAIL")
                    # TAIL
                self.carve_onward(i, cell)

        def visit_cell(self, i, cell):
            """process a cell"""
            # print(cell.index, self.__run)
            if self.can_go_onward(i, cell):
                if self.can_go_inward(i, cell):
                    self.coin_toss(i, cell)
                else:
                    # print("  forge onward")
                    self.carve_onward(i, cell)
            else:
                if self.can_go_inward(i, cell):
                    # print("  forge inward")
                    self.carve_inward()
                else:
                    # print("  maybe go backward")
                    self.maybe_carve_backward(i, cell)

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

# end module mazes.inwinder