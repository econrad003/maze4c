# The Möbius strip grid

If we take a rectangular strip of newspaper and, with a half twist, tape a pair of opposite ends, we get a Möbius strip.  We can extend a rectangular grid into a Möbius strip grid by adding grid connections, by adding either W/E connections along the west and east boundary, or S/N connections along the south and north boundaries.  Of course, we need to take the half twist into account.

We give two examples.  We will use Aldous/Broder to create the mazes, in part because it has about the worst average case performance of our basic algorithms.  (The author is interested in how it fares in actual practice.)

We are following the cylindrical grid documentation closely in this example.  Read the two side-by-side compare the two grid layouts.

## Example 1 - an E/W Möbius maze

We start with a few imports (including the *unicode\_str* method).  Instead of the typical *OblongGrid* class or the *CylinderGrid* class, we import the *MoebiusGrid* class.
```
maze4c$ python
>>> from mazes.Grids.moebius import MoebiusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
>>> from mazes.console_tools import unicode_str
>>> maze = Maze(MoebiusGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1988
                             cells      150
                          passages      149
                     starting cell  (9, 7)
```

Now we label two carefully chosen cells.  (And yes, I did cheat by displaying the maze first!)
```
>>> cell = maze.grid[6, 0]
>>> cell.label = "A"
>>> cell.west.label = "W"
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
        |               |       |                   |
+---+---+   +   +---+   +---+   +   +---+---+---+   +   +   +
        |   |   |       |   |           |               |   |
+   +---+---+   +---+   +   +---+   +---+---+---+   +---+---+
    |               |           |   |       |               |
+---+---+---+---+   +   +---+---+---+---+   +   +   +   +---+
  A |   |   |   |   |       |                   |   |   |
+   +   +   +   +---+   +---+---+   +---+---+---+---+---+   +
|                   |   |   |           |               |   |
+   +---+---+---+   +   +   +---+---+   +---+---+   +   +   +
|           |                   |   |   |           |       |
+---+---+---+---+   +   +---+---+   +   +   +---+   +---+---+
    |   |       |   |               |   |   |           | W
+   +   +---+   +   +   +---+   +---+   +---+---+---+   +   +
|   |   |   |   |   |       |       |       |       |
+---+   +   +   +---+---+   +   +   +   +---+---+   +   +---+
|                           |   |   |                   |
+---+---+---+   +---+   +---+---+---+   +---+   +---+   +   +
        |       |               |       |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Notice that the cell that's west of the cell labelled "A" is not in the same row...  Well, as a result of that half twist, it actually is in the same row.  Labelling the physical rows helps to clear things up a bit:
```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9         ┃               ┃       ┃                   ┃         0
    ┣━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ┫
  8         ┃   ┃   ┃       ┃   ┃           ┃               ┃   ┃ 1
    ┣   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
  7     ┃               ┃           ┃   ┃       ┃               ┃ 2
    ┣━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━┫
  6   A ┃   ┃   ┃   ┃   ┃       ┃                   ┃   ┃   ┃     3
    ┣   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ┫
  5 ┃                   ┃   ┃   ┃           ┃               ┃   ┃ 4
    ┣   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ┫
  4 ┃           ┃                   ┃   ┃   ┃           ┃       ┃ 5
    ┣━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━┫
  3     ┃   ┃       ┃   ┃               ┃   ┃   ┃           ┃ W   6
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ┫
  2 ┃   ┃   ┃   ┃   ┃   ┃       ┃       ┃       ┃       ┃         7
    ┣━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
  1 ┃                           ┃   ┃   ┃                   ┃     8
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ┫
  0         ┃       ┃               ┃       ┃       ┃       ┃     9
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Here we labelled the rows on the right from top to bottom.  Row 6 and row 3 of the rectangle are, as a result of the all-important half twist, two parts of the same row in the Möbius strip.  As a rectangular lattice, this grid has 10 rows, but, topologically speaking, as a Möbius strip, there are only five rows.

