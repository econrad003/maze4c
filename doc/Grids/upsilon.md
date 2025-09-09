# The upsilon grid

An *upsilon lattice* is a regular tiling of the plane using squares and regular octagons with a fixed side length.  Each octagon is diagonally adjacent to four octagons and orthogonally adjacent to four squares.  Conversely, each square is orthogonally adjacent to four octagons.

If we number the rows and columns and then take the *m* rows numbered *0* through *m-1* and the *n* columns numbered *0* through *n-1* we have a "rectangular" upsilon grid.

Here we have an upsilon grid with four rows and five columns that has an octagonal cell in the lower left.  The three octagonal cells in the interior each have eight neighboring cells, while the three interior square cells have four.  For our purposes, if the cell in the lower left is octagonal, we'll say the grid has even parity.  Cells with indices whose sum is even are octagonal.
```
         ---- column -----
    row  0   1   2   3   4
   ------------------------
     3   S - O - S - O - S     Legend:
         | / | \ | / | \ |        S = a square cell
     2   O - S - O - S - O        O = an octagonal cell
         | \ | / | \ | / |        | = vertical grid edge
     1   S - O - S - O - S        - = horizontal grid edge
         | / | \ | / | \ |        / = ascending diagonal grid edge
     0   O - S - O - S - O        \ = descending diagonal grid edge
```

If the cells whose indices sum to an even number are square, then the grid has odd parity. Note that this implies that the cell in the lower left is square:
```
         ---- column -----
    row  0   1   2   3   4
   ------------------------
     3   O - S - O - S - O
         | / | \ | / | \ |
     2   S - O - S - O - S
         | / | \ | / | \ |
     2   O - S - O - S - O
         | \ | / | \ | / |
     0   S - O - S - O - S
```

Upsilon grids are implemented in module *mazes.Grids.upsilon* as class *UpsilonGrid*.  A simple test module was written to verify the implementation -- it is module *tests.upsilon*.  It can be run from the working directory as:
```
    maze4c$ python -m tests.upsilon
```

Consider the following four-cell configuration from either diagram:
```
          O       O
            \   /
              O
              |
              S
```
That configuration suggests the letter Y in the Latin alphabet.  But the Latin letter Y was originally used to transliterate Greek words containing the Greek letter upsilon (majuscule Y, minuscule υ).  That is presumably how the lattice received its name.

The implementation is similar to the implementation of the rectangular grid class *OblongGrid*, so just a few examples should suffice.

## Example 1 - An even parity upsilon maze using Aldous/Broder

Why Aldous/Broder?

* I am interested in how well Aldous/Broder performs in practice on various grids.  Performance depends in part on the number of grid connections, and in part on how easy it is to disconnect the grid.  With a lot of connection, the walk simply gets lost.  If it is easy to disconnect the grid, the walk tends to get stuck in one of these separate regions.)

Even parity (*parity=False*) is the default.  Note that *int(False)* is *0*, which is even.

