"""
mazes.Graphics.oblong1 - a simple graphics driver for the oblong grid
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module mimics the string form for an oblong grid using matplotlib
    and the spider graphics driver.  It does not support one-way connections
    or insets. One class is defined:

        Pholcidae -- named after the family of daddy long-leg spiders.

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

from mazes.maze import Maze
from mazes.Graphics.matplot_driver import Spider

class Phocidae(Spider):
    """The daddy long legs of drivers

    The daddy long-legs spider has long somewhat clumsy legs.  This driver
    works well for mazes defined on oblong grids provided all passages are
    undirected and the only exits from a cell are to its north, south, east
    and west neighbors.  The passages are wide with no insets, perfect for
    the daddy long-legs to seek its prey.  Simplicity is the order of the
    day.
    """

    __slots__ = ("__maze", "__grid")

    def __init__(self, maze:Maze):
        """constructor"""
        super().__init__()
        self.__maze = maze
        self.__grid = maze.grid

    def setup(self, color='black', aspect='equal', display_axes=False):
        """setup for the plot"""
        self.color(color)
        if aspect:
            self.ax.set_aspect(aspect)
        if not display_axes:
            self.plt.axis('off')

    @property
    def maze(self):
        """returns the maze"""
        return self.__maze

    @maze.setter
    def maze(self, new_maze):
        """changes the maze"""
        self.__maze = new_maze
        self.__grid = new_maze.grid
        return self.__maze

    @property
    def grid(self):
        """returns the maze"""
        return self.__grid

    def draw_maze(self, origin=(0,0)):
        """draws the maze"""
        h, k = origin
        for cell in self.__grid:
            i, j = cell.index
            x, y = j+h, i+k
            self.goto(x+1, y)             # southeast corner
                    # from SE corner to NE corner
            if cell.is_linked(cell.east):
                self.goto(x+1, y+1)
            else:
                self.draw_segment(x+1, y+1)
                    # from NE corner to NW corner
            if cell.is_linked(cell.north):
                self.goto(x, y+1)
            else:
                self.draw_segment(x, y+1)

                # draw the south boundary
        for cell in self.__grid.row(0):
                    # from SW corner to SE corner
            if not cell.is_linked(cell.south):
                i, j = cell.index
                x, y = j+h, i+k
                self.goto(x, y)
                self.draw_segment(x+1, y)

                # draw the west boundary
        for cell in self.__grid.column(0):
                    # from SW corner to NW corner
            if not cell.is_linked(cell.west):
                i, j = cell.index
                x, y = j+h, i+k
                self.goto(x, y)
                self.draw_segment(x, y+1)

# end module mazes.Graphics.matplot_driver
