# The 8-connected rectangular grid

The usual rectangular or oblong grid uses a Von Neumann or 4-neighborhood of a cell.  The interior cells have neighbors to the south, east, north and west.  if we add in the nearest cells on the diagonals, we have Moore or 8-neighborhoods of each interior cell.  Instead of treating the cells as square, we think of them as regular octagons even though the plane cannot actually be tiled by regular octagons.

The implementation is class *MooreGrid* in module *oblong8.py* located in the *mazes/Grids* folder.  We may variously refer to this class of grids as Moore grids, rectangular Moore grids, 8-grids, rectangular 8-grids, and 8-connected rectangular grids.

The constructor takes the numbers of rows and columns, and an optional keyword argument *configure* which we use to create several subgrid classes.

## 1 - Algorithms

   Any method that is designed for a Von Neumann rectangular grid can be used to carve a maze on a Moore grid, but, if our desire is to produce perfect mazes (*i.e.* spanning trees), there is not much point in that. The more general algorithms can, of course, be used.  We will consider the uniform maze algorithms (Aldous/Broder and Wilson), depth-first search, and Kruskal's algorithm.

## Example 1.1 - Aldous/Broder

Aldous/Broder generally performs reasonably on the 4-grid small enough to fit on an 80x25 console display -- roughly the same on the 8-grid.  The additional grid connections don't make it much harder to complete the random walk.

We start, of course, by importing a few things:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong8 import MooreGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.aldous_broder import AldousBroder
```

Next we create the maze and run Aldous/Broder:
```
>>> maze = Maze(MooreGrid(10, 15))
>>> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     3087
                             cells      150
                          passages      149
                     starting cell  (4, 8)
```

Here is the resulting maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |       |   |   |       |       |       |   |   |   |
+---/---X---+---/---+   +   +---/---+---\---\---+---X   +   +
|   |       |   |   |       |   |   |   |       |   |       |
+---/---+---/   +---X   +---+---\---X---+---/---/---/---+   +
|           |       |   |       |       |       |   |   |   |
+---+---/   +---/   \---+   +   +---+---+---\---+   /---+---+
|   |   |   |   |   |   |   |       |       |   |   |       |
+---X---\---+---+---+---+---\---+   /---+---+---/   \---/   +
|   |   |       |   |   |       |   |       |   |   |   |   |
+   /---+---+---\---X---\---/   \---/---/---\---+---\---\---+
|       |       |   |   |   |   |   |   |   |   |       |   |
+---+---+---/---+   +   /---/---+---+---/---/---\---\---+---+
|       |   |   |   |   |           |   |   |   |   |       |
+---/   \   /---\---\---+---\---+   +---X   X---+---\   +   +
|   |   |       |   |       |   |   |   |   |   |   |   |   |
+---+---+---/   \---\   +---+---+---/---+---/   \---\---+---+
|   |   |   |   |   |   |       |       |   |   |           |
+   \   X---+---+---/---/---/---/---+---+---/   +---\---+---+
|   |   |   |           |   |           |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The slashes and backslashes represent northeastward and northwestward passages, respectfully.  If both are present from a cell, the passage crossing is represented by a capital X.  (This particular run produced 8 passage crossings.)

### Example 1.2 - Wilson's algorithm

Wilson's algorithm offers no unpleasant surprises on the 8-grid.  We start with an import:
```
>>> from mazes.Algorithms.wilson import Wilson
```

Next we create the grid and run Wilson:
```
>>> maze = Maze(MooreGrid(10, 15))
>>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       77
                             cells      150
                          passages      149
                 paths constructed       77
                     cells visited      637
                          circuits      133
                    markers placed      427
                   markers removed      278
                     starting cell  (5, 11)
```
This run was uneventful.  Here is the maze:

```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |       |   |   |   |   |   |   |           |   |
+---+   +---+   +---+---\---X---/---\---X---+---X---+---/---+
|                       |       |   |   |   |   |       |   |
+---+---\---+   \---+---\---\---+---X---+---X---+---+---\   +
|   |   |   |   |   |       |   |   |       |   |   |   |   |
+---\   +---+   +---+   \---+   +---+---+---+   /---/   +   +
|           |   |   |   |       |       |   |   |   |   |   |
+   +---+---\---/---+---/---\---+---/---+   /---+---+   /---+
|       |   |       |   |   |   |   |           |   |   |   |
+---+---+---\   +   /---/---/---\---\---+---X---/---/---+   +
|   |       |   |       |   |   |   |       |               |
+   +   +---+---+   +   +---\---\---\---+---+---/   \---+---+
|   |       |   |   |   |   |   |       |       |   |   |   |
+---\   \---/---+---+   +---\---+---+---/---/---+---\---+   +
|   |   |   |       |   |           |   |   |       |   |   |
+   /   +---+---\---\---\---+---+   /---\---\---+---\---\   +
|   |           |   |   |   |       |   |   |   |   |   |   |
+---+---/---\---+---/   X---\   +   /---+---+---\   X---+---+
|           |       |   |   |   |               |   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Again there were 8 crossing diagonal passages...

### Example 1.3 - Depth-first search

Because there are more connections than in the 4-grid, we would expect to go deeper before we are blocked.

