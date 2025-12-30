# Tools inspired by Herman Tulleken's blog post

The blog post may be found here:

* https://www.gamedeveloper.com/programming/algorithms-for-making-more-interesting-mazes

The blog's focus is on mazes used in games like Minecraft or DigDug.  These mazes use rectangular grids with the usual four-neighbor Von Neumann configuration.  The idea here is to generalize the blog's basic ideas to arbitrary grids.

This document consists of the following examples:

1. A test run illustrating the features
2. A programmer look at the test run
3. A tile-based demonstration (2×2)
4. A tile-based demonstration (3×3)
5. A tile-based demonstration (3×3)

The first two examples are long and detailed -- they cover the inner workings.  Examples 3 through 5 give a brief sketch -- they are intended as examples of how one might use the partitioning tool to create a maze for a game.  Additional examples may be added at a later date.

## Example 1.  Test run, with annotations

Here is the sample run, with some interruptions...
```
$ python -m tests.tulleken
Importing the toolset...
```
### The tools

The grid is partitioned into pillars, walls and rooms.  Pillars are basically collections of cells that are never linked.  Walls are cells that might be linked.  Rooms are cells that can be linked to cells in other rooms, but only through a wall.  Neighboring cells in the same rooms can optionally be linked to one another.

The maze here is a five-row eleven-column rectangular maze.  Pillars are placed in the leftmost and rightmost column.  There are three rooms, namely a ground floor, a basement, and a mine.  The ground floor and the basement are carved, but the mine is not.

The ground floor and the basement are separated by a wall (called the floor) which has an optional passageway called the steps.

The basement and the mine are separated by a wall (called the wall).  Any of the cells in the wall might be used as a passage from the basement into the mine.

```
Initializing the partition...
Creating some pillars...
Creating the rooms...
    Ground floor (level 0) - room 0;
    Basement (level B) - room 1;
    Mine (level M) - room 2;
Creating the walls...
    Floor (wall F with door S) - wall 3;
    Mine Wall (wall W) - wall 4;
```

At this point we need to link up the three rooms.  Essentially that means opening the steps and creating and opening an access panel to the mine. We'll use Wilson's algorithm.  The carving is done on an auxiliary maze containing exactly one cell for each room and exactly one cell for each wall:
```
Carving auxiliary maze...
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits        1
                             cells        5
                          passages        4
                 paths constructed        1
                     cells visited        5
                          circuits        0
                    markers placed        4
                   markers removed        0
                     starting cell        0
```

Here is the GraphViz dot representation of the maze:
```
Auxiliary maze:
digraph D {
"3" -> "1" [dir="none"]
"4" -> "1" [dir="none"]
"3" -> "0" [dir="none"]
"4" -> "2" [dir="none"]
}
    len(partition.skeleton.grid)=5
```
The auxiliary maze contains five cells, namely 3 rooms and 2 walls.  Here is a visualization of the actual layout:
```
            GROUND FLOOR (0)
                 ━┓                 (4)
                  ┗━┓                ║
               (3)  ┗━ BASEMENT (1)  ║   MINE (2)
                                     ║
```
Once the access panel to the mine has been selected the solution is unique: the maze carving algrorithm must "open" the steps and open the access panel.  Here is what the maze actually looks like:
```
Final maze:
+---+---+---+---+---+---+---+---+---+---+---+
| P | 0   0   0   0   0   0   0   0   0 | P |
+---+   +---+---+---+---+---+---+---+---+---+
| P | S | F | F | F | F | F | F | F | F | P |
+---+   +---+---+---+---+---+---+---+---+---+
| P | B   B   B   B   W   M | M | M | M | P |
+---+   +   +   +   +---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+   +   +   +   +---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+---+---+---+---+---+---+---+---+---+---+
Legend:
    P - pillars
    0 - ground floor; B - basement; M - mine
    F - floor; S - steps down; W - wall
```
Note that the steps are adjacent to the ground floor and to the basement.  There is also an opening in the wall which is adjacent to both the basement and the mine.  The pillars on the side are just dead cells.

Note that the steps and the wall access have been closed.  The ground floor and the basement are carved and the mine is not.  The carving of rooms was handled by the partitioning tool.  Wilson's algorithm was only concerned with the potential wall openings, namely the stairs and the access panel in the basement wall.

