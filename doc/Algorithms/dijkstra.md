# Dijkstra's distance algorithm

Dijkstra's algorithm is an algorithm that can be used to compute the distance from one cell to another.  The distance can be "unweighted", in which case the distance between two cells is equivalent to the path length, *i.e.* the number of *passages* (*i.e.* edges or arcs) in the path.  Distance can also be weighted in which case the distance is equal to the sum of the weights of the passages.

We omit a description of the algorithm.  (The algorithm is described in the docstring for module *mazes.Algorithms.dijkstra*.)

## Example 1 - Computing path lengths

We start by creating a maze:
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.simple_binary_tree import BinaryTree
    5> status = BinaryTree.on(maze)
```

For this demonstration, we will use the cells in the southwest, northeast and northwest corners.  These will be called cell1, cell2, and cell3, respectively.

```
    6> grid=maze.grid
    7> cell1, cell2, cell3 = grid[0,0], grid[7,12], grid[7,0]
```

Now we run the algorithm... Unlike the maze carving algorithms, we create an instance of class Dijkstra.  The constructor takes up to four arguments:

* maze - the maze to process;
* source - the starting cell;
* target - an optional ending cell -- if a target is supplied, the algorithm terminated when target is reached; and
* weight - an optional weight function -- the default is to assign a weight of 1 to each passage.

The first two arguments are required.  We will set the source to cell1 (SW corner) and the target to cell2 (NE corner):

```
    8> from mazes.Algorithms.dijkstra import Dijkstra
    9> dijkstra = Dijkstra(maze, cell1, cell2)
```

Distances are from cell1.  The *distance* method returns the distance from the source cell to some other cell (called the sink).  The *path_to* method returns the corresponding path as a list of cells starting with the source and ending with the sink.  The *label_path* method supplies text labels for the path.  (Method *label_path* has optional arguments that can be used if the default symbols 'S', 'T' and '*' are not suitable.  The required argument for all three methods is the sink.)

```
    10> dijkstra.distance(cell2)
    19
    11> dijkstra.label_path(cell2)
    12> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                                 *   *   *   *   T |
    +   +---+---+   +   +---+---+---+   +   +   +   +   +
    |   |           |   |         *   * |   |   |   |   |
    +   +   +   +   +---+---+---+   +   +---+---+---+   +
    |   |   |   |   | *   *   *   * |   |               |
    +---+---+---+---+   +---+---+---+---+---+   +---+   +
    |             *   * |                       |       |
    +---+   +   +   +   +---+---+---+   +---+   +   +   +
    |       |   | * |   |               |       |   |   |
    +---+   +---+   +---+---+   +---+---+   +   +---+   +
    |       | *   * |           |           |   |       |
    +---+---+   +   +---+   +---+---+---+   +---+   +   +
    | *   *   * |   |       |               |       |   |
    +   +   +---+---+   +---+   +---+   +---+   +   +   +
    | S |   |           |       |       |       |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

And what is the distance to cell3?

```
    13> dijkstra.distance(cell3)
    inf
```

That is clearly not right.  The problem is that we stopped calculating paths when we reached the northeast corner,  The northwest corner is several steps further away, making it effectively unreachable.  We could create a new Dijkstra object, but that isn't necessary.  We can simply recalculate path lengths.  Method *calculate* takes a source cell and an optional target cell.  This time we'll omit the target cell so that all reachable cells are catalogued:

```
    14> dijkstra.calculate(cell1)        # recalculate
    15> dijkstra.distance(cell2)
    19
    16> dijkstra.distance(cell3)
    23
```

We can supply weights for passages.  Setting the weight option to the string "random" uses the built-in random number generator to supply the weights.  For a tree, there is a unique path between two cells, so using weights doesn't change the paths.  (The situation changes if the graph contains one or more circuits.)

```
>>> randweights = Dijkstra(maze, cell1, weight="random")
>>> randweights.distance(cell2)
8.894329203922494
>>> randweights.distance(cell3)
10.82454810963001
>>> randweights.distance(cell1)
0
```

## Example 2 - longest path and diameter

If the maze is a perfect maze (*i.e.* a tree), then Dijkstra's algorithm can be used to find a longest path in the tree.  The length of a longest path is the diameter of the tree.  The choice of an algorithm can govern the range of diameters as well as the average diameter -- the mean and standard deviation of the diameter taken over a number of runs can be an indicator for bias in the algorithm.

In the examples that follow, we won't attempt to carry out a program along these lines.  Instead, we will just find the diameter and a longest path for each of several algorithms and perhaps make a few brief observations.

To use Dijkstra's algorithm to find the diameter of a tree, we run the algorithm twice.  The first time, we run it from an arbitrarily chosen cell without a target.  We then find a cell which is at a maximum distance from the source and run the algorithm a second time using this farthest cell as a source.  (Note that there may be more than one longest path.)  If the maze is not a tree, this strategy will not necessarily work.

Here is some typical code:

```python
    from mazes import rng
    from mazes.Algorithms.dijkstra import Dijkstra

    arbitrary = rng.choice(list(maze.grid))   # pick an arbitrary start cell
    dijkstra = Dijkstra(maze, arbitrary)      # Dijkstra's algorithm
    source = = dijkstra.farthest
    dijkstra.calculate(source)                # Dijkstra's algorithm
    sink = dijkstra.farthest
    longest = dijkstra.path(sink)             # a longest path
    diameter = dijkstra.distance(sink)        # one less than len(longest)
    dijkstra.label_path(sink)                 # etch it into the maze
```

