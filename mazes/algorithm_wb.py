"""
mazes.algorithm_wb - base class implementation for wall-building algorithms
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is an adaptation of the Algorithms class to handle wall-building
    algorithms.  Basically it just prepares the grid by making all available
    connections.

IMPLEMENTATION

    Two classes are implemented here:

        AlgorithmWB - contains a single class method 'on', inherited from
            class Algorithm.

        AlgorithmWB.Status - methods are inherited from Algorithm.Status
            with one change:
                initialize - initializes the grid so that all possible
                    passages exist.

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
from mazes.algorithm import Algorithm

class AlgorithmWB(Algorithm):
    """wall-building maze generation algorithm (stub)"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "wall-building maze algorithm"

        __slots__ = tuple()         # don't store anything here!

        def initialize(self):
            """prepare the grid by linking adjacent cells

            If additional initialization is done, be sure to call
                    super().initialize()
            This should normally be the first statement in the override
            of the initialize call.
            """
            super().initialize()        # Algorithm.initialize(self)
            self["links"] = 0
            maze = self.maze
            grid = self.grid
            for cell in grid:
                for nbr in cell.neighbors:
                    if nbr in grid and not cell.is_linked(nbr):
                        maze.link(cell, nbr)
                        self["links"] += 1

# end module mazes.algorithm_wb