```
>>> from mazes.Algorithms.dfs_better import DFS
>>> maze = Maze(MooreGrid(10, 15))
>>> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      299
                        start cell  (3, 1)
               maximum stack depth       93
                             cells      150
                          passages      149
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |       |   |       |               |   |   |
+   +---+---/---X---+---X   +---\---X---+---/---+---\---X   +
|   |       |       |   |   |   |   |   |   |       |   |   |
+   \---\---+---+---+   +---/---\---+---+---\   +---\---+   +
|   |   |   |   |       |   |   |           |   |       |   |
+   +---X---/---/---+---+   /---\---+---+   +   +   +---+---+
|   |   |   |       |   |   |   |   |   |   |   |   |       |
+   +   +   +---+   +   \---/---+   +   \   +   +---\---X---+
|   |   |       |   |   |   |       |   |   |   |   |   |   |
+---+   +---/---+   +   +---/---+---+   +---+---/---\---X---+
|       |       |   |   |   |       |       |       |   |   |
+---\---+   +   /---+---\---X---+   \---+   +---+   +---/---+
|   |   |   |   |   |   |   |       |   |   |   |   |   |   |
+   +---+---\---+   X---\---+---+---+---X---/   /---+---X---+
|           |   |   |   |               |   |   |   |   |   |
+---+---\---+   +   +---\---+---+---+---+---+---/---X---X---+
|       |   |   |   |   |   |   |   |       |   |   |   |   |
+---\---X---+---X---X---\---X   +   /   +---+---X---+---/   +
|       |       |   |   |   |   |   |           |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Here we have 17 diagonal passage crossings.  The maximum stack depth tells us that the longest path has 93 cells and 92 passages giving us a diameter of 92.  

### Example 1.4 - Kruskal's algorithm

We start in the usual way:
```
>>> from mazes.Algorithms.kruskal import Kruskal
>>> maze = Maze(MooreGrid(10, 15))
>>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      277
                 components (init)      150
               queue length (init)      527
                             cells      150
                          passages      149
                components (final)        1
              queue length (final)      250
```
Nothing alarming in these statistics... And here is the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |   |       |           |   |       |       |   |
+---+---+   /   +---+   X---+   +---/---+---\---\---/---\   +
|   |   |   |       |   |   |   |   |       |   |   |   |   |
+---X---/   +---+   +---+---\---+---\---/   /---+   X---+   +
|   |   |       |   |   |           |   |       |   |   |   |
+   /---+---\---+---+---\   +---/---+---\---+---+---+---+---+
|   |   |   |           |   |       |       |       |       |
+---+   +---\   +---X---\---+   +---X---X---X---+---/---+   +
|       |       |   |   |   |   |   |   |   |       |   |   |
+---/---\---/   +---+---+   \---/---+---+---\---\---+---X---+
|   |       |   |       |   |       |   |   |   |   |   |   |
+---+---+   +---+---+   /---+---+---/---\   /---+   \---/   +
|   |   |           |   |   |   |   |           |   |   |   |
+---\   \   +---/---+---\---X---+---+---+---/---\---+---+---+
|       |   |       |   |   |                   |   |   |   |
+---/---\---+---X---\   +---+---+   +   \---+---/   /---X---+
|   |   |   |   |   |   |   |       |   |   |   |   |       |
+---+   +---/---X---+   +   \---+---+   \---\---+---+   +---+
|           |   |   |       |   |       |   |   |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## 2 - Paradoxes (or how grids break reality)

### Example 2.1 - Moore grid - a simple circuit with a leak

A simple circuit in a Moore grid does not necessarily disconnect the grid.  (A  circuit in the plane does disconnect the plane.)  In the illustration below, our circuit consists of the cells labelled "C" and the indicated passages.  The hashed cell in the physical center of the circuit has four neighboring cells which are physically outside the circuit.  Thus, in the sense of Moore neighborhoods, the pictured circuit doesn't actually have an inside.

```
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
|   |   | C |   |   |
+---+---/---\---+---+
|   | C | # | C |   |
+---+---\---/---+---+
|   |   | C |   |   |
+---+---+---+---+---+
|   |   |   |   |   |
+---+---+---+---+---+
```
This particular example does not apply in the Von Neumann grid as the four cells labelled "C" do not form a circuit.  (They are not adjacent.)

Note that the issue here arises because of crossing diagonal edges.  If we eliminate either the descending diagonals (slope -1) or the ascending diagonals (slope 1), the paradox disappears.

### Example 2.2 - Von Neumann grid - a simple circuit with two insides

The Von Neumann neighborhood system creates a different paradox.  Pictured below left is a simple circuit in a Von Neumann 4-grid.  The two hashed cells are indeed inside the circuit and the unlabelled cells form a connected outside.

The paradox is that the inside is not connected -- with a single simple circuit, we created not one, but two holes.

This example does not apply in the Moore grid because, although the indicated walk is a circuit, it is not a simple circuit.  The figure on the right shows a diagonal passage between two cells in the circuit that separates the two cells.
```
+---+---+---+---+---+---+    +---+---+---+---+---+---+
|   |   |   |   |   |   |    |   |   |   |   |   |   |
+---+---+---+---+---+---+    +---+---+---+---+---+---+
|   |   | C - C - C |   |    |   |   | C - C - C |   |
+---+---+-|-+---+-|-+---+    +---+---+-|-+---+-|-+---+
|   | C - C | # | C |   |    |   | C - C |   | C |   |
+---+-|-+---+---+-|-+---+    +---+-|-+---\---+-|-+---+
|   | C | # | C - C |   |    |   | C |   | C - C |   |
+---+-|-+---+-|-+---+---+    +---+-|-+---+-|-+---+---+
|   | C - C - C |   |   |    |   | C - C - C |   |   |
+---+---+---+---+---+---+    +---+---+---+---+---+---+
|   |   |   |   |   |   |    |   |   |   |   |   |   |
+---+---+---+---+---+---+    +---+---+---+---+---+---+
```
