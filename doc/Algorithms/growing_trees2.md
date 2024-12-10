# Arc-based growing trees

In some searches it may be desirable not only to know the current item (as in vertex-based growing trees) but also the item that directed the search to the current item (which we'll call the previous item or the predecessor).  Calling this item the "previous" item is a bit misleading as this item might not be the second item in the queue -- the second item in the queue is the *physical* predecessor, but we're more in *logical* predecessor.

If both the current item and its logical predecessor are adjacent cells, then we have an arc-based search.

## Algorithm

The algorithm is basically the same as the vertex-based algorithm -- the difference is that the objects in the queue are packets consisting of a cell and its predecessor, or equivalently (assuming we are not admitting parallel arcs), an arc.

This presents a small problem for initialization. With the starting cell we must make an adjustment.  There are a number of corrections.  Here is just one approach.

```
Initialization:
   Initialize q as a queue.
   Mark all cells in the grid as unvisited.
   Choose a cell from the grid and mark it as visited.
   For each adjacent unvisited neighbor (nbr):
      arc := (cell, nbr)
      q.enter(arc).

Loop:
   While not q.is_empty:
      let prev, curr = q.leave();
      if curr has been visited:
          do nothing  (i.e. ignore this queue entry);
      otherwise:
          mark curr as visited;
          for each adjacent unvisited neighbor (nbr) of curr:
              arc := (curr, nbr)
              q.enter(arc);
          maze.link(prev, curr).
```

Here we let the queue discipline determine the order in which *edges* are carved.  (The queue contains *arcs*, but we carve *edges* in the maze.  Note that edges are carver at when cells are removed.  This may have some implications for a search (such as DFS or BFS) where the queue is not a priority queue.  And it does have some implications for the growth of the queue.

Note that in the initialization, we said "each unvisited neighbor" instead of just "each neighbor".  There are two reasons for this:

* the wording is the same as the for the wording in the program loop, suggesting a common procedure or method; and
* if the grid happens to have a loop (an arc or edge from a cell to itself) -- a circuit of length 1 -- then we don't want to enter the loop into queue.

In the program loop. the wording "each unvisited neighbor" is to avoid cluttering the queue with known circuits (including loops, of course).  After popping an arc from the queue, we already know the previous cell has been visited.  If at some point since the arc was entered into the queue, the current cell was also visited, then adding the arc would create a circuit, and since we are growing a spanning tree, circuits are not permitted.

This is the arc-based growing tree algorithm implemented in module *mazes.Algorithms.growing\_tree2*.  The implement class is *ArcGrowingTree*.

An alternative approach is to work one arc at a time.

```
Initialization:
   Initialize q as a queue.
   Mark all cells in the grid as unvisited.
   Choose a cell from the grid and mark it as visited.
   Choose a lowest weight arc from the cell (arc := (cell, nbr)).
   Mark nbr as visited.
   maze.link(cell, nbr)
   q.enter(arc).

Loop:
   While not q.is_empty:
      let prev, curr = q.top;
      if curr has been visited:
          q.jettison();
      otherwise:
          choose a lowest weight arc from curr (arc := (curr, nbr)).
          mark nbr as visited.
          maze.link(curr, nbr)
          q.enter(arc).
```

This approach has both an advantage and a disadvantage.  The disadvantage is that, if we have a priority queue, then we have to work with weights both inside and outside the priority queue.  The advantage is that there are more barriers to entering the queue.  (For queues other than priority queues, a lowest weight arc is simply a random choice of all the permissible arcs.)

We will save this alternative approach for a separate implementation.

## Examples

The implementation is similar to the vertex-based implementation.  As with the vertex-based growing tree, we have some helper methods implemented in the folder *mazes/AGT*.  Because of the similarities, we will focus on the helper methods and skip the raw *ArcGrowingTree* class.

### Example 1 - Depth-first search (*aka* DFS, *aka* recursive backtracker)

Depth-first search is just growing tree with a stack...

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.AGT.dfs import init_maze, dfs
    2> maze = init_maze(5, 13)
    3> print(dfs(maze))
          Arc Growing Tree (statistics)
                            visits       90
                        start cell  (1, 6)
                             cells       65
                          passages       64
    4> maze.grid[1,6].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                           |               |       |
    +---+---+---+---+---+   +   +   +---+---+   +   +   +
    |           |           |       |       |       |   |
    +   +---+   +   +---+---+---+---+   +---+---+---+   +
    |       |       |               |           |       |
    +   +   +---+   +   +---+---+   +   +   +---+   +---+
    |   |   |       |   | x | S     |   |   |       |   |
    +   +   +---+---+   +   +---+---+   +   +   +---+   +
    |   |               |               |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

For DFS, we see is the characteristic long passage from the starting cell (labelled 'S') and ending in the cell manually marked 'x' (just left of 'S').
There may be some subtle biases which make this differ from vertex-based DFS, but the resulting mazes are very similar.

### Example 2 - Breadth-first search (*aka* BFS)

Breadth-first search is growing tree with a FIFO queue.

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.AGT.bfs import init_maze, bfs
    2> maze = init_maze(5, 13)
    3> print(bfs(maze))
          Arc Growing Tree (statistics)
                            visits      111
                        start cell  (1, 10)
                             cells       65
                          passages       64
    4> maze.grid[1,10].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                           |   |   |   |   |   |   |
    +---+---+---+---+---+---+   +   +   +   +   +   +   +
    |                                       |   |   |   |
    +---+---+---+---+---+---+---+---+---+   +   +   +   +
    |                                           |   |   |
    +---+---+---+---+---+---+---+---+---+---+   +   +   +
    |                                         S         |
    +---+---+---+---+---+---+---+---+   +   +   +   +   +
    |                                   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The result here is just what one would expect from a vertex-based BFS.  Any peculiar biases owing specifically to arc-based implementation are probably very difficult to identify.

### Example 3 - Simplified "Prim"

As usual, we include a disclaimer: This is not Prim's algorithm.  Simplified "Prim" uses a "random queue" (random in, first out).

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.AGT.sprim import init_maze, sprim
    2> maze = init_maze(5, 13)
    3> print(sprim(maze))
          Arc Growing Tree (statistics)
                            visits      106
                        start cell  (4, 10)
                             cells       65
                          passages       64
    4> maze.grid[4,10].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |   |   |                         S     |   |
    +   +---+   +   +---+---+---+---+---+   +   +---+   +
    |   |   |                               |           |
    +   +   +---+   +---+---+   +---+   +---+   +   +---+
    |   |           |           |           |   |       |
    +   +   +---+---+   +   +---+---+   +---+---+   +---+
    |       |           |       |       |   |           |
    +   +---+---+---+---+   +---+---+   +   +   +   +---+
    |   |                       |       |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

As with its vertex-based cousin, corridors in arc-based simpflified "Prim" tend to wind and radiate outward from the starting cell.

### Example 4 - Prim's algorithm (finally!)

Our first implementation of Prim's algorithm uses the helper module "mazes.AGT.primic*, named for a wordplay involving the phrase "mimic Prim".  To demonstrate, we will need to set up some edge weights.  As evidence that the result is a minimum weight spanning tree, we will create several additional mazes and compare the net weights of the spanning trees.

There are some subtleties in correctly implementing Prim's algorithm, so we will cover this example in quite a bit of detail.

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.AGT.primic import init_maze, primic
    2> maze = init_maze(5, 13)
    3>     # create weights
    4> from mazes import rng
    5> weights = dict()
    6> arcs = 0
    7> for cell in maze.grid:
    ...     for nbr in cell.neighbors:
    ...         arc = [cell, nbr]
    ...         edge = frozenset(arc)
    ...         weights[edge] = rng.random()
    ...         arcs += 1
    ...
    8> print(f"number of arcs = {arcs}, number of edges = {len(weights)}")
        number of arcs = 224, number of edges = 112
    9> assert len(weights) == arcs / 2
```

In lines 1 and 2, we import the arc-based helper method and create an empty maze.  In lines 4 and 5, and in the *for* loop in lines 7*ff*. we create the weights.  In line 6 and the last line of the for loop we count the total number of arcs.  Note that our dictionary contains grid edges instead of grid arcs.  These are implemented as Python *frozenset* instances, not as *tuple* instances.  Each grid edge is equivalent to exactly two distinct arcs, one in each direction.  In lines 8 and 9 we verify by counting that our weights dictionary contains edges instead of arcs.

The *primic* method is defined as follows:
```python
    from mazes.Algorithms.growing_tree2 import ArcGrowingTree as AGT
    def primic(maze:Maze, start_cell:Cell=None,
              shuffle=True, pr_map:dict={},
              action="unstable",
              cache=True) -> AGT.Status:
```

Prim's algorithm is *generally* insensitive to the choice of starting cell, so we will (as usual) not specify one.  (DFS, BFS and simplified "Prim" are very sensitive to the choice of starting cell.)  Prim's algorithm is also *generally* insensitive to the dictionary ordering of the cell neighborhoods, so, to save a little time, we won't shuffle.  Priority queues can handle equal weights in various ways.  Here the choices are "stable" (like a queue: FIFO), "antistable" (like a stack: LIFO), or unstable (randomly).  It *generally* doesn't matter, so we'll stick with the default.  Finally, we want to make sure that our edge weights cover all the queue entries, so we'll tell the priority queue not to use its cache.

What do we mean by "*generally*"?  Essentially we that there is only one minimum weight spanning tree for the given assignment of weights.  If there are two or three minimum weight spanning trees, then the algorithm results will be somewhat sensitive to the starting cell, and if a lot of weights are equal, the result will be very sensitive to the starting cell.

Here we are *trusting* Python's random number generator to (i) give us weights which are, for the most part, unequal and (ii) when we add them up to get the weight of a spanning tree, for the most part, different spanning trees give different total weights.  Despite all this, Prim's algorithm should give us the lowest total weight.  (There is one *caveat* -- we are using floating point, so rounding errors might cause a problem with large mazes.)

```
    10> print(primic(maze, shuffle=False, pr_map=weights, cache=False))
          Arc Growing Tree (statistics)
                            visits       89
                        start cell  (0, 0)
                             cells       65
                          passages       64
    11> maze.grid[0,0].label = 'S'
    12> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                               |           |       |
    +   +---+---+   +---+   +---+---+---+   +---+   +   +
    |   |           |       |   |       |   |       |   |
    +   +---+---+   +---+---+   +   +   +   +   +---+   +
    |       |   |                   |       |   |       |
    +---+   +   +---+---+   +---+---+---+---+   +---+---+
    |       |       |       |       |           |       |
    +---+   +   +   +   +---+   +---+   +---+   +   +   +
    | S     |   |                       |           |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Now we need to define a function which calculate the total weight of a maze...

```
    13> def net_weight(maze, weights):
    ...     net = 0
    ...     for edge in maze:
    ...         grid_edge = frozenset(edge)
    ...         weight = weights[grid_edge]
    ...         net += weight
    ...     return net
    ...
    14> print(f"total weight = {net_weight(maze, weights)}")
       total weight = 20.79631095937737
```

In the line:
```
    ...         grid_edge = frozenset(edge)
```
the variable *edge* names an instance of class *Edge* which contains an iterator which yields the two cells used to create the edge.  So this line of code is equivalent to:
```
    ...         cell1, cell2 = edge
    ...         grid_edge = frozenset([cell1, cell2])
```

We use edges in the maze instead of cells in the grid and their neighboods in order to avoid counting an edge twice.

To reuse this maze, we can use the method *unlink\_all*.  As a quick check, the total weight of an empty maze is 0...  We are reusing the maze since our weight mapping is tied to the underlying grid.  We could use the cell indices to create an equivalent mapping, but erasing the maze is a lot easier and less prone to error than copying the weight map.

```
    15> maze.unlink_all()
    16> print(f"total weight = {net_weight(maze, weights)}")
       total weight = 0
```

Prim's algorithm should give us the same total weight with some other starting point (labelled '2')...  (But rounding errors could result in a small error.)

```
    17> start2 = maze.grid[2,6]
    18> start2.label = '2'
    19> print(primic(maze, shuffle=False, pr_map=weights, cache=False,
    ...     start_cell=start2))
    ...
          Arc Growing Tree (statistics)
                            visits       89
                        start cell  (2, 6)
                             cells       65
                          passages       64
    20> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                               |           |       |
    +   +---+---+   +---+   +---+---+---+   +---+   +   +
    |   |           |       |   |       |   |       |   |
    +   +---+---+   +---+---+   +   +   +   +   +---+   +
    |       |   |             2     |       |   |       |
    +---+   +   +---+---+   +---+---+---+---+   +---+---+
    |       |       |       |       |           |       |
    +---+   +   +   +   +---+   +---+   +---+   +   +   +
    | S     |   |                       |           |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    21> print(f"total weight = {net_weight(maze, weights)}")
        total weight = 20.79631095937737
```
The reported weight is the same, so rounding errors did not affect anything.

The two mazes appear to be the same.  Prim's algorithm only guarantees a minimum weight spanning tree and not necessarily the same minimum weight spanning trees.  But with random weights, we really don't expect there to be more than one.  (But there might be!  Even with distinct weights, there can be more than one way to arrive at the same total!)

Now, let's try our setup with different algorithms and see what happens.  In each case, we will erase the maze, run the algorithm and report the new weight.

If we run *primic* with no options set, we will get a different result.  Arc weights (not edge weights) will be determined by the priority queue and cached:

```
    22> maze.unlink_all()      # ERASE!  IMPORTANT!
    23> print(primic(maze))    # USING DEFAULTS!
          Arc Growing Tree (statistics)
                            visits       77
                        start cell  (4, 1)
                             cells       65
                          passages       64
    24> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |           |           |                   |
    +---+   +   +   +---+---+---+   +---+---+---+---+   +
    |   |       |           |       |       |   |       |
    +   +   +---+   +---+   +---+   +---+   +   +   +   +
    |       |           |     2             |       |   |
    +   +---+   +---+---+---+---+---+   +---+---+   +   +
    |   |   |       |   |       |                   |   |
    +   +   +   +---+   +   +   +   +   +   +   +   +   +
    | S |       |           |       |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    25> print(f"total weight = {net_weight(maze, weights)}")
        total weight = 32.05255140579125
```

Notice that the total weight is larger than for our two run's of Prim's algorithm.

To finish, let's run simple binary tree and sidewinder...  We won't display the maze...

```
    26> maze.unlink_all()                # ERASE!
    27> from mazes.Algorithms.simple_binary_tree import BinaryTree
    28> print(BinaryTree.on(maze))
          Simple Binary Tree (statistics)
                            visits       66
                             cells       65
                          passages       64
                            onward  east
                            upward  north
                              bias        0.5000
    29> print(f"total weight = {net_weight(maze, weights)}")
        total weight = 30.440884346235173
    30> maze.unlink_all()                # ERASE!
    31> from mazes.Algorithms.sidewinder import Sidewinder
    32> print(Sidewinder.on(maze))
          Sidewinder Tree (statistics)
                            visits       66
                             cells       65
                          passages       64
                            onward  east
                            upward  north
                              bias        0.5000
    33> print(f"total weight = {net_weight(maze, weights)}")
        total weight = 31.590205552774442
```

In both cases, again as expected, the resulting mazes have greater weight than Prim's algorithm.
