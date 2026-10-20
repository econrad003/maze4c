# Triangular grids

## 1  Rectangular grids consisting of triangular cells

A cell with three grid arcs is a triangular cell.  So, if we take an ordinary square cell and remove all but three connections, we get a triangular cell.  Now consider the usual rectangular grid and ignore square cells on the boundary.  Call a cell an upward cell if the sum of its indices is even and downward otherwise:
```
    ...        ...     ...   ...
          +---+   +---+   +-
    3     | D   U   D   U    ...
          +   +---+   +---+-
    2     | U   D   U   D    ...
          +---+   +---+   +-
    1     | D   U   D   U    ...
          +   +---+   +---+-
    0     | U   D   U   D    ...
          +---+---+---+---+-
            0   1   2   3    ...

```
Note that we can always move east or west in the the grid unless we reach the boundary wall.  But to move north we need an up cell, and to move south we need a down cell.  In order for the grid to be connected, we normally need the number of rows to be even and the number of columns to be at least two in order to insure that we can always find a way north.  There are two classes of exceptions, both of which can be considered trivial.  First, a grid with 2 rows and 1 column is connected even though it violates the column constraint.  Second, a grid with a single row is connected even though it violates the row constraint (and perhaps also the column constraint).  We can ignore the trivial cases as these can be realized as ordinary rectangular grids.

Now suppose we have *perfect* maze on such a grid.  A perfect maze is a spanning tree -- and since each cell can have at most three incident passages, the maze is also a binary tree.  This type of grid gives us a way of creating creating perfect binary mazes with more varied structure using algorithms like Wilson's algorithm, Kruskal's algorithm, or even depth-first search.  And since we are staying inside Von Neumann neighborhoods, we can create these mazes in a command shell...

Let's create a few perfect binary mazes...

### 1.1  Depth-first search

Depth-first search is a good place to start...  We import the grid and maze classes, and also the unicode console tool:

```
    maze4c$ python
    Python 3.10.12
    >>> from mazes.Grids.oblong3 import TriangularGrid
    >>> from mazes.maze import Maze
    >>> from mazes.console_tools import unicode_str
```

We also need depth-first search:
```
    >>> from mazes.Algorithms.dfs_better import DFS
```

Now we need a maze object, and oops!
```
    >>> maze = Maze(TriangularGrid(9, 13))
    Traceback (most recent call last):
    File "maze4c/mazes/grid.py", line 67, in __init__
        self._initialize()
    File "maze4c/mazes/Grids/oblong3.py", line 94, in _initialize
        assert self.m % 2 == 0, "the number of rows must be even"
    AssertionError: the number of rows must be even
```
Did you read the part about the restrictions on the numbers of rows and of columns -- an even (and positive!) number of rows and at least two columns...

And here we go:
```
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      207
                        start cell  (4, 1)
               maximum stack depth       77
                             cells      104
                          passages      103
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃           ┃                               ┃       ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ┫
    ┃       ┃           ┃           ┃           ┃       ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃                       ┃       ┃   ┃               ┃
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃   ┃                   ┃       ┃           ┃       ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃                   ┃       ┃       ┃       ┃       ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃       ┃       ┃       ┃           ┃       ┃       ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃       ┃       ┃                       ┃       ┃   ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃       ┃                       ┃                   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

Unlike the binary growing tree algorithms, we have a guarantee that the result will be a *spanning* binary tree because (1) the grid is connected and (2) no cell has more than three incident grid edges.

### 1.2  Wilson's algorithm

We can also use Wilson's algorithm (or Aldous/Broder) to create (theoretically) uniformly random spanning binary trees on *this* grid type.  (On this grid, but not on *arbitrary* Von Neumann or Moore grids**!!!**  "Theoretically" -- because our random number generator is periodic and isn't really random.) 

```
    >>> from mazes.Algorithms.wilson import Wilson
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       40
                             cells      104
                          passages      103
                 paths constructed       40
                     cells visited     1075
                          circuits      368
                    markers placed      667
                   markers removed      564
                     starting cell  (5, 3)    
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃                                                   ┃
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃       ┃   ┃                       ┃       ┃       ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃           ┃       ┃                       ┃       ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃   ┃       ┃   ┃   ┃   ┃           ┃           ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃       ┃   ┃                       ┃               ┃
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃       ┃                       ┃   ┃       ┃       ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃               ┃   ┃   ┃   ┃                       ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃               ┃                   ┃               ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

### 1.3  Kruskal's algorithm

We can produce minimum weight binary spanning trees if we have a suitable mapping from grid edges to weights -- or we can simply let Kruskal's algorithm connect the dots as we do here:
```
    >>> from mazes.Algorithms.kruskal import Kruskal
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      127
                 components (init)      104
               queue length (init)      142
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)       15
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃   ┃                                           ┃   ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ┫
    ┃           ┃           ┃       ┃       ┃           ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃               ┃       ┃           ┃           ┃   ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃           ┃       ┃                           ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━┫
    ┃       ┃   ┃   ┃       ┃       ┃           ┃       ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
    ┃                   ┃   ┃           ┃               ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃           ┃                       ┃   ┃   ┃       ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃       ┃       ┃       ┃                       ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

###  1.4  Breadth-first search

If the stresses of life require a simple binary maze or perhaps a binary labyrinth for contemplation, breadth-first search might fill the bill:
```
    >>> from mazes.Algorithms.bfs import BFS
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(BFS.on(maze))
          Breadth-first Search (BFS) (statistics)
                            visits      104
                        start cell  (2, 6)
              maximum queue length       16
                             cells      104
                          passages      103
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃   ┃       ┃       ┃       ┃           ┃       ┃   ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃       ┃       ┃       ┃           ┃       ┃       ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃   ┃       ┃       ┃           ┃       ┃           ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
    ┃                       ┃           ┃               ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃                                                   ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃                         X                         ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━┫
    ┃                       ┃                           ┃
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃                   ┃           ┃       ┃       ┃   ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Notice the pattern that radiates from the start cell, labelled here with an X.

