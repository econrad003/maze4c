"""
mazes.Graphics.animation - an animation driver using Python turtle
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module is an inderface for producing simple animations of maze
    making algorithms that uses Python's turtle module.

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
from mazes.animated_maze import AnimatedMaze
from mazes.maze import Maze
from mazes.arc import Arc
from mazes.edge import Edge
from mazes.Grids.oblong import OblongGrid
import turtle

class Animation(object):
    """"""

    def __init__(self, *args, **kwargs):
        """constructor"""
        self.parse_args(*args, **kwargs)
        self.initialize()
        self.configure()

    def parse_args(self, maze:Maze, quiet:bool=False, speed:int=6):
        """validate the arguments

        REQUIRED ARGUMENTS

            maze - a maze object on a rectangular grid

        KEYWORD ARGUMENTS

            quiet - suppress the informational messages

            speed - the speed to use for the animation (default=6)
                0 - fastest
                1 - slowest
                3 - slow
                6 - normal
                10 - fastest
        """
        self.verbose = not quiet
        self.speed = speed
        if self.verbose:
            print("Verbose mode: hints will be displayed...")
        if not isinstance(maze, Maze):
            raise TypeError("The maze must be drived from class Maze")
        if not isinstance(maze.grid, OblongGrid):
            raise TypeError("The grid must be a rectangular grid")
        self._maze = maze                   # unwrapped
        self.grid = maze.grid
        self.spider = spider = turtle.Turtle()
        self.screen = spider.screen
                # spider operation
        self.pendown = spider.pendown
        self.penup = spider.penup
        self.goto = spider.goto
        self.pencolor = spider.pencolor
        self.pensize = spider.pensize
        self.fillcolor = spider.fillcolor
        self.begin_fill = spider.begin_fill
        self.end_fill = spider.end_fill

    def initialize(self):
        """initialization"""
        self.screen = self.spider.screen    # get the screen
        self.canvas = self.screen.getcanvas()

    def configure(self):
        """configure the window and draw the maze"""
        if self.verbose:
            print("Spider setup in progress. Please stand by...")
        self.maze = AnimatedMaze(self._maze)     # wrap the maze
        width, height = self.screen.screensize()
        # print(width, height)
        m, n = self.grid.m, self.grid.n
        relwidth = width / (n + 2)
        relheight = height / (m + 2)
        pixels = min(relwidth, relheight)
        xmax, ymax = width / pixels, height / pixels
        # print(pixels, xmax, ymax)
        self.set_window_coordinates(-1, -1, xmax, ymax)
        self.initial_maze()

            ### ADDITIONAL SETUP OPTIONS

    def set_window_size(self, width:int, height:int):
        """change the canvas dimensions"""
        self.screen.setup(width=width, height=height)
        self.configure()

    def set_window_coordinates(self, llx, lly, urx, ury):
        """set the coordinates for the bounding box"""
        self.screen.setworldcoordinates(llx, lly, urx, ury)

    def title(self, label):
        """set a title for the animation"""
        self.screen.title(label)

    def initial_maze(self):
        """draw the starting maze"""
        self.screen.clearscreen()
        self.spider.speed(0)                # fastest speed
        self.spider.hideturtle()            # even faster...
            # sketch the grid
        self.penup()
        color1, color2 = "black", "grey"
        self.pensize(2)                     # draw outline
        m, n = self.grid.m, self.grid.n
        self.point(0, 0, color2)            # this might not draw (turtle bug)
        self.point(0, 0, color2)            # this will draw
        self.point(n, 0, color2)
        self.point(n, m, color2)
        self.point(0, m, color2)
        self.pencolor(color1)
        self.polyline(0, 0, n, 0, n, m, 0, m, 0, 0)
        self.pencolor(color2)
        self.pensize(1)
        for i in range(1, m):               # grid rows
            # print(f"row {i}")
            self.draw_line(0, i, n, i)
        for j in range(1, n):               # grid columns
            # print(f"column {j}")
            self.draw_line(j, 0, j, m)
        errors = 0
        loops = 0
        self.__nodes = set()
        for join in self.maze:
            cells = list(join)
            if len(cells) == 1:
                self.draw_cell(cell, "red")
                self.__nodes.add(cell)
                loops += 1
            elif isinstance(join, Arc):
                cell1, cell2 = cells                    # 8 Nov 2025
                self.draw_arc(cell1, cell2)
                self.__nodes.add(cell1)
                self.__nodes.add(cell2)
            elif isinstance(join, Edge):
                cell1, cell2 = cells                    # 8 Nov 2025
                self.draw_edge(cell1, cell2)
                self.__nodes.add(cell1)
                self.__nodes.add(cell2)
            else:
                errors += 1
        self.spider.showturtle()            # slow down
        self.spider.speed(self.speed)       # animation speed
        self.__nodes = set()
        if self.verbose:
            print("Spider setup complete...")
            print("Run your algorithm using 'spider.maze'")
            print("Then run the animation: spider.animate()")
        if loops:
            print(f"{loops} loops detected -- node is colored red")
        if errors:
            raise TypeError(f"{errors} join errors ")

            # ANIMATION

    def animate(self, exitclick:bool=True):
        """run the animation"""
        for tracer in self.maze._trace:
            if tracer[0] == "link":
                self.animate_link(*tracer)
            elif tracer[0] == "unlink":
                self.animate_unlink(*tracer)
            elif tracer[0] == "visit":
                self.animate_visit(*tracer)
        if exitclick:
            self.screen.exitonclick()

    def animate_link(self, _, op2, *cells):
        """animate a link"""
        if op2 == "loop":
            self.draw_cell(cell, "red")
            return
        cell1, cell2 = cells
        if op2 == "arc":
            self.draw_arc(cell1, cell2, color="blue", nodecolor="blue")
        elif op2 == "edge":
            self.draw_edge(cell1, cell2, color="blue", nodecolor="blue")

    def animate_unlink(self, _, op2, *cells):
        """animate an unlink"""
        if op2 == "loop":
            self.draw_cell(cell, "red")
            return
        cell1, cell2 = cells
        if op2 == "arc":
            self.draw_arc(cell1, cell2, color="white", nodecolor="blue")
        elif op2 == "edge":
            self.draw_edge(cell1, cell2, color="white", nodecolor="blue")

    def animate_visit(self, _, op2, *args):
        """animate a visit"""
        if op2 == "cell":
            self.draw_cell(args[0], "cyan")         # the current cell
            self.draw_cell(args[1], "magenta")      # the previous cell
            return
        cells = list(args[0])
        if len(cells) == 1:                     # loop
            self.draw_cell(cells[0], "red")
            return
        cell1, cell2 = cells
        if op2 == "arc":
            self.draw_cell(cell1, "cyan")           # the source
            self.draw_cell(cell2, "magenta")        # the target
        elif op2 == "edge":
            self.draw_cell(cell1, "cyan")           # one end
            self.draw_cell(cell2, "cyan")           # the other end

            # DRAWING TOOLBOX

    def draw_line(self, x0, y0, x1, y1):
        """draw a line (assuming pen is in the up position)"""
        self.goto(x0, y0)
        self.pendown()
        self.goto(x1, y1)
        self.penup()

    def polyline(self, x0, y0, x1, y1, *args, fillcolor:str=None):
        """draw several lines (assuming pen is in the up position)"""
        if fillcolor:
            self.fillcolor(fillcolor)
            self.begin_fill()
        self.goto(x0, y0)
        self.pendown()
        self.goto(x1, y1)
        for n in range(0, len(args), 2):
            x1, y1 = args[n], args[n+1]
            self.goto(x1, y1)
        if fillcolor:
            if (x1, y1) != (x0, y0):
                self.goto(x0, y0)
            self.end_fill()
        self.penup()

    def draw_arc(self, cell1, cell2, color:str="black", size:int=3,
                 nodecolor:str="black"):
        """draw an arc"""
        i1, j1 = cell1.index
        i2, j2 = cell2.index
        x1, y1, x2, y2 = j1+0.5, i1+0.5, j2+0.5, i2+0.5
        x3, y3 = (4*x1+x2)/5, (4*y1+y2)/5               # 1/5 point
        x4, y4 = (7*x1+5*x2)/12, (7*y1+5*y2)/12         # 5/12 point
        self.pencolor(color)
        self.pensize(size)
        self.draw_line(x3, y3, x4, y4)
        if cell1 not in self.__nodes:
            self.draw_node(x1, y1, nodecolor)
        if cell2 not in self.__nodes:
            self.draw_node(x2, y2, nodecolor)

    def draw_edge(self, cell1, cell2, color:str="black", size:int=3,
                  nodecolor:str="black"):
        """draw an edge"""
        i1, j1 = cell1.index
        i2, j2 = cell2.index
        x1, y1, x2, y2 = j1+0.5, i1+0.5, j2+0.5, i2+0.5
        x3, y3 = (4*x1+x2)/5, (4*y1+y2)/5               # 1/5 point
        x4, y4 = (x1+4*x2)/5, (y1+4*y2)/5               # 4/5 point
        self.pencolor(color)
        self.pensize(size)
        self.draw_line(x3, y3, x4, y4)
        if cell1 not in self.__nodes:
            self.draw_node(x1, y1, nodecolor)
        if cell2 not in self.__nodes:
            self.draw_node(x2, y2, nodecolor)

    def draw_node(self, x1, y1, nodecolor):
        """draw a node"""
        self.pencolor(nodecolor)
        self.pensize(1)
        args = [x1-0.2, y1-0.2]
        args += [x1+0.2, y1-0.2]
        args += [x1+0.2, y1+0.2]
        args += [x1-0.2, y1+0.2]
        args += [x1-0.2, y1-0.2]
        self.polyline(*args, fillcolor=nodecolor)

    def draw_cell(self, cell, nodecolor):
        """draw a cell"""
        if cell:
            i, j = cell.index
            self.draw_node(j+0.5, i+0.5, nodecolor)

    def point(self, x1, y1, color):
        """draw a point"""
        self.goto(x1, y1)
        self.pendown()
        self.spider.dot(color)
        self.penup()

# end module mazes.Graphics.animation
