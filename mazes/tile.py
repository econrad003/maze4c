"""
mazes.tile - base class implementation for tiles
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

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
from mazes.grid import Grid
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze

class Tiles(object):
    """a set of tiles to be used to create larger mazes"""

    __slots__ = ("__tiles", "__indices", "__cons", "__index")

    def __init__(self, TileClass:object, *args, **kwargs):
        """constructor

        The argument list tells us how tiles are initized:
            tile = Maze(TileClass(*args, **kwargs))
        """
        if not issubclass(TileClass, Grid):
            raise TypeError("'TileClass' must be a subclass of class 'Grid'")
        self.__cons = (TileClass, args, kwargs)
        self.__tiles = dict()
        self.__indices = dict()
        self.__index = 0
        self.initialize()
        self.configure()

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    def new_tile(self) -> Maze:
        """create a tile -- returns a maze object"""
        i = self.__index
        self.__index += 1
        TileClass, args, kwargs = self.__cons
        self.__tiles[i] = tile = Maze(TileClass(*args, **kwargs))
        self.__indices[tile] = i
        return tile

    def index_of(self, tile:Maze) -> int:
        """returns an index"""
        return self.__indices[tile]

    def tile(self, i:int) -> Maze:
        """return the indexed tile"""
        return self.__tiles[i]

    def __len__(self) -> int:
        """returns the number of tiles"""
        return len(self.__tiles)

    def __iter__(self):
        """iterates through the tiles"""
        tiles = list(self.__indices.keys())
        for tile in tiles:
            yield tile

Tullekin_patterns = list()
Tullekin_patterns.append(["    ", "XXX ", "    ", "X XX"])
Tullekin_patterns.append(["  X ", "XXXX", "  X ", "X X "])
Tullekin_patterns.append(["X X ", "X XX", "    ", "X XX"])
Tullekin_patterns.append(["X X ", "X XX", "  X ", "X XX"])
Tullekin_patterns.append(["  X ", "X XX", "X X ", "X XX"])
Tullekin_patterns.append(["  X ", "XXXX", "X X ", "X XX"])

class TullekenTiles(Tiles):
    """Tulleken's 4x4 tile set'"""

    __slots__ = ("__debug", "__patterns")

    def __init__(self, patterns:list=Tullekin_patterns,
                 GridType:object=OblongGrid, debug:bool=False):
        """constructor"""
        self.__debug = bool(debug)
        rows = len(patterns[0])
        cols = len(patterns[0][0])
        self.__patterns = patterns
        super().__init__(GridType, rows, cols)

    def configure(self):
        """build the tiles"""
        super().configure()
        for pattern in self.__patterns:
            tile = self.new_tile()
            grid = tile.grid
            for i in range(len(pattern)):
                for j in range(len(pattern[i])):
                    grid[i,j].label = pattern[i][j]
            if self.__debug:
                index = self.index_of(tile)
                print(f"Tile {index=}:")
                print(tile)

# END mazes.tile
