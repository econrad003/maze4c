"""
mazes.animated_maze - Maze class wrapper
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    An animated maze is essentially a maze combined with a list of
    actions which trace the construction of the maze.  It is a wrapper
    for the maze class and works using four methods:

        link
        unlink
        visit_cell
        visit_join

    These methods are logged and then passed on to the wrapped maze
    object.  The actual animation must be written separately.

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
from mazes.arc import Arc
from mazes.edge import Edge
from mazes.maze import Maze

_LINK = "link"
_UNLINK = "unlink"
_VISIT = "visit"

_ARC = "arc"
_EDGE = "edge"
_JOIN = "join"
_CELL = "cell"
_LOOP = "loop"

class AnimatedMaze(Maze):
    """animation maze wrapper class"""

    slots = ("__maze", "__trace")

    def __init__(self, maze:Maze, *args, **kwargs):
        """constructor"""
        super().__init__(maze.grid, *args, **kwargs)
        self.__maze = maze
        self.__trace = list()

            # PROPERTIES

    @property
    def grid(self):
        """returns the grid"""
        return self.__maze.grid

            # DUNDER MAGIC METHODS

    def __len__(self):
        """returns the number of edges and arcs"""
        return len(self.maze)

    def __getitem__(self, pair:'hashable') -> 'Edge':
        """returns an cell with the given index ('pair'), if any.

        If the index is not present, the value None is returned.
        """
        return self.__maze[pair]

    def __setitem__(self, pair:'hashable', join:'Edge'):
        """Not recommended!"""
        if join == None:
            del self[pair]
        else:
            self.link(pair)
        return self[pair]

    def __delitem__(self, pair:'hashable'):
        """Not recommended!"""
        self.unlink(self[pair])

    def __iter__(self):
        """visits the joins (edges or arcs)"""
        for join in self.__maze.joins:
             yield join

            # OTHER INHERITED METHODS

    @property
    def pairs(self):
        """visits the indices"""
        for pair in self.__maze.pairs:
             yield pair

    @property
    def _pairs(self):
        """visits all the indices, including the hidden ones"""
        for pair in self.__maze._pairs:
            yield pair

    @property
    def joins(self):
        """visits the joins (edges/arcs, same as __iter__)"""
        for join in self.__maze.joins:
            yield join

    @property
    def _joins(self):
        """visits all the joins, including the hidden ones"""
        for join in self.__maze._joins:
            yield join

            # ANIMATION SUPPORT

    @property
    def _trace(self):
        """returns the trace"""
        return self.__trace

    @_trace.setter
    def _trace(self, packet:tuple):
        """adds a packet to the trace"""
        self.__trace.append(packet)

    def _unpack_join(self, join:(Edge, Arc)):
        """unpack a join"""
        if isinstance(join, Arc):
            op = _ARC
        elif isinstance(join, Edge):
            op = _EDGE
        else:
            op = _JOIN
        cells = tuple(join)
        if len(cells) == 1:
            op = _LOOP
        return (op, *cells)

    def link(self, *args, **kwargs):
        """link two cells"""
        join = self.__maze.link(*args, **kwargs)
        args = self._unpack_join(join)
        packet = (_LINK, *args)
        self.__trace.append(packet)
        return join

    def unlink(self, join:(Edge, Arc)):
        """unlink two cells"""
        args = self._unpack_join(join)
        packet = (_UNLINK, *args)
        self.__trace.append(packet)
        self.__maze.unlink(join)

    def visit_cell(self, curr:Cell, prev:Cell=None):
        """visit a cell"""
        packet = (_VISIT, _CELL, curr, prev)
        self.__trace.append(packet)
        self.__maze.visit_cell(curr, prev)

    def visit_join(self, join:(Edge, Arc)):
        """visit a join"""
        args = self._unpack_join(join)
        packet = (_VISIT, *args)
        self.__trace.append(packet)
        self.__maze.visit_join(curr, prev)

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

# end module mazes.animated_maze
