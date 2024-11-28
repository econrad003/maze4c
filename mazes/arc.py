"""
mazes.arc - base class implementation for arcs
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An arc in a maze is a directed passage between two cells.

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

class Arc(object):
    """Directed passages in a maze (arcs in a directed graph)"""

    __slots__ = ("__maze", "__cells", "__label", "__weight")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, maze:'Maze', cell1:'Cell', cell2:'Cell', *args,
                 label=None, weight=1, **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override _parse_args,
            _initialize, or _configure.

        REQUIRED ARGUMENTS

            grid - a maze or other container

            cell1, cell2 - the cells being joined.  These must be distinct as
                loops are undirected.

        OPTIONAL ARGUMENTS

            label - a string or an integer.  This value can be changed.

            weight - a number (default=1).  This value can be changed
        """
        if cell1 == cell2:
            raise ValueError("directed loops (cell1==cell2) are not permitted")
        self.__maze = maze
        self.__cells = (cell1, cell2)
        self.__label = label
        self.__weight = weight
        self._parse_args(*args, **kwargs)           # pass remaining arguments
        self._initialize()
        self._configure()

    def _parse_args(self):
        """argument parser for Arc class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        pass

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """configuration (stub)"""
        cell1, cell2 = self.__cells
        cell1._link(self, cell2)

    def __delete__(self, instance):
        """unlink two joined cells"""
        cell1, cell2 = self.__cells
        cell1._unlink(self)

        # IDENTIFICATION AND GRID MANAGEMENT

    @property
    def maze(self):
        """return the owner of the arc"""
        return self.__maze

    @property
    def index(self) -> 'hashable':
        """return the index of the arc

        For an arc, this is the tuple for the cells.  Note that this
        precludes parallel arcs, but a return arc or an edge is permitted.
        (For parallel arcs, some other indexing scheme is required.)
        """
        return self.__cells

    @property
    def cells(self) -> tuple:
        """return the cells in the arc"""
        return self.__cells

    def __iter__(self):
        """generates the cells"""
        for cell in self.__cells:
            yield cell

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
    def weight(self):
        """returns the weight"""
        return self.__weight

    @weight.setter
    def weight(self, new_weight):
        """set the weight"""
        self.__weight = new_weight
        return new_weight

    @property
    def hidden(self):
        """determine whether the edge (or arc) is hidden"""
        for cell in self:
            if cell.hidden: return True
        return False

# end module mazes.arc
