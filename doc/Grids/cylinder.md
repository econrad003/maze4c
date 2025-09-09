# The cylindrical grid

If we take a rectangular strip of newspaper and, without twisting, tape a pair of opposite ends, we get a cylinder.  We can extend a rectangular grid into a cylinder by adding grid connections, by adding either W/E connections along the west and east boundary, or S/N connections along the south and north boundaries.

We give two examples.  We will use Aldous/Broder to create the mazes, in part because it has about the worst average case performance of our basic algorithms.  (The author is interested in how it fares in actual practice.)

## Example 1 - An E/W cylindrical maze

We start (as usual) with a few imports.  In this case, we need the *CylinderGrid* class, the vanilla *Maze* class, and an *Algorithm* subclass -- *AldousBroder* for this example.  We then create the grid and maze objects and run the algorithm:
```
maze4c$ python
Python
>>> from mazes.Grids.cylinder import CylinderGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
>>> maze = Maze(CylinderGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1580
                             cells      150
                          passages      149
                     starting cell  (3, 12)
```
Run-time performance was acceptable for a 10x15 cylindrical grid...

For purposes of illustrating the use of tape, we will label a cell on the west boundary wall and its neighbor on the east boundary wall:
```
>>> cell = maze.grid[8, 0]
>>> cell.label = "A"
>>> cell.west.label = "W"
```

And now the labelled maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |                           |               |
+---+   +---+---+---+   +   +   +   +---+   +---+---+   +---+
  A |           |       |   |   |   |   |   |           | W
+   +---+   +---+---+   +---+   +---+   +   +---+---+   +---+
|       |       |       |       |       |   |       |       |
+   +---+   +---+   +   +---+   +---+   +---+   +---+---+   +
|   |           |   |   |   |   |                   |       |
+   +   +   +---+---+---+   +   +---+---+---+---+   +   +---+
        |   |                   |       |   |   |       |
+   +---+---+---+---+---+   +   +   +---+   +   +   +   +   +
|                           |   |       |   |       |   |   |
+---+   +   +---+---+---+---+   +---+   +   +---+   +   +   +
|       |       |                           |       |       |
+   +---+---+---+---+---+---+---+---+---+   +---+---+   +---+
|       |       |                   |               |       |
+---+---+---+   +---+   +---+   +---+   +---+   +   +   +---+
|           |           |               |       |   |       |
+   +---+   +---+   +   +---+---+---+   +---+   +---+---+   +
    |           |   |               |   |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
This run created three passages of which each joined a cell along the west boundary wall to a cell along the east boundary wall.

We can also illustrate this using the *unicode\_str* method:
```
>>> from mazes.console_tools import unicode_str
>>> print(unicode_str(maze, h="N"))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
  9 ┃               ┃                           ┃               ┃ 9
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  8   A ┃           ┃       ┃   ┃   ┃   ┃   ┃   ┃           ┃ W   8
    ┣   ╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━┫
  7 ┃       ┃       ┃       ┃       ┃       ┃   ┃       ┃       ┃ 7
    ┣   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  6 ┃   ┃           ┃   ┃   ┃   ┃   ┃                   ┃       ┃ 6
    ┣   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋━━━┫
  5         ┃   ┃                   ┃       ┃   ┃   ┃       ┃     5
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ┫
  4 ┃                           ┃   ┃       ┃   ┃       ┃   ┃   ┃ 4
    ┣━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ┫
  3 ┃       ┃       ┃                           ┃       ┃       ┃ 3
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
  2 ┃       ┃       ┃                   ┃               ┃       ┃ 2
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋━━━┫
  1 ┃           ┃           ┃               ┃       ┃   ┃       ┃ 1
    ┣   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ┫
  0     ┃           ┃   ┃               ┃   ┃               ┃     0
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Each cell in the first column has a grid neighbor to the *west* in the last column.  Conversely each cell in the last column has a grid neighbor to the *east* in the first column.  The respective neighbors are in the same row.

## Example 2 - An N/S cylindrical maze

We repeat, this time orienting the cylinder vertically instead of horizontally. As before, we create the grid and maze objects, and run the carving algorithm.  The difference is the *parity=True* option: if *parity* is *False* (the default), the cylinder is horizontal (i.e. its axis is vertical); and if *parity* is *True*, the cylinder is vertical, with a horizontal axis.

```
>>> maze = Maze(CylinderGrid(10, 15, parity=True))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1534
                             cells      150
                          passages      149
                     starting cell  (7, 1)
