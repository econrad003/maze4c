"""
mazes.Graphics.tiled_oblong - coloring for Wang tiles
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    A Wang tile is a single cells in a maze with exits that have
    assiged colours.

    For example if our cell is a typical square cell, and our color
    set is cyan, magenta, yellow and black (=key), then we might have
    a tile that takes the form:

            M       Legend:
          +---+        C-cyan     Y-yellow
        Y |   | C      M-magenta  K-black
          +---+
            K

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
from mazes.Graphics.oblong1 import Pholcidae

class WangTileFill(Pholcidae):
    """coloring based on Wang tiles"""

    __slots__ = ("__tiles", )

    def __init__(self, maze:"Maze", tiles:dict):
        """constructor

        POSITIONAL ARGUMENTS

            maze - a rectangular maze

            tiles - a dictionary which maps cells to Wang tiles 
        """
        self.__tiles = tiles
        super().__init__(maze)

    def setup(self, color='black', aspect='equal', display_axes=False,
              fillcolors=None):
        """setup for the plot"""
        if fillcolors:
            raise TypeError("'fillcolors' must be a None for WangTileFill")
        super().setup(color=color, aspect=aspect, display_axes=display_axes)

    def draw_maze(self, origin=(0,0)):
        """draws the maze"""
        h, k = origin
        for cell in self.__tiles:
            i, j = cell.index
            x, y = j+h, i+k
            tile = self.__tiles[cell]
            self.tile_fill(tile, x, y)
        super().draw_maze(origin=origin)

    def tile_fill(self, tile, x, y):
        """fill cell with tile colors"""
        color = tile.color_of("south")      # south triangle
        if color:
            xs = [x, x+1, x+0.5]
            ys = [y, y, y+0.5]
            self.fill_polygon(xs, ys, color=color)
        color = tile.color_of("east")       # east triangle
        if color:
            xs = [x+1, x+1, x+0.5]
            ys = [y, y+1, y+0.5]
            self.fill_polygon(xs, ys, color=color)
        color = tile.color_of("north")       # north triangle
        if color:
            xs = [x+1, x, x+0.5]
            ys = [y+1, y+1, y+0.5]
            self.fill_polygon(xs, ys, color=color)
        color = tile.color_of("west")       # west triangle
        if color:
            xs = [x, x, x+0.5]
            ys = [y+1, y, y+0.5]
            self.fill_polygon(xs, ys, color=color)

if __name__ == "__main__":
    from mazes import rng
    from mazes.Grids.oblong import OblongGrid
    from mazes.maze import Maze
    from mazes.tetris.wang_tile import WangTile

    print("\t\t=== Wang tiling demo ===")
    print("1) Create an 8x13 binary maze")
    maze = Maze(OblongGrid(8, 13))
    for cell in maze.grid:
        nbrs = list()
        for way in {"east", "north"}:
            if cell[way]:
                nbrs.append(cell[way])
        if nbrs:
            nbr = rng.choice(nbrs)
            maze.link(cell, nbr)
    print(maze)
    print("2) place tiles in the maze")
    visited = dict()
    for cell in maze.grid:
        i, j = cell.index
        k = f"{i}{j}"
        tile = WangTile(ID=k)
        # print(tile)
        visited[cell] = tile
    print("3) graphics")
    spider = WangTileFill(maze, visited)
    spider.setup()
    spider.title("Wang tiles, badly placed")
    spider.draw_maze()
    spider.fig.tight_layout()
    spider.show()
