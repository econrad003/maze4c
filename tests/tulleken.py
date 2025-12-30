"""
tests.tulleken - test the implementation of Herman Tulleken's toolset
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
from mazes.Grids.oblong import OblongGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson

print("Importing the toolset...")
from mazes.tools.tulleken import Tulleken

print("Initializing the partition...")
maze = Maze(OblongGrid(5,11))
partition = Tulleken(maze)

print("Creating some pillars...")
partition.create_pillar(maze.grid[i,0] for i in range(5))
partition.create_pillar((maze.grid[i,10] for i in range(5)), check=True)
assert len(partition.visited) == 10
for cell in partition.visited:
    cell.label = "P"

print("Creating the rooms...")
ground = set(maze.grid[4,j] for j in range(1,10))
for cell in ground:
    cell.label = "0"
ground = partition.create_room(ground)
print(f"    Ground floor (level 0) - room {ground};")
assert len(partition.visited) == 19, f"{len(partition.visited)=}"

basement = set()
mine = set()
for i in range(3):
    for j in range(1, 5):
        cell = maze.grid[i,j]
        basement.add(cell)
        cell.label = "B"
        cell = maze.grid[i,j+5]
        mine.add(cell)
        cell.label = "M"
basement = partition.create_room(basement)
print(f"    Basement (level B) - room {basement};")
assert len(partition.visited) == 31, f"{len(partition.visited)=}"
mine = partition.create_room(mine, carve=False)
print(f"    Mine (level M) - room {mine};")
assert len(partition.visited) == 43, f"{len(partition.visited)=}"

print("Creating the walls...")
floor = set(maze.grid[3,j] for j in range(1,10))
for cell in floor:
    cell.label = "F"
steps = maze.grid[3,1]
steps.label = "S"
floor = partition.create_wall(floor, ground, basement, door=steps)
print(f"    Floor (wall F with door S) - wall {floor};")

wall = set(maze.grid[i,5] for i in range(3))
for cell in wall:
    cell.label = "W"
wall = partition.create_wall(wall, mine, basement)
print(f"    Mine Wall (wall W) - wall {wall};")

assert len(partition.unvisited) == 0, f"{len(partition.unvisited)=}"

print("Carving auxiliary maze...")
print(Wilson.on(partition.skeleton))

print("Auxiliary maze:")
print(partition.skeleton.grid.graphviz_dot)
print(f"    {len(partition.skeleton.grid)=}")

partition.update()

print("Final maze:")
print(maze)
print("Legend:")
print("    P - pillars")
print("    0 - ground floor; B - basement; M - mine")
print("    F - floor; S - steps down; W - wall")

print("Undoing everything...")
partition.skeleton.unlink_all()
partition.update()
print("Empty maze:")
print(maze)
print("Legend:")
print("    P - pillars")
print("    0 - ground floor; B - basement; M - mine")
print("    F - floor; S - steps down; W - wall")

print("Redo everything...")
print(Wilson.on(partition.skeleton))
partition.update()
print("Empty maze:")
print(maze)
print("Legend:")
print("    P - pillars")
print("    0 - ground floor; B - basement; M - mine")
print("    F - floor; S - steps down; W - wall")

# END tests.tulleken