```

After looking at the maze, we label two carefully chosen cells:
```
>>> cell = maze.grid[0, 4]
>>> cell.label = "A"
>>> cell.south.label = "S"
```

And now we display the maze:
```
>>> print(unicode_str(maze, v="A"))
  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
┏   ┳━━━┳   ┳━━━┳   ┳━━━┳   ┳━━━┳━━━┳   ┳   ┳   ┳━━━┳   ┳━━━┓
┃       ┃   ┃     S ┃                   ┃   ┃   ┃           ┃
┣   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
┃       ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃           ┃       ┃
┣   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━┫
┃           ┃       ┃       ┃   ┃   ┃           ┃   ┃       ┃
┣   ╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ┫
┃       ┃       ┃       ┃   ┃           ┃   ┃   ┃       ┃   ┃
┣   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━┫
┃   ┃       ┃                   ┃   ┃           ┃       ┃   ┃
┣   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋   ┫
┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃       ┃           ┃
┣━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ┫
┃       ┃       ┃   ┃   ┃                   ┃       ┃   ┃   ┃
┣   ╋━━━╋   ╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋━━━┫
┃           ┃           ┃   ┃                   ┃           ┃
┣━━━╋━━━╋━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ┫
┃       ┃   ┃       ┃   ┃       ┃       ┃   ┃   ┃   ┃   ┃   ┃
┣━━━╋   ╋   ╋━━━╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋━━━┫
┃       ┃         A ┃       ┃   ┃       ┃                   ┃
┗   ┻━━━┻   ┻━━━┻   ┻━━━┻   ┻━━━┻━━━┻   ┻   ┻   ┻━━━┻   ┻━━━┛
  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
```
The chosen cells were in column E, *i.e.* column 4.  The passage *south* from cell (0, 4) in the bottom row, labelled "A", leads to cell (9, 4) in the top row, labelled "S" for *south*.

## Example 3 - a warning

### 3A) E/W cylinder

Algorithms designed for the standard rectangular grid (*OblongGrid* class) will typically fail on the cylindrical grid.  We will illustrate using the simple *BinaryTree* class.

```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.cylinder import CylinderGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.simple_binary_tree import BinaryTree
>>> maze = Maze(CylinderGrid(10, 15))
>>> print(BinaryTree.on(maze))
          Simple Binary Tree (statistics)
                            visits      151
                             cells      150
                          passages      150
                            onward  east
                            upward  north
                              bias        0.5000
