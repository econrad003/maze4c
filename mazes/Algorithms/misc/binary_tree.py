"""
mazes.Algorithms.misc.binary_tree - analogues of the simple binary tree algorithm
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module adapts the simple binary tree algorithm to a number of
    special grids.  Each adaptation is built in its own class and each
    is kept as simple as is reasonable.  To add features, try writing
    a subclass.

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

    The following classes are implemented here:

        CylinderMaze - create a simple binary tree on a cylinder maze.

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
from mazes import rng, Algorithm, Cell
from mazes.maze import Maze

class OneShot(object):
    """the base (stub)

    DESCRIPTION

        Two calls are required to carve a maze.  The constructor is
        called to create an object which contains the maze and,
        ultimately, the algorithm status.  Then the "on" method
        is called to run the algorithm and return the status.  The
        usage pattern is:

            obj = OneShot(GridClass, *args, **kwargs)  # create maze
            status = obj.on(status, *args, **kwargs)   # carve maze

        This class is a stub, so the real way to do this is to create
        a subclass which has its own __init__ method and supplies
        the correct grid class and parameters.  Here is a minimal
        nonworking implementation using a hypothethical grid class:

            class Subclass(OneShot):
                class Status(OneShot.Status):
                    pass        # modifications go here
                def __init__(self, *args, **kwargs):
                    from mazes.foobar import FooGrid
                    super().__init__(FooGrid, *args, **kwargs)

        The calling sequence becomes:

            obj = Subclass(*args, **kwargs)     # create FooGrid maze
            status = obj.on(*args, **kwargs)    # carve maze

        Calling the "on" method a second time will raise a RuntimeError
        exception.
    """

    __slots__ = ("__maze", "__status", "__once")

    class Status(Algorithm.Status):
        """Simple binary tree status(stub)

                    *** BRIEFLY, HOW TO USE THIS ***

        First, read the description in the OneShot class docstring.

        Most of the work is done here.  This should be subclassed to
        fine tune the algorithm.  The can_go_onward, can_go_upward, and
        parse_args methods will likely need to be overriden.

        The subclass should normally provide the correct onward and
        upward directions, and the correct bias using the
        super().parse_args method.  In more difficult cases, the
        onward, upward, and bias properties might need to be
        overridden.

        Any preprocessing can be done in initialize and configure
        methods.

        For an example, see the Cylinder class and the Cylinder.Status
        class below.
        """

        NAME = "Simple Binary Tree (stub)"

        __slots__ = ("__iter", "__onward", "__upward", "__bias")

        @property
        def onward(self) -> str:
            """onward getter"""
            return self.__onward

        @property
        def upward(self) -> str:
            """onward getter"""
            return self.__upward

        @property
        def bias(self) -> float:
            """bias getter"""
            return self.__bias

        def flip_head(self):
            """flip the coin"""
            return OneShot.flip(self.__bias)

        def link(self, cell, nbr):
            """carve a link"""
            self.increment_item("passages")
            self.maze.link(cell, nbr)

        def can_go_onward(self, cell:Cell) -> (Cell, None):
            """returns the upward neighbor unless the cell is blocked"""
            return cell[self.__onward]

        def can_go_upward(self, cell:Cell) -> (Cell, None):
            """returns the upward neighbor"""
            return cell[self.__upward]

        def visit_cell(self, cell:Cell):
            """visit a cell"""
            onward = self.can_go_onward(cell)
            upward = self.can_go_upward(cell)
            if onward:
                if upward:
                    if self.flip_head():
                        self.increment_item("heads")
                        self.link(cell, upward)
                    else:
                        self.increment_item("tails")
                        self.link(cell, onward)
                else:
                    self.link(cell, onward)
            elif upward:
                self.link(cell, upward)

        def visit(self):
            """visit or basic pass"""
            try:
                cell = next(self.__iter)
                self.visit_cell(cell)
            except StopIteration:
                self.more = False

        def parse_args(self, onward:str, upward:str, bias:float):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

                onward - the onward direction

                upward - the upward direction

                bias - the probability of a head in a coin toss
            """
            super().parse_args()              # chain to parent
            self.__onward = onward
            self.__upward = upward
            self.__bias = bias

        def configure(self):
            """configuration (minimal)"""
            self.store_item("cells", len(self.grid))
            self.store_item("passages", 0)
            self.store_item("heads", 0)
            self.store_item("tails", 0)
                # set up the iteration
            self.__iter = iter(self.grid)
            self.more = True

    @property
    def maze(self):
        """maze getter"""
        return self.__maze

    @property
    def status(self):
        """status getter"""
        return self.__status

    @property
    def already_carved(self) -> bool:
        """returns true if the maze has already been carved"""
        return self.__once

    @staticmethod
    def flip(bias:float) -> bool:
        """a simple coin flip

        ARGUMENTS

            bias - the probability for a head
        """
        return rng.random() < bias

    def __init__(self, GridClass:object, *args, **kwargs):
        """creates the maze object"""
        self.__maze = Maze(GridClass(*args, **kwargs))
        self.__status = None
        self.__once = False

    def on(self, *args, **kwargs):
        """carves the maze"""
        if self.__once:
            raise RuntimeError('This may not be run more than once')
        status = self.Status(self.maze, *args, **kwargs)
        self.__status = Algorithm.on(self.maze, status=status)
        self.__once = True
        return status

