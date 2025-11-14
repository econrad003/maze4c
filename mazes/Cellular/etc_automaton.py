"""
mazes.Cellular.etc_automaton - edge-toroidal-Conway CA maze generator
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The automata defined here are edge-based using a Von Neumann topology,
    i.e. each cell has 4 neighboring cells.  The automata use a toroidal grid
    which is at least as large as the maze being generated.  Conway-style
    birth and death rules are used.  Live grid edges inside the border of the
    torus correspond to passages in the target maze.

    Two grid-edge based cellular automata are defined here.  The basic one
    is class Automaton.  It defines a 7-grid edge neighborhood consisting of
    a grid edge and the six incident grid edges in the Von Neumann topology.

    Class Automaton2 differs from the base class by adding two additional
    grid edges to form a neighborhood of nine grid edges.  The only difference
    in implementation is the initialize() method.  The added grid edges are both
    incident to two cells incident to the central edge.

    See the respective initialize() method for a diagram of the automaton's
    neighborhoods.

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
from mazes import rng
from mazes.maze import Maze
from mazes.cell import Cell
from mazes.Grids.oblong import OblongGrid

class Automaton(object):
    """an edge-based toroidal automaton with Conway-style rules"""

    __slots__ = ("__ruleB", "__ruleD", "__generation", "__curr",
                 "__topology", "__rows", "__cols", "__border",
                 "__maze", "__grid")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, birth_rule:set, death_rule:set,
                 *args,                 # rows and columns
                 border:int=5, bias:float=0.1,
                 **kwargs):
        """constructor

        REQUIRED ARGUMENTS

            birth_rule, death_rule - sets of integers.

                The numbers in the birth rule are the numbers of neighboring
                live grid edges required for a dead grid edge to become alive.

                The numbers in the death rule are the numbers of neighboring
                live grid edges required for a live grid edge to stay alive.

            rows, cols - dimensions of the target maze.

        KEYWORD ARGUMENTS

            border - the number of extra cells in the automaton
            bias - the probability of a grid edge being alive in the first
                generation.  This is passed as an argument to
                Automaton.configure().
        """
        if border < 0:
            raise ValueError("The number of border cells cannot be negative")
        self.__ruleB = frozenset(birth_rule)
        self.__ruleD = frozenset(death_rule)
        self.__border = int(border)
        self.__topology = dict()
        self.parse_args(*args, **kwargs)
        self.initialize()
        self.configure(bias=bias)

    def parse_args(self, *args, **kwargs):
        """create the target maze"""
        self.__maze = self.new_maze(*args, **kwargs)
        self.__grid = self.maze.grid

    def new_maze(self, rows:int, cols:int):
        """target maze"""
        return Maze(OblongGrid(rows, cols))

    def initialize(self):
        """initialization

                             Neighborhoods of {A,B}
                +---+---+---+
                |   | 2 |   |                 +---+---+---+---+
                +---+   +---+                 |   | 6 | 1 |   |
                | 1   B   3 |                 +---+   +   +---+
                +---+ | +---+                 | 5   A - B   2 |
                | 6   A   4 |                 +---+   +   +---+
                +---+   +---+                 |   | 4 | 3 |   |
                |   | 5 |   |                 +---+---+---+---+
                +---+---+---+
                north edge from A             east edge from A

            The neighboring grid edges are:
                {B,1}, {B,2}, {B,3}, {A,4}, {A,5}, {A,6}

            The neighboring edges are the edges incident to {A,B}
        """
        rows = self.grid.m + self.border
        cols = self.grid.n + self.border
        _south = lambda x: ((x[0]-1)%rows, x[1])
        _east = lambda x: (x[0], (x[1]+1)%cols)
        _north = lambda x: ((x[0]+1)%rows, x[1])
        _west = lambda x: (x[0], (x[1]-1)%cols)
        edge = lambda u, v: frozenset([u, v])
        for i in range(rows):
            for j in range(cols):
                cell = (i, j)
                north = _north(cell)
                east = _east(cell)
                e1 = edge(cell, north)
                e2 = edge(cell, east)
                    # neighbors of e1
                e11 = edge(north, _west(north))
                e12 = edge(north, _north(north))
                e13 = edge(north, _east(north))
                e14 = e2
                e15 = edge(cell, _south(cell))
                e16 = edge(cell, _west(cell))
                self.topology[e1] = {e11, e12, e13, e14, e15, e16}
                    # possible additional neighbors of e1
                # e1W = edge(_west(cell), _west(north))
                # e1E = edge(_east(cell), _east(north))
                # self.__topology[e1] = {e11, e12, e13, e1E, e14, e15, e16, e1W}
                    # neighbors of e2
                e21 = edge(east, _north(east))
                e22 = edge(east, _east(east))
                e23 = edge(east, _south(east))
                e24 = e15
                e25 = e16
                e26 = e1
                self.topology[e2] = {e21, e22, e23, e24, e25, e26}
                    # possible additional neighbors of e2
                # e2S = edge(_south(cell), _south(east))
                # e2N = edge(_north(cell), _north(east))
                # self.__topology[e2] = {e21, e22, e23, e2S, e24, e25, e26, e2N}
                    # assertions to check that things make sense
                    #   FYI: These assertions will fail if the extended grid is
                    #       too small.
                assert len(self.topology[e1]) == 6
                assert len(self.topology[e2]) == 6

    def configure(self, bias:float):
        """configuration

        Creates the first generation.  We keep track of the live edges.
        """
        self.__generation = 0
        self.__curr = dict()
        for edge in self.topology:
            if rng.random() < bias:
                self.__curr[edge] = True
        self.configure_maze()

    def configure_maze(self):
        """based on the current state, modify the maze

        This is called when __curr is updated, namely after configure()
        and after next_generation().
        """
            # unlink dead edges
        joins = list(self.maze)
        for join in joins:
            cell1, cell2 = join
            index1, index2 = cell1.index, cell2.index
            edge = frozenset([index1, index2])
            if edge not in self.__curr:
                self.maze.unlink(join)

            # link live edges
        for edge in self.__curr:
            index1, index2 = edge
            cell1, cell2 = self.grid[index1], self.grid[index2]
            if cell1 in self.grid and cell2 in self.grid:
                if cell2 in cell1.neighbors:
                    if not cell1.is_linked(cell2):
                        self.maze.link(cell1, cell2)

    def next_generation(self, verbose:bool=True):
        """create the next generation

        A StopIteration exception is raised if the torus is empty.
        (This is not a generator.)

        A Warning exception is raised if the configuration does not change.
        """
        if self.__generation > 0:
            if len(self.__curr) == 0:
                raise StopIteration("All the grid edges are dead.")
        nextgen = dict()
        for edge in self.topology:
            nbrs = self.topology[edge]
            alive = 0
            for nbr in nbrs:
                if self.__curr.get(nbr):        # It's ALIVE!!!
                    alive += 1
            if self.__curr.get(edge):       # It's ALIVE!!!
                if alive in self.death_rule:
                    nextgen[edge] = True            # It SURVIVES!!!
            else:                           # It's DEAD!!!
                if alive in self.birth_rule:
                    nextgen[edge] = True            # The Phoenix RISES!!!
        if verbose:
            print(f"generation {self.__generation}:",
                  f"(automaton) {len(self.__curr)} alive;",
                  f"(maze) {len(self.maze)} passages.")
            if nextgen == self.__curr:
                print(f"generation {self.__generation}: stable configuration")
        if nextgen == self.__curr:
            raise Warning(f"generation {self.__generation}: stable configuration")
        self.__curr = nextgen
        self.__generation += 1
        self.configure_maze()

            # IMMUTABLE PROPERTIES

    @property
    def rows(self) -> int:
        """the number of rows (of vertices)"""
        return self.__rows

    @property
    def cols(self) -> int:
        """the number of rows (of vertices)"""
        return self.__columns

    @property
    def birth_rule(self) -> set:
        """returns the birth rule"""
        return self.__ruleB

    @property
    def death_rule(self) -> set:
        """returns the death rule"""
        return self.__ruleD

    @property
    def border(self) -> int:
        """return the width of the border"""
        return self.__border

    @property
    def topology(self) -> dict:
        """returns the automaton's cell to neighbor dictionary

        The topology dictionary maps a grid edge to its neighboring
        grid edges.  The endpoints are expressed as ordered pairs of
        indices.  The edges are immutable sets (type frozenset) containing
        two ordered pairs each.  In the base class, the initialize()
        method defines the neighboring edges as the six incident edges.

        This dictionary is set up in initialize().  It should never be
        modified by any method except initialize()!!!  Never!  Never ever!
        You have been warned!!!
        """
        return self.__topology

    @property
    def maze(self):
        """the maze being shaped by the automaton (target maze)"""
        return self.__maze

    @property
    def grid(self):
        """the grid being shaped by the automaton (target grid)"""
        return self.__grid

    @property
    def generation(self):
        """returns the number of generations since configuration"""
        return self.__generation

        # Other methods

    def alive(cell1:("index", Cell), cell2:("index", Cell)):
        """is the grid edge alive?"""
        if isinstance(cell1, Cell):
            cell1 = cell1.index
        if isinstance(cell2, Cell):
            cell2 = cell2.index
        edge = frozenset([cell1, cell2])        # pack the indices
        return edge in self.__curr

    def dead(cell1:("index", Cell), cell2:("index", Cell)):
        """is the grid edge dead?"""
        if isinstance(cell1, Cell):
            cell1 = cell1.index
        if isinstance(cell2, Cell):
            cell2 = cell2.index
        edge = frozenset([cell1, cell2])        # pack the indices
        return edge not in self.__curr

    def is_edge(cell1:("index", Cell), cell2:("index", Cell)):
        """is this a valid edge?"""
        if isinstance(cell1, Cell):
            cell1 = cell1.index
        if isinstance(cell2, Cell):
            cell2 = cell2.index
        edge = frozenset([cell1, cell2])        # pack the indices
        return edge not in self.__topology

class Automaton2(Automaton):
    """each grid edge has eight neighbors"""

    def initialize(self):
        """initialization

                             Neighborhoods of {A,B}

                +---+---+---+
                |   | 2 |   |                 +---+---+---+---+
                +---+   +---+                 |   | 6 = 1 |   |
                | 1   B   3 |                 +---+   +   +---+
                + | + | + | +                 | 5   A - B   2 |
                | 6   A   4 |                 +---+   +   +---+
                +---+   +---+                 |   | 4 = 3 |   |
                |   | 5 |   |                 +---+---+---+---+
                +---+---+---+
                north edge from A             east edge from A


            The neighboring grid edges are:
                {B,1}, {B,2}, {B,3}, {3,4}, {A,4}, {A,5}, {A,6}, {1,6}

            In addition to the incident edges in the base class, the edges
            between cells 1 and 6 and between cells 3 and 4 are included
            in the automaton.
        """
        rows = self.grid.m + self.border
        cols = self.grid.n + self.border
        _south = lambda x: ((x[0]-1)%rows, x[1])
        _east = lambda x: (x[0], (x[1]+1)%cols)
        _north = lambda x: ((x[0]+1)%rows, x[1])
        _west = lambda x: (x[0], (x[1]-1)%cols)
        edge = lambda u, v: frozenset([u, v])
        for i in range(rows):
            for j in range(cols):
                cell = (i, j)
                north = _north(cell)
                east = _east(cell)
                e1 = edge(cell, north)
                e2 = edge(cell, east)
                    # neighbors of e1
                e11 = edge(north, _west(north))
                e12 = edge(north, _north(north))
                e13 = edge(north, _east(north))
                e14 = e2
                e15 = edge(cell, _south(cell))
                e16 = edge(cell, _west(cell))
                # self.topology[e1] = {e11, e12, e13, e14, e15, e16}
                    # possible additional neighbors of e1
                e1W = edge(_west(cell), _west(north))
                e1E = edge(_east(cell), _east(north))
                self.topology[e1] = {e11, e12, e13, e1E, e14, e15, e16, e1W}
                    # neighbors of e2
                e21 = edge(east, _north(east))
                e22 = edge(east, _east(east))
                e23 = edge(east, _south(east))
                e24 = e15
                e25 = e16
                e26 = e1
                # self.topology[e2] = {e21, e22, e23, e24, e25, e26}
                    # possible additional neighbors of e2
                e2S = edge(_south(cell), _south(east))
                e2N = edge(_north(cell), _north(east))
                self.topology[e2] = {e21, e22, e23, e2S, e24, e25, e26, e2N}
                    # assertions to check that things make sense
                    #   FYI: These assertions will fail if the extended grid is
                    #       too small.
                assert len(self.topology[e1]) == 8
                assert len(self.topology[e2]) == 8

# end module mazes.Cellular.etc_automaton
