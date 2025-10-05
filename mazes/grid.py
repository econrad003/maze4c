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
"""

from mazes.cell import Cell

class Grid(object):

    CELL = Cell                             # default cell type

    __slots__ = ("__cells", "__fmt", "__cons")

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