## Example 2 - a N/S Möbius maze

Continuing with the imports above, we change the "axis" of the Möbius strip, so that the rectangle is taped north to south.
```
>>> maze = Maze(MoebiusGrid(10, 15, parity=True))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     2168
                             cells      150
                          passages      149
                     starting cell  (3, 2)
```

We label two carefully selected cells and display the maze:
```
>>> cell = maze.grid[0, 1]
>>> cell.label = "A"
>>> cell.south.label = "S"
>>> print(unicode_str(maze, s="A", n="R"))
  O   N   M   L   K   J   I   H   G   F   E   D   C   B   A
┏   ┳━━━┳   ┳   ┳   ┳━━━┳━━━┳   ┳   ┳   ┳━━━┳   ┳━━━┳   ┳   ┓
┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃     S ┃   ┃
┣━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ┫
┃   ┃   ┃   ┃       ┃       ┃   ┃   ┃   ┃   ┃   ┃           ┃
┣   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ┫
┃       ┃   ┃           ┃       ┃                   ┃       ┃
┣   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
┃   ┃   ┃   ┃       ┃       ┃       ┃   ┃   ┃       ┃       ┃
┣   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ┫
┃           ┃   ┃   ┃           ┃       ┃                   ┃
┣━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
┃           ┃           ┃                           ┃   ┃   ┃
┣   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ┫
┃           ┃       ┃   ┃   ┃       ┃   ┃           ┃   ┃   ┃
┣   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ┫
┃       ┃   ┃   ┃   ┃           ┃       ┃       ┃   ┃       ┃
┣━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃               ┃
┣━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━┫
┃   ┃ A         ┃                           ┃               ┃
┗   ┻   ┻━━━┻   ┻━━━┻   ┻   ┻   ┻━━━┻━━━┻   ┻   ┻   ┻━━━┻   ┛
  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```

Note here that, except for column H which consists of just 10 cells, the columns of the Möbius strip consist of two columns of the rectangle for a total of 20 cells each.  In particular, column N from bottom to top continues in column B, also from bottom to top.

## Example 3 - a warning

The half twist in a Möbius strip makes adapting rectangular grid algorithms much more difficult than for a cylindrical grid.  Let's look at just one example using simple *BinaryTree*.
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.moebius import MoebiusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.simple_binary_tree import BinaryTree
>>> maze = Maze(MoebiusGrid(10, 15))
>>> print(BinaryTree.on(maze))
          Simple Binary Tree (statistics)
                            visits      151
                             cells      150
                          passages      150
                            onward  east
                            upward  north
                              bias        0.5000
```
There are one too many passages to be a spanning tree (or perfect) maze.  So there is certainly a circuit some where in the maze.  Unlike the E/W cylinder, there isn't really a top row, as the top and bottom row are parts of the same physical row.  So finding the circuit may be tricky.
```
>>> print(unicode_str(maze, w="N", e="NR"))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9 ┃                                                             0
    ┣━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━┫
  8             ┃   ┃   ┃           ┃   ┃   ┃   ┃       ┃         1
    ┣   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━┫
  7     ┃       ┃   ┃   ┃           ┃   ┃   ┃       ┃             2
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  6 ┃                   ┃               ┃   ┃           ┃         3
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  5 ┃   ┃       ┃       ┃       ┃   ┃       ┃   ┃           ┃     4
    ┣   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
  4     ┃   ┃                   ┃   ┃   ┃       ┃       ┃       ┃ 5
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ┫
  3     ┃       ┃       ┃                   ┃   ┃               ┃ 6
    ┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  2             ┃   ┃           ┃   ┃                   ┃   ┃     7
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  1     ┃       ┃           ┃           ┃       ┃   ┃       ┃     8
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  0     ┃   ┃   ┃   ┃   ┃   ┃   ┃               ┃   ┃           ┃ 9
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

