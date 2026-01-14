"""
mazes.Inform.room - convert a maze to Inform 7 text
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Builds a room plan based on a maze.

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
from mazes import Cell, Grid
from mazes.maze import Maze

class Room(object):
    """extracts defining information for a room"""

    __slots__ = ("__cell", "__name", "__passage_to", "__passage_from",
                 "__description", "__inverted", "__kind")

    _OXFORD_COMMA = False           # no Oxford comma
    _ET = "and"                     # the conjunction

    @classmethod
    def Oxford_comma(cls, comma:bool=False):
        """Oxford comma setting (default=False)

        Oxford comma is typical UK usage, while the default is typical
        US usage.

        Lists of three or more strings are affected:

            dog, cat, canary
                (default)       dog, cat and canary
                (Oxford)        dog, cat, and canary
        """
        cls.OXFORD_COMMA = bool(comma)

    @classmethod
    def concat(cls, *args):
        """make a list"""
        if len(args) == 0:
            return ""
        if len(args) == 1:
            return args[0]
        if len(args) == 2:
            return f"{args[0]} {cls._ET} {args[1]}"
        s = ", ".join(map(str, args[:-1]))
        if cls._OXFORD_COMMA:
            s += ","
        s += f" {cls._ET} {args[-1]}"
        return s

    def __init__(self, *args, **kwargs):
        """constructor: collects data from the cell"""
        self.__passage_to = dict()
        self.__passage_from = dict()
        self.__description = str()
        self.__inverted = False
        self.__kind = "room"
        self._parse_args(*args, **kwargs)
        self._initialize()
        self._configure()

    def _parse_args(self, cell:Cell):
        """argument parser"""
        self.__cell = cell

    def _initialize(self):
        """initialization"""
        self.__name = self.__default_name

    def _configure(self):
        """configuration"""
        for way in self.cell.ways:
            nbr = self.cell[way]
            if self.cell.is_linked(nbr):
                self.new_way_to(nbr, way)

    @property
    def cell(self):
        """returns the cell"""
        return self.__cell

    def __getitem__(self, nbr:Cell):
        """passage information"""
        way_to = self.__passage_to(nbr)
        way_back = self.__passage_from(nbr)
        return (way, way_back)

    def new_way_to(self, nbr:Cell, way_to:str):
        """create, modify, or delete a passage"""
        if way_to == None:
            del self.__passage_to[nbr]
        else:
            self.__passage_to[nbr] = way_to

    def new_way_back(self, nbr:Cell, way_back:str):
        """create, modify, or delete a return passage"""
        if way_back == None:
            del self.__passage_from[nbr]
        else:
            self.__passage_to[nbr] = way_back

    @property
    def __default_name(self):
        """generate a (hopefully) unique name"""
        cell = self.__cell
        error = False
        if type(cell.index) == tuple:
            s = "Room"
            for component in cell.index:
                if type(component) == int:
                    s += f"_{component}"
                else:
                    error = True
                    break
            if not error:
                return s
        if type(cell.index) == int:
            return f"Room_{cell.index}"
        return f"Room_{id(cell)}"

    @property
    def name(self) -> str:
        """returns the current name"""
        return str(self.__name)

    @property
    def Name(self) -> str:
        """returns the current name, capitalized"""
        name = self.name
        return name[:1].upper() + name[1:]

    @name.setter
    def name(self, new_name:str):
        """changes the name"""
        self.__name = new_name

    @property
    def description(self) -> str:
        """returns the description"""
        ways = tuple(self.__passage_to.values())
        s = '"'
        br = ""
        if len(self.__description) > 0:
            s += self.__description
            br = "[paragraph break]"
        if len(ways) > 0:
            s += f"{br}There are passages {self.concat(*ways)}."
        s += '"'
        return s

    @description.setter
    def description(self, descr) -> str:
        """sets the description"""
        self.__description = descr

    @property
    def inverted(self):
        """get the inverted format setting"""
        return self.__inverted

    @inverted.setter
    def inverted(self, invert:bool=True):
        """sets the inverted format flag.

        The flag is initially False.  The default is to change the setting
        to True.

            Normal room declaration:
                Foo is a room.

            Inverted room declaration:
                There is a room called foo.
        """
        self.__inverted = bool(invert)

    @property
    def kind(self) -> str:
        """the kind of room (default: room)"""
        return self.__kind

    @kind.setter
    def kind(self, other:str):
        """set the kind of room

        A "kind" in Inform corresponds to a type or a class in other
        languages.
        """
        self.__kind = other

    @property
    def paragraph(self) -> str:
        """write a paragraph about the room"""
        s = ""
        s += f"There is a {self.kind} called {self.name}." if self.inverted \
            else f"{self.Name} is a room."
        s += f"  The description is {self.description}."
        return s

    def set(self, name:str=None, kind:str=None, inverted:bool=None,
            description:str=None):
        """set the attributes"""
        if name:
            self.name = name
        if kind:
            self.kind = kind
        if inverted != None:
            self.inverted = bool(inverted)
        if description != None:
            self.description = str(description)

class RoomPlan(object):
    """convert a maze into a room plan"""

    __slots__ = ("__maze", "__rooms", "__Room", "__start")

    def __init__(self, *args, **kwargs):
        """constructor"""
        self.__rooms = dict()
        self._parse_args(*args, **kwargs)
        self._initialize()
        self._configure()

    def _parse_args(self, maze:Maze, RoomType:"class"=Room, start_cell:Cell=None):
        """argument parser"""
        self.__maze = maze
        self.__Room = RoomType
        self.__start = None

    def _initialize(self):
        """gets the room data from the maze"""
        for cell in self.grid:
            self[cell] = self.__Room(cell)

    def _configure(self):
        """configure each room"""
        for cell in self.grid:
            for way in cell.ways:
                nbr = cell[way]
                room = self[nbr]
                if cell.is_linked(nbr):
                    room.new_way_back(cell, way)

    def __getitem__(self, cell:Cell):
        """get the data for a room"""
        return self.__rooms[cell]

    def __setitem__(self, cell:Cell, room:Room):
        """set the room"""
        self.__rooms[cell] = room

    @property
    def maze(self) -> Maze:
        """returns the base maze"""
        return self.__maze

    @property
    def grid(self) -> Grid:
        """returns the base maze"""
        return self.__maze.grid

    def __iter__(self):
        """iterator for the rooms"""
        if self.__start != None:
            yield self[self.__start]
        for cell in self.__maze.grid:
            if cell != self.__start:
                yield(self[cell])

# END mazes.Inform.room
