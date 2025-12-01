"""
mazes.Mazes.multimaze - base class implementation for multiomazes
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A multimaze is (usually) an undirected graph which defines passages
    between cells.  A multimaze admits parallel passages.

    A pseudomultimaze is a multimaze in which loops are also permitted.

    The grid manages the cells, and the maze manages the passages.

    Loops must be enabled before they are admitted.  They may be admitted
    either when the pseudomaze is constructed, or conditionally, or when
    a loop is created.

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
from mazes.edge import Edge
from mazes.maze import Maze

DEFAULT = "default"

def make_Multimaze(MazeClass:"class"):
    """create a multimaze class"""
    if not issubclass(MazeClass, Maze):
        raise TypeError("MazeClass must be derived from class Maze")
    if hasattr(MazeClass, "make_loop"):
        raise AttributeError("MazeClass must not contain 'make_loop' attribute")

    class MultiMaze(MazeClass):
        """multimaze class - parallel passages are permitted

        Loops may also be permitted, but are prohibited by default.

        By default, loops are disabled.  They can be enabled when
        the class is instantiated, at any time during the life of the
        class, or on a link-by-link basis.  Loops can also be disabled.
        """

        slots = ("__enabled", "__loops")

        @property
        def loops_enabled(self) -> bool:
            """are loops enabled?"""
            return self.__enabled

        @loops_enabled.setter
        def loops_enabled(self, enable:bool):
            """enable or disable loops"""
            self.__enabled = enable

        @property
        def loops(self) -> int:
            """returns the number of loops"""
            return self.__loops

        def _parse_args(self, *args, enable_loops:bool=False, **kwargs):
            """argument parser for PseudoMaze class

            REQUIRED ARGUMENTS

                grid - the underlying grid

                *args - additional arguments required by Maze subclasses

            KEYWORD ARGUMENTS

                enable_loops (default: False)
                    allow loops if True.

            Keyword arguments must be passed using the keyword.
            """
            self.__loops = 0
            self.loops_enabled = bool(enable_loops)
            super()._parse_args(*args, **kwargs)        # pass to parent
            self.grid.parallels_disabled = False

        def link(self, cell1, cell2,
                 directed=False, label:str="", weight:'Number'=1,
                 no_loops:bool=DEFAULT) -> 'Join':
            """link two cells

            The value for no_loops should be "default", True or False:
                "default" - permit a loop if loops are enabled for the object
                True - permit a loop this time regardless of the object setting
                False - do not permit a loop this time regardless of the
                    object setting

            The default is the string "default".
            """
            if cell1 != cell2:
                return super().link(cell1, cell2, directed=directed,
                                label=label, weight=weight)
            enable = self.loops_enabled if no_loops == DEFAULT \
                else not bool(no_loops)
            if enable:
                return self.make_loop(cell1, label=label, weight=weight)
            raise ValueError("loops have not been enabled")

        def make_loop(self, cell, label:str="", weight:'Number'=1) -> 'Join':
            """create a loop regardless of the setting"""
            edge = Edge(self, cell, cell, no_loops=False, label=label,
                        weight=weight)
            self[edge.index] = edge
            self.__loops += 1
            return edge

        def unlink(self, join):
            """delete a join"""
            super().unlink(join)
            if len(list(join)):
                self.__loops -= 1

        def __str__(self):
            """string representation"""
            s = super().__str__()
            s += f"\n{self.__loops} loops"
            parallels = 0
            for cell in self.grid:
                for nbr in cell.passages:
                    if cell.tally_joins(nbr) > 1:
                        parallels += 1
            s += f"\n{parallels} sets of parallel passages"
            s += " (counted as directed)"
            return s

    return MultiMaze

Multimaze = make_Multimaze(Maze)
Multimaze.__name__ = "Multimaze"

# end module mazes.Mazes.multimaze
