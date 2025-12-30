"""
mazes.tools.tulleken - Herman Tulleken's toolset
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

REFERENCES

    [1] Herman Tulleken. Algorithms for making more interesting mazes.
        Web. Accessed 28 December 2025.
            https://www.gamedeveloper.com/programming/ -
                algorithms-for-making-more-interesting-mazes

ROOMS, WALLS and PILLARS

    Tulleken's Rules of Formation
        F1. Each room is adjacent to four walls.
        F2. Each wall is adjacent to one or two rooms.
        F3. The adjacency relation is symmetric.

    Rules of Closure
        C1. A room is always open.
        C2. A wall may be open or closed.
        C3. A pillar is always closed.

    Interpretation
        I1. The rooms, walls, and pillars partition a graph.
        I2. Each room, wall, and pillar forms a connected subset.

    Notes:
        N1. Each pillar forms a connected component in the graph.  (Saying that
           a pillar is always closed means that there is never a passage leading
           from a pillar into another component.)
        N2. If a wall is open, then it contains a passage between two rooms.  If
           it is closed, then it is essentially just another pillar.
        N3. Rooms are never adjacent to one another.

REMARKS

    As we are generalizing the rules to arbitrary grids, there is no reason to
    enforce Rule F1.

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
from mazes import rng, Cell, Grid
from mazes.maze import Maze

class RoomCell(Cell):
    """cells in the auxiliary maze"""

    def _parse_args(self, room:set):
        """argument parser"""
        self.cells = room

class WallCell(Cell):
    """cells in the auxiliary maze"""

    def _parse_args(self, wall:set, door:Cell):
        """argument parser"""
        self.cells = wall
        self.door = door

class Tulleken(object):
    """partition the grid into rooms, walls, and pillars"""

    __slots__ = ("__maze", "__auxmaze", "__rooms", "__walls",
                 "__visited", "__unvisited", "__color", "__noloops")

    def __init__(self, maze:Maze):
        """constructor"""
        self.__maze = maze
        self.__rooms = dict()
        self.__walls = dict()
        self.__visited = set()
        self.__unvisited = set(list(maze.grid))
        self.__auxmaze = Maze(Grid())
        self.__color = 0
        self.__noloops = True
        self.initialize()
        self.configure()

    def initialize(self):
        """initialization (stub)"""
        pass

    def configure(self):
        """configuration (stub)"""
        pass

    def connected(self, cells:"iterable"):
        """check to see whether a group of cells is connected

        If the cells form a connected set, then the method returns.  If
        the cells do not form a connected set, then a ValueError
        exception is raised.

        This can be used to insure that a room or a wall forms a
        connected set in the grid.

        An IndexError is raised if a cell is not in the grid.
        """
        unvisited = set(cells)
        start = next(iter(unvisited))
        stack = [start]
        while len(stack) > 0:               # depth-first search
            cell = stack.pop()
            if cell not in self.__maze.grid:
                raise IndexError("the cell is not in the grid")
            if cell in unvisited:
                unvisited.remove(cell)
                for nbr in cell.neighbors:
                    if nbr in unvisited:
                        stack.append(nbr)
        if len(unvisited) > 0:
            raise ValueError("the cells do not form a connected set")

    def _remove_from_play(self, cells:set):
        """move the cells from unvisited to visited"""
        if cells <= self.__unvisited:
            pass            # subset
        else:
            raise ValueError("some of the cells have been visited")
        self.__visited |= cells
        self.__unvisited -= cells

    def _get_room(self, index, check:bool=False):
        """returns the cell representing the room"""
        cell = self.__rooms[index]
        if check:
            if not isinstance(cell, RoomCell):
                raise TypeError("room check failed")
        return cell

    def _find_a_door(self, cells:set, room1:RoomCell, room2:RoomCell):
        """locate a door cell"""
        doors = list()
        for cell in cells:
            nbrs = set(cell.neighbors)
            nbrs1 = nbrs & room1.cells
            if len(nbrs1) == 0:
                continue
            nbrs2 = nbrs & room2.cells
            if len(nbrs2) == 0:
                continue
            vector = cell, nbrs1, nbrs2
            doors.append(vector)
        if len(doors) == 0:
            raise ValueError("The wall doesn't have any doors")
        return rng.choice(doors)

    def _verify_door(self, door:Cell, cells:set,
                     room1:RoomCell, room2:RoomCell):
        """verify and pack door cell"""
        if door not in cells:
            raise ValueError("The door is not a member of the wall")
        nbrs = set(door.neighbors)
        nbrs1 = nbrs & room1.cells
        if len(nbrs1) == 0:
            raise ValueError("The door doesn't have neighbor in room1")
        nbrs2 = nbrs & room2.cells
        if len(nbrs2) == 0:
            raise ValueError("The door doesn't have neighbor in room1")
        return door, nbrs1, nbrs2

    def create_room(self, cells:"iterable", carve:bool=True,
                    check:bool=True) -> int:
        """creates a room

        DESCRIPTION

            Identifies

        OPTIONS

            carve - if True, neighboring pairs in the room are linked

            check - if True, an IndexError exception is raised if the
                cell array is not grid-connected

        RETURNS

            the color (or index) of the room
        """
            # preparation
        cells = set(cells)
        if check:
            self.connected(cells)
        self._remove_from_play(cells)

            # carve the room
        if carve:
            for cell in cells:
                for nbr in set(cell.neighbors) & cells:
                    if not cell.is_linked(nbr):
                        self.__maze.link(cell, nbr)

            # add the room to the auxiliary maze
        grid = self.__auxmaze.grid
        index = self.__color
        self.__color += 1
        cell = RoomCell(grid, index, cells)
        grid[index] = cell
        self.__rooms[index] = cell
        return index

    def create_wall(self, cells:"iterable",
                    room1:int, room2:int, door:Cell=None,
                    check:bool=False) -> int:
        """create a wall

        REQUIRED ARGUMENTS

            cells that form the wall

            room1 - the index of a room

            room2 - the index of another room

        OPTIONS

            door - the connecting cell.  The default None indicates that
                the door cell is to be chosen at random.  The door cell
                must have grid neighbors in each of the rooms.

            check - if True, the wall is checked for connectedness.
        """
            # preparation
        cells = set(cells)
        room1 = self._get_room(room1, check)
        room2 = self._get_room(room2, check)
        if self.__noloops and room1 == room2:
            raise ValueError("room1 and room2 are the same")
        
        door = self._find_a_door(cells, room1, room2) if door == None \
            else self._verify_door(door, cells, room1, room2)
        if check:
            self.connected(cells)
        self._remove_from_play(cells)

            # add the wall to the auxiliary maze
        grid = self.__auxmaze.grid
        index = self.__color
        self.__color += 1
        cell = WallCell(grid, index, cells, door)
        grid[index] = cell
        cell[1] = room1
        cell[2] = room2
        self.__walls[index] = cell
            # and add the wall to each room
        room1[index] = cell
        room2[index] = cell
        return index

    def create_pillar(self, cells:"iterable", check:bool=False):
        """create a pillar (removes cells from play)

        REQUIRED ARGUMENTS

            cells that form the wall

        OPTIONS

            check - if True, the wall is checked for connectedness.
        """
            # preparation
        cells = set(cells)
        if check:
            self.connected(cells)
        self._remove_from_play(cells)

    @property
    def maze(self) -> Maze:
        """returns the primary maze"""
        return self.__maze

    @property
    def skeleton(self) -> Maze:
        """returns the room-wall maze

        This is where work should be done.
        """
        return self.__auxmaze

    @property
    def visited(self) -> set:
        """returns the visited set"""
        return self.__visited

    @property
    def unvisited(self) -> set:
        """returns the visited set"""
        return self.__unvisited

    def room(self, index:int):
        """returns a room cell"""
        return self.__rooms[index]

    def wall(self, index:int):
        """returns a wall cell"""
        return self.__walls[index]

    def _update_side(self, cell:WallCell, side:int, door:Cell, nbrs:set):
        """check one side of a door"""
        joined = set(door.passages) & nbrs
        if cell.is_linked(cell[side]):
            if len(joined) == 0:
                nbr = rng.choice(list(nbrs))
                self.__maze.link(door, nbr)
        else:
            # print(f"{door.index=} {len(joined)=}")
            for nbr in joined:
                # print(f"    {nbr.index=}")
                if door.is_linked(nbr):
                    join = door.join_for(nbr)
                    self.__maze.unlink(join)

    def update_wall(self, cell:WallCell):
        """uodate each side of the door"""
        door, nbrs1, nbrs2 = cell.door
        self._update_side(cell, 1, door, nbrs1)
        self._update_side(cell, 2, door, nbrs2)

    def update(self):
        """updates the maze

        Changes to the room-wall maze are recorded in the main maze.
        Note that the room cells can be ignored.  We only need to consider
        the door in each walls.
        """
        for cell in self.__walls.values():
            self.update_wall(cell)

# END mazes.tools.tulleken
