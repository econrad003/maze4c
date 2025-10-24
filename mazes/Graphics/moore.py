"""
mazes.Graphics.oblong1 - a simple graphics driver for the oblong grid
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module mimics the string form for an oblong grid using matplotlib
    and the spider graphics driver.  It does not support one-way connections
    or insets. One class is defined:

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

MODIFICATIONS

    23 December 2024 - EC
        Added cell fill with color.
    28 December 2024 - EC
        Correct a typo in the docstring.
    23 Oct 2025 - EC
        correct name of fill routine
"""
from math import sqrt
from mazes.maze import Maze
from mazes.Graphics.matplot_driver import Spider

class Huntsman(Spider):
    """The huntsman spider of drivers

    The huntsman spider is much beloved in its native Australia as it
    eats household insect pests.  This driver works well for mazes defined
    on oblong grids provided all passages are undirected and the only exits
    are to the up-to-eight neighboring cells in the Moore neigborhood.
    """

    __sqrt2 = sqrt(2)
    __slots__ = ("__maze", "__grid", "__fill", "__octagon", "__doorways")

    def __init__(self, maze:Maze):
        """constructor"""
        super().__init__()
        self.__maze = maze
        self.__grid = maze.grid
        self.__fill = {}
        self.setup()

    def setup(self, color='black', aspect='equal', display_axes=False,
              fillcolors=None, inset1=1/9, inset2=1/3, door=5/12):
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
        self.octagon(inset1, inset2)
        self.doorways(inset1, inset2, door)

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

    def octagon(self, inset1, inset2):
        """compute the octagon offsets

        cell to be displayed in a bounding box ((x0,y0), (x0+1,y0+1))

            +------------+------------+------------+
            |                |    |                |
            |            *---*    *---*            |
            |                           * /        |
            |                              * /     |
            |                                 *    |
            +                                   *  +
            |                                   |  |
            |                                   *--|     East Neighbor
            |                                      |
            |                                   *--|
            |                                   |  |
            +                                   *  +
            |                                      |                          
            |                                   *  |
            |                                      |
            |                                      |
            |                                      |
            +------------+------------+------------+
            O                D    E   B         A  C

        inset1 is the distance between the boundary and the inner square
            inset1 = C-A
        inset2 is a distance between the boundary and a vertex
            inset2 = C-B
        door is the width of a passage
            door = C-E = D
        """
        assert 0 < inset1 < inset2 < 0.5
            # S - SE - E - NE - N - NW - W - SW
        dxs = [inset2, 1-inset2, 1-inset1, 1-inset1,
               1-inset2, inset2, inset1, inset1]
        dys = [inset1, inset1, inset2, 1-inset2,
              1-inset1, 1-inset1, 1-inset2, inset2]
        self.__octagon = dict()
        self.__octagon["S"] = ((dxs[0], dys[0]), (dxs[1], dys[1]))
        self.__octagon["SE"] = ((dxs[1], dys[1]), (dxs[2], dys[2]))
        self.__octagon["E"] = ((dxs[2], dys[2]), (dxs[3], dys[3]))
        self.__octagon["NE"] = ((dxs[3], dys[3]), (dxs[4], dys[4]))
        self.__octagon["NE1"] = self.__octagon["NE"]
        self.__octagon["NE2"] = self.__octagon["NE"]
        self.__octagon["N"] = ((dxs[4], dys[4]), (dxs[5], dys[5]))
        self.__octagon["NW"] = ((dxs[5], dys[5]), (dxs[6], dys[6]))
        self.__octagon["W"] = ((dxs[6], dys[6]), (dxs[7], dys[7]))
        self.__octagon["SW"] = ((dxs[7], dys[7]), (dxs[0], dys[0]))
        self.__octagon["SW1"] = self.__octagon["SW"]
        self.__octagon["SW2"] = self.__octagon["SW"]

    def doorways(self, inset1, inset2, door):
        """compute the doorway vertices"""
        assert 0 < inset1 < inset2 < 0.5
        assert inset2 < door < 0.5

        diag1 = (door-inset2) / Huntsman.__sqrt2
        diag2 = (0.5-door) / Huntsman.__sqrt2
        self.__doorways = dict()

        x0 = door
        x1 = 1-door
        self.__doorways["S"] = \
            ((x0, inset1), (x0, 0), (x1, 0), (x1, inset1))
        self.__doorways["N"] = \
            ((x1, 1-inset1), (x1, 1), (x0, 1), (x0, 1-inset1))

        y0 = door
        y1 = 1-door
        self.__doorways["E"] = \
            ((1-inset1, y0), (1, y0), (1, y1), (1-inset1, y1))
        self.__doorways["W"] = \
            ((inset1, y1), (0, y1), (0, y0), (inset1, y0))

            # y = -(x - u) + v
            # x = u + v if y = 0
        (x0, y0), (x1, y1) = self.__octagon["SE"]
        self.__doorways["SE"] = \
            ((x0+diag1, y0+diag1), (x0+y0+2*diag1, 0),
             (x1+y1-2*diag1, 0), (x1-diag1, y1-diag1))

            # y = (x - u) + v
            # x = u - v + 1 if y = 1
        (x0, y0), (x1, y1) = self.__octagon["NE"]
        self.__doorways["NE1"] = \
            ((x0-diag1, y0+diag1), (x0-y0-2*diag1+1, 1),
             (x1-y1+2*diag1+1, 1), (x1+diag1, y1-diag1))

            # y = -(x - u) + v
            # x = u + v - 1 if y = 1
        (x0, y0), (x1, y1) = self.__octagon["NW"]
        self.__doorways["NW"] = \
            ((x0-diag1, y0-diag1), (x0+y0-2*diag1-1, 1),
             (x1+y1+2*diag1-1, 1), (x1+diag1, y1+diag1))

            # y = (x - u) + v
            # x = u - v if y = 0
        (x0, y0), (x1, y1) = self.__octagon["SW"]
        self.__doorways["SW1"] = \
            ((x0+diag1, y0-diag1), (x0-y0+2*diag1, 0),
             (x1-y1-2*diag1, 0), (x1-diag1, y1+diag1))

                # door crossings
            # y = (x-u) + v             NE/SW
            # y = -(x-s) + t            NW/SE
            # (x-u) + v = -(x-s) + t
            # 2x = u + s + t - v

        u1, v1 = self.__doorways["NE1"][0]
        s1, t1 = self.__doorways["NW"][3]
        t1 += 1                             # 1 cell east
        x1 = (u1 + s1 + t1 - v1) / 2
        y1 = (x1 - u1) + v1
        u2, v2 = self.__doorways["NE1"][3]
        s2, t2 = self.__doorways["SE"][0]
        t2 += 1                             # 1 cell north
        x2 = (u2 + s2 + t2 - v2) / 2
        y2 = (x2 - u2) + v2
        self.__doorways["NE2"] = \
            ((u1, v1), (x1, y1),
             (x2, y2), (u2, v2))

        u1, v1 = self.__doorways["SW1"][0]
        s1, t1 = self.__doorways["SE"][3]
        s1 -= 1                             # 1 cell west
        x1 = (u1 + s1 + t1 - v1) / 2
        y1 = (x1 - u1) + v1
        u2, v2 = self.__doorways["SW1"][3]
        s2, t2 = self.__doorways["NW"][0]
        t2 -= 1                             # 1 cell south
        x2 = (u2 + s2 + t2 - v2) / 2
        y2 = (x2 - u2) + v2
        self.__doorways["SW2"] = \
            ((u1, v1), (x1, y1),
             (x2, y2), (u2, v2))

    def wall_or_door8(self, cell, nbr, direction, x, y):
        """draw the wall or the door"""
        (dx1, dy1) = self.__octagon[direction][1]
        if direction == "NE":
            direction2 = direction + "1"
            if cell.north and cell.east:
                if cell.north.is_linked(cell.east):
                        # crossing - weave under
                    direction2 = direction + "2"
        elif direction == "SW":
            direction2 = direction + "1"
            if cell.south and cell.west:
                if cell.south.is_linked(cell.west):
                        # crossing - weave under
                    direction2 = direction + "2"
        else:
            direction2 = direction
        x1, y1 = x+dx1, y+dy1
        if nbr and cell.is_linked(nbr):
                # we have a passage
            (dx2, dy2), (dx3, dy3), (dx4, dy4), (dx5, dy5) \
                = self.__doorways[direction2]
            x2, y2 = x+dx2, y+dy2
            self.draw_segment(x2, y2)       # right wall
            x3, y3 = x+dx3, y+dy3
            self.draw_segment(x3, y3)       # right arch
            x4, y4 = x+dx4, y+dy4
            self.goto(x4, y4)               # PASSAGE IS HERE!
            x5, y5 = x+dx5, y+dy5
            self.draw_segment(x5, y5)       # left arch
            # wall or left wall
        self.draw_segment(x1, y1)

    def draw_cell8(self, cell, x, y):
        """cell to be displayed in a bounding box ((x,y), (x+1,y+1))

            +------------+------------+------------+
            |                |    |                |
            |            *---*    *---*            |
            |                           * /        |
            |                              * /     |
            |                                 *    |
            +                                   *  +
            |                                   |  |
            |                                   *--|     East Neighbor
            |                                      |
            |                                   *--|
            |                                   |  |
            +                                   *  +
            |                                      |                          
            |                                   *  |
            |                                      |
            |                                      |
            |                |    |                |
            +------------+---+----+---+------------+
                             D    E   B         A  C

        inset1 is the distance between the boundary and the inner square
            inset1 = AC
        inset2 is a distance between the boundary and a vertex
            inset2 = BC
        door is the distance between the boundary and a passage
            door = EC
        """
            # the octagon, starting along the south wall
        (dx0, dy0) = self.__octagon["S"][0]
        x0, y0 = x+dx0, y+dy0
        self.goto(x0, y0)               # SW corner vertex

        self.wall_or_door8(cell, cell.south, "S", x, y)
        self.wall_or_door8(cell, cell.southeast, "SE", x, y)
        self.wall_or_door8(cell, cell.east, "E", x, y)
        self.wall_or_door8(cell, cell.northeast, "NE", x, y)
        self.wall_or_door8(cell, cell.north, "N", x, y)
        self.wall_or_door8(cell, cell.northwest, "NW", x, y)
        self.wall_or_door8(cell, cell.west, "W", x, y)
        self.wall_or_door8(cell, cell.southwest, "SW", x, y)

    def fill_cell8(self, cell, x, y, colour):
        """fill a cell"""
        xs = list()
        ys = list()
        for direction in ("S", "SE", "E", "NE", "N", "NW", "W", "SW"):
            dx, dy = self.__octagon[direction][0]
            xs.append(x+dx)
            ys.append(y+dy)
        self.fill_polygon(xs, ys, color=colour)

    def draw_maze(self, origin=(0,0)):
        """draws the maze"""
        h, k = origin
        for cell in self.__fill:                    # 23 Dec 2024
            if cell not in self.__grid:
                continue
            i, j = cell.index
            x, y = j+h, i+k
            self.fill_cell8(cell, x, y, self.__fill[cell])  # 23 Oct 2025

        for cell in self.__grid:
            i, j = cell.index
            x, y = j+h, i+k
            self.draw_cell8(cell, x, y)

# end module mazes.Graphics.moore