We want to make this work with passage carvers and with wall builders.  So we close everything up:
```
Undoing everything...
Empty maze:
+---+---+---+---+---+---+---+---+---+---+---+
| P | 0   0   0   0   0   0   0   0   0 | P |
+---+---+---+---+---+---+---+---+---+---+---+
| P | S | F | F | F | F | F | F | F | F | P |
+---+---+---+---+---+---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+   +   +   +   +---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+   +   +   +   +---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+---+---+---+---+---+---+---+---+---+---+
```

And now we open everything back up.  Note that the partition establishes the location of the access panel, so the resulting maze is the same as before.
```
Redo everything...
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits        3
                             cells        5
                          passages        4
                 paths constructed        3
                     cells visited        7
                          circuits        0
                    markers placed        4
                   markers removed        0
                     starting cell        1
Empty maze:
+---+---+---+---+---+---+---+---+---+---+---+
| P | 0   0   0   0   0   0   0   0   0 | P |
+---+   +---+---+---+---+---+---+---+---+---+
| P | S | F | F | F | F | F | F | F | F | P |
+---+   +---+---+---+---+---+---+---+---+---+
| P | B   B   B   B   W   M | M | M | M | P |
+---+   +   +   +   +---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+   +   +   +   +---+---+---+---+---+---+
| P | B   B   B   B | W | M | M | M | M | P |
+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 2.  Programming with the tool

We start with some imports.  We will need a grid, a maze, a passage carver, and the Tulleken partitioning tool.
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.wilson import Wilson
>>> from mazes.tools.tulleken import Tulleken
```

We create a maze object and feed it into the partitioning tool:
```
>>> maze = Maze(OblongGrid(5,11))
>>> partition = Tulleken(maze)
```

At this point all cells are available and none have been allocated.
```
>>> len(partition.unvisited), len(partition.visited), len(maze.grid)
(55, 0, 55)
```

Here is the declaration for method *create\_pillar()*:
```python
    def create_pillar(self, cells:"iterable", check:bool=False):
        pass
```
The *check* option checks to see whether the cells that were supplied form a grid-connected subset.  For pillars, it nomally shouldn't matter, so the default is to omit the check.

Let's put up some pillars:
```
>>> partition.create_pillar(maze.grid[i,0] for i in range(5))
>>> partition.create_pillar(maze.grid[i,10] for i in range(5))
```

We allocated 10 cells, so 45 cells are unallocated.
```
>>> len(partition.unvisited), len(partition.visited), len(maze.grid)
(45, 10, 55)
```

We haven't allocated any rooms or walls, so the allocated cells are all pillars.  Let's label them suggestively:
```
>>> for cell in partition.visited:
...     cell.label = "█"
...
>>> print(maze)
      1   2   3   4   5   6   7   8   9
+---+---+---+---+---+---+---+---+---+---+---+
| █ |   |   |   |   |   |   |   |   |   | █ | 4
+---+---+---+---+---+---+---+---+---+---+---+
| █ |   |   |   |   |   |   |   |   |   | █ | 3
+---+---+---+---+---+---+---+---+---+---+---+
| █ |   |   |   |   |   |   |   |   |   | █ | 2
+---+---+---+---+---+---+---+---+---+---+---+
| █ |   |   |   |   |   |   |   |   |   | █ | 1
+---+---+---+---+---+---+---+---+---+---+---+
| █ |   |   |   |   |   |   |   |   |   | █ | 0
+---+---+---+---+---+---+---+---+---+---+---+
```
(The row and column labels were added.)

Now let's divide the remainder of the grid into four rooms.  The rooms will be a kitchen, a living room (the "salon"), a dining room, and a teenager's bedroom.  The first three rooms are devoid of clutter and the last is completely cluttered.  We need to be sure that the rooms are separated by walls, so we will verify the layout before we actually partition the grid.
```
>>> kitchen = set()
>>> salon = set()
>>> for i in range(2):
...     for j in range(1, 5):
...         kitchen.add(maze.grid[i,j])
...         salon.add(maze.grid[i,j+5])
...
>>> for cell in kitchen:
...     cell.label = "K"
...
>>> for cell in salon:
...     cell.label = "S"
...
>>> dining = set()
>>> bedroom = set()
>>> for i in range(3, 5):
...     for j in range(1, 5):
...         dining.add(maze.grid[i,j])
...         bedroom.add(maze.grid[i,j+5])
...
>>> for cell in dining:
...     cell.label = "D"
...
>>> for cell in bedroom:
...     cell.label = "B"
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+
| █ | D | D | D | D |   | B | B | B | B | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | D | D | D | D |   | B | B | B | B | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ |   |   |   |   |   |   |   |   |   | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | K | K | K | K |   | S | S | S | S | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | K | K | K | K |   | S | S | S | S | █ |
+---+---+---+---+---+---+---+---+---+---+---+
```
To create a room, we use the *create\_room()* method:
```python
    def create_room(self, cells:"iterable", carve:bool=True,
                    check:bool=True) -> int:
        pass
```
Checking for connectedness is recommended for rooms.  We can also optionally carve out the room.  Carving is the default -- the bedroom is cluttered, so we won't carve it.  The method returns an index which we will need when we create the walls.

