"""
mazes.Algorithms.sidewinder - the sidewinder maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In the sidewinder algorithm, rows (in principle) are processed in parallel.
    The algorithm is a generalization of the simple binary tree algorithm.
    In each cell where there is a choice, a coin is tossed.  If the
    coin is a head, the rule is to carve a passage northward from somewhere
    in the east-west run containing the cell.  In the event of a tail, the
    response is to extend the current run eastward.  The spanning tree that is
    returned is not in general a binary tree as degree 4 cells can be created
    when carving northward.

    Sidewinder is a true generalization of the simple binary tree algorithm:
    if we always choose the last cell in a run when carving northward, the
    algorithm reduces to simple binary tree.  If, instead, we always choose the
    first cell, the algorithm reduces to a west/north simple binary tree (where
    we carve westward instead of eastward).  If we always choose either the
    first or the last entry in the run, the result is a binary spanning tree
    which generalizes the east/north and west/north binary trees.

    The result on an oblong grid is a spanning tree with a continuous east-west
    corridor along the north boundary wall.  To find a path between two cells,
    simply go north whenever possible or east otherwise until the north
    corridor is reached.  Follow one of these paths until the two paths either
    meet or they end in the north corridor, and then trace the second path
    back to its source.

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).

IMPLEMENTATION

    Two classes are implemented here:

        Sidewinder - a subclass of Algorithm.

        Sidewinder.Status - a subclass of Algorithm.Status

    In addition, two default methods are defined.  The first is the following
    default coin flip method is defined:

        result = cointoss(cell, bias=0.5, **kwargs)

    The return value is a boolean, True for a head or false for a Tail.  The
    cell argument is ignored.  If a uniformly random value (rng.random()) is less
    than the bias, the result is a head.

    The second method is a run choice method:

        cell, nbr = run_choice(run, which=None, **kwargs)

    The value of 'which' can be the constant None or an integer.  If the
    integer is -1, the last run entry is chosen; if 0, the first entry.  If
    the value is None, the choice is uniformly random.  Integers are
    tried once -- if the integer is not a valid index, then the default
    (None) will be used.  Tuples of integers can also be entered -- in this
    case, a choice will be made from the tuple and tried as the index -- for
    example (0, -1) randomly chooses the first or last element.

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
from mazes.Grids.oblong import EAST, NORTH, WEST, SOUTH

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

class Sidewinder(Algorithm):
    """the sidewinder maze carving algorithm"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Sidewinder Tree"

        __slots__ = ("__upward", "__onward", "__tier", "__in_tier",
                     "__bias", "__flip", "__choose_in_run", "__which",
                     "__iter1", "__iter2", "__run",
                     "__current_tier", "__current_cell", "__next_cell")

        def parse_args(self, onward:str="east", upward:str="north",
                       bias:float=0.5, flip:callable=coin_toss,
                       choose_in_run:callable=run_choice,
                       which=None,
                       **kwargs):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                name - handled by __init__ in the base class.

                onward - the onward directions (tail). The default is "east".

                upward - the upward direction (head). The default is "north".

                flip - a function which takes a cell and some keyword arguments
                    as input and returns a boolean value: True for a head and
                    False for a tail.  The default is method 'cointoss' defined
                    above.

                choose_in_run - a function which takes a run and some keyword
                    arguments and returns an ordered pair from the run.  The
                    default is 'run-choice' defined above.

                bias - the probability of a head.  This argument is passed to
                    flip, if present.

                which - the Python built-in any, or an integer, or a tuple of
                    integers which controls the way elements of a run are
                    chosen for carving in the upward direction.
            """
            super().parse_args()            # chain to parent
            self.__onward = onward
            self.__upward = upward
            self.__bias = bias
            self.__flip = flip
            self.__choose_in_run = choose_in_run
            self.__which = which

        def add_iterator(self, way:str, tier:list, in_tier:list):
            """set up the iterator

            ARGUMENTS

                way - an onward direction

                tier - the tier generator (callable), positional arguments
                    (tuple), and the keyword arguments (dict)

                in_tier - the in-tier generator (callable), additional
                    positional arguments (tuple), and the keyword arguments
                    (dict)
            """
            self.__tier[way] = tier
            self.__in_tier[way] = in_tier

        def initialize(self):
            """initialization

            Here we set up the iterables.  If the onward direction is
            west or south, we reverse the flow.  The upward direction
            is perpendicular and flow doesn't matter.
            """
            self.__tier = dict()
            self.__in_tier = dict()
            self.add_iterator(EAST, [self.grid.rows, (), {}],
                              [self.grid.row, (), {}])
            self.add_iterator(WEST, [self.grid.rows, (), {}],
                              [self.grid.row, (), {'reverse':True}])
            self.add_iterator(NORTH, [self.grid.columns, (), {}],
                              [self.grid.column, (), {}])
            self.add_iterator(SOUTH, [self.grid.columns, (), {}],
                              [self.grid.column, (), {'reverse':True}])

        def configure(self):
            """configuration"""
                # set up the statistics
            self.store_item("cells", 0)
            self.store_item("passages", 0)

                    # set up the first row
            iterator, args, kwargs = self.__tier[self.__onward]
            self.__iter1 = iter(iterator(*args, **kwargs))
            self.__next_cell = None
            self.more = True

        def upward(self, cell):
            """upward neighbor?"""
            north = cell[self.__upward]
            return [north] if north and not north.hidden else []

        def onward(self, cell):
            """onward neighbor?

            As this method uses the iterator, we need to be careful:
                1) Do not call this method more than once per visit...
                2) Do not call the iterator in the visit except when
                   when retrieving the first cell in the 'row'.
            """
            try:
                successor = next(self.__iter2)
                self.__next_cell = successor
                if successor in cell.neighbors:
                    return successor                # can link
            except StopIteration:
                self.__next_cell = None             # end of row

                    # either the current cell and its successor are not
                    # neighbors, or the end of the 'row' has been reached
            return None                             # cannot link

        def link(self, cell, nbr):
            """carve a passage"""
            self.increment_item("passages")
            self.maze.link(cell, nbr)

        def coin_toss(self, cell) -> bool:
            """flip a coin in a cell"""
            return self.__flip(cell, bias=self.__bias)

        def add_to_run(self, cell, upward):
            """add the cells upward neighbors to the current run"""
            for nbr in upward:
                pack = (cell, nbr)
                self.__run.append(pack)

        def close_run(self):
            """select a cell/neighbor pair and link"""
            cell, nbr = self.__choose_in_run(self.__run, self.__which)
            self.link(cell, nbr)
            self.__run = list()

        def visit_cell(self, cell):
            """process the cell"""
            self.increment_item("cells")
            if cell.hidden:
                raise ValueError(f"hidden cell {cell.index} in iteration")
            onward = self.onward(cell)
            upward = self.upward(cell)
            self.add_to_run(cell, upward)
            if bool(onward):
                if len(self.__run) > 0:
                    if self.coin_toss(cell):              # head
                        self.close_run()
                    else:                               # tail
                        self.link(cell, onward)
                else:
                    self.link(cell, onward)
            elif len(self.__run) > 0:
                self.close_run()

        def visit(self):
            """visit or basic pass"""
            self.__current_cell = self.__next_cell
            self.__next_cell = None
            while self.__current_cell == None:
                try:
                    tier = self.__current_tier = next(self.__iter1)
                    # print(tier)
                except StopIteration:
                    self.more = False
                    return                  # no more rows
                iterator, args, kwargs = self.__in_tier[self.__onward]
                self.__iter2 = iter(iterator(tier, *args, **kwargs))
                try:
                    self.__current_cell = next(self.__iter2) # first in row
                    # print("visit", self.__current_cell.index)
                except StopIteration:
                    self.__current_cell = None               # empty row
                self.__run = list()
            self.visit_cell(self.__current_cell)

        def __str__(self):
            """string representation"""
            self.store_item("onward", self.__onward)
            self.store_item("upward", self.__upward)
            bias = self.__bias
            self.store_item("bias", bias)
            return super().__str__()

# end module mazes.sidewinder
