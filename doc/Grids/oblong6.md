# The 6-connected rectangular grid

In the documentation for module *oblong8*, we documented a couple of paradoxical results that arise with square and octagonal grids.  In square grids, a simple circuit can enclose a disconnected inside.  This doesn't happen with octagonal grids: instead the simple circuit might leak -- in other words, it might actual fail to enclose an inside region.  One way of avoiding these problems is to have diagonals restricted to a single direction.  This makes the grid hexagonal.

Of course, the hexagonal grid is not a continuous rectangle, so it will undoubtedly behave in its own unexpected ways.

## Example 1 - Positively sloped diagonals

We will create a maze using Kruskal's algorithm.  We proceed in the usual way:
```
maze4c$ python
Python 3.10.12
>>> from mazes.Grids.oblong6 import HexagonalGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.kruskal import Kruskal
>>> maze = Maze(HexagonalGrid(10, 15))
>>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      251
                 components (init)      150
               queue length (init)      401
                             cells      150
                          passages      149
                components (final)        1
              queue length (final)      150
```
The statistics show no cause for alarm.  Let's look at the maze:
```
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |       |               |           |
+---/---/   +---+---+   +---/---+---/---+   +   +---+---+   +
|   |   |   |   |       |           |   |   |   |       |   |
+   /---+---+   /   +---/---/---+---/---+   +---+---+   /---+
|       |       |   |   |   |                           |   |
+---+   /---+---+---/   +---+   +---/---+   +   +---/---/   +
|   |   |   |   |   |       |   |   |       |   |   |   |   |
+   +   +   +   +---/---+---+---+---/   +---+---/---+---/   +
|       |       |       |   |       |       |   |       |   |
+---+   +---+   /   +---/---+---+---/---+---+---+---/---+---+
|       |       |       |   |   |   |               |       |
+---/---+---+   +---/   /---/---+---+---+---+---+   +---+   +
|       |   |   |   |       |   |       |       |           |
+---/---+   /---+---/   +---+   /   +---/---/---+---+   +---+
|           |   |   |   |   |   |   |   |       |   |       |
+---+---/   /---+---/---+   +   +---/---+   +---/---+   +---+
|       |   |       |       |       |   |           |   |   |
+---+   +---+   +---+---/---+   +---+   +---/---+---/   +   +
|           |                   |                   |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note that all the diagonals are positively sloped.

## Example 2 - Negatively sloped diagonals

Adding the option *slope=-1* changes the direction of the diagonal grid connections:
```
>>> maze = Maze(HexagonalGrid(10, 15, slope=-1))
>>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      256
                 components (init)      150
               queue length (init)      401
                             cells      150
                          passages      149
                components (final)        1
              queue length (final)      145
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |               |   |       |   |   |           |
+---+---\   \---+---+---+   +---\   +   +---\   \---+   \---+
|   |   |   |   |   |   |           |           |   |   |   |
+   \   +   \---+   +   \---+---+---\---\---+---+---\---+   +
|   |   |   |   |   |   |   |   |   |   |   |   |           |
+   +---+---+---\   +---+   +   +---\   +---+   \---+---+   +
|   |   |   |       |       |   |       |   |   |   |       |
+   +   +---\---+   \   +---\   \---+   \   +   +---+---+   +
|               |   |       |   |   |   |   |           |   |
+   +---+   \---+---+   \---+   \---\   +---+---+---\---\---+
|   |       |   |   |   |   |   |   |       |       |   |   |
+---+   +---+---\   +   +---\---\---+---+   +---+---\   +---+
|           |   |   |   |   |   |   |   |   |   |           |
+   \---+---\   +---\---+   +   +---\   +   \   \   +---+---+
|   |   |       |   |           |       |   |   |           |
+---+   +---+---\   \---+---+   \---+---+---+   +---\---+   +
|           |   |   |       |   |       |   |   |       |   |
+   +---+---+   +---+   +---+---+   +   +   +   +---+   +   +
|               |           |       |       |   |       |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note here that all of the diagonal passages are negatively sloped.
