"""
mazes.grid - base class implementation for grids
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A grid is a directed graph which defines the neighborhoods of its cells.

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

MODIFICATION HISTORY

    29 November 2025 - add a flag which enables parallel passages.  Associated
        with this flag are a property and a setter.  Cells can check this flag
        before adding parallel edges.
    14 December 2025 - add property graphviz_dot.
"""

from mazes.cell import Cell
from mazes.maze import Maze

class Grid(object):

    CELL = Cell                             # default cell type

    __slots__ = ("__cells", "__fmt", "__cons", "__parallels_disabled")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, *args, **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override _parse_args,
            _initialize, or _configure.

            Most of the work in a grid should be done by configure.
        """
        self.__cells = dict()               # index : cell
        self.__fmt = dict()
        self.__cons = dict()                # save constructor information
        self.parallels_disabled = True
        self.__cons["cls"] = self.__class__.__name__
        self.__cons["args"] = args
        self.__cons["kwargs"] = kwargs
        self._parse_args(*args, **kwargs)           # pass remaining arguments
        self._initialize()
        self._configure()

    @property
    def _cons(self):
        """constructor information"""
        return self.__cons

    def _parse_args(self):
        """argument parser for Grid class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        pass

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """configuration (stub)"""
        pass

    def newcell(self, *args, **kwargs):
        """called by initialize to create cells"""
        return self.CELL(self, *args, **kwargs)

    @property
    def parallels_disabled(self) -> bool:
        """are parallel passages prohibited?"""
        return self.__parallels_disabled

    @parallels_disabled.setter
    def parallels_disabled(self, disable:bool):
        """enable or disanle parallel passages"""
        self.__parallels_disabled = bool(disable)

            # TOPOLOGY (NEIGHBORHOOD)

    def __getitem__(self, index:'hashable') -> 'Cell':
        """returns the cell with the given index, if any

        If the index is not present, the value None is returned.
        """
        return self.__cells.get(index, None)

    def __setitem__(self, index:'hashable', cell:'Cell'):
        """sets the cell in the given direction"""
        if cell == None:
            del self[index]
        else:
            self.__cells[index] = cell
        return cell

    def __delitem__(self, index):
        """removes the direction from the neighborhood"""
        del self.__cells[index]

    def __len__(self):
        """returns the number of cells"""
        return len(self.__cells)

    def __iter__(self):
        """visits the cells"""
        for cell in self.__cells.values():
            if not cell.hidden:
                yield cell

    def format(self, name):
        """return print formatting, if supported"""
        return self.__fmt.get(name, 0)

    def set_format(self, name, value):
        """set print formatting, if supported"""
        self.__fmt[name] = value

    def _joins_from_maze(self):
        """try to get the joins from the maze object"""
        maze = self.format("maze")
        if maze == 0 or not isinstance(maze, Maze) or maze.grid != self:
            return None
        return set(maze)

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
                s += f'"{cell1.index}" -> "{cell1.index}" [dir="none"]\n'
            elif isinstance(cells, frozenset):
                cell1, cell2 = cells
                s += f'"{cell1.index}" -> "{cell2.index}" [dir="none"]\n'
            elif isinstance(cells, tuple):
                cell1, cell2 = cells
                s += f'"{cell1.index}" -> "{cell2.index}"\n'
            else:
                s += f"// unknown join type\n"
        return s

    @property
    def graphviz_dot(self) -> str:
        """return a simple graphviz representation"""
        s = "digraph D {\n"
        joins = self._get_joins()
        s += self._display_joins(joins)
        s += "}"
        return s

    @property
    def indices(self):
        """visits the indices"""
        for index, cell in self.__cells.items():
            if not cell.hidden:
                yield index

    @property
    def _indices(self):
        """visits all the indices, including the hidden ones"""
        for index in self.__cells:
            yield index

    @property
    def cells(self):
        """visits the cells (same as __iter__)"""
        for cell in self.__cells.values():
            if not cell.hidden:
                yield cell

    @property
    def _cells(self):
        """visits all the cells, including the hidden ones"""
        for cell in self.__cells.values():
            yield cell

# end module mazes.grid