Instead of typing this out every time along with some *print* statements to explain what is going on, we will use the *test* method in the module. That shortens the series of statements above to two lines:

```python
   from mazes.Algorithms.dijkstra import test
   dijkstra = test(maze)
```

Of course the test method is of little help if you want to compute the mean and standard deviation (and perhaps other measures of tendencies) using the diameter from several runs.

Note that the choice of the first source cell is completely arbitrary as long as the maze is connected.  We don't nee the random number generator.  For a rectangular grid, we could just as easily choose the southwest corner cell:

```python
    arbitrary = maze.grid[0,0]
```

For connected maze on an arbitrary grid, we could choose the first or last element in lexical order:

```python
   arbitrary = list(maze.grid)[0]            # first
   # arbitrary = list(maze.grid)[-1]           # last
```

### 2A - Simple binary tree

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.simple_binary_tree import BinaryTree
    5> print(BinaryTree.on(maze))
          Simple Binary Tree (statistics)
                            visits      105
                             cells      104
                          passages      103
                            onward  east
                            upward  north
                              bias        0.5000
    6> from mazes.Algorithms.dijkstra import test
    7> dijkstra = test(maze)
    Dijkstra: starting at (0, 11)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (0, 0), farthest at (0, 4)
    The results may mislead if the maze is not a tree.
    diameter=34
    8> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                             *   *   *   *   *   * |
    +---+   +---+---+   +   +---+   +   +---+---+---+   +
    |       |           |   | *   * |   |             * |
    +   +---+---+   +---+---+   +   +---+   +   +---+   +
    |   |           |         * |   |       |   |     * |
    +---+   +   +   +   +---+   +   +   +---+---+---+   +
    |       |   |   |   |     * |   |   |         *   * |
    +   +---+---+---+---+---+   +   +   +---+---+   +   +
    |   |             *   *   * |   |   | *   *   * |   |
    +---+---+---+   +   +   +---+   +---+   +   +   +   +
    |               | * |   |       |     * |   |   |   |
    +   +   +---+---+   +---+---+---+---+   +---+   +   +
    |   |   |     *   * | *   *   *   *   * |       |   |
    +---+---+---+   +---+   +   +   +   +---+   +---+   +
    | S   *   *   * | T   * |   |   |   |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

For this algorithm, the length of a path from a given cell to the northeast corner does not depend on the coin tosses.  For example, for the cell in the southwest corner of an 8x13 maze, a path to the northeast corner will always involve 7 steps east and 13 steps north, so the path length will always be 19 steps.

The diameter will vary, but we might guess for a typical run, there might be a path from a cell near the southwest corner that head roughly northeast to the northwest corner and then wiggles back to another cell near the southwest corner.  If that works, then the diameter will be a few steps shy of 2x19=38 steps.  For an 8x13 maze, with a little hand-waving, we actually proved:

```
    diameter(maze) < 38.
```

For an m row, n column simple binary tree:

```
   diameter(maze) < 2(m-1) + 2(n-1)
   diameter(maze) < 2m + 2n - 4
```

### 2B - Sidewinder

Sidewinder is trickier to analyze.  A longest path might typically wind its way upward from bottom to top, and then back downward from bottom to top.  The path probably would not cover the entire grid, but, in principle it could.  In practice, the average behavior will be tied to the average run length...


```
    9> maze = Maze(OblongGrid(8, 13))
    10> from mazes.Algorithms.sidewinder import Sidewinder
    11> print(Sidewinder.on(maze))
          Sidewinder Tree (statistics)
                            visits      105
                             cells      104
                          passages      103
                            onward  east
                            upward  north
                              bias        0.5000
    12> dijkstra = test(maze)
    Dijkstra: starting at (2, 12)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (0, 2), farthest at (0, 8)
    The results may mislead if the maze is not a tree.
    diameter=34
    13> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |             *   *   *   *   *                     |
    +   +   +   +   +---+---+   +   +---+---+   +   +   +
    |   |   |   | *   *   * |   | *   * |       |   |   |
    +   +   +   +   +---+   +---+   +   +---+---+   +---+
    |   |   |   |   |     *   * |   | *   *     |       |
    +   +   +---+   +---+---+   +---+---+   +---+   +   +
    |   |   |       |     *   * | *   *   * |       |   |
    +---+   +---+   +   +   +---+   +   +   +---+   +   +
    |           |   |   | *     | * |   |   |       |   |
    +   +---+---+---+---+   +---+   +   +---+---+---+   +
    |               | *   * | *   * |               |   |
    +   +   +   +---+   +---+   +---+   +---+   +   +   +
    |   |   |   | *   * | *   *     |   |       |   |   |
    +   +   +---+   +   +   +---+---+---+   +---+---+   +
    |   |   | S   * |   | *   *   *   T |           |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

If we look at the runs of asterisks in the path, they seem to average at about two cells per run or roughly the reciprocal of the bias. For a bias of 50%, we might a lot of longest paths that look something like the one above, with very roughly 2m+2m=4m cells.  (This path has 35 cells and 4m=32.)  With a bias of 1/3, a reasonable guess is 3 cells per run or about 6m=48 cells giving a diameter of about 47...

But if the bias (probability of a head) is too low, we are more likely to see several runs in the maze, each covering an entire row.  That would change the  game as it would reduce the number of rises.

Here is an actual run with bias=1/3:

```
    13> maze = Maze(OblongGrid(8, 13))
    14> print(Sidewinder.on(maze, bias=1/3))
          Sidewinder Tree (statistics)
                              bias        0.3333
    15> dijkstra = test(maze)
    diameter=42
