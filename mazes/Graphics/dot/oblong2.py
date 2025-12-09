"""
mazes.Graphics.dot.oblong2 - graphical representation of rectangular mazes
        using Graphviz (customizable)
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a graphics interface using the graphviz "neato" engine.  Unlike
    its predecessor (oblong1), it offers considerable support for
    customizing a sketch.

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
from mazes.arc import Arc
from mazes.Grids.projective import ProjectiveGrid

class Plotter(object):
    """plot an undirected rectangular maze"""

    def __init__(self, maze:Maze, comment:str=None, edgewidth:int=5,
                 format:str="svg", shape:str="square", tabs:str="circle",
                 tabsize:float=None,
                 cell_attrs:dict=dict(), join_attrs:dict=dict(),
                 labels:bool=False):
        """constructor

        POSITIONAL ARGUMENTS

            maze - a rectangular maze

        KEYWORD ARGUMENTS

            comment - a short descriptive comment for the graphviz source;
                the default is the name of the grid class.

            edgewidth (default: 5) - the penwidth for edges.

            format (default: "svg") - the image format to use.  Vector formats
                (like svg) generally work better than raster formats (like png,
                jpg or webp).

            shape (default: "square") - the shape to be used for cells

            tabs (default: "circle") - the shape to be used for tabs on grids
                like the toroidal grid, the cylindrical grid, the Moebius
                grid, the Klein grid, and the projective grid.  These tabs
                are for passages which leave one side of the fundamental
                rectangle and return through another.

            tabsize (default: None) - the minimum width of a tab in inches.  The
                graphviz default is 3/4 of an inch.  Values between 1/100 and 3/4,
                inclusive, are permitted.

            cell_attrs - a dictionary which maps a cell to a dictionary
                of attributes which supplement or override the default
                cell attributes.

            join_attrs - a dictionary which maps a passage  to a dictionary
                of attributes which supplement or override the default
                passage attributes.

            labels - if set to True, use the cell labels as labels in the image

        ATTRIBUTE OVERRIDE EXAMPLE

            Suppose we have a Maze object named "maze" and we want to
            display the cells at (0,0) and (5,4) as circles instead of
            squares.  In addition, we want to label the (0,0) cell with
            the label "SW".  We can construct a cell attribute dictionary
            as follows:

                cell_attrs = dict()
                cell_attrs[maze.grid[0,0]] = {"shape":"circle", "label":"SW"}
                cell_attrs[maze.grid[5,4]] = {"shape":"circle"}

            Note that the graphviz package requires that both elements
            of the colon-separated pair must be strings.

            In the graphviz source language, the defaults look like
            this:

                N0_0 [label="" pos="0,0!" shape=square]
                N5_4 [label="" pos="5,4!" shape=square]

            After combining he overrides, the graphviz node are:

                N0_0 [label="SW" pos="0,0!" shape=circle]
                N5_4 [label="" pos="5,4!" shape=circle]

        """
        self.maze = maze
        self.edgewidth = edgewidth
        self.format = format
        self.comment = comment if comment else (maze.grid.__class__.__name__)
        self.shape = shape
        self.tabs = tabs
        self.tabsize = str(tabsize) \
            if isinstance(tabsize, float) and 0 < tabsize < 1 \
            else ""
        self.cell_attrs = cell_attrs
        self.join_attrs = join_attrs
        self.labels = bool(labels)
        self.extra_nodes = 0
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
            kwargs = {"pos":position, "label":"", "shape":self.shape}
            kwargs |= self.cell_attrs.get(cell, dict())
            if self.labels and cell.label and cell.label != " ":
                kwargs |= {"label":str(cell.label)}
            self.dot.node(node, **kwargs)
        for join in self.maze:
            if len(set(join)) == 1:
                self.loop_join(join)
            else:
                if self.is_exterior_join(join):
                    self.exterior_join(join)
                else:
                    self.interior_join(join)

    def loop_join(self, join):
        """loop"""
        cell = list(join)[0]
        node = self.nodes[cell]
        kwargs = {"penwidth":str(self.edgewidth)}
        kwargs |= self.join_attrs.get(join, dict())
        self.dot.edge(node, node, **kwargs)

    def is_exterior_join(self, join):
        """is this an exterior join?"""
        m, n = self.maze.grid.m, self.maze.grid.n
        cell1, cell2 = join
        i1, j1 = cell1.index
        if 0 < i1 < m - 1 and 0 < j1 < n - 1:
            return False
        i2, j2 = cell2.index
        if 0 < i2 < m - 1 and 0 < j2 < n - 1:
            return False
        return max(abs(i1-i2), abs(j1-j2)) > 1

    def exterior_join(self, join):
        """configure an exterior passage"""
        m, n = self.maze.grid.m, self.maze.grid.n
        cell1, cell2 = join
        node1, node2 = self.nodes[cell1], self.nodes[cell2]
        i1, j1 = cell1.index
        i2, j2 = cell2.index
                # row matching
        if i1==m-1 and i2==0:
            i3, i4 = m, -1
        elif i1==0 and i2==m-1:
            i3, i4 = -1, m
        else:
            i3, i4 = i1, i2
                # column matching
        if j1==n-1 and j2==0:
            j3, j4 = n, -1
        elif j1==0 and j2==n-1:
            j3, j4 = -1, n
        else:
            j3, j4 = j1, j2
                # projective plane special cases
        if isinstance(self.maze.grid, ProjectiveGrid):
            if (i1, j1) == (m-1, 1) and (i2, j2) == (0, n-1):
                i3, j3, i4, j4 = m, 0, 0, n
            if (i1, j1) == (m-1, n-2) and (i2, j2) == (0, 0):
                i3, j3, i4, j4 = m, n-1, 0, -1
            if (i1, j1) == (m-2, 0) and (i2, j2) == (0, n-1):
                i3, j3, i4, j4 = m-1, 0, -1, n-1
            if (i1, j1) == (m-2, n-1) and (i2, j2) == (0, 0):
                i3, j3, i4, j4 = m-1, n-1, -1, 0
                        # --- reversed
            if (i2, j2) == (m-1, 1) and (i1, j1) == (0, n-1):
                i4, j4, i3, j3 = m, 0, 0, n
            if (i2, j2) == (m-1, n-2) and (i1, j1) == (0, 0):
                i4, j4, i3, j3 = m, n-1, 0, -1
            if (i2, j2) == (m-2, 0) and (i1, j1) == (0, n-1):
                i4, j4, i3, j3 = m-1, 0, -1, n-1
            if (i2, j2) == (m-2, n-1) and (i1, j1) == (0, 0):
                i4, j4, i3, j3 = m-1, n-1, -1, 0

                # extra node A
        xtra = self.extra_nodes
        self.extra_nodes += 1
        cell3 = (i3, j3)            # row, column
        if cell3 in self.nodes:
            node3 = self.nodes[cell3]
        else:
            node3 = f"A{xtra}"
            self.nodes[cell3] = node3
            position = f"{j3},{i3}!"
            kwargs = {"pos":position, "label":str(xtra), "shape":self.tabs}
            if self.tabsize:
                kwargs["width"] = self.tabsize
                kwargs["fixedsize"] = "true"
            self.dot.node(node3, **kwargs)
                # extra node B
        cell4 = (i4, j4)            # row, column
        if cell4 in self.nodes:
            node4 = self.nodes[cell4]
        else:
            node4 = f"B{xtra}"
            self.nodes[cell4] = node4
            position = f"{j4},{i4}!"
            kwargs = {"pos":position, "label":str(xtra), "shape":self.tabs}
            if self.tabsize:
                kwargs["width"] = self.tabsize
                kwargs["fixedsize"] = "true"
            self.dot.node(node4, **kwargs)
                # join the exterior nodes
        kwargs = {"penwidth":str(max(round(self.edgewidth/2), 1))}
        kwargs |= self.join_attrs.get(join, dict())
        if isinstance(join, Arc):
            kwargs |= {"dir":"forward"}
        self.dot.edge(node1, node3, **kwargs)
        self.dot.edge(node4, node2, **kwargs)

    def interior_join(self, join):
        """configure an interior passage"""
        cell1, cell2 = join
        node1, node2 = self.nodes[cell1], self.nodes[cell2]
        kwargs = {"penwidth":str(self.edgewidth)}
        kwargs |= self.join_attrs.get(join, dict())
        if isinstance(join, Arc):
            kwargs |= {"dir":"forward"}
        self.dot.edge(node1, node2, **kwargs)

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

# end mazes.Graphics.dot.oblong2
