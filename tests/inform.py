"""
tests.inform - test the maze/Inform 7 text converter
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
from mazes.Algorithms.bfs import BFS
from mazes.Inform.room import Room, RoomPlan
from mazes.Inform.treasure import Treasures

    # create a maze with some hidden nodes
maze = Maze(OblongGrid(4, 4))
for j in (0, 1, 2):
    maze.grid[1, j].hide()
maze.grid[2, 2].hide()
print(BFS.on(maze, start_cell=maze.grid[0, 0]))
print(maze)

    # check some basics
rooms = RoomPlan(maze)
assert maze == rooms.maze
assert maze.grid == rooms.grid
grid = maze.grid
for cell in grid:
    room = rooms[cell]
    assert type(room) == Room
    i,j = cell.index
    expected = f"Room_{i}_{j}"
    assert room.name == expected, f"{room.name=}, {expected=}"

    # name change
room = rooms[grid[0,0]]
room.name = "the landing site"
expected = "the landing site"
assert room.name == expected, f"{room.name=}, {expected=}"

expected = '"There are passages west."'
assert room.description == expected, f"{room.description=}, {expected=}"

room.description = "The quick brown fox!"
expected = '"The quick brown fox![paragraph break]There are passages west."'
assert room.description == expected, f"{room.description=},\n\t{expected=}"

print(room.paragraph)

treasures = Treasures(rooms)
gold = "the gold brick"
treasures.new_treasure(gold, grid[0,0], description="It's shiny!")
print(treasures.paragraph(gold))
print(treasures.paragraph(gold, here=True))
sofa = "the old sofa"
treasures.new_treasure(sofa, grid[0,0], "enterable", kind="supporter")
print(treasures.paragraph(sofa))
print(treasures.paragraph(sofa, here=True))
women = "the young ladies"
treasures.new_treasure(women, None, kind="women",
    description="They eye you with suspicion.", pronoun="they", is_are="are")
print(treasures.paragraph(women))
print(treasures.paragraph(women, here=True))

print()
print("Rooms:")
for room in rooms:
    print(f"\t{room.paragraph}")

print()
print("Treasures and other things:")
for treasure in treasures:
    print(f"\t{treasures.paragraph(treasure)}")

# END tests.inform