```

A diameter of 42 indicates a longest path of 43 cells, a few cells shy of our conjecture.  Of course this was just a guess and just one run based on the guess.  And the maze itself isn't very wide!  Here is the maze:

```
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |         *   *   *   *   *   *   *                 |
    +---+---+   +---+   +---+---+   +   +   +---+---+---+
    | *   *   * |               |   | * |               |
    +   +---+---+---+   +---+---+---+   +---+---+---+---+
    | * |               |             *   *   *         |
    +   +---+---+---+---+---+---+---+---+---+   +---+---+
    | *   *   *   *   *   *   *   *   T |     *         |
    +---+   +   +---+---+---+---+---+---+---+   +---+   +
    |       |                       |     *   *     |   |
    +   +   +---+---+   +---+---+---+---+   +---+---+   +
    |   |       |       | *   *   *   *   *     |       |
    +---+   +---+---+---+   +---+   +   +   +   +---+   +
    |           | *   *   * |       |   |   |   |       |
    +   +---+---+   +---+---+---+---+---+---+---+---+   +
    |           | *   *   *   *   *   *   *   S |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note that our runs as we move up from S tend to be only slightly longer on average than expected.  On the downward trip to T, we had far too little freedom on the right side of the maze, and not enough freedom on the left side to maintain an average of three asterisks per run all the way to the bottom.

To get a better estimate using a simulation, we could:

1. consider a much taller and wider maze -- wider to see how the bias is related to the runs of asterisks and taller to reduce the effect of the top row;
2. run more mazes of a given size to get a larger sample;
3. run more sizes and try to ascertain a n approximate relationship between numbers of rows, numbers of columns, bias and the diameter.

