"""
mazes.cell - base class implementation for cells
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The cells in a grid or a maze are the vertices in graph or, more generally,
    nodes in a network.

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

MODIFICATIONS

    1 December 2024 - EC
        Corrected unlink.
"""

class Cell(object):
    """the cells in a maze

    The cell in a maze are its vertices (graph) or nodes (digraph or network).
    """

    __slots__ = ("__grid", "__index", "__label", "__neighbors", "__passages",
                 "__hidden", "__linked")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, grid:'Grid', index:'hashable', *args,
                 label=None, **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override _parse_args,
            _initialize, or _configure.

        REQUIRED ARGUMENTS

            grid - a grid or other container

            index - for use by the grid

        OPTIONAL ARGUMENTS

            label - a string or an integer.  This can be changed.
        """
        self.__grid = grid
        self.__neighbors = dict()
        self.__passages = dict()
        self.__linked = dict()
        self.__index = index
        self.__label = label
        self.__hidden = False
        self._parse_args(*args, **kwargs)           # pass remaining arguments
        self._initialize()
        self._configure()

    def _parse_args(self):
        """argument parser for Cell class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        pass

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """configuration (stub)"""
        pass

        # IDENTIFICATION AND GRID MANAGEMENT

    @property
    def grid(self):
        """return the cell's owner"""
        return self.__grid

    @property
    def index(self):
        """return the cell's index"""
        return self.__index

    @property
    def label(self):
        """returns the label"""
        return self.__label

    @label.setter
    def label(self, new_label):
        """set the label"""
        self.__label = new_label
        return new_label

    @property
    def char(self) -> str:
        """returns the most significant character or digit"""
        label = self.__label
        if isinstance(label, str):
            if len(label) > 0:
                return label[0]
            else:
                return ' '
        if isinstance(label, bool):
            return 'T' if label else 'F'
        if isinstance(label, int):
            return str(label % 10)
        if label == None:
            return ' '
        return "X"                  # type not recognized

            # TOPOLOGY (NEIGHBORHOOD)

    def __getitem__(self, way:str) -> 'Cell':
        """returns the cell in the given direction, if any

        If the neighbor does not exist, the value None is returned.
        """
        return self.__neighbors.get(way, None)

    def __setitem__(self, way:str, cell:'Cell'):
        """sets the cell in the given direction"""
        if cell == None:
            del self[way]
        else:
            self.__neighbors[way] = cell
        return cell

    def __delitem__(self, way:str):
        """removes the direction from the neighborhood"""
        del self.__neighbors[way]

    @property
    def neighbors(self):
        """visits the neighbors"""
        for way, cell in self.__neighbors.items():
            if not cell.hidden:
                yield cell

    @property
    def ways(self):
        """visits the neighbors by direction"""
        for way, cell in self.__neighbors.items():
            if not cell.hidden:
                yield way

    @property
    def _neighbors(self):
        """visits all the neighbors, including the hidden ones"""
        for cell in self.__neighbors.values():
            yield cell

    @property
    def _ways(self):
        """visits all the neighbors by direction, including the hidden ones"""
        for way in self.__neighbors:
            yield way

            # MAZE (GRAPHIC PROPERTIES)

    def _link(self, join:'Edge', cell:'Cell'):
        """create an arc joining the cell

        This is called by Edge.configure -- there should be no need to call
        this directly.
        """
        self.__passages[join] = cell
        self.__linked[cell] = join

    def _unlink(self, join:'Edge'):
        """delete an arc joining the cell

        This is called by Edge.unlink -- there should be no need to call
        this directly.
        """
        cell = self.__passages[join]
        del self.__passages[join]
        del self.__linked[cell]

    def is_linked(self, cell:'Cell') -> bool:
        """is the cell linked?"""
        return cell in self.__linked

    def join_for(self, cell:'Cell') -> 'Edge':
        """return the edge or arc, if any"""
        return self.__linked.get(cell, None)

    def cell_for(self, join:'Edge') -> 'Cell':
        """return the joined cell"""
        return self.__passages.get(join, None)

    @property
    def passages(self):
        """visits the cells joined by passages"""
        for cell in self.__linked:
            if not cell.hidden:
                yield cell

    @property
    def joins(self):
        """visits the passages (by edge or arc)"""
        for join, cell in self.__passages.items():
            if not cell.hidden:
                yield join

    @property
    def _passages(self):
        """visits all the joined cells, including the hidden ones"""
        for cell in self.__linked:
            yield cell

    @property
    def _joins(self):
        """visits all the passages, including the hidden ones"""
        for join in self.__passages:
            yield join

        # HIDING (or CLOAKING or MASKING)

    def hide(self):
        """hide (or mask) the cell"""
        self.__hidden = True

    def reveal(self):
        """reveal (or unmask) the cell"""
        self.__hidden = False

    @property
    def hidden(self):
        """is the cell hiding"""
        return self.__hidden

# end module mazes.cell