```
We immediately see a problem.  The algorithm carved one too many passages, so the maze cannot be a spanning tree.  Looking at the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

+---+---+   +   +---+---+---+---+   +---+---+---+   +   +---+
            |   |                   |               |   |
+---+---+   +   +---+   +---+---+---+   +   +---+   +---+---+
            |   |       |               |   |       |
+---+   +   +---+   +---+   +   +---+   +   +   +   +---+   +
|       |   |       |       |   |       |   |   |   |       |
+---+---+   +   +   +   +   +---+   +   +   +   +---+---+---+
            |   |   |   |   |       |   |   |   |
+---+   +   +---+---+   +   +---+---+   +---+   +   +   +   +
|       |   |           |   |           |       |   |   |   |
+   +---+---+---+---+---+---+---+---+---+---+   +   +   +---+
    |                                           |   |   |
+   +   +   +---+   +   +   +   +   +---+   +---+   +---+   +
|   |   |   |       |   |   |   |   |       |       |       |
+---+   +---+---+   +---+   +   +   +---+   +---+   +---+---+
        |           |       |   |   |       |       |
+---+   +   +---+---+   +---+---+   +   +   +---+   +   +---+
        |   |           |           |   |   |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Look at the top row: the top row is a circuit.  Since we created an E/N binary tree on an E/W cylinder, this is exactly what should happen.  There is an *east* connection but no *north* connection in every cell in the top row, so the algorithm says go *east*.  This "error" is inevitable.

Note that none of the other rows happens to be a circuit.  So we could fix this maze by simply erecting one wall somewhere in the top row.

But there is another problem, even though it didn't surface here.  In one of the other rows, we might have chosen to go *east* in every cell.  That would cause the maze to be disconnected as, from cells in the chosen row and rows below, there would be no path to the top row.  Again, this woould be fixable as we could simply choose one cell, erect a wall to the *east* and carve a passage north.

There are several take-aways:

1. The algorithm may guarantee that certain problems occur;
2. Some problems may be intermittent;
3. Some problems may be fixable; and
4. It may be possible to adapt the algorithm.

The success of (4) depends on the nature of the problems that arise in (1) and (2) and how they might be avoided or fixed.

In the case of simple binary tree, the adaptation here is to guarantee for each row that there is some cell where one cannot go east.

### 3B) N/S cylinder

Now let's look at a N/S cylinder.  Here we immediately see that the rightmost column will inevitably form a circuit.  This will result in an extra passage.  Other columns may also (but intermittently) form circuits that result in a disconnected maze.

```
>>> maze = Maze(CylinderGrid(10, 15, parity=True))
>>> print(BinaryTree.on(maze))
          Simple Binary Tree (statistics)
                            visits      151
                             cells      150
                          passages      150
                            onward  east
                            upward  north
                              bias        0.5000
>>> print(maze)
+---+---+---+   +---+   +   +---+   +   +---+   +---+---+   +
|               |       |   |       |   |       |           |
+---+---+---+   +---+---+   +---+   +   +   +   +---+---+   +
|               |           |       |   |   |   |           |
+   +   +---+---+   +   +---+---+   +   +   +---+---+---+   +
|   |   |           |   |           |   |   |               |
+---+   +---+   +---+   +   +   +   +   +---+   +---+   +   +
|       |       |       |   |   |   |   |       |       |   |
+   +---+   +   +   +---+   +   +---+---+---+   +---+   +   +
|   |       |   |   |       |   |               |       |   |
+---+---+---+   +   +   +   +---+   +   +---+   +   +---+   +
|               |   |   |   |       |   |       |   |       |
+   +   +---+---+   +   +   +   +---+---+---+   +---+---+   +
|   |   |           |   |   |   |               |           |
+   +---+---+   +   +   +---+   +---+---+---+---+---+   +   +
|   |           |   |   |       |                       |   |
+   +---+---+   +   +---+---+---+   +   +---+---+   +   +   +
|   |           |   |               |   |           |   |   |
+   +---+   +---+   +   +---+---+   +---+   +---+   +   +   +
|   |       |       |   |           |       |       |   |   |
+---+---+---+   +---+   +   +---+   +   +---+   +---+---+   +
```

We did not see the intermittent problem, but we do have the inevitable extra passage in the last column.  With 10 cells and a bias of 1/2, the probability for a particular column other the last to form a circuit is:
```
    (1/2)^10 = 1/1024
```
We can raise this probability by raising the bias.  With a bias of 9/10, the probability is a little more than 1/3:
```
    (9/10)^10 = 3,486,784,401/10,000,000,000 = 0.348...
```

With 15 columns (14 plus the last), we can expect (*i.e.* on average) about 4 or 5 such circuits.  In our solo trial experiment, we got three:
```
>>> maze = Maze(CylinderGrid(10, 15, parity=True))
>>> print(BinaryTree.on(maze, bias=0.9))
          Simple Binary Tree (statistics)
                            visits      151
                             cells      150
                          passages      150
                            onward  east
                            upward  north
                              bias        0.9000
