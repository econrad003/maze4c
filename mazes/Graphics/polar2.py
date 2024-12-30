"""
mazes.Graphics.polar2 - another simple graphics driver for the theta grid
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module plots the edges and arcs of a theta maze using matplotlib
    and the spider graphics driver.  It supports one-way and diagonal
    connections. Parallel edges are not supported.  In addition, edges and arcs
    between cells that are not geometrically one unit away orthogonally or
    diagonally will simply make a mess.  In particular, weaving and gluing are
    not supported.  The resulting maze has a weblike structure -- as with its
    oblong counterpart we call the class SpiderWeb.

    The idea is from a suggestion found on Jamis Buck's web blog.  In an
    article [1] on how to create Minecraft-like mazes, he begins the
    discussion with:

        Once you start playing with mazes, you soon discover that there are a
        lot of different ways to draw them. The easiest way is what I call a
        linewise rendering, and ...

    So this driver produces linewise mazes.  In mathematical terms, if the maze
    is undirected, with no loops and no parallel edges, then viewed as a simple
    graph, we are representing the graphic matroid.  If we try to sketch an
    empty maze using this driver, we just get a blank image.

REFERENCES

    [1] Jamis Buck.  "Mazes with Blockwise Geometry" in The Buckblog.  31
        October 2015.  Web. Accessed 30 November 2024.
        http://weblog.jamisbuck.org/2015/10/31/mazes-blockwise-geometry.html

    [2] Jamis Buck.  Mazes for Programmers.  2015, Pragmatic Bookshelf.

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

from mazes.arc import Arc
from mazes.edge import Edge
from mazes.maze import Maze
from mazes.Graphics.matplot_driver import Spider
from mazes.Grids.polar import xy

class SpiderWeb(Spider):
    """The spider web of drivers

    This driver draws edges as line segments and arcs as arrows.  It doesn't
    draw the cells.
    """

    __slots__ = ("__maze")

    def __init__(self, maze:Maze):
        """constructor"""
        super().__init__()
        self.__maze = maze

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
        return self.__maze

    def draw_join(self, join, h, k):
        """handles exceptional joins"""
        if isinstance(join, Edge):
            self.draw_edge(join, h, k)
        elif isinstance(join, Arc):
            self.draw_arc(join, h, k)
        else:
            self.draw_undefined_join(join, h,k)

    def get_location_of(self, cell, h, k):
        """get the coordinates for the cell's location"""
        if cell.pole:
            return (h, k)
        r = cell.r + 0.5
        theta = (cell.theta0 + cell.theta1) / 2
        u, v = xy(r, theta)                     # convert to Cartesian
        x, y = u+h, v+k                         # translation
        return x, y

    def draw_edge(self, join:Edge, h, k):
        """draws an undirected pairwise join (i.e. an edge)"""
        cell1, cell2 = join
        x1, y1 = self.get_location_of(cell1, h, k)
        x2, y2 = self.get_location_of(cell2, h, k)
        self.up()
        self.goto(x1, y1)
        self.draw_segment(x2, y2)

    def draw_arc(self, join:Edge, h, k):
        """draws an directed pairwise join (i.e. an arc)"""
        cell1, cell2 = join
        x1, y1 = self.get_location_of(cell1, h, k)
        x2, y2 = self.get_location_of(cell2, h, k)
        self.up()
        self.goto(x1, y1)
        self.draw_arrow(x2, y2)

    def draw_undefined_join(self, join, h, k):
        """undefined joins are ignored"""
        pass

    def draw_maze(self, origin=(0,0)):
        """draws the maze"""
        h, k = origin
        for join in self.__maze:
            self.draw_join(join, h, k)

# end module mazes.Graphics.polar2