class Cylinder(OneShot):
    """carves a cylindrical maze using the simple binary tree algorithm

    DESCRIPTION

        If we naively use the simple binary tree algorithm on a
        cylindrical grid obtained by identifying a pair of opposite
        sides of a 4-connected rectangular grid, we will not
        produce a perfect maze.  The maze will necessarily contain
        a circuit, and it will not necessarily be connected.

        Suppose we identify the left and right edges of our fundamental
        rectangle and in carving, our carving choices are right and up.
        Then (1) in the top row, since we cannot carve upward and can
        always carve rightward, we will necessarily end up with a
        circuit in the top row.  This is enough to guarantee that the
        resulting maze is imperfect.  In particular, it cannot be a
        tree.  (2) In some other row, if for each cell, there is a
        chance that we might might carve rightward, then there is
        a chance that we might carve rightward in every cell in the
        row.  In addition to creating a circuit, as there is no
        way to reach the cells above from this row, the maze is
        disconnected.

        The fix for both problems is quite simple.  In each row, we
        must designate a cell where we cannot carve to the right.
        The designated cell in the top row is special, in that
        we can reach it from every cell by simply following a path
        using a mix of leftward and upward steps.

        If our cylinder was produced by identifying the top and bottom
        sides, then in each column, we require a barrier cell where we
        cannot carve upward.

    USAGE

        There are two steps.

            (1) Create the maze object:

                    cylinder = Cylinder(rows, cols, parity=False/True])

                The empty maze object will be:

                    cylinder.maze

            (2) Carve the maze:

                    cylinder.on([bias=0.5/BIAS, reverse=False/True])

                The carved maze is cylinder.maze.  The status object is
                returned and can be retrived separately as
                cylinder.status.
    """

    class Status(OneShot.Status):
        """the workhorse"""

        NAME = "Simple Binary Tree (Cylinder)"

        __slots__ = ("__iter", "__barriers")

        @property
        def barriers(self) -> frozenset:
            """barriers getter"""
            return self.__barriers

        def can_go_onward(self, cell:Cell) -> (Cell, None):
            """returns the onward neighbor unless the cell is blocked"""
            if cell in self.barriers:
                return None
            return cell[self.onward]

        def parse_args(self, bias:float=1/2, reverse:bool=False):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                bias - a coin flip probability for a head (default: 1/2)

                reverse - if False (default), the upward direction will
                    be either left or up.  If True, it will be either
                    right or down.  In either case, it will always be
                    towards an edge.
            """
            S, E, N, W = "south", "east", "north", "west"
            ways = dict()                   # parity, reverse -> directions
            ways[False, False] = (E, N)
            ways[False, True] = (E, S)
            ways[True, False] = (N, E)
            ways[True, True] = (N, W)
            parity = self.grid.parity
            onward, upward = ways[parity, reverse]
            super().parse_args(onward, upward, bias)    # chain to parent

        def initialize(self):
            """initialization

            Depending on the parity, we need to insure that there is a
            cell in each row (parity=False) or column (parity=True)
            where going "onward" is not permitted.
            """
            super().initialize()
            def select_by_row(grid, m, n):
                """select the barrier cells"""
                barriers = set()
                for i in range(m):
                    j = rng.randrange(n)
                    cell = grid[i, j]
                    barriers.add(cell)
                return barriers

            def select_by_column(grid, m, n):
                """select the barrier cells"""
                barriers = set()
                for j in range(n):
                    i = rng.randrange(m)
                    cell = grid[i, j]
                    barriers.add(cell)
                return barriers

            grid = self.grid
            rows, cols = grid.m, grid.n
            barriers = select_by_row(grid, rows, cols) \
                if self.onward == "east" \
                else select_by_column(grid, rows, cols)
            self.__barriers = frozenset(barriers)

        def configure(self):
            """configuration"""
            super().configure()
                # more statistics
            self.store_item("barriers", len(self.__barriers))

    def __init__(self, rows:int, cols:int, parity:bool=False):
        """creates the maze object"""
        from mazes.Grids.cylinder import CylinderGrid
        super().__init__(CylinderGrid, rows, cols, parity=parity)

class Torus1(OneShot):
    """carves a toroidal maze using the simple binary tree algorithm

    DESCRIPTION

        If we naively use the simple binary tree algorithm on a
        toroidal grid obtained by identifying a pair of opposite
        sides of a 4-connected rectangular grid, we will not
        produce a perfect maze.  The maze will necessarily contain
        a circuit, and it will not necessarily be connected.

        The problems occur both horizontally and vertically.  The
        fix is similar to the fix for the cylinder: barriers.

        We have two types of barriers.  One type blocks the onward
        direction.  A second type blocks the upward direction.
        The rules for barriers are as follows:

            1) each row contains exactly one type-1 barrier;
            2) each column contains exactly one type-2 barrier; and
            3) there is exactly one cell which contains both
               a type-1 and a type-2 barrier.

    USAGE

        There are two steps.

            (1) Create the maze object:

                    torus = Torus(rows, cols)

                The empty maze object will be:

                    torus.maze

            (2) Carve the maze:

                    torus.on([bias=0.5/BIAS])

                The carved maze is torus.maze.  The status object is
                returned and can be retrived separately as
                torus.status.
    """

    class Status(OneShot.Status):
        """the workhorse"""

        NAME = "Simple Binary Tree (Torus)"

        __slots__ = ("__iter", "__barriers1", "__barriers2", "__dijkstra")

        @property
        def type1_barriers(self) -> frozenset:
            """type 1 barriers getter"""
            return self.__barriers1

        @property
        def type2_barriers(self) -> frozenset:
            """type 2 barriers getter"""
            return self.__barriers2

        def can_go_onward(self, cell:Cell) -> (Cell, None):
            """returns the onward neighbor unless the cell is blocked"""
            if cell in self.type1_barriers:
                return None
            return cell[self.onward]

        def can_go_upward(self, cell:Cell) -> (Cell, None):
            """returns the upward neighbor unless the cell is blocked"""
            if cell in self.type2_barriers:
                return None
            return cell[self.upward]

        def parse_args(self, bias:float=1/2):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.

            KEYWORD ARGUMENTS

                bias - a coin flip probability for a head (default: 1/2)
            """
                # direction doesn't matter
            super().parse_args('east', 'north', bias)    # chain to parent

        def usage_warning(self):
            """a warning is required"""
            print("*** WARNING:  The maze that results might not be connected. ***")

        def initialize(self):
            """initialization

            We need to place the barriers.  This passes through each row
            once, and then through each cell once.
            """
            self.usage_warning()
            super().initialize()

            grid = self.maze.grid
            rows, cols = grid.m, grid.n

                # select the row barriers
            row_barriers = list()
            for i in range(rows):
                j = rng.randrange(cols)
                cell = grid[i, j]
                row_barriers.append(cell)
            self.__barriers1 = frozenset(row_barriers)

                # select the root cell
            root = rng.choice(row_barriers)
            h, k = root.index

                # select the column barriers
            col_barriers = list([root])
            for j in range(cols):
                if j == k:
                    continue        # this column contains the root
                choices = list()
                    # since this is not the column containing the root
                    # the cell in in the root row is available as as
                    # type-2 barrier...
                    # its safer to get a list and make a choice than to
                    # keep throwing away choices until one is available.
                for i in range(rows):
                    cell = grid[i, j]
                    if cell not in self.type1_barriers:
                        choices.append(cell)    # there will be at least one
                cell = rng.choice(choices)
                col_barriers.append(cell)
            self.__barriers2 = frozenset(col_barriers)

        def configure(self):
            """configuration"""
            super().configure()
                # more statistics
            self.store_item("row barriers", len(self.type1_barriers))
            self.store_item("column barriers", len(self.type2_barriers))
            both = self.type1_barriers.intersection(self.type2_barriers)
            self.store_item("root barriers", len(both))

    def __init__(self, rows:int, cols:int):
        """creates the maze object"""
        from mazes.Grids.torus import TorusGrid
        super().__init__(TorusGrid, rows, cols)

    @property
    def dijkstra(self):
        """getter for the Dijkstra distance object"""
        return self.__dijkstra

    def label_barriers(self):
        """label the barrier cells"""
        if not self.already_carved:
            raise ValueError("You first need to carve the maze.")
        b1 = self.status.type1_barriers     # row barriers
        b2 = self.status.type2_barriers     # column barriers
        both = b1.intersection(b2)          # two barriers, one cell
        for cell in b1.union(b2):         # all cells with barriers
            if cell in both:
                cell.label = "B"
            elif cell in b1:
                cell.label = "E"
            else:
                cell.label = "N"

    def verify(self):
        """check whether the maze was connected

        returns a cell, if any, which is not reachable from the root.
        """
        from mazes.Algorithms.dijkstra import Dijkstra
        if not self.already_carved:
            raise ValueError("You first need to carve the maze.")
        status = self.status
        meet = status.type1_barriers.intersection(status.type2_barriers)
        root = list(meet)[0]
        self.__dijkstra = Dijkstra(self.maze, root)
        grid = self.maze.grid
        for cell in grid:
            if self.__dijkstra.distance(cell) > len(grid):
                print("*** WARNING: the maze is disconnected. ***")
                return cell
        return None                

# end mazes.Algorithms.misc.binary_tree