This looks good, so let's partition accordingly:
```
>>> kitchen = partition.create_room(kitchen)
>>> salon = partition.create_room(salon)
>>> dining = partition.create_room(dining)
>>> bedroom = partition.create_room(bedroom, carve=False)
>>> len(partition.unvisited), len(partition.visited), len(maze.grid)
(13, 42, 55)
```
Now we need to create the connecting walls.  First let's add some icons to our maze.
```
>>> for i in range(5):
...     maze.grid[i,5].label = "|"
...
>>> for j in range(1,10):
...     maze.grid[2,j].label = "="
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+
| █ | D   D   D   D | | | B | B | B | B | █ |
+---+   +   +   +   +---+---+---+---+---+---+
| █ | D   D   D   D | | | B | B | B | B | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | = | = | = | = | █ | = | = | = | = | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | K   K   K   K | | | S   S   S   S | █ |
+---+   +   +   +   +---+   +   +   +   +---+
| █ | K   K   K   K | | | S   S   S   S | █ |
+---+---+---+---+---+---+---+---+---+---+---+
```
Let place a pillar in the center.  Note that we need an iterable.  We will enclose the cell in braces to form a set:
```
>>> partition.create_pillar({maze.grid[2,5]})
```

For our wall, we use method *create\_wall()*:
```python
    def create_wall(self, cells:"iterable",
                    room1:int, room2:int, door:Cell=None,
                    check:bool=False) -> int:
        pass
```
The connectedness check is optional.  We can also specify a door, or we can let the partition tool find a door.  We identify the room by their indices.  Note that we have 12 unallocated cells:
```
>>> len(partition.unvisited), len(partition.visited), len(maze.grid)
(12, 43, 55)
```
Four of these are in column 5.  We will place doors at the top and bottom:
```
>>> wall1 = set(maze.grid[i,5] for i in {0,1})
>>> door1 = maze.grid[0,5]
>>> wall1 = partition.create_wall(wall1, kitchen, salon, door=door1)
>>> wall2 = set(maze.grid[i,5] for i in {3,4})
>>> door2 = maze.grid[4,5]
>>> wall2 = partition.create_wall(wall2, dining, bedroom, door=door2)
>>> door1.label = door2.label = "*"
>>> len(partition.unvisited), len(partition.visited), len(maze.grid)
(8, 47, 55)
```

And we have eight cells left in row 2...  We will let the partition choose the north-south bedroom door:
```
>>> wall3 = set(maze.grid[2,j] for j in {1,2,3,4})
>>> door3 = maze.grid[2,1]
>>> door3.label = "*"
>>> wall3 = partition.create_wall(wall3, kitchen, dining, door=door3)
>>> wall4 = set(maze.grid[2,j] for j in {6,7,8,9})
>>> wall4 = partition.create_wall(wall4, salon, bedroom)
>>> len(partition.unvisited), len(partition.visited), len(maze.grid)
(0, 55, 55)
```
Now let's locate that last door.  First we need to find the cell in the auxiliary maze that corresponds to the wall:
```
>>> aux_cell = partition.wall(wall4)
>>> type(aux_cell)
<class 'mazes.tools.tulleken.WallCell'>
```
There is an attribute *door* which is a vector consisting of a door cell, a set of neighbors on one side, and a set of neighbors on the other.  For the rectangular grid, both sets are singletons.
```
>>> door4, nbrs1, nbrs2 = aux_cell.door
>>> door4.label = "*"
>>> door4.index
(2, 6)
>>> len(nbrs1), len(nbrs2)
(1, 1)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+
| █ | D   D   D   D | * | B | B | B | B | █ |
+---+   +   +   +   +---+---+---+---+---+---+
| █ | D   D   D   D | | | B | B | B | B | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | * | = | = | = | █ | * | = | = | = | █ |
+---+---+---+---+---+---+---+---+---+---+---+
| █ | K   K   K   K | | | S   S   S   S | █ |
+---+   +   +   +   +---+   +   +   +   +---+
| █ | K   K   K   K | * | S   S   S   S | █ |
+---+---+---+---+---+---+---+---+---+---+---+
```

