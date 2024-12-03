"""
mazes.edge - base class implementation for edges
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An edge in a maze is an undirected passage between two cells.

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
        added unlink method, removed __delete__.
"""

class Edge(object):
    """Bidirectional (aka: undirected) passages in a maze

    If a maze has no one-way passages, then it is a graph -- its cells are its
    vertices and its passages are its edges.
    """

    __slots__ = ("__maze", "__cells", "__label", "__weight")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, maze:'Maze', cell1:'Cell', cell2:'Cell', *args,
                 label=None, weight=1, no_loops=True, **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override _parse_args,
            _initialize, or _configure.

        REQUIRED ARGUMENTS

            grid - a maze or other container

            cell1, cell2 - the cells being joined

        OPTIONAL ARGUMENTS

            label - a string or an integer.  This value can be changed.

            weight - a number (default=1).  This value can be changed

            no_loops - a boolean (default=True).  If False, loops are
                admissible.  If True, a loop will raise a ValueError exception.
                (A loop is an edge which joins a cell to itself.)
        """
        if cell1 == cell2 and no_loops:
            raise ValueError("loops (cell1==cell2) are not admissible")
        self.__maze = maze
        self.__cells = frozenset((cell1, cell2))
        self.__label = label
        self.__weight = weight
        self._parse_args(*args, **kwargs)           # pass remaining arguments
        self._initialize()
        self._configure()

    def _parse_args(self):
        """argument parser for Edge class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        pass

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """configuration (stub)"""
        cells = list(self.__cells)
        if len(cells) == 1:                         # loop
            cells[0]._link(self, cells[0])
        else:                                       # ordinary edge
            cell1, cell2 = cells
            cell1._link(self, cell2)
            cell2._link(self, cell1)

    def unlink(self):
        """unlink two joined cells"""
        cells = list(self.__cells)
        for cell in cells:
            cell._unlink(self)

        # IDENTIFICATION AND GRID MANAGEMENT

    @property
    def maze(self):
        """return the owner of the edge"""
        return self.__maze

    @property
    def index(self) -> 'hashable':
        """return the index of the edge

        For an edge, this is the frozenset for the cells.  Note that this
        precludes parallel edges.  (For parallel edges, some other indexing
        scheme is required.)
        """
        return self.__cells

    @property
    def cells(self) -> frozenset:
        """return the cells in the edge"""
        return self.__cells

    def __iter__(self):
        """generates the cells

        If the edge is a loop, the generator yields just one cell
        """
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

# end module mazes.edge