"""
mazes.Graphics.dot.oblong1 - graphical representation of rectangular mazes
        using Graphviz (spartan)
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a very simple graphics interface using the graphviz "neato"
    engine.

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
from graphviz import Graph
from mazes.maze import Maze

class Plotter(object):
    """plot an undirected rectangular maze"""

    def __init__(self, maze:Maze, comment:str=None, edgewidth:int=5,
                 format:str="svg", shape:str="square"):
        """constructor"""
        self.maze = maze
        self.edgewidth = edgewidth
        self.format = format
        self.comment = comment if comment else (maze.grid.__class__.__name__)
        self.shape = shape
        self.initialize()
        self.configure()

    def initialize(self):
        """initialization"""
        self.dot = Graph(engine='neato', comment=self.comment,
                         format=self.format)
        self.nodes = dict()         # cell -> mode name
        for cell in self.maze.grid:
            i, j = cell.index
            nodename = f"N{i}_{j}"
            self.nodes[cell] = nodename

    def configure(self):
        """configuration"""
        for cell in self.maze.grid:
            node = self.nodes[cell]
            i, j = cell.index
            position = f"{j},{i}!"
            self.dot.node(node, pos=position, label="", shape=self.shape)
        for join in self.maze:
            cell1, cell2 = join
            node1, node2 = self.nodes[cell1], self.nodes[cell2]
            self.dot.edge(node1, node2, penwidth=str(self.edgewidth))

    def render(self, filename:str, cleanup:bool=True):
        """render to a file"""
        print("Output:", filename, f"({self.format})")
        self.dot.render(filename=filename, cleanup=cleanup)

    @property
    def source(self) -> str:
        """returns the source"""
        return self.dot.source

    def view(self, filename:str="output", cleanup:bool=True):
        """render and view"""
        print("Output:", filename, f"({self.format})")
        self.dot.view(filename=filename, cleanup=cleanup)

    def save(self, filename:str="output"):
        """save the source to output.gv"""
        pathname = filename + ".gv"
        print("Source:", pathname, "(engine: neato)")
        with open(pathname, "w") as fp:
            fp.write(self.source)
            fp.write("\n")
            fp.write("// Use the neato engine, for example:\n")
            fp.write(f"//    neato -Tsvg -O {pathname}\n")

# end mazes.Graphics.dot.oblong1
