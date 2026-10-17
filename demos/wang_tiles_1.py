"""
demos.wang_tiles_1 - make a few Wang tiles
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

REFERENCES

    [1] Ian Stewart.  Reaching for the extreme.  Princeton (New Jersey, 2026).
        ISBN 978-0-691-26899-6.  Book.  pp 43-44.

    [2] Jacob Olesen.  "51 unique color names you’ve probably never heard
        of".  Web.  Accessed 16 October 2026.
        https://www.color-meanings.com/unique-color-names/

    Tardis blue was found using an Ecosia search.

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

print("Wang tiles introductory demo")
#######################################################################
# The code in the block that follows is included in doc.wang_tiles.md #
#######################################################################
### START OF CODE INCLUDED IN THE DOCUMENTATION

    # import a few things
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.tetris.wang_tile import TileLayout, WangTile, SENW, CMYK
from mazes.Graphics.tiled_oblong import WangTileFill

    # unpack directions, colors
S, E, N, W = SENW
C, M, Y, K = CMYK

    # make five places to put the tiles
maze = Maze(OblongGrid(5, 8))
cell1a = maze.grid[0,0]; cell1a.label='1'
cell2 = maze.grid[1,0]; cell2.label='2'
cell3 = maze.grid[2,2]; cell3.label='3'
cell4 = maze.grid[2,4]; cell4.label='4'
cell5 = maze.grid[2,6]; cell5.label='5'
cell1b = maze.grid[4,0]; cell1b.label='1'
cell1c = maze.grid[4,1]; cell1c.label='1'
maze.link(cell1a, cell2)
print(maze)

placements = dict()             # cell:tile

    # make two tiles that fit together vertically
alpha = {S:C, E:M, N:K, W:Y}
beta = {S:K, E:Y, N:C, W:M}
print("α =", alpha)
print("β =", beta)
placements[cell1a] = WangTile(sigma=alpha)
placements[cell1b] = placements[cell1a]
placements[cell1c] = placements[cell1a]
placements[cell2] = WangTile(sigma=beta)

    # two more tiles, CMYK default layout
placements[cell3] = WangTile()
placements[cell4] = WangTile(sigma="r")

    # one with a five-color layou
tardis_blue = "#003B6F"
phlox = "#DF00FF"
atrovirens = "#0D9494"
feldgrau = "#4D5D53"
smaragdine = "#4A9976"
palette = (tardis_blue, phlox, atrovirens, feldgrau, smaragdine)
new_layout = TileLayout(colors=palette)
placements[cell5] = WangTile(layout=new_layout)
for cell in [cell3, cell4, cell5]:
    print(placements[cell])

    # display the maze
spider = WangTileFill(maze, placements)
spider.setup()
spider.title("Wang tiles")
spider.draw_maze()
spider.fig.tight_layout()
spider.show()

### END OF CODE INCLUDED IN THE DODUMENTATION
#######################################################################

print("SUCCESS!")

