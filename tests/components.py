"""
tests.components - test the components module
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This module runs a few tests using the components module.

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
from mazes import rng, Cell
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.sidewinder import Sidewinder

from mazes.components import ComponentRegistry, GridComponents, MazeComponents

def test1(rows, cols):
    """make sure everything agrees with the usual oblong grid topology"""
    print(f"  test1({rows}, {cols})")
    maze = Maze(OblongGrid(rows, cols))

    print("    testing grid components... ", end="", flush=True)
    components = GridComponents(maze.grid)
    assert components.grid is maze.grid
    registry = components.registry
    assert len(registry) == 1           # just one component for the grid
    items = registry.components
    assert len(items) == 1
    component = set(registry.items_in(items[0]))
    assert len(component) == len(maze.grid)
    for cell in maze.grid:
        assert cell in component
        assert registry.component_for(cell) == items[0]
    print("pass!")
    print(f"      (k={len(items)} for grid)")

    print("        (before sidewinder)")
    print("    testing maze components... ", end="", flush=True)
    components = MazeComponents(maze)
    assert components.maze is maze
    registry = components.registry
    assert len(registry) == len(maze.grid)   # isolated cells
    items = registry.components
    assert len(items) == len(maze.grid)
    all_cells = set()
    for component in items:
        cells = set(registry.items_in(component))
        assert len(cells) == 1
        all_cells.update(cells)
    assert all_cells == set(maze.grid)
    print("pass!")
    print(f"      (k={len(items)} for empty maze)")

    print(Sidewinder.on(maze))
    print("        (after sidewinder)")
    print("    testing maze components... ", end="", flush=True)
    components = MazeComponents(maze)
    assert components.maze is maze
    registry = components.registry
    assert len(registry) == 1           # just one component for the maze
    items = registry.components
    assert len(items) == 1
    component = set(registry.items_in(items[0]))
    assert len(component) == len(maze.grid)
    for cell in maze.grid:
        assert cell in component
        assert registry.component_for(cell) == items[0]
    print("pass!")
    print(f"      (k={len(items)} for spanning tree)")

def test2():
    """a disconnected grid"""
    print("  test2() -- a disconnected grid")
    grid = OblongGrid(5, 5)
    foo = Cell(grid, "foo")
    bar = Cell(grid, "bar")
    foo["foobar"] = bar
    bar["barfoo"] = foo
    baz = Cell(grid, "baz")
    for cell in (foo, bar, baz):
        grid[cell.index] = cell
    print("    testing grid components... ", end="", flush=True)
    components = GridComponents(grid)
    assert components.grid is grid
    registry = components.registry
    assert len(registry) == 3           # three components for the grid
    items = registry.components
    assert len(items) == 3
    lengths = set()
    cells = set()
    for item in items:
    	cells.update(registry.items_in(item))
    	lengths.add(len(registry.items_in(item)))
    cells = set(grid)
    assert lengths == {1, 2, 25}
    print("pass!")
    print(f"      (k={len(items)} for grid)")


def main(rows, cols):
    """run some simple tests"""
    print("test mazes.components")
    test1(rows, cols)
    test2()
    print("SUCCESS!")

if __name__ == "__main__":
    main(34,55)

# end module tests.components