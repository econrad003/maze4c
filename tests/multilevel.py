"""
tests.multilevel - test the implementation of multilevel grids
Eric Conrad
Copyright ©2025 by Eric Conrad.  Licensed under GPL.v3.

DESCRIPTION

    This is a simple test of the multilevel grids module.
"""
from mazes.Grids.oblong import OblongGrid
from mazes.Grids.multilevel import MultistoryGrid
from mazes.maze import Maze
from mazes.Algorithms.wilson import Wilson

        # create the maze
stories = 4
rows, cols = 5, 9
maze = Maze(MultistoryGrid(stories, OblongGrid, rows, cols))
grid = maze.grid

assert stories == grid.levels
        # check the number of cells
for floor in range(grid.levels):
    assert len(grid.grid(floor)) == rows * cols
assert len(grid) == stories * rows * cols

elevators = list()

print("Create the main elevator shafts...")
SW, NE = (0,0), (rows-1,cols-1)
for index in {SW, NE}:
    for floor in range(grid.levels - 1):
        cell1 = grid.grid(floor)[index]
        cell1.label = "↑" if floor == 0 else "↕"
        cell2 = grid.grid(floor + 1)[index]
        if floor == grid.levels - 2: cell2.label = "↓"
        grid.make_elevator(cell1, cell2)
        elevator = ("main", floor, floor+1, cell1, cell2)
        elevators.append(elevator)
            # verification
        assert cell1["up"] == cell2, f"{floor=}, {index=}"
        assert cell2["down"] == cell1, f"{floor=}, {index=}"

print("Create the freight elevator shafts...")
SE, NW = (0,cols-1), (rows-1,0)
for index in {SE, NW}:
    cell1 = grid.grid(0)[index]
    cell1.label = "↑"
    cell2 = grid.grid(1)[index]
    cell2.label = "↓"
    grid.make_elevator(cell1, cell2)
    elevator = ("freight", 0, 1, cell1, cell2)
    elevators.append(elevator)
         # verification
    assert cell1["up"] == cell2, f"{floor=}, {index=}"
    assert cell2["down"] == cell1, f"{floor=}, {index=}"

print("Create the express elevator shaft...")
index = express = (rows//2,cols//2)
cell1 = grid.grid(0)[index]
cell1.label = "↑"
cell2 = grid.grid(-1)[index]
cell2.label = "↓"
grid.make_elevator(cell1, cell2)
elevator = ("express", 0, stories-1, cell1, cell2)
elevators.append(elevator)
    # verification
assert cell1["up"] == cell2, f"{floor=}, {index=}"
assert cell2["down"] == cell1, f"{floor=}, {index=}"

print("Carving the maze...")

print(Wilson.on(maze))
for elevator in elevators:
    name, from_floor, to_floor, cell1, cell2 = elevator
    if cell1.is_linked(cell2):
        continue
    cell1.label = "↧" if cell1.label == "↕" else "B"
    cell2.label = "↥" if cell2.label == "↕" else "B"

for i in range(grid.levels):
    print("FLOOR", i)
    print(grid.grid(i))
    for elevator in elevators:
        name, from_floor, to_floor, cell1, cell2 = elevator
        if from_floor != i:
            continue
        index1, index2 = cell1.index, cell2.index
        state = "active" if cell1.is_linked(cell2) else "inactive"
        print("\t", name, "elevator:", f"{from_floor}-{index1}",
              f"{to_floor}-{index2}", state)


