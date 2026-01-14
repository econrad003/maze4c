"""
demos.inform - demonstration of the maze/Inform 7 text converter
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

NOTE

    This is similar to module tests.inform, but more complete.

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

    # create a maze
maze = Maze(OblongGrid(4, 5))
grid = maze.grid
for j in (0, 2, 3):
    grid[1, j].hide()
grid[2, 3].hide()
grid[0, 0].hide()
grid[0, 1].hide()
print(BFS.on(maze, start_cell=grid[0, 2]))
    # label the rooms
grid[0,2].label = grid[0,3].label = grid[0,4].label = "S"
grid[1,4].label = grid[2,4].label = grid[3,4].label = "P"
grid[3,3].label = "L"
grid[2,2].label = "K"
grid[3,2].label = "D"
grid[1,1].label = grid[2,0].label = "B"
grid[2,1].label = grid[3,1].label = "H"
grid[3,0].label = "b"
    # make some changes
    #   we want the accesses to the bedrooms to be from the hallway
bathroom = grid[3,0]
if bathroom.is_linked(bathroom.south):
    join = bathroom.join_for(bathroom.south)
    maze.unlink(join)
    maze.link(bathroom.south, bathroom.south.east)
kitchen = grid[2,2]
if kitchen.is_linked(kitchen.west):
    join = kitchen.join_for(kitchen.west)
    maze.unlink(join)
    maze.link(kitchen.west, kitchen.west.north)
    # display the maze
print(maze)

    # prepare the room plan
plan = RoomPlan(maze)
things = Treasures(plan)
elm = tuple(plan[grid[0,j]] for j in {2, 3, 4})
elm[0].set("the cul-de-sac", description="The west end of Elm Street.")
elm[1].set("Elm Street", description="The street is deserted...")
things.new_treasure("the abandoned pickup truck", elm[1].cell, "fixed in place",
                    kind="enterable container",
                    description="Its tires are missing and" \
                    + " its doors have been stripped.")
elm[2].set("the dead end", description="Elm Street comes to an abrupt end" \
           + " in a sinkhole.")
things.new_treasure("the sinkhole", elm[2].cell, kind="scenery",
                    description="There is no way to get around it," \
                    + " but the walkway to the north seems to lead to a house.")
path = tuple(plan[grid[i,4]] for i in {1, 2, 3})
path[0].set("the south end of the path",
            description="The beginning of a paved walkway that seems to lead" \
            + " to a house to the north.")
things.new_treasure("the penny", path[0].cell,
                    description="People claim that they are an a good luck omen," \
                    + " but the research is inconclusive.")
path[1].set("the walkway",
            description="There seems to be a house to the north, and a" \
            + " street to the south.")
things.new_treasure("the gardener", path[1].cell, kind="woman", pronoun="she",
                    description="She stares at you with disdain.")
path[2].set("the north end of the path",
            description="The path countinues south.  To the east is the" \
            + " entrance to a house.")

salon = plan[grid[3,3]]
salon.set("the living room",
          "You are inside a ranch-style home.")
things.new_treasure("the sofa", salon.cell, "fixed in place",
                    kind="enterable supporter",
                    description="It looks comfortable, but it's quite large.")
dining = plan[grid[3,2]]
dining.set("the dining room",
          "You are in the dining room of a ranch-style home.")
things.new_treasure("the dinner table", salon.cell, "fixed in place",
                    kind="supporter",
                    description="It looks comfortable, but it's quite large.")
kitchen = plan[grid[2,2]]
kitchen.set("the modern kitchen", kind="kitchen")

hallway = tuple(plan[grid[i,1]] for i in {3, 2})
hallway[0].set("one end of the hallway", inverted=True)
hallway[1].set("the other end of the hallway", inverted=True)

bathroom = plan[grid[3,0]]
bathroom.set("the upscale bathroom", kind="bathroom")

bedroom = (plan[grid[2,0]], plan[grid[1,1]])
bedroom[0].set("the master bedroom")
things.new_treasure("the uncomfortable bed", bedroom[0].cell, "fixed in place",
                    kind="enterable supporter",
                    description="One side is too soft, the other too hard.")
bedroom[1].set("the little bedroom")
things.new_treasure("the comfortable bed", bedroom[1].cell, "fixed in place",
                    kind="enterable supporter",
                    description="Just right!")

locations = dict()
for item in things:
    room = things[item]
    if room not in locations:
        locations[room] = list()
    locations[room].append(item)

    # print the results

print('"The Goldilocks affair"')
print("\nPart 1 - Extensions")
print("\nInclude Modern Conveniences by Emily Short.")

print("\nPart 2 - Generated code")

def paragraphs(cell):
    """print paragraphs for each room"""
    room = plan[cell]
    print("\n" + room.paragraph)
    if room in locations:
        for item in locations[room]:
            print("\n" + things.paragraph(item, True))
unvisited = list(grid)
cell = elm[0].cell
unvisited.remove(cell)
paragraphs(cell)
unvisited.reverse()
while unvisited:
    cell = unvisited.pop()
    paragraphs(cell)

print("\nPart 3 - Additional things")
print("\nThe porridge is on the dining room table.  It is edible.")

print("\nPart 4 - Actions")

print("\nAfter entering the comfortable bed:")
print('\tsay "Some angry bears arrive suddenly.";')
print('\tend the story finally saying "RIP Goldilocks!".')

# END demos.inform
