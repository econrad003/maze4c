"""
mazes.tetris.wang_tile - implementation for Wang tiles
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
from itertools import permutations

from mazes import rng, Cell

SENW = ("south", "east", "north", "west")
OPPOSITES = (("south", "north"), ("east", "west"))
CMYK = ("cyan", "magenta", "yellow", "grey")

class TileLayout(object):
    """defines the layout for a tile"""

    __slots__ = ("__directions", "__opposites", "__colors")

    def __init__(self, directions:dict=SENW, opposites=OPPOSITES, colors=CMYK):
        """constructor"""
        self.directions = directions
        self.opposites = opposites
        self.colors = colors

    @property
    def directions(self) -> tuple:
        """fetch the available directions"""
        return self.__directions

    @directions.setter
    def directions(self, value:tuple):
        """set the available directions"""
        self.__directions = tuple(value)

    @property
    def opposites(self) -> dict:
        """fetch a table mapping a direction to its opposing direction"""
        return self.__opposites

    @opposites.setter
    def opposites(self, value:(tuple, list, dict)):
        """sets the table of opposites"""
        if type(value) == dict:
            self.__opposites = value                # already formatted
        else:
            self.__opposites = dict()
            for pair in value:
                left, right = pair
                self.__opposites[left] = right
                self.__opposites[right] = left

    @property
    def colors(self) -> tuple:
        """fetch the color list"""
        return self.__colors

    @colors.setter
    def colors(self, value:tuple):
        """set the color list"""
        self.__colors = tuple(value)

    def __len__(self):
        """returns the number of colors"""
        return len(self.__colors)

    def __iter__(self):
        """iterate through the list of directions"""
        for direction in self.__directions:
            yield direction

    def random_color(self) -> str:
        """return a uniformly random color"""
        return rng.choice(self.__colors)

    def all_colors(self, random=True):
        """generate the colors

        if "random" is True, the colors are shuffled.
        """
        if random:
            colors = list(self.__colors)
            rng.shuffle(colors)
        else:
            colors = self.__colors
        for color in colors:
            yield color

    def all_permutations(self, random=True):
        """generate all the permutations of the color set"""
        m = len(self.__colors)
        n = len(self.__directions)
        if m < n:
            raise ValueError("too few colors")
        sigmas = list(permutations(range(m), n))
        if random:
            rng.shuffle(sigmas)
        for sigma in sigmas:
            yield {self.__directions[i]: self.__colors[j] for i, j in enumerate(sigma)}

    @property
    def random_permutation(self):
        """generate a random permutation of colors"""
        m = len(self.__colors)
        n = len(self.__directions)
        sigma = list(rng.sample(range(m), n))
        tau = dict()
        for i in range(n):
            j = sigma[i]
            tau[self.__directions[i]] = self.__colors[j]
        return tau

default_layout = TileLayout()

class WangTile(object):
    """a Wang tile"""

    NEXT_ID = 0

    __slots__ = ("__ID", "__sigma", "__layout", "__opposites", "__reason")

    @classmethod
    def next_id(cls) -> int:
        """get the next automatic ID"""
        cls.NEXT_ID += 1;
        return cls.NEXT_ID

    def __init__(self, *args, ID=None, **kwargs):
        """constructor -- create a tile type"""
        self.__ID = self.next_id() if ID == None else ID
        self.parse_args(*args, **kwargs)
        self.initialize()
        self.configure()

    def parse_args(self, *, sigma:dict=None, layout:TileLayout=default_layout):
        """parse the arguments

        KEYWORD ARGUMENTS

            ID - an optional identifier to represent the tile class.
                This ID is handled in the constructor.
            sigma - a dictionary which maps a direction to a color.
                If sigma == None, then colors will be assigned at random (without
                replacement!)
                If sigma == "uniform" (actually any string), the colors will be 
                assigned at random (with replacement).
            layout - a TileLayout object which supplies additional
                information such as opposing directions
        """
        if sigma == None:
            sigma = layout.random_permutation
        elif type(sigma) == str:
            sigma = dict()
            for way in layout:
                sigma[way] = layout.random_color()
        self.sigma = sigma
        self.__opposites = layout.opposites
        self.__layout = layout

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    def __len__(self):
        """returns the number of colored edges"""
        return len(self.__sigma)

    def __str__(self):
        """returns the string representation of the mapping"""
        s = f"WangTile[{self.__ID}]: "
        s += "{"
        keys = list(self.__sigma.keys())
        key = keys[0]
        s += f"{key}:{self.sigma[key]}"
        for i in range(1, len(keys)):
            key = keys[i]
            s += f", {key}:{self.sigma[key]}"
        s += "}"
        return s

    @property
    def sigma(self) -> dict:
        """returns the color mapping"""
        return self.__sigma

    @sigma.setter
    def sigma(self, value:dict):
        """set the color mapping"""
        self.validate_sigma(value)
        self.__sigma = value

    def validate_sigma(self, sigma:dict):
        """make sure sigma has the correct form"""
        if not isinstance(sigma, dict):
            raise TypeError("sigma must be a dictionary")

    def color_of(self, way:str, error:str=None) -> str:
        """returns the coloring, if any, for a given direction"""
        return self.__sigma.get(way, error)

    def __getitem__(self, way:str) -> str:
        """returns the coloring, if any, for a given direction

        synonymous with color_of
        """
        return self.__sigma.get(way)

    def opposite_of(self, way:str) -> str:
        """returns the opposite direction"""
        return self.__opposites[way]

    @property
    def layout(self):
        """return the tile layout"""
        return self.__layout

    def matching_edge(self, cell:Cell, way, visited:dict) -> bool:
        """determine whether a neigboring edge is a match"""
        self.__reason = None
        color = self.color_of(way)              # edge color
        if color == None:                       # not colored
            self.__reason = 1
            return True                             # automatic match
        nbr = cell[way]                         # fetch neighbor
        if nbr == None:                         # nbr does not exist
            self.__reason = 2
            return True                             # automatic match
        rway = self.opposite_of(way)            # return direction
        if nbr[way] != cell:                    # validate
            raise RuntimeError("return direction failure")
        tile = visited.get(cell)                # has neighbor been tiled?
        if tile == None:
            self.__reason = 3
            return True                             # no, automatic match
        if tile.color_of(rway) == color:        # matching color?
            self.__reason = 0
            return True                             # yes!
        return False                            # no!

    def fits_in(self, cell, visited:dict) -> bool:
        """does the tile fit here?"""
        for way in cell.ways:
            if not self.matching_edge(cell, way, visited):
                return False
        return True

if __name__ == "__main__":
    print("verifying layout... ", end="")
    assert len(default_layout) == 4
    assert tuple(iter(default_layout)) == SENW
    assert tuple(iter(default_layout.all_colors(random=False))) == CMYK
    assert set(iter(default_layout.all_colors())) == set(CMYK)
    P4 = 4*3*2*1
    assert len(list(default_layout.all_permutations())) == P4
    print("ok!")
    n = 0
    for sigma in default_layout.all_permutations():
        n += 1
        print(n, sigma)
    tile = WangTile()
    print(f"tile={tile}")
    tile = WangTile(sigma="uniform")
    print(f"tile={tile}")
    print("SUCCESS!")
