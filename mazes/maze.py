"""
mazes.maze - base class implementation for mazes
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A maze is (usually) an undirected graph which defines passages between cells.
    The grid manages the cells, and the maze manages the passages.

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

    2 December 2024 - EC
        Added link_all and unlink_all methods.
"""

from mazes.arc import Arc
from mazes.edge import Edge

class Maze(object):

    __slots__ = ("__grid", "__joins")

        # CONSTRUCTION AND INITIALIZATION

    def __init__(self, grid:'Grid', *args, **kwargs):
        """constructor

        DESCRIPTION

            Don't override this constructor.  Instead, override _parse_args,
            _initialize, or _configure.
        """
        self.__grid = grid
        self.__joins = dict()               # frozenset : edge
        self._parse_args(*args, **kwargs)           # pass remaining arguments
        self._initialize()
        self._configure()

    def _parse_args(self):
        """argument parser for Maze class (stub)

        A TypeError exception is raised if there are any unprocessed arguments.
        """
        pass

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """configuration (stub)"""
        pass

    @property
    def grid(self):
        """returns the grid"""
        return self.__grid

    def __str__(self):
        """string representation"""
        return str(self.__grid)

    def __len__(self):
        """returns the number of edges and arcs"""
        return len(self.__joins)

            # TOPOLOGY (NEIGHBORHOOD)

    def __getitem__(self, pair:'hashable') -> 'Edge':
        """returns an cell with the given index ('pair'), if any.

        If the index is not present, the value None is returned.
        """
        return self.__joins.get(pair, None)

    def __setitem__(self, pair:'hashable', join:'Edge'):
        """sets the edge in the given pair"""
        if join == None:
            del self[pair]
        else:
            self.__joins[pair] = join
        return join

    def __delitem__(self, pair):
        """removes the index from the joins"""
        del self.__joins[pair]

    def __iter__(self):
        """visits the joins (edges or arcs)"""
        for join in self.__joins.values():
            if not join.hidden:
                yield join

    @property
    def pairs(self):
        """visits the indices"""
        for pair, join in self.__joins.items():
            if not join.hidden:
                yield pair

    @property
    def _pairs(self):
        """visits all the indices, including the hidden ones"""
        for pair in self.__joins:
            yield pair

    @property
    def joins(self):
        """visits the joins (edges/arcs, same as __iter__)"""
        for join in self.__joins.values():
            if not join.hidden:
                yield join

    @property
    def _joins(self):
        """visits all the joins, including the hidden ones"""
        for join in self.__cells.values():
            yield join

    def link(self, cell1, cell2,
             directed=False,
             label:str="", weight:'Number'=1) -> 'Join':
        """link two cells"""
        Join = Arc if directed else Edge
        join = Join(self, cell1, cell2, label=label, weight=weight)
        self[join.index] = join

    def unlink(self, join):
        """delete a join"""
        index = join.index
        del self[index]
        join.unlink()

    def link_all(self, label:str="link_all"):
        """creates a passage between every pair of unlinked neighbors"""
        for cell in self.grid:
            for nbr in cell.neighbors:
                if not cell.is_linked(nbr):
                    self.link(cell, nbr, label=label)

    def unlink_all(self):
        """removes every join"""
        joins = list(self)
        for join in joins:
            self.unlink(join)

# end module mazes.maze