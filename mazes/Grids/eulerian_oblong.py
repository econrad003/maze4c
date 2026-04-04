"""
mazes.Grids.eulerian_oblong - maximally Eulerian oblong (aka: rectangular) grids
Eric Conrad
Copyright ©2026 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    Creates 4-connected oblong grids and carves passages to form maximally Eulerian
    mazes.

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
from mazes.Grids.oblong import OblongGrid, SquareCell
from mazes.maze import Maze

def check_vertex_degrees(maze:Maze, warn=True) -> bool:
    """make sure all cells have even positive degree, ignoring loops"""
    errors = 0
    for cell in maze.grid:
        degree = 0
        for join in cell.joins:
            nbr = cell.cell_for(join)
            if nbr != cell:
                degree += 1
        if degree == 0:
            if warn:
                print(f"{cell.index}: cell is isolated")
            cell.label = "X" if is_black(cell) else "Y"
            errors += 1
            continue
        if degree % 2 == 1:
            if warn:
                print(f"{cell.index}: cell has odd degree")
            cell.label = "X" if is_black(cell) else "Y"
            errors += 1
    if errors:
        print(f"{errors} errors in Eulerianization")
        return False
    return True

def on_north_border(cell:SquareCell) -> bool:
    """returns True if the cell is on the north border"""
    return not cell.north

def on_south_border(cell:SquareCell) -> bool:
    """returns True if the cell is on the north border"""
    return not cell.south

def on_east_border(cell:SquareCell) -> bool:
    """returns True if the cell is on the north border"""
    return not cell.east

def on_west_border(cell:SquareCell) -> bool:
    """returns True if the cell is on the north border"""
    return not cell.west

def in_interior(cell:SquareCell) -> bool:
    """returns True if the cell is in the interior"""
    return bool(cell.south and cell.east and cell.north and cell.west)

def is_black(cell:SquareCell) -> bool:
    """returns True if the cell is black

    A cell is black if and only if the sum of its indices is even, and
    (conversely) white if odd.
    """
    return sum(cell.index) % 2 == 0

def TwoRows(maze:Maze, other_constraints:bool=True):
    """carve a simple circuit"""
    grid = maze.grid
    assert isinstance(grid, OblongGrid)
    assert grid.m == 2, "row constraint"
    assert grid.n >= 2, "column constraint"
    for cell in grid:
        if cell.east:
            maze.link(cell, cell.east)
        i, j = cell.index
        if j in {0, grid.n-1}:
            if i == 0:
                maze.link(cell, cell.north)

def TwoColumns(maze:Maze, other_constraints:bool=True):
    """carve a simple circuit"""
    grid = maze.grid
    assert isinstance(grid, OblongGrid)
    assert grid.m >= 2, "row constraint"
    assert grid.n == 2, "column constraint"
    for cell in grid:
        if cell.north:
            maze.link(cell, cell.north)
        i, j = cell.index
        if i in {0, grid.m-1}:
            if j == 0:
                maze.link(cell, cell.east)

def EvenEven(maze:Maze, other_constraints:bool=True):
    """carve the passages to make a maximally Eulerian maze

    This works on 4-connected rectangular and 4-connected toroidal grids
    with even numbers of rows and columns.
    """
    grid = maze.grid
    assert isinstance(grid, OblongGrid)
    assert grid.m % 2 == 0 and grid.m >= 2, "row constraint"
    assert grid.n % 2 == 0 and grid.n >= 2, "column constraint"
    if grid.m == 2:
        TwoRows(maze)
        return
    if grid.n == 2:
        TwoColumns(maze)
        return
    for cell in grid:
        if not is_black(cell):
            continue
        if in_interior(cell):
                    # link it to all of its orthogonal neighbors
            maze.link(cell, cell.south)
            maze.link(cell, cell.east)
            maze.link(cell, cell.north)
            maze.link(cell, cell.west)
            continue
        if on_south_border(cell):
            maze.link(cell, cell.east)
            if cell.west:
                maze.link(cell, cell.north)
        if on_east_border(cell):
            maze.link(cell, cell.south)
            if cell.north:
                maze.link(cell, cell.west)
        if on_north_border(cell):
            maze.link(cell, cell.west)
            if cell.east:
                maze.link(cell, cell.south)
        if on_west_border(cell):
            maze.link(cell, cell.north)
            if cell.south:
                maze.link(cell, cell.east)

def EvenOdd(maze:Maze, other_constraints=True):
    """carve the passages to make a maximally Eulerian maze

    This works on 4-connected rectangular grids with an even number of
    rows and an odd number of columns.
    """
    grid = maze.grid
    assert isinstance(grid, OblongGrid)
    assert grid.m % 2 == 0 and grid.m >= 2, "row constraint"
    assert grid.n % 2 == 1 and grid.n >= 3, "column constraint"
    if grid.m == 2:
        TwoRows(maze)
        return
    if grid.n == 3 and grid.m > 2:
        msg = f"EvenOdd: cannot construct Eulerian m={grid.m}>2 and n=3"
        if other_constraints:
            raise ValueError(msg)
        else:
            print("(WARNING)", msg)
    for cell in grid:
        if not is_black(cell):
            continue
#        print(cell.index)
        i, j = cell.index
        if in_interior(cell):
            if j != 1:
                    # link it to all of its orthogonal neighbors
                maze.link(cell, cell.south)
                maze.link(cell, cell.north)
            maze.link(cell, cell.east)
            maze.link(cell, cell.west)
            continue
        if on_south_border(cell):
            if j == 0:
                maze.link(cell, cell.east)
            else:
                maze.link(cell, cell.west)
            if grid.n - 1 > j >= 2:
                maze.link(cell, cell.north)
        if on_east_border(cell):
            maze.link(cell, cell.north)
            if cell.south:
                maze.link(cell, cell.west)
        if on_north_border(cell):
            if j == 1:
                maze.link(cell, cell.west)
            else:
                maze.link(cell, cell.south)
            maze.link(cell, cell.east)
        if on_west_border(cell):
            maze.link(cell, cell.north)
            if cell.south:
                maze.link(cell, cell.east)

def OddEven(maze:Maze, other_constraints=True):
    """carve the passages to make a maximally Eulerian maze

    This works on 4-connected rectangular grids with an odd number of
    rows and an even number of columns.
    """
    grid = maze.grid
    assert isinstance(grid, OblongGrid)
    assert grid.n % 2 == 0 and grid.n >= 2, "column constraint"
    assert grid.m % 2 == 1 and grid.m >= 3, "row constraint"
    if grid.n == 2:
        TwoColumns(maze)
        return
    if grid.m == 3 and grid.n > 2:
        msg = f"OddEven: cannot construct Eulerian m=3 and n={grid.n}>2"
        if other_constraints:
            raise ValueError(msg)
        else:
            print("(WARNING)", msg)
    for cell in grid:
        if not is_black(cell):
            continue
#        print(cell.index)
        i, j = cell.index
        if in_interior(cell):
            if i != 1:
                    # link it to all of its orthogonal neighbors
                maze.link(cell, cell.east)
                maze.link(cell, cell.west)
            maze.link(cell, cell.south)
            maze.link(cell, cell.north)
            continue
        if on_west_border(cell):
            if i == 0:
                maze.link(cell, cell.north)
            else:
                maze.link(cell, cell.south)
            if grid.m - 2 > i >= 2:
                maze.link(cell, cell.east)
        if on_north_border(cell):
            maze.link(cell, cell.east)
            if cell.west:
                maze.link(cell, cell.south)
        if on_east_border(cell):
            if i == 1:
                maze.link(cell, cell.south)
            else:
                maze.link(cell, cell.west)
            maze.link(cell, cell.north)
        if on_south_border(cell):
            maze.link(cell, cell.east)
            if cell.west:
                maze.link(cell, cell.north)

def OddOdd(maze:Maze, other_constraints=True):
    """carve the passages to make a maximally Eulerian maze

    This works on 4-connected rectangular grids with an odd number of
    rows and an odd number of columns.
    """
    grid = maze.grid
    assert isinstance(grid, OblongGrid)
    if grid.m == 1 == grid.n:
        return                  # trivially Eulerian

    assert grid.n % 2 == 1 and grid.n >= 3, "column constraint"
    assert grid.m % 2 == 1 and grid.m >= 3, "row constraint"
    if grid.m == 3 and grid.n == 3:
        msg = f"OddOdd: cannot construct Eulerian m={grid.m} and n={grid.n}"
        if other_constraints:
            raise ValueError(msg)
        else:
            print("(WARNING)", msg)
    for cell in grid:
        if not is_black(cell):
            continue
#        print(cell.index)
        i, j = cell.index
        if in_interior(cell):
            if (i, j) == (1, 1):
                    # link it to all of its orthogonal neighbors
                maze.link(cell, cell.north)
                maze.link(cell, cell.east)
            elif (i, j) == (grid.m-2, grid.n-2):
                maze.link(cell, cell.south)
                maze.link(cell, cell.west)
            else:
                maze.link(cell, cell.south)
                maze.link(cell, cell.east)
                maze.link(cell, cell.north)
                maze.link(cell, cell.west)
            continue
        if on_south_border(cell):
            if cell.west:
                maze.link(cell, cell.west)
            else:
                maze.link(cell, cell.east)
            if not on_east_border(cell) and not on_west_border(cell):
                maze.link(cell, cell.north)
        if on_east_border(cell):
            if cell.north:
                maze.link(cell, cell.north)
            else:
                maze.link(cell, cell.south)
            if not on_south_border(cell) and not on_north_border(cell):
                maze.link(cell, cell.west)
        if on_north_border(cell):
            if cell.east:
                maze.link(cell, cell.east)
            else:
                maze.link(cell, cell.west)
            if not on_east_border(cell) and not on_west_border(cell):
                maze.link(cell, cell.south)
        if on_west_border(cell):
            if cell.south:
                maze.link(cell, cell.south)
            else:
                maze.link(cell, cell.north)
            if not on_south_border(cell) and not on_north_border(cell):
                maze.link(cell, cell.east)

def maximally_Eulerian(rows:int, cols:int, *args,
                       GridType:"OblongGrid"=OblongGrid,
                       debug:bool=False,
                       constrain:bool=True,
                       **kwargs) -> Maze:
    """create a maximally Eulerian maze on a rectangular grid

    By default, the grid type is "OblongGrid", but a subclass can be used.
    But maximality is only guaranteed for the base class as the pattern of
    passages is fixed and depends only on the number of rows and columns.

    If additional arguments or keyword arguments are passed as argument,
    these will be passed as additional arguments to the grid constructor.
    """
    if not issubclass(GridType, OblongGrid):
        raise TypeError("Must be an OblongGrid subclass.")
    grid = GridType(rows, cols, *args, **kwargs)
    maze = Maze(grid)
    if rows % 2 == 0:       # EVEN (rows)
        maker = EvenEven if cols % 2 == 0 else EvenOdd
    else:                   # ODD (rows)
        maker = OddEven if cols % 2 == 0 else OddOdd
    maker(maze, other_constraints=constrain)
    if debug:
        check_vertex_degrees(maze)
    return maze

# END Grids.eulerian_oblong