Now let's create the maze:
```
>>> print(Wilson.on(partition.skeleton))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits        4
                             cells        8
                          passages        7
                 paths constructed        4
                     cells visited       11
                          circuits        0
                    markers placed        7
                   markers removed        0
                     starting cell        0
```
There are 8 cells in the auxiliary maze (the property *skeleton*), namely the four rooms and the four walls.  The maze was created by carving just seven passages.  We need to transfer the changes to the primary maze (using the *update()* method).  Then we can look at the final result.
```
>>> partition.update()
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+
| █ | D   D   D   D   *   B | B | B | B | █ |
+---+   +   +   +   +---+---+---+---+---+---+
| █ | D   D   D   D | | | B | B | B | B | █ |
+---+   +---+---+---+---+---+---+---+---+---+
| █ | * | = | = | = | █ | * | = | = | = | █ |
+---+   +---+---+---+---+   +---+---+---+---+
| █ | K   K   K   K | | | S   S   S   S | █ |
+---+   +   +   +   +---+   +   +   +   +---+
| █ | K   K   K   K   *   S   S   S   S | █ |
+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 3 - a tile based demonstration (2×2)

Some simple demonstrations have been set up in the demonstration module *demos.tulleken*.  The first involves 2×2 tiles of the following form:
```
    +---+---+
    | W | P |       LEGEND:
    +---+---+           W - wall
    |   | W |           P - pillar
    +---+---+           blank - room
```
The "wall" cells act as double doors.  The pillars are cells that stay out of play.  If we place two tiles side by side or one atop the other, we can see one way to work with them:
```
    Tile 1  Tile 2         Figure 3.1(a)
    +---+---+---+---+         Two side-by-side tiles
    | W | P | W | P |
    +---+---+---+---+
    | x | W | y | W |
    +---+---+---+---+

                Figure 3.1(b)
                    Ways to link the walls

    Solution 1          Solution 2          Solution 3
    +---+---+---+---+   +---+---+---+---+   +---+---+---+---+
    | P | P | P | P |   | P | P | P | P |   | P | P | P | P |
    +---+---+---+---+   +---+---+---+---+   +---+---+---+---+
    | x       y | P |   | x     | y | P |   | x |     y | P |
    +---+---+---+---+   +---+---+---+---+   +---+---+---+---+
    x and y connected   not connected       not connected
```
There are four outcomes for a wall in this type of tile.  Consider the first wall in the bottom row.  It might be linked to both its neighbors (Solution 1) or to just one of its neighbors (Solutions 2 and 3).  In the former case a path of length 2 is established between the rooms that it connects.

Another possibility is that the wall becomes a pillar.  This will happen when the wall has just one neighboring room.  Note that if the number of rows or the number of columns is even, then the maze will necessarily have (respectively) a top row or a roghtmost column consisting of pillars. With an odd length or width, we can cut the tile in half or in quarters to produce an extra room.

Our example shows the result using an 8×13 grid after running vertex Prim on the auxiliary maze.  The number of rows is even, so the walls in the top row have been changed to pillars.  In the rightmost columm, we used 2×1 tiles of the following form:
```
    +---+
    | W |
    +---+
    |   |
    +---+
```

Here is the demonstration output.
```
$ python -m demos.tulleken -p 0
          Vertex Growing Tree (statistics)
                            visits      145
                        start cell       66
                             cells       73
                          passages       72
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| █ | █ | █ | █ | █ | █ | █ | █ | █ | █ | █ | █ | █ |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |               |                       |
+   +---+   +---+   +---+   +---+   +---+   +---+   +
|   | █ |   | █ |   | █ |   | █ |   | █ |   | █ |   |
+   +---+   +---+   +---+---+---+   +---+---+---+   +
|       |                   |               |       |
+   +---+   +---+   +---+---+---+   +---+---+---+   +
|   | █ |   | █ |   | █ |   | █ |   | █ |   | █ |   |
+   +---+   +---+   +---+   +---+   +---+   +---+   +
|               |                               |   |
+   +---+   +---+   +---+   +---+   +---+---+---+---+
|   | █ |   | █ |   | █ |   | █ |   | █ |   | █ |   |
+   +---+---+---+   +---+---+---+   +---+   +---+   +
|   |               |                               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Our maze consists of:
```
             4 × 7 = 28 room cells
             4 × 6 = 24 horizontal wall cells
             3 × 7 = 21 vertical wall cells
        3 × 6 + 13 = 31 pillars
```
Adding these up, we have:
```
       28 + 24 + 21 = 73 cells in the auxiliary maze
            73 + 31 = 104 = 8 × 13 cells in the displayed maze
```
If we discard the pillars, then we expect 72 passages in a perfect maze.