We start with the usual imports:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.upsilon import UpsilonGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
```

Then we create the grid and the empty maze object, and we run the carving algorithm:
```
>>> maze = Maze(UpsilonGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     2945
                             cells      150
                          passages      149
                     starting cell  (1, 13)
```

Performance note:

* Performance is similar to performance on the usual 4-connected (Von Neumann) rectangular grid.

Here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |   |   |       |           |       |       |   |
+---+   +   /   \   +   \---/---+---+   \   +   +---/---+   +
|           |   |       |       |       |   |   |           |
+---\---+---+---/---\---+---+---+   \---+---+   /   \---+   +
|   |   |       |           |   |   |   |       |   |   |   |
+   /---\---+---+---/---+---+---\---+   +   +---+---+---+---+
|       |   |   |               |   |   |       |   |       |
+---+---+---+   +---+---+---+   /---+   +---\---/---+---/   +
|       |   |       |   |           |   |               |   |
+---+   +   /---+---/---+---/---\---+   +   +---+---+---\---+
|   |   |       |       |   |   |   |   |   |   |   |   |   |
+   \   +---\---+---+   +---\   +---+---+   +   +   \   +   +
|   |   |   |       |   |           |   |       |   |       |
+   +---\   /---+   /---\---+   +---/   +---+---+   +---+---+
|   |       |           |   |       |   |                   |
+---+---+---+   +   +---+---\---/---+---/---+---/---+---+   +
|   |           |   |   |       |       |   |   |       |   |
+   /   +---+---+   +---\   +---\---+---+   +   +---+---\   +
|   |   |               |       |           |       |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Lots of diagonal passages!

In the even parity case, the cells whose indices sum to an even number have four diagonal neighbors.  The cell in the lower left (row 0 column 0) has a northeast grid connection to the cell in row 1 column 1.  In this run, Aldous/Broder chose this grid edge to carve a passage.

## Example 2 - An odd parity maze using Wilson's algorithm

For odd parity, we specify *parity=True* since *int(True)=1*.

```
maze4c$ python
Python 3.10.12
>>> from mazes.Algorithms.wilson import Wilson
>>> maze = Maze(UpsilonGrid(10, 15, parity=True))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       72
                             cells      150
                          passages      149
                 paths constructed       72
                     cells visited      497
                          circuits      104
                    markers placed      321
                   markers removed      172
                     starting cell  (9, 5)
```

Performance note:

* Again nothing noteworthy.

Here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |       |       |       |           |       |
+   \---+---+   +---\---/   +---+   +---/   +---/   \   +---+
|   |           |       |   |   |       |   |   |   |       |
+   +---+---+   +---+   \---+   \---+---+   +   \---+   \---+
|   |               |   |   |   |           |   |   |   |   |
+---+---+---+   +---\---+   +---+---+   +   +---+---+---/---+
|       |   |   |           |           |   |   |   |       |
+---+---\   /---+   +---\---+---+   +   +---/---+   +   \---+
|   |       |           |           |   |   |       |   |   |
+   +---+   +---/---+---+   +---/---+---/   \---/---\---/   +
|       |   |       |   |   |   |       |   |   |   |   |   |
+---+---\   +   +---+   \---+   +---+   +---+---+   +---+   +
|       |   |   |       |   |   |       |   |       |   |   |
+---+   +---+   +---+---/   \   +   +---+---\---/   +   +   +
|           |   |   |   |   |   |           |   |   |   |   |
+---/---+---+   +   +---+---/---+---/---+---/---+---/---+---+
|           |   |   |   |   |   |                   |       |
+   +---+---\   +   \   /---+   /---+   +---+---+---\---/   +
|       |       |   |       |       |               |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Again, lots of diagonal passages.  In this maze, if the indices sum to an odd number, the cell has four diagonal neighbors.  Note that the cell in row 1 column 0 has a diagonal passage to the cell in row 2 column 1.

## Example 3 - A depth-first upsilon maze

We can, of course, use other algorithms.  Any algorithm which works on a rectangular grid should work on the upsilon grid, though some will not be able to take advantage of the diagonal grid connections.  DFS is one that can.  We use it here on an even parity upsilon grid:

```
maze4c$ python
Python 3.10.12
>>> from mazes.Algorithms.dfs_better import DFS
>>> maze = Maze(UpsilonGrid(10, 15))
>>> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      299
                        start cell  (5, 5)
               maximum stack depth       89
                             cells      150
                          passages      149
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |                               |       |           |
+   +   +---+   +---+---+---+---+---+---\   +   +---/---+   +
|   |           |               |       |   |       |   |   |
+   +---+---+---+   +---+---+   +---+   +---+---+---+   +   +
|   |               |       |       |               |   |   |
+   /---+---+---+---+   +---+   +   +   +   +   +---/---\   +
|   |   |               |   |   |   |   |   |   |   |   |   |
+---+   /---\---+   +---/---\---/---+---/---+   +---\   +---+
|       |       |   |   |   |   |       |       |   |       |
+   +---+   +---+---+---+   +---+---+   \---+---\   +---+   +
|       |                           |   |   |           |   |
+---+   +---+---+   +---+---+---/---+---/   +---+   +---+   +
|   |   |   |       |   |               |   |   |   |       |
+   +---\   +---\---/---\---+---+---+   +---/   +---/---+---+
|   |       |   |   |   |           |   |   |   |   |   |   |
+   +   +---+   +---+   +---+---+   +---/---+   /---+   /   +
|   |       |   |       |       |   |       |   |       |   |
+   +---+   /   +---+   \---+   +   +---+   +---+---+---+   +
|           |           |       |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

With a maximum stack depth of 89, we expect a longest path to be 88 steps in length, comprising 88 cells and 89 passages.  Time to call on Mr Dijkstra:
```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> dijkstra.distance(target)
88
```

Here is the maze with a labelled longest path:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
| *   * |     *   *   *   *   *   *   * | *   * |     *   * |
+   +   +---+   +---+---+---+---+---+---\   +   +---/---+   +
| * | *   *   * | *   *   *   * |       | * | *   * |   | * |
+   +---+---+---+   +---+---+   +---+   +---+---+---+   +   +
| * | *   *   *   * |       | *   * |               | * | * |
+   /---+---+---+---+   +---+   +   +   +   +   +---/---\   +
| * |   | *             | * |   | * |   |   |   | * |   | * |
+---+   /---\---+   +---/---\---/---+---/---+   +---\   +---+
| *   * | *   * |   | S |   | * |       |       |   | *   * |
+   +---+   +---+---+---+   +---+---+   \---+---\   +---+   +
| *   * | *   *   *                 |   |   |           | * |
+---+   +---+---+   +---+---+---/---+---/   +---+   +---+   +
|   | * |   | *   * | * |               |   | * |   | *   * |
+   +---\   +---\---/---\---+---+---+   +---/   +---/---+---+
|   | *   * |   | * |   | *   *   * |   | * | * | * |   |   |
+   +   +---+   +---+   +---+---+   +---/---+   /---+   /   +
|   | *   * | * |     * | T   * | * | *   * | * |       |   |
+   +---+   /   +---+   \---+   +   +---+   +---+---+---+   +
|         * | *   *   * | *   * | *   *   *                 |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The path covers 3/5 of the maze.  It appears to use most of the available diagonal passages.

## Example 4 - A breadth-first upsilon maze

Breadth-first search produces what are probably the most boring mazes, but the resulting mazes can help to unlock some of the grid's secrets.  The path to any cell from the algorithm's starting cell will be a minimum length grid path to that cell.  Bear in mind the Dijkstra's algorithm is, at its heart, a breadth-first search.
```
>>> from mazes.Algorithms.bfs import BFS
>>> maze = Maze(UpsilonGrid(10, 15))
>>> print(BFS.on(maze))
          Breadth-first Search (BFS) (statistics)
                            visits      150
                        start cell  (6, 13)
              maximum queue length       20
                             cells      150
                          passages      149
```
The queue length is related both the length of a path and to the size of neighborhoods.  There is not much hope of deducing specific information about the maze from the maximum queue length.

Here is the maze.  Note that there are many diagonal passages -- the diagonal passages are shortcuts.  DFS hates shortcuts, so the maze in Example 3 tends to avoid them.  But BFS loves shortcuts:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |       |       |       |   |   |   |   |   |
+---+---\---+---\---+---\---+---\---+---\   +---\   +   +   +
|   |       |       |       |       |       |   |   |   |   |
+---\---+---\---+---\---+---\---+---\---+---\   +---\   /---+
|       |       |       |       |       |       |   |       |
+---+---\---+---\---+---\---+---\---+---\---+---\   +   +---+
|   |       |       |               |       |               |
+---\---+---\---+---\---/---+---/---\---+---\---/   +   +   +
|       |       |       |       |               |   |   |   |
+---+---\---/---\---/---+---/---+---/---+---/   +---/   \---+
|           |       |       |       |       |   |   |   |   |
+---+---/---+---/---+---/---+---/---+---/   +---/   \---+   +
|       |       |       |       |       |   |   |   |   |   |
+---/---+---/---+---/---+---/---+---/   +---/   \---+   \---+
|   |       |       |       |       |   |   |   |   |   |   |
+---+---/---+---/---+---/---+---/   +---/   +   +   \---+   +
|       |       |       |       |   |   |   |   |   |   |   |
+---/---+---/---+---/---+---/   +---/   +---/   \---+   \---+
|   |       |       |       |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
And now Mr Dijkstra will take the stage:
```
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> dijkstra.distance(target)
19
```
Note that the queue stores cells.  A longest path consists of 20 cells and 19 passages.
The diameter is 18, so longest paths are 18 steps in length, and consist of 19 cells and 18 passages.

Longest paths in a BFS maze pass through the BFS starting cell, so we should label that as well.
```
>>> maze.grid[6,13].label = 'X'
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |       |       |       |   |   |   |   |   |
+---+---\---+---\---+---\---+---\---+---\   +---\   +   +   +
|   |       |       |       |       |       |   |   |   |   |
+---\---+---\---+---\---+---\---+---\---+---\   +---\   /---+
|       |       |       |       |       |       |   |       |
+---+---\---+---\---+---\---+---\---+---\---+---\   +   +---+
| T |       |       |     *   *   * |       |     *   X     |
+---\---+---\---+---\---/---+---/---\---+---\---/   +   +   +
|     * |     * |     * |       |     *   *   * |   | * |   |
+---+---\---/---\---/---+---/---+---/---+---/   +---/   \---+
|         * |     * |       |       |       |   | * |   |   |
+---+---/---+---/---+---/---+---/---+---/   +---/   \---+   +
|       |       |       |       |       |   | * |   |   |   |
+---/---+---/---+---/---+---/---+---/   +---/   \---+   \---+
|   |       |       |       |       |   |   |   | * |   |   |
+---+---/---+---/---+---/---+---/   +---/   +   +   \---+   +
|       |       |       |       |   |   |   |   |   | * |   |
+---/---+---/---+---/---+---/   +---/   +---/   \---+   \---+
|   |       |       |       |   |   |   |   |   |   |   | S |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Note that the path from S to T is primarily along diagonal passages.  The BFS algorithm had a lot of choices along this path, but the best choice was normally a diagonal.

## Example 5 - Recursive division on an upsilon grid using watersheds

The basic recursive division algorithm cannot take advantage of the diagonal connections.  But watersheds can.

We import the needed classes and create an empty grid:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.upsilon import UpsilonGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.watershed_division import WatershedDivision
>>> maze = Maze(UpsilonGrid(10, 15))
```

And now we carve the maze:
```
>>> print(WatershedDivision.on(maze, 2, 3))
          Watershed Recursive Division (statistics)
                            visits      332
                             cells      150
                          passages        0
                             links      149
                           unlinks        0
                             doors      149
                         max stack        9
                       extra pumps        0
                  watershed errors        0
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |               |   |   |       |       |
+---/---+---+---+   /   +   +---+   /   +   +   +   +   +---+
|   |   |       |   |   |       |   |   |   |   |   |       |
+---\   +---+   +---+---+   +---+---+   +   +---/---+---+   +
|   |   |   |   |       |           |   |           |   |   |
+   /---+   +---\   +---\---/---+---+   +---+---+   +   +   +
|   |   |       |   |       |       |   |   |   |       |   |
+   +   /   +   +---\---+---\---/---+---+---\   /---+---+   +
|   |   |   |       |   |       |           |   |           |
+   +   +---+   +---/---+   +---+   +   +---+   +---+   +   +
|   |       |           |       |   |   |               |   |
+   +---+   \---+   +---+---+   +   +   +   +---+---+---+   +
|   |       |   |           |       |       |   |   |       |
+   +---+---+   +---+   \---+   +---+---+---/   +   +---\---+
|       |   |   |       |   |   |       |   |   |   |       |
+---+   +   \---+---+---+   +   /   \---+---\---+---\   +---+
|   |   |   |   |           |   |   |   |   |           |   |
+   +   +   +---\   +   +   +   +---/---\   +---+---+---+   +
|               |   |   |   |   |   |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
