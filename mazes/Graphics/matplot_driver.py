"""
mazes.Graphics.matplot_driver - a turtle graphics driver using matplotlib
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module is an inderface for producing simple turtle graphics using
    the matplotlib graphics library.  There is a single class defined here:

        Spider - logo-style turtle graphics (FYI: turtles are cool but
            I like spiders, and with mazes, a spider web is an appropriate
            analogy.)

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

import matplotlib.pyplot as plt
import numpy as np

class Spider(object):
    """"""

    __slots__ = ("__plt", "__fig", "__ax", "__x", "__y", "__pen", "__color")

    def __init__(self):
        """constructor"""
        self.__plt = plt
        self.__fig, self.__ax = plt.subplots()
        self.__x, self.__y = (0, 0)             # current position
        self.__pen = False                      # pen is in the up position
        self.__color = 'black'

    def title(self, label, loc="center", **kwargs):
        """set a title for the plot"""
        self.__ax.set_title(label, loc=loc, **kwargs)

    def up(self):
        """raise the pen"""
        self.__pen = False

    def down(self):
        """lower the pen

        This doesn't make a mark.  Moving the pen is required in order to
        draw.
        """
        self.__pen = True

    def color(self, new_color):
        """replace the pen"""
        self.__color = new_color

    @property
    def state(self) -> tuple:
        """returns the pen state

        The pen state is:
            (xy, down, color)
        where:
            xy = (x, y) -- the current location of the pen
            down -- True if the pen is prepared to draw (i.e. in the down
                position) and False if it is raised
            color -- the current pen color
        """
        return ((self.__x, self.__y), self.__pen, self.__color)

    @property
    def plt(self) -> 'plot':
        """access the pyplot object"""
        return self.__plt

    @property
    def fig(self) -> 'figure':
        """access the figure object"""
        return self.__fig

    @property
    def ax(self) -> 'axes':
        """access the axes object"""
        return self.__ax

    def goto(self, x, y, color=None, **kwargs):
        """move the pen to a new position

        If the pen is down, it will draw a line segment.  If color is not
        set, the current pen color will be used
        """
        if not color:
            color = self.__color
        if self.__pen:
            xs = (self.__x, x)
            ys = (self.__y, y)
            self.__ax.plot(xs, ys, color=color, **kwargs)
        self.__x, self.__y = x, y

    def draw_segment(self, x, y, color=None, **kwargs):
        """draw a line segment to the new position, then raise the pen"""
        self.down()
        self.goto(x, y, color, **kwargs)
        self.up()

    def save_image(self, filename="maze.png"):
        """save the plot to a file (e.g. maze.png)"""
        plt.savefig(filename)

    def show(self):
        """display the plot"""
        self.__plt.show()

# end module mazes.Graphics.matplot_driver