A good place to start is the top right at "X", moving *east* or *north*, dropping breadcrumbs (like Hansel and Gretel):
```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9 ┃                                 *   *   *   *   *   *   X > 0
    ┣━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━┫
  8             ┃   ┃   ┃           ┃ * ┃   ┃   ┃       ┃         1
    ┣   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━┫
  7     ┃       ┃   ┃   ┃           ┃ * ┃   ┃       ┃             2
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  6 ┃                   ┃     *   *   * ┃   ┃           ┃         3
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  5 ┃   ┃       ┃       ┃     * ┃   ┃       ┃   ┃           ┃     4
    ┣   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
  4     ┃   ┃ *   *   *   *   * ┃   ┃   ┃       ┃       ┃       ┃ 5
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ┫
  3     ┃     * ┃       ┃                   ┃   ┃               ┃ 6
    ┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  2   *   *   * ┃   ┃           ┃   ┃                   ┃   ┃     7
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  1   * ┃       ┃           ┃           ┃       ┃   ┃       ┃     8
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  0 > * ┃   ┃   ┃   ┃   ┃   ┃   ┃               ┃   ┃           ┃ 9
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Note that we can break this circuit anywhere and still leave a path.  If we do break the circuit, there are two possibilities, either:

1. the maze becomes perfect; or
2. there is another circuit and the resulting maze is disconnected.

Here we break the circuit to the *west* of "X", leaving a path from "X" to "Y".
```
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9 ┃                                 *   *   *   *   *   Y ┃ X > 0
    ┣━━━╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━┫
  8             ┃   ┃   ┃           ┃ * ┃ @ ┃ @ ┃ @   @ ┃         1
    ┣   ╋━━━╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━┫
  7     ┃       ┃   ┃   ┃           ┃ * ┃ @ ┃ @   @ ┃             2
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━┫
  6 ┃                   ┃     *   *   * ┃ @ ┃           ┃         3
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  5 ┃   ┃       ┃       ┃     * ┃ @ ┃ @   @ ┃   ┃           ┃     4
    ┣   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
  4     ┃   ┃ *   *   *   *   * ┃ @ ┃ @ ┃       ┃       ┃       ┃ 5
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ┫
  3     ┃     * ┃ @   @ ┃                   ┃   ┃               ┃ 6
    ┣━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  2   *   *   * ┃ @ ┃           ┃   ┃                   ┃   ┃     7
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
  1   * ┃ @   @ ┃           ┃           ┃       ┃   ┃       ┃     8
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ┫
  0 > * ┃ @ ┃ @ ┃   ┃   ┃   ┃   ┃               ┃   ┃           ┃ 9
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Now we make a few observations:

1. For all cells to the left and above the path, there is a path which ends in a breadcrumb.  We can find it by going *east* or *north* till we reach a breadcrumb.
2. To the right and below the path, we have marke a number of cell with "@".  Eac of these cells has an E/N path to a breadcrumb.
3. The remaining cells right and below have E/N paths leading to a cell in the rightmost column.  If that cell is to the left of the exits at either 8 or 9, then one step east leads to a breadcrumb.  If that cell's exit is at either 1, 2, 3, or 4, then east of the cell is a cell in the upper left.  (For the remaining cells, left of 5, 6, or 9, just continue *north*.)

So the resulting maze is now perfect:  Just follow an E/N path to a breadcrumb and continue along the E/N path to Y.  The maze is connected, and as a result of the wall we erected, it has one passage fewer than the number of cells.

Since the resulting maze is a spanning there are no cells of degree 4, *i.e.* no cells with 4 passages, the maze is also binary.

Questions for further study:

1. Can the simple binary tree algorithm produce a disconnected maze on the Möbius strip grid?
2. Is our choice of the placement of the circuit-breaking wall important or completely arbitrary?
3. Assuming that we have satisfactory answers to (1) and (2) for a given maze, is the resulting maze necessarily binary?

Answers to selected questions:

1. Yes it can.  Consider what happens in grid rows 1 and 8 if we always carve a passage "east".
