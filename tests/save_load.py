"""
mazes.save_maze - test save/load a maze to/from a file
Eric Conrad
Copyright ©2024 by Eric Conrad.  Licensed under GPL.v3.

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
import os
import csv
from mazes.Grids.upsilon import UpsilonGrid
from mazes.maze import Maze
from mazes.edge import Edge

    # create the test maze
maze = Maze(UpsilonGrid(2, 4, parity=True))
maze.link(maze.grid[1,0], maze.grid[0,1], weight=7)
maze.link(maze.grid[0,1], maze.grid[0,2], directed=True)
if os.path.isfile("spam.csv"):
    print("Deleting spam.csv...")
    os.remove("spam.csv")
print("Sample Maze:")
print(maze)

print("Save Maze:")
from mazes.save_maze import save_to
save_to(maze, "spam.csv")

print("="*10, "spam.csv", "="*10)
with open("spam.csv") as spam:
    for line in spam:
        print(line[:-1])
print("="*10, "END FILE", "="*10)

print("Hint for Creating Copy:", end=' ')
from mazes.load_maze import load_from, hint_from
load_from("spam.csv")
assert hint_from("spam.csv") == "UpsilonGrid(2, 4, parity=True)"

print("Attempt to copy maze:")
maze = Maze(UpsilonGrid(2, 4, parity=True))
load_from("spam.csv", maze)
print(maze)

print("Verifying...")
assert len(maze) == 2       # Two joins
assert maze.grid[1,0].is_linked(maze.grid[0,1])     # both ways A -- B
assert maze.grid[0,1].is_linked(maze.grid[1,0])     # both ways B -- A
assert maze.grid[0,1].is_linked(maze.grid[0,2])     # one way A -> B
assert not maze.grid[0,2].is_linked(maze.grid[0,1]) # one way, not B -> A

for join in maze:
    if type(join) == Edge:
        assert join.weight == 7
    else:
        assert join.weight == 1

print("cleaning up... (deleting spam.csv)")
os.remove("spam.csv")

print("SUCCESS!")

# end module tests.save_load