###  1.5  Vertex Prim

Maybe breadth-first search was too predictable and Kruskal too random.  We could try vertex Prim as a compromise...
```
    >>> from mazes.VGT.vprim import vprim
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(vprim(maze))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (3, 6)    
                             cells      104
                          passages      103
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃       ┃   ┃                       ┃               ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃       ┃               ┃           ┃   ┃           ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃               ┃   ┃   ┃   ┃                       ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃                                   ┃   ┃           ┃
    ┣━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃           ┃                   ┃                   ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃               ┃                   ┃       ┃   ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃           ┃   ┃               ┃           ┃   ┃   ┃
    ┣   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ┫
    ┃   ┃               ┃                               ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```

###  1.6  Simplified Prim

And maybe a compromise between breadth-first search and vertex Prim is needed.  Here is simplified Prim:
```
    >>> from mazes.VGT.sprim import sprim
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(sprim(maze))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (5, 5)
                             cells      104
                          passages      103
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃           ┃       ┃           ┃                   ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃               ┃           ┃               ┃       ┃
    ┣━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃                     X         ┃   ┃               ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
    ┃       ┃       ┃   ┃                               ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃       ┃               ┃           ┃   ┃           ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃       ┃   ┃       ┃       ┃       ┃           ┃   ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃       ┃           ┃               ┃       ┃       ┃
    ┣━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━┫
    ┃                       ┃           ┃               ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
The paths radiate outward from the start cell, but the result is not as regular as with BFS.

### Can we use any maze-carving algorithm?

The short answer is no, but there is a more nuanced answer.  Simple binary tree, sidewinder, Eller's algorithm and recursive division will often fail, but the failures are qualitatively different.  Let's try sidewinder and recursive division...
```
    >>> from mazes.Algorithms.sidewinder import Sidewinder
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(Sidewinder.on(maze))
          Sidewinder Tree (statistics)
                            visits      105
                             cells      104
                          passages      102   <---
                            onward  east
                            upward  north
                              bias        0.5000
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃                                                   ┃
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃                       ┃       ┃   ┃       ┃       ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃                   ┃       ┃       ┃   ┃           ┃
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃   ┃       ┃       ┃           ┃   ┃       ┃       ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━┫
    ┃           ┃       ┃   ┃       ┃               ┃ X ┃
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃       ┃                       ┃       ┃ X   X   X ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━┫
    ┃           ┃                               ┃ X   X ┃
    ┣   ╋━━━╋━━━╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ┫
    ┃                   ┃       ┃       ┃       ┃ X   X ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
Since Sidewinder cannot produce a circuit, Euler's edge theorem tells us that the maze is one passage shy of being connected.  I marked the small component in the lower right -- you can verify that there is no way of producing a path from a blank cell to a cell with an X.  Although the result is not a perfect maze, no exception has been raised.

Give this example just a little thought.  Now think about how sidewinder and simple binary tree work -- think about the pseudocode, not the Python implementation.  What happens at the end of a row if the row ends with a down cell?  What can go wrong and what happens when it does?

But sidewinder can sometimes succeed.  For example:
```
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(Sidewinder.on(maze))
          Sidewinder Tree (statistics)
                            visits      105
                             cells      104
                          passages      103     <---
                            onward  east
                            upward  north
                              bias        0.5000
    >>> print(unicode_str(maze))
    ┏━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
    ┃                                                   ┃
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
    ┃           ┃       ┃       ┃       ┃               ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃       ┃                   ┃   ┃           ┃       ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
    ┃           ┃       ┃           ┃   ┃               ┃
    ┣━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃       ┃           ┃   ┃       ┃       ┃           ┃
    ┣━━━╋━━━╋   ╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋━━━╋   ┫
    ┃                                   ┃               ┃
    ┣━━━╋   ╋━━━╋━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━┫
    ┃               ┃       ┃           ┃       ┃       ┃
    ┣━━━╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━┫
    ┃           ┃       ┃       ┃       ┃               ┃
    ┗━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┻━━━┛
```
In this run, Sidewinder was successful.  In both cases, sidewinder produced a maze -- in the first try, it just wasn't connected.  (As Maxwell Smart would say while indicating a length of one millimeter between his thumb and his index finger: "Missed by that much!")

With recursive division, the problem is more severe:
```
    >>> from mazes.Algorithms.recursive_division import RecursiveDivision
    >>> maze = Maze(TriangularGrid(8,13))
    >>> print(RecursiveDivision.on(maze))
    Traceback (most recent call last):
        ...
    File "Algorithms/recursive_division.py", line 213, in divide_vertically
                subgrid1.carve_door_north()
        ...
    File "edge.py", line 107, in _configure
                if cell1.is_linked(cell2) or cell2.is_linked(cell1):
        AttributeError: 'NoneType' object has no attribute 'is_linked'
```
In this run, the cell chosen as a door apparently has no neighbor to the north.

The upshot seems to be that simple binary tree, sidewinder and Eller's algorithm will run, but the resulting maze will typically not be connected. (My implementation of Eller's algorithm will spit out some warning messages, but it should run.)  You could connect the result by following with Kruskal's algorithm.

With recursive division, the door carving method will typically raise an exception.