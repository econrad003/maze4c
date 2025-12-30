"""
denos.tulleken - demonstration of Herman Tulleken's toolset
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
import argparse

from mazes import Cell
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.VGT.vprim import vprim
from mazes.tools.tulleken import Tulleken

def create_empty_maze(rows:int, columns:int) -> Maze:
    """create an oblong grid set up for passage carving"""
    from mazes.Grids.oblong import OblongGrid
    return Maze(OblongGrid(rows, columns))

def create_partition(maze:Maze) -> Tulleken:
    """create the partitioning tool"""
    return Tulleken(maze)

def create_pillar(partition:Tulleken, cells:"iterable", label:str="█"):
    """turn a collection of cells into a pillar"""
    if label:
        for cell in cells:
            cell.label = label
    partition.create_pillar(cells)

def create_room(partition:Tulleken, cells:"iterable", carve=True) -> int:
    """turn a connected collection of cells into a room"""
    if len(cells) < 2:
        carve= False
    return partition.create_room(cells, carve=carve)

def create_wall(partition:Tulleken, cells:"iterable",
                room1:int, room2:int, label:str="█") -> int:
    """turn a collection of cells into a wall with a door"""
    wall = partition.create_wall(cells, room1, room2)
    door = partition.wall(wall).door[0]
    if label:
        for cell in cells:
            if cell != door:
                cell.label = label
    return wall

def pattern0(partition:Tulleken):
    """create a partition

    The 2x2 pattern can be described as follows:
        WP
         W
            where: P-pillar, W-wall (door)
    Walls in the top row or rightmost collumn are replaced by pilars
    """
        # create the rooms
    grid = partition.maze.grid
    cells = dict()
    for i in range(0, grid.m, 2):
        for j in range(0, grid.n, 2):
            cell = grid[i,j]
            cells[cell] = create_room(partition, {cell}, False)
        # create the east-west walls
    for i in range(0, grid.m, 2):
        for j in range(1, grid.n-1, 2):
            cell = grid[i,j]
            room1 = cells[cell.west]
            room2 = cells[cell.east]
            create_wall(partition, {cell}, room1, room2)
        # create the north-south walls
    for i in range(1, grid.m-1, 2):
        for j in range(0, grid.n, 2):
            cell = grid[i,j]
            room1 = cells[cell.south]
            room2 = cells[cell.north]
            create_wall(partition, {cell}, room1, room2)
        # create the pillars
    create_pillar(partition, partition.unvisited)
    assert len(partition.unvisited) == 0

def pattern1(partition:Tulleken):
    """create a partition

    The pattern consists of the following 3x3 tiles:
        PWP
          W
        P P
            where: P-pillar, W-wall (door)
    Walls in the top row or rightmost collumn are replaced by pilars
    """
        # create the rooms
    grid = partition.maze.grid
    cells = dict()
    for i in range(0, grid.m-1, 3):
        for j in range(0, grid.n-1, 3):
            cell1 = grid[i, j+1]
            cell2 = grid[i+1, j]
            cell3 = grid[i+1, j+1]
            # cell1.label = cell2.label = cell3.label = "x"
            room = create_room(partition, {cell1, cell2, cell3})
            # print(f"room {room}: {cell1.index} {cell2.index} {cell3.index}")
            cells[cell1] = cells[cell2] = cells[cell3] = room
    #print(partition.maze)
        # create the east-west walls
    for i in range(0, grid.m-1, 3):
        for j in range(0, grid.n-4, 3):
            cell = grid[i+1,j+2]
            room1 = cells[cell.west]
            room2 = cells[cell.east]
            # print(f"horizontal wall: {cell.index} {room1} {room2}")
            create_wall(partition, {cell}, room1, room2)
        # create the north-south walls
    for i in range(0, grid.m-4, 3):
        for j in range(0, grid.n-1, 3):
            cell = grid[i+2,j+1]
            room1 = cells[cell.south]
            room2 = cells[cell.north]
            # print(f"vertical wall: {cell.index} {room1} {room2}")
            create_wall(partition, {cell}, room1, room2)
        # create the pillars
    create_pillar(partition, partition.unvisited)
    assert len(partition.unvisited) == 0

def pattern2(partition:Tulleken):
    """create a partition

    The pattern consists of the following 3x3 tiles:
         WP
          W
        P
            where: P-pillar, W-wall (door)
    Walls in the top row or rightmost collumn are replaced by pilars
    """
        # create the rooms
    grid = partition.maze.grid
    cells = dict()
    for i in range(0, grid.m-1, 3):
        for j in range(0, grid.n-1, 3):
            cell1 = grid[i, j+1]
            cell2 = grid[i+1, j]
            cell3 = grid[i+1, j+1]
            cell4 = grid[i, j+2]
            cell5 = grid[i+2, j]
            room = {cell1, cell2, cell3}
            if isinstance(cell4, Cell):
                room.add(cell4)
            if isinstance(cell5, Cell):
                room.add(cell5)
            room = create_room(partition, room)
            cells[cell1] = cells[cell2] = cells[cell3] = room
        # create the east-west walls
    for i in range(0, grid.m-1, 3):
        for j in range(0, grid.n-4, 3):
            cell = grid[i+1,j+2]
            room1 = cells[cell.west]
            room2 = cells[cell.east]
            create_wall(partition, {cell}, room1, room2)
        # create the north-south walls
    for i in range(0, grid.m-4, 3):
        for j in range(0, grid.n-1, 3):
            cell = grid[i+2,j+1]
            room1 = cells[cell.south]
            room2 = cells[cell.north]
            create_wall(partition, {cell}, room1, room2)
        # create the pillars
    create_pillar(partition, partition.unvisited)
    assert len(partition.unvisited) == 0

patterns = [pattern0, pattern1, pattern2]

def carve_maze(rows:int, cols:int, pattern:callable):
    """run the algorithm"""
    maze = create_empty_maze(rows, cols)
    partition = create_partition(maze)
    pattern(partition)
    print(vprim(partition.skeleton))
    partition.update()
    print(maze)

def main(argv:list):
    """parse the arguments"""
    DESC = "demonstration of Herman Tulleken's toolset"
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument("-d", "--dim", type=int, nargs=2, \
        default=(8,13), metavar=("ROWS", "COLS"), \
        help="the dimensions of the maze (default: 8,13)")
    parser.add_argument("-p", "--pattern", type=int, default=0,
        help="the pattern to use (default:0, values in [0,0])")
    args = parser.parse_args(argv)
    rows, cols = args.dim
    carve_maze(rows, cols, patterns[args.pattern])

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
    
