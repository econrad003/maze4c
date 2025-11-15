"""
mazes.Graphics.animation2 - another animation driver using Python turtle
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module is an inderface for producing simple animations of maze
    making algorithms that uses Python's turtle module.

    The animations here differ from those in the animation module in
    the following ways:
        1) only the links and unlinks are tracked
        2) only passages are animated 

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
from mazes.Graphics.animation import Animation

class SimpleAnimation(Animation):
    """a much simpler animation"""

    def parse_args(self, maze:"Maze", *args,
                   foreground:str="black", background:str="white",
                   pen_width:int=3, **kwargs):
        """validate the arguments

        REQUIRED ARGUMENTS

            maze - a maze object on a rectangular grid

        KEYWORD ARGUMENTS

            foreground - the foreground color, used for carving passages
            background - the background color, used for erasing passages
            pen_width - the width of the drawing pen

        Any other arguments are passed to the base class
        """
        super().parse_args(maze, *args, **kwargs)
        self.fgcolor = foreground
        self.bgcolor = background
        self.pen_width = pen_width

            ### ADDITIONAL SETUP OPTIONS

    def quick_draw(self):
        """a sketch of the initial maze"""
        self.__nodes = set()            # to avoid displaying cells twice
        for join in self.maze:
            cells = tuple(join)
            if len(cells) == 2:             # edges only; no arcs or loops
                self.draw_edge(*cells)

            # ANIMATION

    def animate_link(self, _1, _2, *cells):
        """animate a link"""
        if len(cells) == 2:
            self.draw_edge(*cells)

    def animate_unlink(self, _1, _2, *cells):
        """animate an unlink"""
        if len(cells) == 2:
            self.erase_edge(*cells)

    def animate_visit(self, *args):
        """animate a visit"""
        pass

            # DRAWING TOOLBOX

    @staticmethod
    def center(cell):
        """get cell graphics coordinates"""
        x, y = cell.index
        return x+0.5, y+0.5

    def erase_edge(self, cell1, cell2):
        """erase an edge"""
        x1, y1 = self.center(cell1)
        x2, y2 = self.center(cell2)
        x3, y3 = 0.8*x1+0.2*x2, 0.8*y1+0.2*y2
        x4, y4 = 0.8*x2+0.2*x1, 0.8*y2+0.2*y1
        self.pencolor(self.bgcolor)
        self.pensize(self.pen_width)
        self.draw_line(x3, y3, x4, y4)

    def draw_edge(self, cell1, cell2):
        """draw an edge"""
        x1, y1 = self.center(cell1)
        x2, y2 = self.center(cell2)
        self.pencolor(self.fgcolor)
        self.pensize(self.pen_width)
        self.draw_line(x1, y1, x2, y2)

# end module mazes.Graphics.animation2