>>> print(maze)
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +---+   +---+---+   +   +   +   +   +   +   +   +   +
|   |   |       |           |   |   |   |   |   |   |   |   |
+---+   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|       |   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |       |   |   |   |   |   |   |   |   |   |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |       |   |   |   |   |   |   |   |   |   |
+---+   +   +   +   +   +   +   +   +   +   +---+   +   +   +
|       |   |   |   |   |   |   |   |   |   |       |   |   |
+   +---+   +   +   +   +   +   +   +   +---+   +   +   +   +
|   |       |   |   |   |   |   |   |   |       |   |   |   |
+   +   +   +---+   +---+   +   +   +   +---+   +   +---+   +
|   |   |   |       |       |   |   |   |       |   |       |
+   +   +   +   +   +   +---+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |       |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +---+   +   +   +   +   +
|   |   |   |   |   |   |   | 1 | 2 |       |   | 3 |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
```
(We don't count the last column since that circuit was inevitable.)

Our maze is disconnected with four components.  Of course we could fix this by choosing a random cell in each circuit column, erecting a wall to the *north*, and, if possible, carving a passage *east*.  Here we will do this manually.  Using a random number generator, my four random integers z : 0≤z≤9 are 4, 8, 9, and 8.
```
+   +   +   +   +   +   +   +   +   +   +   +   +---+   +   +
|   |   |   |   |   |   |   |   |   |   |   |   | C     |   |
+   +   +---+   +---+---+   +   +---+   +   +   +   +   +---+
|   |   |       |           |   | B     |   |   |   |   | D |
+---+   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|       |   |   |   |   |   |   |   |   |   |   |   |   |   |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |       |   |   |   |   |   |   |   |   |   |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |       |   |   |   |   |   |   |   |   |   |
+---+   +   +   +   +   +   +---+   +   +   +---+   +   +   +
|       |   |   |   |   |   | A     |   |   |       |   |   |
+   +---+   +   +   +   +   +   +   +   +---+   +   +   +   +
|   |       |   |   |   |   |   |   |   |       |   |   |   |
+   +   +   +---+   +---+   +   +   +   +---+   +   +---+   +
|   |   |   |       |       |   |   |   |       |   |       |
+   +   +   +   +   +   +---+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |       |   |   |   |   |   |   |   |
+   +   +   +   +   +   +   +   +   +---+   +   +   +   +   +
|   |   |   |   |   |   |   | 1 | 2 |       |   | 3 |   |   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +   +   +
```
And now we have a simple E/N binary tree maze on a N/S cylinder grid.  Easy-peasy.  The proof is simple: starting from any cell, go *north* until you find a passage *east*.  Repeat until you reach the last column.  In the last column, go north until you reach cell "D".

For example, from cell "E":
```
+   +   +   +   +   +   +   +   +   + ^ +   +   +---+ ^ +   +
|   |   |   |   |   |   |   |   |   | * |   |   | *   * |   |
+   +   +---+   +---+---+   +   +---+   +   +   +   +   +---+
|   |   |       |           |   | B   * |   |   | * |   | D |
+---+   +   +   +   +   +   +   +   +   +   +   +   +   +   +
|       |   |   |   |   |   |   |   | E |   |   | * |   | * |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |       |   |   |   |   |   |   | * |   | * |
+   +   +   +   +---+   +   +   +   +   +   +   +   +   +   +
|   |   |   |   |       |   |   |   |   |   |   | * |   | * |
+---+   +   +   +   +   +   +---+   +   +   +---+   +   +   +
|       |   |   |   |   |   | A     |   |   | *   * |   | * |
+   +---+   +   +   +   +   +   +   +   +---+   +   +   +   +
|   |       |   |   |   |   |   |   |   |     * |   |   | * |
+   +   +   +---+   +---+   +   +   +   +---+   +   +---+   +
|   |   |   |       |       |   |   |   | *   * |   | *   * |
+   +   +   +   +   +   +---+   +   +   +   +   +   +   +   +
|   |   |   |   |   |   |       |   |   | * |   |   | * |   |
+   +   +   +   +   +   +   +   +   +---+   +   +   +   +   +
|   |   |   |   |   |   |   | 1 | 2 | *   * |   | 3 | * |   |
+   +   +   +   +   +   +   +   +   + ^ +   +   +   + ^ +   +

Legend:
    * breadcrumbs
    ^ continuing north (top row to bottom row, same column)
```
