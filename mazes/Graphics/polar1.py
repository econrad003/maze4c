"""
mazes.Graphics.polar1 - a simple graphics driver for the theta grid
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module sketches a theta grid using matplotlib and the spider graphics
    driver.  It does not support one-way connections or insets. One class is
    defined:

        Phocidae -- named after the family of daddy long-leg spiders.

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
import numpy as np
from math import pi, ceil, sqrt

from mazes.maze import Maze
from mazes.Graphics.matplot_driver import Spider
from mazes.Grids.polar import xy

class Phocidae(Spider):
    """The daddy long legs of drivers

    The daddy long-legs spider has long somewhat clumsy legs.  This driver
    works well for mazes defined on oblong grids provided all passages are
    undirected and the only exits from a cell are to its north, south, east
    and west neighbors.  The passages are wide with no insets, perfect for
    the daddy long-legs to seek its prey.  Simplicity is the order of the
    day.

        *** This is a misspelling ***

    Apparently Phocidae is actually a family of seals.  Pholcidae is the
    family of spiders which includes the daddy long-legs.
    """

    __slots__ = ("__maze", "__grid", "__fill")

    def __init__(self, maze:Maze):
        """constructor"""
        super().__init__()
        self.__maze = maze
        self.__grid = maze.grid
        self.__fill = {}

    def setup(self, color='black', aspect='equal', display_axes=False,
              fillcolors=None):
        """setup for the plot"""
        self.color(color)
        if aspect:
            self.ax.set_aspect(aspect)
        if not display_axes:
            self.plt.axis('off')
        if fillcolors:                              # 23 Dec 2024
            if not isinstance(fillcolors, dict):
                raise TypeError("'fillcolors' must be a dictionary {cell:fill}")
            self.__fill = fillcolors

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

    def draw_maze(self):
        """draws the maze"""
        for cell in self.__fill:
            if cell not in self.__grid:
                continue
            self.fill(cell, self.__fill[cell])

        for cell in self.__grid:
            r0, theta0, theta1 = cell.r, cell.theta0, cell.theta1
            r1 = r0 + 1
            self.up()
                # draw inward wall, if any
            if cell.inward:
                if not cell.is_linked(cell.inward):
                    k = self.guesstimate(self.grid.n(r0), r0)
                    thetas = np.linspace(theta0, theta1, k, endpoint=True)
                    x, y = xy(r0, theta0)
                    self.goto(x, y)
                    for i in range(1, len(thetas)):
                        x, y = xy(r0, thetas[i])
                        self.draw_segment(x, y)
                # draw clockwise wall, if any
            if cell.clockwise:
                if not cell.is_linked(cell.clockwise):
                    r2 = r0 if r0>0 else 1/3
                    x, y = xy(r2, theta0)
                    self.goto(x, y)
                    x, y = xy(r1, theta0)
                    self.draw_segment(x, y)

                # draw the innermost boundary if any
        if self.grid.n(0) > 1:
            r = 1/3
            k = self.guesstimate(1/3, r)
            thetas = np.linspace(0, 2*pi, k, endpoint=True)
            self.up()
            x, y = xy(r, 0)
            self.goto(x, y)
            for i in range(1, len(thetas)):
                x, y = xy(r, thetas[i])
                self.draw_segment(x, y)

                # draw the outermost boundary
        r = self.grid.m
        k = self.guesstimate(1, r)
        thetas = np.linspace(0, 2*pi, k, endpoint=True)
        self.up()
        x, y = xy(r, 0)
        self.goto(x, y)
        for i in range(1, len(thetas)):
            x, y = xy(r, thetas[i])
            self.draw_segment(x, y)


    def annulus(self, r:int, color):
        """fill an annulus of radius with inner given radius"""
        if r == 0:
                    # single point at the pole
            if color:
                self.ax.add_artist(self.plt.Circle((0,0), 1, color=color))
            else:
                self.ax.add_artist(self.plt.Circle((0,0), 1))
            return

                # This will handle a single point in a given non-polar ring.
                #
                # This may qualify as an undesirable situation that should
                # raise an exception but I'm classifying it as merely weird.
                # With the base polar class, it can only happen when the
                # number of cells at the pole is 1 and the arc length for the
                # split is at least 2π.
        k = self.guesstimate(1, r)
        radii = (r, r+1)
        theta = np.linspace(0, 2*np.pi, k, endpoint=True)
        xs = np.outer(radii, np.cos(theta))
        ys = np.outer(radii, np.sin(theta))
            # the circles must be traversed in opposite directions
            #   See stackoverflow:Plot a donut with fill or fill_between
            #   Answer by Trenton McKinney
        xs[1,:] = xs[1,::-1]
        ys[1,:] = ys[1,::-1]
        if color:
            self.ax.fill(np.ravel(xs), np.ravel(ys), color=color)
        else:
            self.ax.fill(np.ravel(xs), np.ravel(ys))

    def polyfill(self, cell, n, r, color):
        """fill an annular wedge"""
        k = self.guesstimate(n, r+1)
        radii = (r, r+1) if r>0 else (1/3, 1)
        theta0, theta1 = cell.theta0, cell.theta1
        theta = np.linspace(theta0, theta1, k, endpoint=True)
        xs = np.outer(radii, np.cos(theta))
        ys = np.outer(radii, np.sin(theta))
            # the circles must be traversed in opposite directions
            #   See stackoverflow:Plot a donut with fill or fill_between
            #   Answer by Trenton McKinney
        xs[1,:] = xs[1,::-1]
        ys[1,:] = ys[1,::-1]
        self.fill_polygon(np.ravel(xs), np.ravel(ys), color=color)

                # fill a cell
    def fill(self, cell, color):
        """fill cell with color"""
        r = cell.r
        n = self.grid.n(r)
        if n == 1:
            self.annulus(r, color)
            return
        self.polyfill(cell, n, r, color)

    @staticmethod
    def guesstimate(n:int, r:int) -> int:
        """how many points in the interpolation?

        Depends on the magnification, so this is just a wild guess.
        """
        return max(5, int(25 * sqrt(r) / n))

# end module mazes.Graphics.polar1
