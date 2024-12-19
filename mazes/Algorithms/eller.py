"""
mazes.Algorithms.eller - Eller's maze carving algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    In the sidewinder algorithm, a generalization of the simple binary tree
    algorithm, we break a row into a series of runs and carve upward from each
    run.  In the top row, since we can't carve upward, we are forced to carve a
    single run.

    Eller's algorithm, invented by Martin Eller in 1982, generalizes this in a
    way that normally does not leave a single run in the top row. [1, pp 189ff]

    In the simple binary tree algorithm, we could, at least in principle, treat
    every cell as independent -- the result of a coin flip in one cell does not
    depend at all on what happens in another cell.  But the result of this
    independence are long corridors in the top row and rightmost column.  In
    sidewinder, we gain some complexity in the rightmost column, but lose cell
    independence.

    In sidewinder, we still have row independence  But the price for that is
    the long open path in the top row.  With Eller's algorithm, we pay a price
    for some complexity in the top row -- what happens in one cell can affect
    the choices made in a cell in a later row: we lose row independence.

    How does the algorithm work?  It's usually implemented as a passage carver,
    and that is how we implement it here.

    In each row, we modify what we did in sidewinder:

        a) label each new component in the row;
        b) proceeding from left to right, if a cell and its predecessor are
           in different components, toss a coin:
                head) carve a passage, or
                tail) don't;
        c) from each component in a row, carve at least one passage upward.

    If we carve exactly one passage upward each time, we have sidewinder.

    In the top or final row we discard (c) as we cannot carve upward, and we
    modify (b):

        b') proceeding from left to right, if a cell and its predecessor are
           in different components, carve a passage.

    The point of the modication is to insure that we end up with a single
    component.

    For an example, we use a 3x3 oblong grid:

        +---+---+---+
        | 1 | 2 | 3 |   (a) Row 0 - label the new components
        +---+---+---+

        +---+---+---+
        | 1   1   1 |   (b) Row 0 - merge some neighboring components
        +---+---+---+       (For this example, we merged all of them)

        +---+---+---+
        | 1 |   | 1 |
        +   +---+   +
        | 1   1   1 |   (c) Row 0 - carve up at least once per component
        +---+---+---+

        +---+---+---+
        | 1 | 4 | 1 |   (a) Row 1 - label the new components
        +   +---+   +
        | 1   1   1 |
        +---+---+---+

        +---+---+---+
        | 1 | 1   1 |   (b) Row 1 - merge some components
        +   +---+   +       We can carve (1,1)--(1,0) or (1,2)--(1,1) or
        | 1   1   1 |       do neither, but we cannot do both!
        +---+---+---+

        +---+---+---+
        | 1 | 1 |   |
        +   +   +---+
        | 1 | 1   1 |   (c) Row 1 - carve up at least once per component
        +   +---+   +
        | 1   1   1 |
        +---+---+---+

        +---+---+---+
        | 1 | 1 | 5 |   (a) Row 2 (final row) - label new components
        +   +   +---+
        | 1 | 1   1 |
        +   +---+   +
        | 1   1   1 |
        +---+---+---+

        +---+---+---+
        | 1 | 1   1 |   (b') merge components where possible
        +   +   +---+       we cannot carve (1,1)--(1,0)
        | 1 | 1   1 |       we must carve (1,2)--(1,1)
        +   +---+   +
        | 1   1   1 |
        +---+---+---+

REFERENCES

    [1] Jamis Buck.  Mazes for Programmers.  2015 (Pragmatic Bookshelf).
        Book (978-1-68050-055-4).  Pages 189-197, 250.

IMPLEMENTATION

    Two classes are implemented here:

        Eller - a subclass of Algorithm.

        Eller.Status - a subclass of Algorithm.Status

    In this implementation, we take the normal directions only: runs in rows
    from west to east and rises in columns from south to north.

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
from mazes.tier_registry import TierRegistry, ComponentError

def coin_toss(_cell1, _cell2, *args, bias=0.5, **kwargs) -> bool:
    """a simple coin toss

    All arguments except the bias are ignored.  Return a head (True) with
    probability p=bias and a tail (False) with probability q=1-p.
    """
    return rng.random() < bias

def select_pair(run, *args, **kwargs) -> tuple:
    """a simple uniform choice

    All arguments except the run are ignored.  The run is not empty.
    """
    return rng.choice(run)

class _MetaMethod(object):
    """a namespace for an indirect function"""

    def __init__(self, method, *args, **kwargs):
        """constructor"""
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def do(self, *args):
        """execute the method"""
        return self.method(*args, *self.args, **self.kwargs)

class Eller(Algorithm):
    """Martin Eller's maze carving algorithm"""


    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Martin Eller's Spanning Tree"

        VALID_DIRECTIONS = set([(EAST, NORTH), (EAST, SOUTH), (WEST, NORTH), \
            (WEST, SOUTH), (NORTH, EAST), (NORTH, WEST), (SOUTH, EAST), \
            (SOUTH, WEST)])

        __slots__ = ("__row", "__rows",
                     "__current_run", "__next_run",
                     "__onward", "__upward",
                     "__flip1", "__flip2", "__select_upward",
                     "__debug", "__labels")

                # Grid Management

        def make_row(self, onward):
            """create the row method"""
            grid = self.maze.grid
            if onward == EAST:
                self.__row = _MetaMethod(grid.row)
            elif onward == WEST:
                self.__row = _MetaMethod(grid.row, reverse=True)
            elif onward == NORTH:
                self.__row = _MetaMethod(grid.column)
            elif onward == SOUTH:
                self.__row = _MetaMethod(grid.column, reverse=True)
            elif isinstance(onward, _MetaMethod):
                self.__row = onward
            else:
                raise NotImplementedError

        def row(self, i):
            """retrieve row i"""
            return self.__row.do(i)

