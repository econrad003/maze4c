"""
mazes.Grids.multilevel - implementation of multilevel grids
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A multilevel grid is a grid which contains several grids (called levels)
    and a set of elevators which pass between pairs of cells in different
    levels.

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
from mazes.cell import Cell
from mazes.grid import Grid

class MultilevelGrid(Grid):

    __slots__ = ("__grids", "__levels", "__elevators")

        # CONSTRUCTION AND INITIALIZATION

    def _parse_args(self, *grids):
        """argument parser for MultilevelGrid class"""
        self.__grids = grids
        self.__levels = dict()       # grid -> level
        self.__elevators = list()
        super()._parse_args()

    def _initialize(self):
        """initialization (adds the grids' cells)"""
        super()._initialize()
        for i in range(self.levels):
            grid = self.grid(i)
            self.__levels[grid] = i
            if not isinstance(grid, Grid):
                raise TypeError("each level must be an instance of class Grid")
            for cell in grid:
                self[cell] = cell

#    def _configure(self):
#        """configuration (stub)"""
#        pass

            # TOPOLOGY (NEIGHBORHOOD)

    @property
    def levels(self) -> int:
        """returns the number of levels"""
        return len(self.__grids)

    def grid(self, level:int) -> Grid:
        """returns the grid at the given level

        levels are 0, 1, 2, ... up to top or -1, -2, -3, ... down to bottom
        """
        return self.__grids[level]

    def level(self, grid:Grid) -> int:
        """returns a grid's level"""
        return self.__levels[grid]

    def _gv(self, cell:Cell) -> str:
        """graphviz representation of a cell"""
        index = cell.index
        level = self.level(cell.grid)
        return f'"{level}-{index}"'

    def _display_cells(self) -> str:
        """display the cells, cluster by cluster"""
        s = ""
        for grid in self.__grids:
            level = self.level(grid)
            s += f"  subgraph cluster_{i}"
            s += " {\n"
            for cell in grid:
                s += f'    {self._gv(cell)}\n'
            s += "}\n"
        return s

    def _get_joins(self):
        """get the passages for the maze"""
        joins = self._joins_from_maze()
        if isinstance(joins, set):
            return joins
        # print("getting joins")
        joins = set()
        for cell in self:
            for join in cell.joins:
                joins.add(join)
        # print(len(joins))
        return joins

    def _display_joins(self, joins) -> str:
        """build the passage display"""
        s = str()
        for join in joins:
            cells = join.cells
            if len(cells) == 1:
                cell1 = list(cells)[0]
                s += f'"{self._gv(cell1)}" -> "{self._gv(cell1)}" [dir="none"]\n'
            elif isinstance(cells, frozenset):
                cell1, cell2 = cells
                s += f'"{self._gv(cell1)}" -> "{self._gv(cell2)}" [dir="none"]\n'
            elif isinstance(cells, tuple):
                cell1, cell2 = cells
                s += f'"{self._gv(cell1)}" -> "{self._gv(cell2)}"\n'
            else:
                s += f"// unknown join type\n"
        return s

    @property
    def graphviz_dot(self) -> str:
        """return a simple graphviz representation"""
        s = "digraph D {\n"
        s += self._display_cells()
        joins = self._get_joins()
        s += self._display_joins(joins)
        s += "}"
        return s

    def make_elevator(self, cell1, cell2, upward:str="up", downward:str="down"):
        """creates an elevator"""
        if self[cell1] != cell1:
            raise ValueError("cell1 is not a member of the grid")
        grid1 = cell1.grid
        level1 = self.level(grid1)
        if self[cell2] != cell2:
            raise ValueError("cell2 is not a member of the grid")
        grid2 = cell2.grid
        level2 = self.level(grid2)
        if level1 >= level2:
            raise ValueError("cell1 must be at a lower level than cell2")
        if cell1[upward] != None:
            raise ValueError(f"cell1 already has {upward} neighbor")
        if cell2[downward] != None:
            raise ValueError(f"cell2 already has {downward} neighbor")
        n = len(self.__elevators)
        pair = (cell1, cell2)
        self.__elevators.append(pair)
        cell1[upward] = cell2
        cell2[downward] = cell1

    def elevator(self, k) -> tuple:
        """return the kth elevator as an ordered pair of cells"""
        return cell1, cell2

class MultistoryGrid(MultilevelGrid):
    """a multilevel grid with specific initialization requirements"""

    def __init__(self, stories:int, GridType:callable, *args, **kwargs):
        """constructor

        REQUIRED ARGUMENTS

            stories - the number of grids in the layout

            GridType - the type of grid to use

        OPTIONAL ARGUMENTS

            args - the arguments for the grid constructors

        KEYWORD ARGUMENTS

            kwargs - keyword arguments for the grid constructors

        EXAMPLE

            The following sequence initializes a multilevel maze
            consisting of four 13-row 21-column rectangular grids
            stacked vertically:

                stories = 4
                rows, cols = 13, 21
                from mazes.Grids.oblong import OblongGrid
                from mazes.Grids.multilevel import MultistoryGrid
                from mazes.Maze import Maze
                maze = Maze(MultistoryGrid(stories, OblongGrid, rows, cols))
                grid = maze.grid

            At this point, grid edges need to be established between
            the levels.  The following commands establish the following
            additional grid edges:

                1) "elevator shafts" in the southwest and northeast
                   corners that span all three levels;

                print("Create the main elevator shafts...")
                SW, NE = (0,0), (rows-1,cols-1)
                for index in {SW, NE}:
                    for floor in range(grid.levels - 1):
                        cell1 = grid.grids(floor)[index]
                        cell2 = grid.grids(floor + 1)[index]
                        grid.elevator(cell1, cell2)
                            # verification
                        assert cell1["up"] == cell2, f"{floor=}, {index=}"
                        assert cell2["down"] == cell1, f"{floor=}, {index=}"

                2) "freight elevator shafts" between the ground floor
                   and the first floor in the southeast and northwest
                   corners; and

                print("Create the freight elevator shafts...")
                SE, NW = (0,cols-1), (rows-1,0)
                for index in {(0,20), (12,0)}:
                    cell1 = grid.grids(0)[index]
                    cell2 = grid.grids(1)[index]
                    grid.elevator(cell1, cell2)
                            # verification
                    assert cell1["up"] == cell2, f"{floor=}, {index=}"
                    assert cell2["down"] == cell1, f"{floor=}, {index=}"
                
                3) an "express elevator shaft" in the center of the
                   the maze that connects the ground floor and the
                   top floor.

                print("Create the express elevator shaft...")
                index = (rows//2,cols//2)
                cell1 = grid.grids(0)[index]
                cell2 = grid.grids(-1)[index]
                maze.elevator(cell1, cell2)
                            # verification
                assert cell1["up"] == cell2, f"{floor=}, {index=}"
                assert cell2["down"] == cell1, f"{floor=}, {index=}"

            Check the number of cells:

                for floor in grid.levels:
                    assert len(grid.grids(floor)) == rows * cols
                assert len(grid) == stories * rows * cols
        """
        grids = list()
        for i in range(stories):
            grid = GridType(*args, **kwargs)
            grids.append(grid)
        super().__init__(*grids)

# end module mazes.Grids.multilevel