## Example 4 - a tile based demonstration (3×3)

A larger tile was used for this example:
```
    +---+---+---+
    | P | W   P |
    +---+---+---+
    |       | W |
    +---+   +---+
    | P |   | P |
    +---+---+---+
```
The cells are labelled P for pillars, W for walls, and blank for the cells that form a room.  Note that the room is connected.

We use the tile as our plan for an 8×13 rectangular maze.
```
$ python -m demos.tulleken -p 1
          Vertex Growing Tree (statistics)
                            visits       57
                        start cell       15
                             cells       29
                          passages       28
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                           | █ | █ |
+---+   +---+---+   +---+---+   +---+---+   +---+---+
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |
+---+   +---+---+   +---+---+   +---+---+   +---+---+
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |
+---+---+---+---+   +---+---+---+---+---+   +---+---+
|                               |           | █ | █ |
+---+   +---+---+   +---+---+   +---+---+   +---+---+
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |
+---+---+---+---+   +---+---+---+---+---+   +---+---+
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |
+---+   +---+---+   +---+---+   +---+---+   +---+---+
|                               |           | █ | █ |
+---+   +---+---+   +---+---+   +---+---+   +---+---+
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

If we increase the number of columns by 1, we get rid of the two ugly columns of pillars:
```
$ python -m demos.tulleken -d 8 14 -p 1
          Vertex Growing Tree (statistics)
                            visits       73
                        start cell        0
                             cells       37
                          passages       36
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |                           |                   |
+---+   +---+---+   +---+---+   +---+---+   +---+---+   +
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |   |
+---+   +---+---+   +---+---+   +---+---+   +---+---+---+
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |   |
+---+   +---+---+---+---+---+   +---+---+   +---+---+   +
|                                               |       |
+---+   +---+---+   +---+---+   +---+---+   +---+---+   +
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |   |
+---+   +---+---+   +---+---+   +---+---+   +---+---+   +
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |   |
+---+   +---+---+   +---+---+   +---+---+---+---+---+   +
|       |           |                                   |
+---+   +---+---+   +---+---+   +---+---+   +---+---+   +
| █ |   | █ | █ |   | █ | █ |   | █ | █ |   | █ | █ |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Example 5 - a tile based demonstration (3×3)

The previous example has a lot of pillars.  We can modify the tile to reduce the number of pillars without creating any circuits:
```
    +---+---+---+
    |     W   P |
    +   +---+---+
    |       | W |
    +---+   +---+
    | P |       |
    +---+---+---+
```

Here is the result:
```
$ python -m demos.tulleken -d 8 14 -p 2
          Vertex Growing Tree (statistics)
                            visits       73
                        start cell        1
                             cells       37
                          passages       36
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |           |                       |
+---+   +---+---+   +   +---+   +   +---+   +---+---+   +
| █ |       | █ |       | █ |       | █ |       | █ |   |
+---+---+---+---+   +---+---+   +---+---+   +---+---+---+
|       | █ |       | █ |   |   | █ |   |   | █ |   |   |
+   +---+---+   +---+---+   +---+---+   +   +---+   +   +
|       |           |           |                       |
+---+   +---+---+   +   +---+   +---+---+   +---+---+   +
| █ |       | █ |       | █ |       | █ |       | █ |   |
+---+   +---+---+   +---+---+---+---+---+   +---+---+   +
|       | █ |       | █ |   |   | █ |   |   | █ |   |   |
+   +---+---+   +---+---+   +   +---+   +   +---+   +---+
|       |               |       |                       |
+---+   +   +---+   +---+---+   +   +---+   +---+---+   +
| █ |       | █ |       | █ |       | █ |       | █ |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
For the top two rows, the top row of the tile was ignored. Similarly, in the rightmost 2 columns, the rightmost column of the tile was ignored.

If we had included the lower left corner of the tile in our rooms, then the rooms would all contain circuits.  If we had included the top right corner, we would instead have disconnected rooms.