"""
mazes.Inform.treasure - Inform 7 treasures
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Creates objects and places them in rooms.

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
from mazes.Inform.room import Room, RoomPlan

class Treasures(object):
    """manages objects for Inform 7"""

    __slots__ = ("__plan", "__treasures")

    def __init__(self, *args, **kwargs):
        """manages treasures and other objects"""
        self._parse_args(*args, **kwargs)
        self._initialize()
        self._configure()

    def _parse_args(self, room_plan:RoomPlan):
        """parse arguments

        REQUIRED POSITIONAL ARGUMENTS

            room_plan - a room plan object
        """
        self.__plan = room_plan
        self.__treasures = dict()

    @property
    def plan(self) -> RoomPlan:
        """returns the associated room plan"""
        return self.__plan

    @property
    def maze(self) -> Maze:
        """returns the associated maze"""
        return self.__plan.maze

    @property
    def grid(self) -> Grid:
        """returns the associated grid"""
        return self.__plan.maze.grid

    def _initialize(self):
        """initialization (stub)"""
        pass

    def _configure(self):
        """configuration (stub)"""
        pass

    def new_treasure(self, treasure:str, cell:Cell, *attrs,
                     kind:str="thing", description:str=None,
                     pronoun:str="it", is_are:str="is"):
        """create a treasure"""
        room = self.plan[cell] if cell else None
        self.__treasures[treasure] = (room, kind, description,
                                      pronoun, is_are, attrs)

    def paragraph(self, treasure:str, here:bool=False):
        """write a paragraph about something"""
        s = ""
        Name = treasure[0].upper() + treasure[1:]
        room, kind, descr, pronoun, is_are, attrs = self.__treasures[treasure]
        Pronoun = pronoun[0].upper() + pronoun[1:]
        article = "an" if kind[0] in {"a", "e", "i", "o", "u"} else "a"
        if is_are == "are":
            s += f"{Name} are {kind}."
            s += "  They are plural-named."
        else:
            s += f"{Name} is {article} {kind}."
        if here:
            s += f"  {Pronoun} {is_are} here."
        elif room != None:
            s += f"  {Pronoun} {is_are} in {room.name}."
        if len(attrs) > 0:
            predicate = Room.concat(*attrs)
            s += f"  {Pronoun} {is_are} {predicate}."
        if descr != None:
            s += f'  The description is "{descr}".'
        return s

    def __getitem__(self, treasure):
        """return the room where something may be found"""
        return self.__treasures[treasure][0]

    def __iter__(self):
        """generator for the treasures and other things"""
        for treasure in self.__treasures:
            yield treasure

# END mazes.Inform.treasure
