"""
mazes.Algorithms.tetris - creating a maze using Tetris tile drops
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    The algorithm performs a series of tile drops onto an empty
    rectangular maze.

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
from mazes import rng, Algorithm
from mazes.tetris.tetris import configs as _default_descriptors
from mazes.tetris.tetris import create_tile
from mazes.Grids.oblong import OblongGrid

class Tetris(Algorithm):
    """the Tetris algorithm (passage carver)"""

    class Status(Algorithm.Status):
        """this is where most of the work is done"""

        NAME = "Tetris tile carver"

        __slots__ = ("__occupied", "__places", "__columns",
                     "__tiles", "__tile", "__tile_num", "__state",
                     "__drops", "__debug")

        def parse_args(self, tiles:'TileDescriptorSet'=None, debug=False):
            """parse constructor arguments

            POSITIONAL ARGUMENTS

                maze - handled by __init__ in the base class.
                    The grid must be an instance of class OblongGrid
                    or a subclass thereof.

            KEYWORD ARGUMENTS

                tiles - the tile descriptors; each descriptor is a
                    tuple consisting of a tile shape descriptor,
                    a tile width, a tile height, and the column
                    location of the start cell for the tile. (The
                    starting cell, cell 0, is always a cell in the
                    bottom row.

                    If this argument is None, then the descriptor
                    set is the set named "configs" imported from
                    mazes.tetris.tetris.

                    Method "create_tile" in mazes.tetris.tetris is
                    used to create the tiles that are dropped.
            """
            super().parse_args()                # chain to parent
            if not isinstance(self.grid, OblongGrid):
                raise TypeError("The grid must be instance of OblongGrid")
            if not tiles:
                tiles = self.default_tile_set
            self.__tiles = list(tiles)
            self.__occupied = set()
            self.__places = dict()
            self.__state = 0                    # prepare to drop
            self.more = True
            self.__debug = debug

        @property
        def default_tile_set(self) -> tuple:
            """imports als the configurations from mazes.tetris.tetris

            The elements are representations of Tetris tiles.
            """
            return _default_descriptors

        @property
        def occupied(self) -> set:
            """the set of cells covered by tiles"""
            return self.__occupied

        def initialize(self):
            """initialization

            The places and columns arrays are initialized here.
            """
            for j in self.grid.columns():
                cells = list()
                for cell in self.grid.column(j):
                    cells.append(cell)
                self.__places[j] = cells
            self.__columns = tuple(self.__places.keys())

        def configure(self):
            """configuration

            Set up the statistics.
            """
            self["cells"] = len(self.grid)
            self["passages"] = 0
            self["tile types"] = len(self.__tiles)
            self["tiles"] = 0
            self["drops"] = 0
            self["placements"] = 0

        def draw_tile(self) -> "Tile":
            """pick a tile at random"""
            self["tiles"] += 1
            self.__tile_num = rng.randrange(len(self.__tiles))
            if self.__debug:
                print(f"{self['tiles']})",
                      f"Create tile {self.__tile_num}/{len(self.__tiles)}")
            return create_tile(self.__tiles[self.__tile_num])

        def prepare_drop(self):
            """set up the drop parameters"""
            columns = list(self.__columns)
            if self.__debug:
                locations = 0
                empties = 0
                for column in columns:
                    places = len(self.__places[column])
                    if places == 0:
                        empties += 1
                    locations += places
                print(f"    prepare: {locations} sites, {empties} empty columns")
            n = len(columns)
            j = rng.randrange(n)
            self.__drops = columns[j:] + columns[:j]

        def begin_drop(self):
            """select a tile"""
            if len(self.__tiles) == 0:
                    # no more tiles
                self.more = False
                return
            self.__tile = self.draw_tile()
            self.__state = 1
            self.prepare_drop()

        def discard_tile_type(self):
            """discard tile type that cannot be placed"""
            if self.__debug:
                print(f"    discarding tile type {self.__tile_num}")
            del self.__tiles[self.__tile_num]

        def cleanup(self, tile:"Tile"):
            """clear out occupied cells"""
            cells = tile.cells
            if self.__debug:
                print(f"    cleanup: {len(cells)} cells")
            columns = set()
            for cell in cells:
                i, j = cell.index
                columns.add(j)
            for j in columns:
                obsolete = self.__places[j]
                fresh = list()
                for cell in obsolete:
                    if cell not in cells:
                        fresh.append(cell)
                if self.__debug:
                    print(f"      column {j}: cover {len(obsolete)-len(fresh)} cells;",
                          f"before {len(obsolete)}", f"after {len(fresh)}")
                self.__places[j] = fresh

        def drop(self):
            """carry out a drop"""
            if len(self.__drops) == 0:
                    # there is no place for this tile
                self.discard_tile_type()
                self.__state = 0
                return
            self["drops"] += 1
            column = self.__drops.pop()
            places = list(self.__places[column])
            tile = self.__tile
            if not tile.drop(places, self.__occupied):
                    # unsuccessful drop
                return
                    # successful drop
            self["placements"] += 1
            self["passages"] += tile.carve(self.maze)
            if self.__debug:
                for cell in tile.cells:
                    cell.label = chr(ord('0')+(self['placements']-1) % 10)
            self.__state = 0                # prepare a new drop
            self.cleanup(tile)

        def visit(self):
            """visit"""
            if self.__state == 0:
                self.begin_drop()
                return
            if self.__state == 1:
                self.drop()
                return
            raise RuntimeError(f"Undefined state {self.__state}")
