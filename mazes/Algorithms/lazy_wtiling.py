"""
mazes.Algorithms.lazy_wtileing - easy tiling with Wang tiles
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A Wang tile is a single cells in a maze with exits that have
    assiged colors.

    For example if our cell is a typical square cell, and our color
    set is cyan, magenta, yellow and black (=key), then we might have
    a tile that takes the form:

            M       Legend:
          +---+        C-cyan     Y-yellow
        Y |   | C      M-magenta  K-black
          +---+
            K

TILE PLACEMENT

    The rules for placement:
        1) a tile can be dropped next to a cell if and only if either:
           a) the shared edge is the same color; or
           b) at least one part of the shared edge is uncolored.
        2) Rotations and reflections may be allowed.

    In this particular tile placement, randomly generated tiles are placed
    in the "even" cells of a rectangular grid, i.e. the cells whose
    indices sum to an even number.

    Compatible tiles are place in the odd cells once the eve tiles have
    been placed.

    The color of a grid edge determines its priority.  A maze can then
    be carved using either Kruskal's algorithm or Prim's algorithm.

REFERENCES

    [1] Ian Stewart.  Reaching for the extreme.  Princeton (New Jersey, 2026).
        ISBN 978-0-691-26899-6.  Book.  pp 43-44.

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
import mazes
from mazes import rng, Cell, Algorithm
from mazes.tetris.wang_tile import TileLayout, default_layout, WangTile

def next_tile(layout:TileLayout, cell:Cell, sigma=None) -> WangTile:
    """the default tile creator

    The default is to create tiles randomly using the layout.  The cell
    isn't referenced at all.  Color are assigned randomly to the
    exits without replacement unless sigma is supplied.
    """
    return WangTile(layout=layout, sigma=sigma)

def is_even_cell(cell:Cell) -> bool:
    """returns True if the cell is even and False otherwise

    On a rectangular grid, a cell is even if its indices sum to an
    even number.
    """
    i, j = cell.index
    return (i+j)%2 == 0

class EasyTiling(Algorithm):
    """Easy algorithm for tiling a maze using Wang tiles"""

    class Status(Algorithm.Status):
        """This is where all the work is done"""

        NAME = "Lazy Tiling"

        __slots__ = ("__visited", "__unvisited", "__layout",
                     "__tile_maker", "__cell_selector", "__cells",
                     "__pass", "__error_color", "__priorities")

        def parse_args(self, layout:TileLayout=default_layout,
                       tile_maker:callable=next_tile,
                       cell_selector:callable=is_even_cell,
                       error_color="red"):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - a rectangular maze (handled by __init__).
                    Other types of grids can be handled by providing
                    suitable values in the optional arguents.

            OPTIONAL ARGUMENTS

                layout - the tile layout information

                tile_maker - a method which takes a tile layout and
                    a cell as input, and optionally a color assignment,
                    and returns a Wang tile.

                cell_selector - a function which takes a cell as input
                    and returns True if it is to be selected in the
                    first pass.

                error_color - the color to use if an error occurs
            """
            self.__layout = layout
            self.__tile_maker = tile_maker
            self.__cell_selector = cell_selector
            self.__error_color = error_color
            self.__visited = dict()             # cell:tile
            self.__unvisited = list()           # cells to process in pass 2
            self.__priorities = None

        def configure(self):
            """configure structures (stub)"""
            self.more = True
            self.__pass = 1
            self.__cells = iter(self.maze.grid)
            self["even cells"] = 0
            self["odd cells"] = 0

        @property
        def visited(self) -> dict:
            """returns the visited map

            This is a dictionary whose keys are cells and whose values
            are Wang tiles.
            """
            return self.__visited

        def push(self, cell:Cell):
            """add a cell to the unvisited list"""
            self.__unvisited.append(cell)

        def pop(self) -> Cell:
            """remove and return a cell from the unvisited list

            If the unvisited list is empty, the return value is None.
            """
            if len(self.__unvisited) > 0:
                return self.__unvisited.pop()

        @property
        def current_pass(self) -> int:
            """returns the current pass number"""
            return self.__pass

        @current_pass.setter
        def current_pass(self, next_pass):
            """setss the current pass number"""
            self.__pass = next_pass

        def pass1_visit(self):
            """if the next cell is even, place a tile..."""
            try:
                cell = next(self.__cells)
                if self.__cell_selector(cell):      # even cell
                    tile = self.__tile_maker(self.__layout, cell)
                    self.__visited[cell] = tile
                    self["even cells"] += 1
                else:                               # odd cell
                    self.push(cell)
                    self["odd cells"] += 1
            except StopIteration:
                self.current_pass = 2

        def match_tile(self, cell):
            """match a tile with its neighbors"""
            sigma = dict()
            available = set(self.__layout.colors)
            opposites = self.__layout.opposites
            assigned = set()
            error = self.__error_color
            for way in cell.ways:
                nbr = cell[way]
                if nbr == None:
                    continue
                tile = self.__visited.get(nbr)
                if tile == None:
                    continue
                rway = opposites[way]
                color = tile.color_of(rway, error)
                # print(cell.index, way, nbr.index, rway)
                sigma[way] = color
                available.discard(color)
                assigned.add(way)
            available = list(available)
            rng.shuffle(available)
            ways = list(self.__layout.directions)
            rng.shuffle(ways)
            for way in ways:
                if way not in assigned:
                    color = available.pop() if available else error
                    sigma[way] = color
            # print(sigma)
            tile = self.__tile_maker(self.__layout, cell, sigma=sigma)
            self.__visited[cell] = tile

        def pass2_visit(self):
            """format a tile for odd cells"""
            cell = self.pop()
            if cell:
                self.match_tile(cell)
            else:
                self.more = False

        def visit(self):
            """the visit method"""
            if self.current_pass == 1:          # first pass
                self.pass1_visit()
            elif self.current_pass == 2:        # second pass
                self.pass2_visit()
            else:
                raise NotImplementedError("This is a two-pass algorithm")

        def set_priorities(self, debug=False):
            """create a priority map based on the edge coloring"""
                # associate a base priority with each color
            colors = list(self.__layout.colors)
            rng.shuffle(colors)
            colormap = dict()
            p = 0
            if debug:
                print("Priorities:")
            for color in colors:
                colormap[color] = p
                if debug:
                    print(f"\t{p:3} - {color}")
                p += 1
            colormap[self.__error_color] = p
                # retrieve the edges
            edgemap = dict()
            for cell in self.maze.grid:
                for way in cell.ways:
                    tile = self.__visited[cell]
                    color = tile.color_of(way)
                    p = colormap[color]
                    edge = frozenset([cell, cell[way]])
                    edgemap[edge] = p
            edges = list(edgemap.keys())
            rng.shuffle(edges)
                # build the priority table
            e = 0 
            delta = 1 / (len(self.maze.grid)**2)
            self.__priorities = dict()
            for edge in edges:
                p = edgemap[edge]
                signal = p + e * delta
                e += 1                          # increasing noise
                self.__priorities[edge] = signal

        @property
        def priorities_map(self) -> dict:
            """retrieve the priorities map"""
            if self.__priorities == None:
                print("building the priorities map...")
                self.set_priorities()
            return self.__priorities

        def to_edge(self, cell, nbr):
            """map cells to an edge"""
            return frozenset([cell, nbr])

        def to_priority(self, edge:frozenset):
            """find the priority of an edge"""
            return self.priorities_map[edge]