(We won't do any of that here!)

### 2C - Inwinder

```
    16> maze = Maze(OblongGrid(8, 13))
    17> from mazes.Algorithms.inwinder import Inwinder
    18> print(Inwinder.on(maze))
          Inwinder Tree (statistics)
                            visits        5
                             cells      104
                          passages      103
                             tiers        4
                            onward       60
                            inward       43
                          backward        0
    19> dijkstra = test(maze)
    Dijkstra: starting at (7, 7)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (5, 0), farthest at (3, 12)
    The results may mislead if the maze is not a tree.
    diameter=24
    20> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | *   * |   |   |       |       |           |   |   |
    +   +   +   +   +   +---+   +---+---+---+   +   +   +
    | * | *   *   *     |   |   |   |   |     *   *     |
    +   +---+---+   +---+   +   +   +   +---+   +   +---+
    | S |   |     * |       |       |       | * | *     |
    +---+   +---+   +---+   +---+   +   +---+   +   +   +
    |   |       | *         |             *   * | * |   |
    +   +   +   +   +---+---+---+---+---+   +---+   +---+
    |       |     *   *   *   *   *   *   *     | *   T |
    +---+   +   +---+   +---+---+   +   +   +---+---+---+
    |       |   |       |           |   |               |
    +---+   +   +   +---+   +   +---+---+   +   +   +   +
    |   |   |   |       |   |       |       |   |   |   |
    +   +   +---+   +   +   +---+---+---+---+   +---+   +
    |           |   |   |       |               |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Here we have a longest path that starts in the outermost ring, winds its way into the innermost ring where it lingers a bit, then winds its way back to the outermost ring.  This is actually similar to sidewinder's behavior with respect to the top row.  The path that results is shorter, but cutting through the center is shorter that cutting through the boundary.  Or is it?  Let's try Outwinder...

### 2D - Outwinder

Outwinder has a long path covering the perimeter.  But can this path be exploited?

```
    21> maze = Maze(OblongGrid(8, 13))
    22> from mazes.Algorithms.outwinder import Outwinder
    23> print(Outwinder.on(maze))
          Outwinder Tree (statistics)
                            visits        5
                             cells      104
                          passages      103
                             tiers        4
                            onward       72
                           outward       31
    24> dijkstra = test(maze)
    Dijkstra: starting at (7, 8)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (4, 5), farthest at (4, 10)
    The results may mislead if the maze is not a tree.
    diameter=47
    25> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | *   *   *   *     |     *   *   *   *   *   *   * |
    +   +---+---+   +---+---+   +---+---+---+---+   +   +
    | *     |     *     |     *   *   *   * |       | * |
    +   +---+---+   +   +   +---+   +   +   +---+---+   +
    | *         | * |   |   |       |   | *   * |   | * |
    +   +---+---+   +---+---+---+   +---+---+   +   +   +
    | * |       | *   *   S |       |       | T |     * |
    +   +   +---+---+---+---+---+---+---+   +---+---+   +
    | *             |                   |   |   |     * |
    +   +   +   +---+   +---+---+---+---+   +   +---+   +
    | * |   |   |       |           |       |         * |
    +   +   +---+   +---+---+   +---+---+   +---+---+   +
    | * |   |       |   |                   |         * |
    +   +---+   +---+   +   +---+---+---+---+---+---+   +
    | *   *   *   *   *   *   *   *   *   *   *   *   * |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

This longest path starts in the innermost ring, works its way outward.  It makes excellent use of the path in the perimeter, using all but two cells.  Then it works its way inward, but comes to rest in a dead end one cell shy of the innermost ring.  Not bad, and certainly consistent with the behavior we observed in sidewinder and in inwinder.

### 2E - Depth-first search

We expect one very long longest path...
```
    26> maze = Maze(OblongGrid(8, 13))
    27> from mazes.Algorithms.dfs_better import DFS
    28> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      207
                        start cell  (3, 0)
               maximum stack depth       61
                             cells      104
                          passages      103
    29> dijkstra = test(maze)
    Dijkstra: starting at (5, 2)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (7, 12), farthest at (3, 0)
    The results may mislead if the maze is not a tree.
    diameter=60
    30> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |     *   *   * |         *   *   * | *   *   * | S |
    +   +   +---+   +---+---+   +---+   +   +---+   +   +
    |   | * | *   * | *   *   * |   | * | * |     *   * |
    +---+   +   +---+   +---+---+   +   +   +---+---+   +
    | *   * | *   * | *   * |       | * | * | *   * |   |
    +   +---+---+   +---+   +   +---+   +   +   +   +---+
    | *   * |   | *   *   * |   | *   * | *   * | *   * |
    +---+   +   +---+---+---+   +   +---+---+---+   +   +
    | T   * |           |       | * |     *   * |   | * |
    +---+---+   +   +   +   +---+   +   +   +   +---+   +
    |       |   |   |       | *   * |   | * | *   * | * |
    +   +---+   +   +---+   +   +---+---+   +---+   +   +
    |   |       |       |   | * |     *   * |   | *   * |
    +   +   +---+---+   +---+   +---+   +---+   +---+   +
    |               |         *   *   * |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
This particular path covers about 58.65% of the grid, just under 3/5.  The cell labelled T was where DFS started its search, and the resulting longest path ends up painting itself into the northwest corner (S).  The maximum stack depth (61) for this run was equal to the number of cells in a longest path (diameter + 1).

The longest path fossilized the stack operations in DFS.  After carving a passage from the south into the northwest corner, the top cell was obviously the cell two cells south of the corner.  In this sense, this longest path is sediment that hardened and left traces of the stack in its wake.

### 2F - Breadth-first search

We expect the longest path to be fairly short, and very sensitive to the starting cell (marked with an 'X').  We won't be surprised.

```
    31> maze = Maze(OblongGrid(8, 13))
    32> from mazes.Algorithms.bfs import BFS
    33> print(BFS.on(maze))
          Breadth-first Search (BFS) (statistics)
                            visits      104
                        start cell  (0, 8)
              maximum queue length       13
                             cells      104
                          passages      103
    34> dijkstra = test(maze)
    Dijkstra: starting at (3, 4)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (7, 12), farthest at (7, 0)
    The results may mislead if the maze is not a tree.
    diameter=26
    34> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | T |   |   |   |   |   |   |   |   |   |   |   | S |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    | * |   |   |   |   |   |   |   |   |   |   |   | * |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    | *   *   * |   |   |   |   |   |   |   |   |   | * |
    +---+---+   +   +   +   +   +   +   +   +   +   +   +
    |         *   *   * |   |   |   |   |   |   |   | * |
    +---+---+---+---+   +   +   +   +   +   +   +   +   +
    |                 *   * |   |   |   |   |   |   | * |
    +---+---+---+---+---+   +   +   +   +   +   +   +   +
    |                     * |   |   |   |   |   |   | * |
    +---+---+---+---+---+   +   +   +   +   +   +   +   +
    |                     *   * |   | *   *   *   *   * |
    +---+---+---+---+---+---+   +   +   +---+---+---+---+
    |                         *   *   X                 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2G - Simplified "Prim"

Simplified "Prim" tends to produce mazes that radiate outward from the starting cell (again marked with an 'X'(.  That's what happened in this run:

```
    35> from mazes.VGT.sprim import sprim
    36> maze = Maze(OblongGrid(8, 13))
    37> print(sprim(maze))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (5, 3)
                             cells      104
                          passages      103
    38> dijkstra = test(maze)
    Dijkstra: starting at (1, 8)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (4, 12), farthest at (0, 1)
    The results may mislead if the maze is not a tree.
    diameter=25
    38> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                   |       | *   * | *   *   *   * |
    +---+---+   +   +---+   +---+   +   +   +---+---+   +
    |           |   |   |   | *   * | *   *         | * |
    +---+---+---+   +   +   +   +---+   +---+   +   +   +
    |             X   *   *   *     |       |   |   | * |
    +---+   +---+   +   +   +   +---+---+---+---+---+   +
    |       |     * |   |   |                       | S |
    +---+---+---+   +   +   +   +---+   +   +   +---+---+
    |         *   * |   |   |       |   |   |           |
    +---+---+   +   +   +   +   +---+---+   +   +   +---+
    |     *   * |   |   |   |       |       |   |       |
    +---+   +   +   +   +---+---+   +---+   +   +---+---+
    | *   * |   |   |       |           |   |       |   |
    +   +---+   +---+   +   +   +   +   +   +---+---+   +
    | *   T |   |       |   |   |   |   |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2H - Vertex "Prim"

We should see roughly average fairly random behavior:

```
    39> from mazes.VGT.vprim import vprim
    40> maze = Maze(OblongGrid(8, 13))
    41> print(vprim(maze))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (2, 8)
                             cells      104
                          passages      103
    42> dijkstra = test(maze)
    Dijkstra: starting at (0, 6)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (5, 0), farthest at (4, 2)
    The results may mislead if the maze is not a tree.
    diameter=35
    42> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |     *   *   *   * |     *   *   *   * |   |       |
    +---+   +   +---+   +---+   +---+---+   +   +   +---+
    | *   * |   |     *   *   * |   |   | * |           |
    +   +---+   +---+---+---+---+   +   +   +   +---+---+
    | S |   |   |   |   |   |             *   *     |   |
    +---+   +---+   +   +   +---+---+   +---+   +---+   +
    |     *   T |       |   |   |       |     *         |
    +---+   +---+---+   +   +   +---+---+---+   +---+   +
    |     * |   |             *   *   *   *   *     |   |
    +---+   +   +---+   +   +   +   +   +---+   +---+---+
    |     *         |   |   | * |   |   |               |
    +---+   +---+---+---+---+   +---+---+---+   +---+   +
    |     * |   |     *   *   * |   |       |   |       |
    +---+   +   +---+   +---+   +   +   +---+---+   +   +
    |     *   *   *   * |                   |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2J - Kruskal's algorithm

Kruskal's algorithm has biases that a very close to those of Prim's algorithm, but on balance the behavior of either, like that of vertex "Prim" is a good approximation of uniformly random.  We don't expect the paths to be similar, but we expect that they will normally be fairly average in length:

```
    43> maze = Maze(OblongGrid(8, 13))
    44> from mazes.Algorithms.kruskal import Kruskal
    45> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      135
                 components (init)      104
               queue length (init)      187
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)       52
    46> dijkstra = test(maze)
    Dijkstra: starting at (2, 11)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (5, 2), farthest at (6, 10)
    The results may mislead if the maze is not a tree.
    diameter=35
    46> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |     *   * |           |       |   | *   *   * |   |
    +   +   +   +   +---+---+---+   +   +   +---+   +   +
    |   | * | * |                   |   | *   T | *   * |
    +---+   +   +---+   +---+   +   +   +---+---+---+   +
    |   | * | S |   |   |       |   |         *   *   * |
    +   +   +---+   +---+---+---+   +---+---+   +---+---+
    |     * |               |   | *   *   *   *         |
    +   +   +---+   +---+---+   +   +---+---+---+---+   +
    |   | *   * |           |     *                 |   |
    +---+---+   +   +---+---+---+   +---+---+---+   +---+
    |       | * | *   *     |     *         |   |   |   |
    +   +   +   +   +   +---+---+   +---+---+   +---+   +
    |   |     *   * | * | *   *   * |       |           |
    +   +---+---+   +   +   +   +---+   +   +   +---+   +
    |   |           | *   * |           |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2K - Eller's Algorithm (1:1 1:2)

Eller's algorithm is a true generalization of the sidewinder algorithm which adapts a few component-merging techniques from Kruskal's algorithm.  Like sidewinder, a typical longest path will extend from the bottom row up to the top and then wind back down towards the bottom.

The results below reflect an optional merge rate of 50% (head:tail odds are 1:1) and optional carve upward probability of 1/3 (head:tail odds are 1:2).

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Algorithms.eller import Eller
    2> from mazes.Grids.oblong import OblongGrid
    3> from mazes.maze import Maze
    4> maze = Maze(OblongGrid(8,13))
    5> print(Eller.on(maze))
          Martin Eller's Spanning Tree (statistics)
                            visits        8
                             cells      104
                          passages      103
               optional merge left       33
               required merge left        3
             required carve upward       58
             optional carve upward        9
                            onward  east
                            upward  north
    6> from mazes.Algorithms.dijkstra import test
    7> dijkstra = test(maze)
    Dijkstra: starting at (1, 12)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (1, 2), farthest at (1, 3)
    The results may mislead if the maze is not a tree.
    diameter=31
    8> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               | *   *   *   *   *                 |
    +   +   +   +   +   +---+---+   +   +---+---+   +   +
    |   |   |   | *   *     |   |   | *     |       |   |
    +   +   +---+   +---+   +   +   +   +   +---+   +   +
    |   |   | *   * |   |   |       | * |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +---+   +
    |   |   | * |   |   |   |   |   | * |       |   |   |
    +---+---+   +   +   +   +   +   +   +---+   +   +   +
    |     *   * |       |   |   |   | *   * |       |   |
    +   +   +   +   +---+---+---+   +---+   +   +   +   +
    |   | * |   |       |               | * |   |   |   |
    +---+   +---+---+   +   +   +---+---+   +   +   +   +
    |     * | S | T |   |   |   |   | *   * |   |   |   |
    +   +   +   +   +---+---+---+   +   +   +   +   +---+
    |   | *   * | *   *   *   *   *   * |   |   |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2L - Outward Eller

Eller's algorithm, like sidewinder, is not confined to rows and columns.  It can be adapted to other two-tiered grid arrangements.  Outward Eller is one such adaptation.  Here we generally expect a path to run from a ringing in the interior outward from one point and then back inward.  But, as in the example below, the result can meander.

This particular example is intriguing (and, T thought, surprising!) -- it started and ended in neighboring cells just outside the innermost ring.  It passed through the outermost ring twice and made its way into the innermost ring.  In its second pass through the outermost ring, it covered about half of the ring, taking full advantage of little shortcuts. It was a little longer than the example for outwinder (2D) and in third place (so far!) to our examples for depth-first search (2E) and hunt and kill (2Q).

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8,13))
    4> from mazes.Algorithms.outward_eller import OutwardEller
    5> print(OutwardEller.on(maze))
          Outward Eller (statistics)
                            visits        4
                             cells      104
                          passages      103
               optional merge left       50
               required merge left       13
             required carve upward       25
             optional carve upward       15
                            onward  clockwise
                            upward  outward
    6> from mazes.Algorithms.dijkstra import test
    7> dijkstra = test(maze)
    Dijkstra: starting at (2, 6)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (5, 2), farthest at (4, 2)
    The results may mislead if the maze is not a tree.
    diameter=51
    8> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | *   *   *             |                   |       |
    +   +---+   +---+---+---+   +---+   +   +   +   +   +
    | *     | *   *   *   *   *     |   |   |       |   |
    +   +---+---+   +---+---+   +---+---+---+---+---+---+
    | *   *   S |   |     *   *     | *   *   *   * |   |
    +   +---+---+---+---+   +---+---+   +---+---+   +   +
    |   | *   T |         *   *   *   * |   | *   *     |
    +---+   +---+   +---+---+---+---+---+   +   +---+---+
    | *   *     |       |   |   |           | *         |
    +   +---+---+---+   +   +   +---+   +   +   +---+   +
    | *   *     |   |       |   |       |   | *   * |   |
    +---+   +---+   +---+   +   +   +---+---+   +   +---+
    | *   * |   |           | *   * |   |       | *   * |
    +   +---+   +---+---+---+   +   +   +---+---+---+   +
    | *   *   *   *   *   *   * | *   *   *   *   *   * |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2M1 - Aldous/Broder (first entrance random walk)

We next consider three unbiased algorithms.  (The implementations will have some biases that result from biases in the underlying pseudorandom number generator.  Here we are using Python's Mersenne twister-based *random* module.) To get a better sense of random variation in spanning trees, we should really run the algorithm several times and look at the mean and standard deviation of the diameters.  (Here we are just looking at a sample of size 1.)

```
    9> from mazes.Algorithms.aldous_broder import AldousBroder
    10> maze = Maze(OblongGrid(8,13))
    11> print(AldousBroder.on(maze))
          First Entrance Random Walk (Aldous/Broder) (statistics)
                            visits     1370
                             cells      104
                          passages      103
                     starting cell  (4, 8)
    12> dijkstra = test(maze)
    Dijkstra: starting at (4, 0)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (3, 11), farthest at (0, 2)
    The results may mislead if the maze is not a tree.
    diameter=50
    13> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               |       |               | *   *   * |
    +---+   +---+   +---+   +---+   +   +   +   +---+   +
    |       |   |       |   |       |   | *   * | *   * |
    +---+   +   +---+---+   +---+---+---+   +---+   +---+
    |   | *   * | *   * |           |     * |   | *   * |
    +   +   +   +   +   +   +---+   +---+   +   +   +   +
    | *   * | *   * | *     |       |     *     |   | * |
    +   +---+---+---+   +---+---+---+---+   +   +---+   +
    | * |       |   | *     |       |     * |   | S | * |
    +   +---+   +   +   +---+   +   +---+   +---+   +   +
    | *     |       | * |       |         * |   | * | * |
    +   +---+---+   +   +   +---+---+   +   +   +   +   +
    | *   * |     *   * |   |       |   | *   * | * | * |
    +   +   +---+   +---+---+---+   +---+---+   +   +   +
    |   | *   T | *   *   *   *   *   *   *   * | *   * |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2M2 - reverse Aldous/Broder (last exit random walk)

Our sample of one for reverse Aldous/Broder returned a maze with much smaller diameter.  (This suggests that there is wide expected variation in spanning tree diameters for a rectangular grid.)

```
    14> from mazes.Algorithms.reverse_aldous_broder import ReverseAldousBroder
    15> maze = Maze(OblongGrid(8,13))
    16> print(ReverseAldousBroder.on(maze))
          Last Exit Random Walk (Reverse Aldous/Broder) (statistics)
                            visits      773
                             cells      104
                          passages      103
                     starting cell  (5, 0)
    17> dijkstra = test(maze)
    Dijkstra: starting at (3, 9)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (0, 12), farthest at (2, 11)
    The results may mislead if the maze is not a tree.
    diameter=31
    18> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |                               |
    +---+---+   +   +   +---+---+---+---+   +---+---+---+
    |           |   | *   *   * | *   *   * |   |       |
    +---+---+   +---+   +---+   +   +---+   +   +---+   +
    |               | * |   | *   * |     *   *   *     |
    +---+   +---+---+   +   +---+---+   +---+---+   +---+
    |   |           | * |   |   |               | *   * |
    +   +   +---+   +   +   +   +   +   +   +---+---+   +
    |   |   |   |     *   *     |   |   |       | *   * |
    +   +   +   +---+   +   +---+---+   +---+---+   +   +
    |               |   | *   *   * |   |       | T |   |
    +   +---+   +---+   +---+---+   +---+---+   +---+---+
    |       |   |           |   | *   *     |   | *   * |
    +---+   +---+---+   +---+   +---+   +---+   +   +   +
    |               |   |             *   *   *   * | S |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2M3 Wilson's algorithm (circuit-eliminated random walk)

Our third theoretically unbiased example uses Wilson's algorithm.  With a diameter of 40, this example lends some support to the conjecture that expected variation (*e.g.* in variance or standard deviation) for unbiased spanning tree diameters (for a rectangular grid with some given dimensions) is fairly large.

```
    19> from mazes.Algorithms.wilson import Wilson
    20> maze = Maze(OblongGrid(8,13))
    21> print(Wilson.on(maze))
          Circuit-Eliminated Random Walk (Wilson) (statistics)
                            visits       50
                             cells      104
                          passages      103
                 paths constructed       50
                     cells visited      487
                          circuits      131
                    markers placed      306
                   markers removed      203
                     starting cell  (6, 9)
    22> dijkstra = test(maze)
    Dijkstra: starting at (1, 5)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (2, 5), farthest at (1, 12)
    The results may mislead if the maze is not a tree.
    diameter=40
    23> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |   | *   *   * |   |   |   |               |
    +   +   +   +   +---+   +   +   +   +   +---+---+---+
    |   | *   *   *     | *   * |   |           |       |
    +---+   +---+   +---+---+   +   +   +---+   +   +   +
    |     * |           |     *   *   *   * |       |   |
    +   +   +---+---+---+---+---+---+---+   +---+---+---+
    |   | *   *             |     *   *   * |           |
    +---+---+   +---+   +   +---+   +   +---+---+   +---+
    |   | *   * |       |   |     * |   |     *   *   * |
    +   +   +   +---+---+---+   +   +   +   +   +---+   +
    |     * |   | *   *   S |   | * |   |   | *     | * |
    +   +   +---+   +---+---+---+   +---+---+   +   +   +
    |   | *     | * |   |         *   *   *   * |   | T |
    +   +   +---+   +   +   +   +---+   +---+   +   +---+
    |   | *   *   *     |   |       |   |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2N1 - Houston's algorithm

Although Houston's algorithm might not produce uniform spanning trees, it probably comes close. (I don't know whether there is any available proof which decides whethe Houston's algorithm is biased, unbiased or perhaps "quasi-unbiased".) We will run a few examples using a few different parameters to control when the algorithm switches from Aldous/Broder to Wilson.

Our first example uses the defaults (cutoff at 2/3, failure rate at 90%).  The switch was triggered when the unvisited area was reduced to 69 cells (roughly 2/3 of 104).

```
    24> from mazes.Algorithms.houston import Houston
    25> maze = Maze(OblongGrid(8,13))
    26> print(Houston.on(maze))
          Hybrid Random Walk (Houson) (statistics)
                            visits      117
                             cells      104
                          passages      103
                 cuttoff threshold       69
                      failure rate        0.9000
                 paths constructed       37
                     cells visited      212
                          circuits       46
                    markers placed      129
                   markers removed       60
                     starting cell  (7, 5)
                           trigger  cutoff threshold
    27> dijkstra = test(maze)
    Dijkstra: starting at (4, 7)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (5, 1), farthest at (3, 2)
    The results may mislead if the maze is not a tree.
    diameter=37
    28> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | *   *   *   *   *   *   * |   |   |               |
    +   +---+---+   +---+   +   +   +   +---+---+---+   +
    | *     |   |       |   | *   *   *         |       |
    +   +---+   +   +   +---+---+---+   +---+---+---+   +
    | *   S |       |   |       |     *   *   *         |
    +---+---+---+---+---+---+   +---+   +---+   +---+   +
    | *   * |               |   |   |   |   | * |   |   |
    +   +   +---+   +---+   +   +   +---+   +   +   +---+
    | * | *   T |   |   |               |     *     |   |
    +   +---+---+   +   +   +   +---+---+---+   +---+   +
    | *   * |   |       |   |   |   |   | *   *         |
    +---+   +   +   +---+---+   +   +   +   +---+---+---+
    |     * |   |   | *   *   *   *   *   *         |   |
    +   +   +   +---+   +---+   +---+   +---+   +---+   +
    |   | *   *   *   * |       |           |           |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2N2 - Houston's algorithm (cutoff rate 1/2)

In our second example, the switch was triggered when the unvisited area was reduced to 52 cells.

```
    29> maze = Maze(OblongGrid(8,13))
    30> print(Houston.on(maze, cutoff_rate=1/2))
          Hybrid Random Walk (Houson) (statistics)
                            visits      227
                             cells      104
                          passages      103
                 cuttoff threshold       52
                      failure rate        0.9000
                 paths constructed       27
                     cells visited      115
                          circuits       17
                    markers placed       71
                   markers removed       19
                     starting cell  (4, 0)    
                           trigger  cutoff threshold
    31> dijkstra = test(maze)
    Dijkstra: starting at (2, 11)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (6, 10), farthest at (7, 5)
    The results may mislead if the maze is not a tree.
    diameter=32
    32> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   | *   *   *   * | T |               | *   *     |
    +   +   +---+   +   +   +   +---+   +---+   +   +---+
    |     *   * |   | *   * |   |       |   | S | *   * |
    +   +---+   +---+---+---+   +---+---+   +---+---+   +
    |   |   | *     |   |   |           |       | *   * |
    +   +   +   +---+   +   +   +---+---+   +   +   +   +
    |   |     * |       |   |   |   | *   * |   | * |   |
    +   +---+   +---+   +   +   +   +   +   +---+   +---+
    |       | *   *   * |     *   *   * | *   *   * |   |
    +   +---+   +---+   +---+   +---+---+---+---+---+   +
    |   |       |     *   *   * |           |   |       |
    +   +---+   +---+---+   +---+   +---+---+   +   +   +
    |   |       |   |                               |   |
    +---+   +   +   +   +   +---+---+---+   +---+---+---+
    |       |       |   |   |                           |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 2N3 - Houston's algorithm (cutoff rate 1/3)

Our final example used a cutoff rate of 1/3.  The switch was triggered when the unvisited area was pared down to 34 cells.

```
    33> maze = Maze(OblongGrid(8,13))
    34> print(Houston.on(maze, cutoff_rate=1/3))
          Hybrid Random Walk (Houson) (statistics)
                            visits      191
                             cells      104
                          passages      103
                 cuttoff threshold       34
                      failure rate        0.9000
                 paths constructed       23
                     cells visited       73
                          circuits        6
                    markers placed       44
                   markers removed       10
                     starting cell  (1, 7)
                           trigger  cutoff threshold
    35> dijkstra = test(maze)
    Dijkstra: starting at (1, 12)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (2, 0), farthest at (0, 0)
    The results may mislead if the maze is not a tree.
    diameter=36
    36> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |   |           |     *   *   * |       |
    +---+   +   +   +   +---+---+---+   +---+   +---+   +
    |   |   |   |     *   *   *   *   * |     *   * |   |
    +   +   +---+---+   +---+---+   +   +---+---+   +   +
    |             *   * |       |   |   |       | *     |
    +---+   +---+   +---+---+   +---+---+---+   +   +   +
    |   |   | *   * |     *   *   *   *   *   *   * |   |
    +   +---+   +---+---+   +---+   +   +---+   +---+   +
    | *   *   * |     *   * |   |   |   |   |       |   |
    +   +   +---+   +   +---+   +---+   +   +   +---+---+
    | S |       |   | * |   |       |   |   |           |
    +---+---+---+---+   +   +   +   +---+   +---+   +   +
    | *   * | *   *   * |       |   |   |       |   |   |
    +   +   +   +---+   +---+   +---+   +   +   +   +---+
    | T | *   *     |           |           |           |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Our variation in three Houston's algorithm runs was considerably smaller than that for Aldous/Broder, reverse Aldous/Broder and Wilson which implement unbiased algorithms.  Does that mean that Houston's algorithm is biased?  No.  First, it is not a mathematical proof, and second, as statistical evidence, a sample size of three is too small to be significant.

### 2Q - Hunt and kill

Hunt and kill 

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8,13))
    4> from mazes.Algorithms.hunt_kill import HuntKill
    5> print(HuntKill.on(maze))
          Hunt and Kill (statistics)
                            visits      103
                             cells      104
                          passages      103
                              hunt       13
                              kill       90
                     starting cell  (0, 4)
    6> from mazes.Algorithms.dijkstra import test
    7> dijkstra = test(maze)
    Dijkstra: starting at (1, 7)
    diameter: pass 1 skipped
    diameter: pass 2
    diameter: start at (1, 2), farthest at (2, 12)
    The results may mislead if the maze is not a tree.
    diameter=55
    8> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           | *   *   *   * |               |       |
    +   +   +---+   +---+---+   +   +   +---+   +   +   +
    |   |   |     * | *   *   * |   |       |       |   |
    +---+   +   +   +   +---+---+---+---+   +---+---+   +
    |           | * | *   * |               | *   * |   |
    +   +---+---+   +---+   +---+   +---+---+   +   +---+
    |       | *   * | *   *         |     *   * | *   * |
    +---+   +   +---+   +---+---+---+   +   +---+---+   +
    |       | *     | *   *   *   * |   | * |     *   * |
    +---+---+   +   +---+---+---+   +---+   +   +   +---+
    | *   *   * |   |       | *   * | *   * |   | * | T |
    +   +---+---+   +   +---+   +---+   +---+---+   +   +
    | *   * | S |   |         * | *   * | *   *   * | * |
    +---+   +   +   +---+---+   +   +---+   +---+---+   +
    |     *   * |       |     *   * |     *   *   *   * |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Summary

Here are the results for diameter sorted in ascending order:

| **example** | **algorithm**          | **diameter** |
| :---------: | :------------          | -----------: |
|    2E       | DFS                    |           60 |
|    2Q       | Hunt and Kill          |           55 |
|    2L       | Outward Eller          |           51 |
|    2M1      | Aldous/Broder          |           50 |
|    2D       | Outwinder              |           47 |
|    2B       | Sidewinder 33%         |           42 |
|    2M3      | Wilson                 |           40 |
|    2N1      | Houston cut=2/3        |           37 |
|    2N2      | Houston cut=1/3        |           36 |
|    2H       | VertexPrim             |           35 |
|    2J       | Kruskal                |           35 |
|    2A       | BinaryTree 50%         |           34 |
|    2B       | Sidewinder 50%         |           34 |
|    2N2      | Houston cut=1/2        |           32 |
|    2K       | Eller 1:1 1:2          |           31 |
|    2M2      | reverse Aldous/Broder  |           31 |
|    2F       | BFS                    |           26 |
|    2G       | SimplifiedPrim         |           25 |
|    2C       | Inwinder               |           24 |

Table 1. longest path in each example (8x13 grid)

Disclaimer: Since the sample sizes are one maze each, these results might not be typical.