#        def test_row(self, i):
#            """test it"""
#            return list(cell.index for cell in self.row(i))

        def make_rows(self, upward):
            """create the rows method"""
            grid = self.maze.grid
            if upward == NORTH:
                rows = _MetaMethod(grid.rows)
            elif upward == SOUTH:
                rows = _MetaMethod(grid.rows, reverse=True)
            elif upward == EAST:
                rows = _MetaMethod(grid.columns)
            elif upward == WEST:
                rows = _MetaMethod(grid.columns, reverse=True)
            elif isinstance(upward, _MetaMethod):
                rows = upward
            else:
                raise NotImplementedError
            self.__rows = list(rows.do())
            # print(self.__rows)

        def upward(self, cell) -> list:
            """return the cells in the indicated direction"""
            up = self.__upward
            return [cell[up]] if cell[up] else []

                # Component management in one row

        def get_first_row(self):
            """first row only (called by configure)

            We must set up the first row, from scratch.
            """
            n = 0
            mapped = self.__rows[n]
            self.debug(1, f"preparing row {mapped}")
            row = list(self.row(mapped))
            registry = TierRegistry()
            self.__next_run = (n, row, registry)        # ready to go

        def get_next_row(self):
            """all rows rows (called by visit)

            In all rows except the last, we merge upward, so we've already
            set up what will be the current row.
            """
            n = self.__next_run[0]
            mapped = self.__rows[n]
            self.debug(1, f"preparing row {mapped} for step 1")
            self.__current_run = self.__next_run

        def access_current_row(self):
            """the first steps

            Merge some of the cells provided they are not in the same
            component.
            """
            n, row, registry = self.__current_run
            mapped = self.__rows[n]
            if len(row) < 1:                # cells in row might be hidden
                self.debug(-1, f"row {mapped} is masked")
                return
            registry.register(row[0])
            # print(row[0].index)
            self.debug(1, f"accessing row {mapped} for step 1")
            for i in range(1, len(row)):
                cell1, cell2 = row[i-1], row[i]
                k1 = registry.register(cell1)
                k2 = registry.register(cell2)
                # print(i, k1, k2, cell1.index, cell2.index)
                if k1 != k2:
                    if cell1 in cell2.neighbors:       # can merge
                        self.try_merge_left(registry, cell1, cell2)

        def try_merge_left(self, registry, cell1, cell2):
            """merge on coin=head"""
            if self.__flip1.do(cell1, cell2):
                self.debug(5, f"merging {cell1.index}--{cell2.index}")
                self.maze.link(cell2, cell1)
                self.increment_item("passages")
                self.increment_item("optional merge left")
                k1 = registry.component_for(cell1)
                k2 = registry.component_for(cell2)
                registry.merge(k1, k2)


                # next row management (1 of 2)
                #   this is the heart of the algorithm...
                #   there are two basic possibilities:
                #       (1) if this is the last row, we work from left to right
                #           and carve passages between cells in different
                #           components
                #       (2) see next comment block

        def complete_last_row(self, n, row, registry):
            """"""
            self.debug(1, f"completing last row (row {n})")
            if len(row) > 0:                # cells in row might be hidden
                registry.register(row[0])
            for i in range(1, len(row)):
                cell1, cell2 = row[i-1], row[i]
                k1 = registry.register(cell1)
                k2 = registry.register(cell2)
                if k1 != k2:
                    if cell1 in cell2.neighbors:       # can merge
                        self.force_merge_left(registry, cell1, cell2)
            if len(registry.components) > 1:
                self.debug(-1, f"unable to merge all components")
                self.debug(-1, f"the resulting maze is not connected")
            elif len(row) > 0:
                self.debug(1, "all the components in the last row were merged")
            self.more = False

        def force_merge_left(self, registry, cell1, cell2):
            """required merge"""
            self.debug(5, f"merging {cell1.index}--{cell2.index} (required)")
            self.maze.link(cell2, cell1)
            self.increment_item("passages")
            self.increment_item("required merge left")
            k1 = registry.component_for(cell1)
            k2 = registry.component_for(cell2)
            registry.merge(k1, k2)

                # next row management (2 of 2)
                #   this is the heart of the algorithm...
                #   there are two basic possibilities:
                #       (1) see above
                #       (2) if this is not the last row, from each component
                #           we carve a passage from _at least one_ cell to
                #           an upward neighbor.  Note that in some grid
                #           configurations, the required passage may force a
                #           merge.

        def complete_a_row(self, n, row, registry):
            """here we carve upward whenever required and possibly elsewhere"""
            if n+1 >= len(self.__rows):
                self.complete_last_row(n, row, registry)
                return
            mapped = self.__rows[n]
            self.debug(1, f"preparing row {mapped} for step 2")
            np = n+1
            mappedp = self.__rows[np]
            self.debug(1, f"accessing row {mappedp}")
            rowp = list(self.row(mappedp))
            registryp = registry.new_tier_state
            self.__next_run = (np, rowp, registryp)
            if len(row) == 0:
                self.debug(-1, f"step 2 aborted -- masked row {mappedp}")
                return                          # empty row, nothing else to do

                    # REQUIRED UPWARD CARVING
            components = registry.components
            components.sort()
            # print(components)
            for k in components:
                # print(k)
                        # prepare candidates for the required upward carving
                items = registry.items_in(k)
                # print(f"component {k}: {len(items)} cells")
                pair = self.find_upward_carve(k, mapped, items)
                if not pair:
                    self.debug(10, "unsuccessful find_upward_carve")
                    continue
                cell, nbr = pair
                self.upward_carve(registry, registryp, cell, nbr)

                    # OPTIONAL UPWARD CARVING
            for cell in row:
                for nbr in self.upward(cell):
                    if cell.is_linked(nbr):
                        continue                # already linked
                    k2 = None
                    try:
                        k2 = registryp.component_for(cell)
                    except KeyError:
                        pass
                    if k2 == None:
                        self.maybe_carve_upward(registry, registryp, cell, nbr)

        def find_upward_carve(self, k, mapped, items) -> tuple:
            """find location of forced carve upward"""
            run = list()
            for cell in items:
                upward = self.upward(cell)
                for nbr in upward:
                    pair = (cell, nbr)
                    run.append(pair)
            if len(run) == 0:
                self.debug(-1, f"empty run in row {mapped} component {k}")
                self.debug(-1, f"the resulting maze will not be connected")
                return None
            return self.__select_upward.do(run)

        def upward_carve(self, registry, registryp, cell, nbr):
            """carve upward from the given cell to the given neighbor"""
            k1 = registry.register(cell)
            try:
                k2 = registryp.register(nbr, component=k1)
                self.maze.link(cell, nbr)           # carve up
                self.increment_item("passages")
                self.increment_item("required carve upward")
                self.debug(5, f"required carve up {cell.index}--{nbr.index}")
                return                          # successful!
            except ComponentError:
                pass                            # need to merge
                    # forced merge
            k2 = registryp.component_for(nbr)
            registry.merge(k1, k2)
            self.debug(1, f"merged forced by carve up from {cell.index}")

        def maybe_carve_upward(self, registry, registryp, cell, nbr):
            """flip for carve from the given cell to the given neighbor"""
            if not self.__flip2.do(cell, nbr):
                return                          # tail, don't carve
            self.debug(5, f"optional carve up {cell.index}--{nbr.index}")
            self.maze.link(cell, nbr)
            self.increment_item("passages")
            self.increment_item("optional carve upward")
            k1 = registry.register(cell)
            registryp.register(nbr, component=k1)

                # Initialization and configuration

        def parse_args(self, onward:str=EAST, upward:str=NORTH,
                       flip1 = (coin_toss, (), {"bias":0.5}),
                       flip2 = (coin_toss, (), {"bias":1/3}),
                       required_choice = (select_pair, (), {}),
                       debug = 0, labels=False):
            """parse constructor arguments

            USAGE

                The first argument, the uncarved maze, is passed as the
                first argument to the constructor (__init__ in class
                Algorithm.Status).  Method parse_args is called by the
                constructor with any remaining arguments.

                The remaining arguments are processed here.

            KEYWORD ARGUMENTS

                onward - the onward compass direction

                upward - the upward direction direction

                flip1 - the coin toss handler for merging two adjacent cells
                    in the same row.  The default is a fair coin.

                flip2 - the coin toss handler for optional upward carving. The
                default is a head in 1 of 3 tosses, or equivalently 1:2 odds
                for head:tail.

                    The method handlers for flip1 and flip2.are provided with
                    two required arguments, namely the cells whose components
                    may be merged.  These, along with any optional arguments
                    and any keyword arguments except "bias", are ignored.

                required_choice - the handler for required upward carving.  The
                    method handler is provided a run consisting of (cell,nbr)
                    pairs with cell in the current row (or column, or more
                    generally: tier) and nbr its grid neighbor in the next tier.

                    The method handlers for flip1, flip2, and required choice
                    are triples (name, args, kwargs) consisting of:
                        name - a method name;
                        args - a tuple listing and additional named or
                            optional arguments;
                        kwargs - a dictionary which supplies keyword arguments.
                    The default method for flip1 and flip2 is the procedure
                    coin_toss defined immediately after the Eller module
                    docstring.  The default method for required_choice is
                    procedure select_pair defined after coin_toss.

                debug - display some informative messages indicating what
                    is going on.  If False or 0, no simply informative messages
                    are displayed.  If True or 1, messages tracking row state
                    are displayed.  Higher values will display additional
                    messages.  For example, a value of 5 will also trace merges
                    and a value of 10 will print all of the trace messages.

                    To suppress the warning messages as well as the informative
                    messages, use a value of -10.  The warnings detect
                    connectivity problems that can occur if the the grid is
                    configured in an unusual way or if some cells have been
                    masked.

                    (At this point in time, the author does not plan to use
                    Python's logging module for these messages.)

                labels - default is False; set to true for debugging
            """
            self.__debug = debug
            self.__onward = onward
            self.__upward = upward
            self.__flip1 = _MetaMethod(flip1[0], *flip1[1], **flip1[2])
            self.__flip2 = _MetaMethod(flip2[0], *flip2[1], **flip2[2])
            self.__select_upward = _MetaMethod(required_choice[0], \
                *required_choice[1], **required_choice[2])
            self.__labels = labels

        def initialize(self):
            """initialization"""
            self.make_row(self.__onward)
            self.make_rows(self.__upward)
            directions = (self.__onward, self.__upward)
            if directions not in self.VALID_DIRECTIONS:
                raise ValueError("directions are incompatible")

        def configure(self):
            """configuration"""
            self.more = True
            self.get_first_row()
            self.store_item("cells", len(self.maze.grid))
            self.store_item("passages", 0)
            self.store_item("optional merge left", 0)
            self.store_item("required merge left", 0)
            self.store_item("required carve upward", 0)
            self.store_item("optional carve upward", 0)
            self.store_item("onward", self.__onward)
            self.store_item("upward", self.__upward)

        def visit(self):
            """visit protocol"""
            self.get_next_row()
            self.access_current_row()                   # in-row actions
            self.complete_a_row(*self.__current_run)    # out-of-row actions
            if self.__labels:
                self.__relabel(*self.__current_run)

        def debug(self, level, *msg):
            """display a debugging message"""
            if level <= self.__debug:
                print(f"Eller.Status({int(level)}):", *msg)

        def __relabel(self, n, row, registry):
            """for debugging"""
            for cell in row:
                k = registry.register(cell)
                cell.label = chr(ord('A') + (k % 26))

# end module mazes.Algorithms.eller