if __name__ == "__main__":
    print("quick test of Algorithm")
    from mazes import rng
    from mazes.Grids.oblong import OblongGrid
    from mazes.maze import Maze
    from mazes.Graphics.tiled_oblong import WangTileFill
    from mazes.Algorithms.kruskal import Kruskal

    print("\t\t=== Wang tiling demo ===")
    print("1) Create an 8x13 rectangular grid")
    maze = Maze(OblongGrid(8, 13))
    print("2) place tiles in the maze")
    status = EasyTiling.on(maze)
    print(status)
    print("3) connect the maze")
    status.set_priorities(debug=True)
    print()
    print(Kruskal.on(maze, priority=status.to_priority))
    print(maze)
    tally = dict()
    for color in default_layout.colors:
        tally[color] = [0, 0]
    tally["red"] = [0, 0]
    for cell in maze.grid:
        for way in ["east", "north"]:
            if not cell[way]:
                continue
            tile = status.visited[cell]
            color = tile.color_of(way)
            tally[color][0] += 1
            if cell.is_linked(cell[way]):
                tally[color][1] += 1
    print("Edges:")
    for color in tally:
        grid_edges, maze_edges = tally[color]
        print(f"\tgrid: {grid_edges:3}, maze: {maze_edges:3}   {color}")
    print("4) graphics")
    spider = WangTileFill(maze, status.visited)
    spider.setup()
    spider.title("Wang tiles, neatly placed")
    spider.draw_maze()
    spider.fig.tight_layout()
    spider.show()
    
