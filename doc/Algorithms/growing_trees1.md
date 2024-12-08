# Vertex-based Growing Trees

## Algorithm

In vertex-based growing trees the objects in the queue are cells (*i.e* vertices).  There is no additional context.  In that sense, this family is as general as it gets.  The algorithm is as stated in *growing\_trees.md*:

```
Initialization:
   Initialize q as a queue.
   Mark all cells in the grid as unvisited.
   Choose a cell from the grid and mark it as visited.
   q.enter(cell).

Loop:
   While not q.is_empty:
      let cell = q.top;
      If cell has unvisited neighbors:
          choose an unvisited neighbor (nbr);
          q.enter(nbr);
          maze.link(cell, nbr)
          mark nbr as visited;
      otherwise:
          q.jettison().
```
All we need to do is specify the queue discipline.  (For a priority queue we need to specify how priorities are assigned, but this is part of the queue discipline.)

## Examples

In this tutorial, each example will be self-contained, consisting of a single python session.

### Example 1A - Depth-first search (DFS; aka recursive backtracker)

To start, we must call the Python 3 interpreter, and create an empty maze object.  Here we use the oblong (*i.e.* rectangular) grid, but any connected grid type can be used with a growing tree algorithm.

```
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(5, 8))
```

With a growing tree algorithm, we need to specify a queue discipline.  For depth-first search, we need a stack class.  We don't instantiate as the algorithm implementation handles instantiation.  All we need a properly implemented queue class:

```
   4> from mazes.Queues.stack import Stack
```

In addition to specifying a maze object, we must specify a queuing class (keyword *QueueClass*).  If the queue class requires initialization arguments, we must supply these (keyword *init*).  (Class Stack doesn't require any.)  For a priority queue, if a priority lookup is not specified in the initialization, then it will need to handled when objects enter the queue.  The *priority* keyword provides the lookup.  (The Stack class doesn't use a priority lookup.  The most recently entered object is always at the top of the stack.)

The other option is a starting cell (keyword *start\_cell*).  For an oblong grid, we specify a cell by its row and column.  For example, the southwest corner cell will be `maze.grid[0,0]` and, in the 5x8 grid, the northeast corner will be `maze.grid[4,7]`.  (Rows are numbered south to north from 0 in the south and columns from west to east from 0 in the west.)  But we can also let the algorithm select a starting cell at random.

We will let the algorithm choose the starting cell:

```
    5> from mazes.Algorithms.growing_tree1 import VertexGrowingTree
    6> print(VertexGrowingTree.on(maze, QueueClass=Stack))
          Vertex Growing Tree (statistics)
                            visits       79
                        start cell  (2, 5)
                             cells       40
                          passages       39
    7> maze.grid[2,5].label = 'S'
    8> print(maze)
    +---+---+---+---+---+---+---+---+
    |   |               |           |
    +   +   +---+   +---+   +---+   +
    |   |       |               |   |
    +   +---+   +---+---+---+---+   +
    |       |           | S         |
    +   +   +---+---+   +---+---+---+
    |   |   |           |       |   |
    +   +   +   +---+---+   +   +   +
    |   |                   |       |
    +---+---+---+---+---+---+---+---+
```
The module *mazes.Algorithms.growing\_tree1* defines the algorithm class *VertexGrowingTree*.

In line 7, we labelled the randomly chosen start cell.

A longest path in the maze starts in the cell S and ends in the southeast corner.  It consists of 30 cells (29 passages), so the diameter of the maze is 29.  (The length of a path is the number of passages, or one shy of the number of cells.)  The other longest path is simply the reversal from the southeast corner to S.

This is equivalent to DFS as implemented in *mazes.dfs*.

### Example 1B - DFS, with less detail

In the folder *mazes.VGT*, there are some modules that do some of the required setup.  For DFS, we can use *mazes.VGT.dfs*.  The module defines two methods, *dfs* and *init\_maze*.  The method *init\_maze* creates a pristine oblong maze.  The method *dfs* sets up and runs the algorithm.  If you want to use another grid type for your maze, that's not a problem -- using *init\_maze* just saves a couple of lines when initializing oblong grids.

Method *dfs* takes just three arguments.  The *maze* argument is required.  The *start\_cell* argument provides an optional starting cell.

The remaining argument *shuffle* determines whether neighborhoods of cells are processed in fixed order (*shuffle=False*) or random order (*shuffle=True*, the default.)  Fixed order will be a little more than twice as fast, but less random.  Depending on how dictionaries are implemented in the Python interpreter itself, corridors in the resulting maze will tend to be straighter with fixed order.  For most practical situations, the time difference won't be noticeable, so stick with the default.

We will let the algorithm choose a starting cell, and following my recommendation, we'll process the neighborhoods in random order.

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.VGT.dfs import dfs, init_maze
    2> maze = init_maze(5, 8)
    3> print(dfs(maze))
          Vertex Growing Tree (statistics)
                            visits       79
                        start cell  (1, 3)
                             cells       40
                          passages       39
    4> maze.grid[1,3].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+
    |               |       |     a |
    +   +---+   +---+   +   +   +---+
    |       |           |   |       |
    +---+   +---+---+---+   +   +   +
    |   |       |           |   |   |
    +   +---+   +   +---+---+   +   +
    |       |   | S |       | b |   |
    +   +   +   +---+   +   +---+   +
    |   |               |           |
    +---+---+---+---+---+---+---+---+
```
In line 4, we labelled the starting cell.

There are longest paths in the maze that start at S and end in either the northeast corner (marked 'a') or in the cell in row 1 column 6 (marked 'b').  These each have 32 cells (31 passages) so the diameter is 31.  Large diameters relative to the total number of passages is very characteristic of DFS.

We could combine lines 2 and 3 into a one-liner using `:=` instead of `=` for assignment:
```
    >>> print(dfs(maze := init_maze(5, 8)))
```

### Example 2 - Breadth-first search

For BFS, we won't do an example like Example 1A for DFS.  But here is the required queue definition if you go that route:

```
    >>> from mazes.Queues.queue import Queue
```
The short version uses module *mazes.VGT.bfs* which defines methods *bfs* and *init\_maze*.  It's just a drop-in replacement for Example 1B:
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.VGT.bfs import bfs, init_maze
    2> maze = init_maze(5, 8)
    3> print(bfs(maze))
          Vertex Growing Tree (statistics)
                            visits       79
                        start cell  (1, 6)
                             cells       40
                          passages       39
    4> maze.grid[1,6].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+
    |           |   |   |   |   |   |
    +---+---+   +   +   +   +   +   +
    |           |   |   |   |   |   |
    +---+---+   +   +   +   +   +   +
    |                       |   |   |
    +---+---+---+---+---+   +   +   +
    |                         S     |
    +---+---+---+---+---+---+   +   +
    |                           |   |
    +---+---+---+---+---+---+---+---+
```
In lines 1 and 3, we just typed bfs instead of dfs.  As for the maze, that's about as complicated as you can get with breadth-first search.

### Example 3 - Simplified "Prim"

As with breadth-first search, we won't do an example like Example 1A.  But here is the required queue definition:
```
    >>> from mazes.Queues.random_queue import RandomQueue
```

Module *mazes.VGT.sprim* again defines two methods, *sprim* which does the required work, and *init\_maze* which (as above) creates empty oblong mazes.  Usage is exactly like its counterparts for depth-first and breadth-first search:
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.VGT.sprim import sprim, init_maze
    2> maze = init_maze(5, 8)
    3> print(sprim(maze))
          Vertex Growing Tree (statistics)
                            visits       79
                        start cell  (2, 2)
                             cells       40
                          passages       39
    4> maze.grid[2,2].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+
    |       |                   |   |
    +   +   +   +---+---+---+---+   +
    |   |       |               |   |
    +---+   +   +   +---+---+---+   +
    |       | S             |       |
    +   +   +---+   +---+---+---+   +
    |   |   |                       |
    +---+   +   +---+   +---+   +---+
    |       |       |       |       |
    +---+---+---+---+---+---+---+---+
```

Paths from the start cell tend to be short, on average, (like those in BFS) but winding (very unlike BFS).

## Vertex "Prim"

For vertex "Prim", we use a priority queue.  This complicates the setup, so we'll run through several approaches.  But first we need a disclaimer...

In vertex "Prim", we use vertex weights as priorities.  The goal in Prim's algorithm is to minimize the total weight of a spanning.  But every spanning tree contains the same cells, so any spanning tree whatever is a minimum vertex-weighted spanning tree.  Vertex "Prim", like any greedy algorithm, does at least locally minimize something.  And in a very trivial sense, vertex "Prim" does actually minimize total vertex weight.  What isn't clear is what is really being minimized.

That being said, vertex "Prim" does create almost uniform spanning trees without too much effort.  That requires a bit of explanation.  An algorithm that places one copy of every possible spanning tree in an urn and randomly selects one is a uniform spanning tree algorithm.  There are algorithms that do this: Aldous/Broder and Wilson's algorithm are example.  (They don't, however, directly implement an urn.)  But if a uniform spanning tree algorithm doesn't directly implement the urn, it has a drawback -- it might not terminate.  And implement the urn directly is fine for tiny mazes, as the mazes grow in size, they soon overwhelm the available resources (memory and time).

Vertex "Prim" has a fairly tight bound on resources, but it does create uniform spanning trees.  It does, however create reasonably good substitutes.  For more information, read pages 181-183 in the Jamis Buck book. (⋄)

⋄ Jamis Buck.  *Mazes for Programmers*.  2015, Pragmatic Bookshelf.

> Prim's algorithm is described in detail on pages 175-179.  Vertex "Prim" is described on pages 181-183 under the heading "True Prim's Algorithm" with the qualication that "it's still slightly modified".

All that being said, it's time to create some mazes.

### Example 4A - vertex "Prim", the hard way

As before, we begin by creating a pristine maze, a maze where every cell is an isolated cell, devoid of entrances and exits. We'll use a larger maze than usual, but not much larger...

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
```

Next prepare the infrastructure for a priority queue.  We'll need a priority function which maps cells to their cell weights.  For weights, we'll simply use random weights.  If we want to introduce biases, we can assign weights more systematically.

```
    4>     # assign weights
    5> from mazes import rng
    6> weights = dict()
    7> for cell in maze.grid:
    ...    weights[cell] = rng.random()
    ...
    8>     # define priority mapping
    9> weight = lambda cell: weights[cell]
    10> weight(maze.grid[0,0])      # test it
    0.8636543802063315
```

In line 5, I import the current random number generator. (It's basically a wrapper for Python's random.)  In lines 6 and 7, I use a dictionary to map a cell to a weight.  Line 9 turns the map into a callable function.  Line 10 is just a quick test which displays the priority of the southwest corner cell.

At this point we have all the preliminaries.  We need to import the priority queue class and the growing tree class.  Then we can run the algorithm.  It's the same as before except we omit lines 4 through 10.
```
    11> from mazes.Queues.priority_queue import PriorityQueue
    12> from mazes.Algorithms.growing_tree1 import VertexGrowingTree
    13> print(VertexGrowingTree.on(maze, QueueClass=PriorityQueue,
    ...       priority=weight))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (2, 0)
                             cells      104
                          passages      103
    14> maze.grid[2,0].label = 'S'
    15> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               |   |   |                           |
    +   +   +---+   +   +   +---+---+   +---+   +---+   +
    |   |   |                   |       |   |       |   |
    +   +---+---+   +---+   +---+---+---+   +   +---+---+
    |   |           |   |       |   |   |               |
    +   +   +   +---+   +   +---+   +   +   +---+   +   +
    |   |   |   |               |   |   |       |   |   |
    +   +---+   +---+   +---+---+   +   +   +---+---+   +
    |   |   |   |   |       |   |                   |   |
    +---+   +---+   +   +---+   +   +---+   +   +---+---+
    | S         |   |   |           |   |   |           |
    +---+   +---+   +   +   +---+   +   +---+---+   +---+
    |           |               |           |           |
    +---+   +---+   +   +   +---+---+   +---+---+---+   +
    |               |   |           |           |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 4B - Vertex "Prim", simplifying a bit...

Since we are just randomly assigning weights, we can let the priority queue handle weight assignment in its cache.  (This is built into the PriorityQueue implementation.)

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Queues.priority_queue import PriorityQueue
    5> from mazes.Algorithms.growing_tree1 import VertexGrowingTree
    4> print(VertexGrowingTree.on(maze, QueueClass=PriorityQueue))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (7, 8)
                             cells      104
                          passages      103
    5> maze.grid[7,8].label = 'S'
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |                   |     S     |           |
    +---+   +---+   +   +---+   +---+   +---+   +---+---+
    |           |   |   |       |                   |   |
    +---+---+   +---+---+---+   +---+   +   +   +---+   +
    |   |               |               |   |   |   |   |
    +   +---+---+   +---+---+   +   +---+---+---+   +   +
    |   |                   |   |   |           |       |
    +   +---+---+   +---+---+---+   +   +---+---+---+   +
    |                   |                   |           |
    +---+---+---+   +   +---+   +   +   +---+---+   +   +
    |   |           |   |   |   |   |           |   |   |
    +   +---+---+   +---+   +---+---+   +   +---+---+   +
    |       |       |                   |   |   |   |   |
    +   +---+---+   +---+---+   +   +   +   +   +   +   +
    |                           |   |   |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

In this example, the weights are hidden with the priority queue in the *VertexGrowingTree.Status* object and are not not available for review.

### Example 4c - Vertex "Prim", automated setup

We can simplify the setup using the module *mazes.VGT.vprim*.  If we don't need to access the weight, we can just use the priority queue cache as in Example 4B.  But using *vprim* the setup is simplified:

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.VGT.vprim import vprim, init_maze
    2> maze = init_maze(8, 13)
    3> print(vprim(maze))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (2, 12)
                             cells      104
                          passages      103
    4> maze.grid[2,12].label = 'S'
    5> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                   |       |                       |
    +   +---+   +---+   +---+   +---+   +---+   +---+   +
    |   |       |                       |       |   |   |
    +---+---+   +---+---+---+   +   +---+---+   +   +---+
    |               |   |   |   |       |           |   |
    +---+---+   +---+   +   +---+   +---+   +---+---+   +
    |           |                   |           |       |
    +---+   +---+---+   +---+   +   +---+   +---+---+   +
    |   |   |           |       |   |           |       |
    +   +---+---+   +   +---+   +---+---+---+   +---+   +
    |               |       |   |       |             S |
    +   +   +   +---+   +---+---+   +---+---+   +   +   +
    |   |   |   |                       |       |   |   |
    +---+   +---+---+   +---+   +   +---+---+   +   +---+
    |           |           |   |   |           |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 4d - Vertex "Prim", explicit priorities (no caching)

If we need to access the priorities afterward, then we must establish them beforehand.  This can be done in *vprim* by setting the *cache* option to *False* and supplying a dictionary containing all the cell weights.  (If the *cache* option is *True*, *i.e.* the default value, the priority queue will cache any missing weights...)

Here's what will happen if you set the *cache* option to False and forget to supply one or more of the cell weights...
```
    $ python
    Python 3.10.12.
    1> from mazes.VGT.vprim import init_maze, vprim
    2> maze = init_maze(8, 13)
    3> weights = {}     # some of the weights are missing
    4> print(vprim(maze, cell_map=weights, cache=False))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      ... <lots of lines deleted>
      File ".../maze4c/mazes/Queues/priority_queue.py", line 117, in _lookup
        raise ValueError("priority lookup failed")
    ValueError: priority lookup failed
```

This time, let's supply *all* the needed weights...  Here we'll simply weight the cells in dictionary order...

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.VGT.vprim import init_maze, vprim
    2> maze = init_maze(8, 13)
    3> weights = {}
    4> w = 0
    5> for cell in maze.grid:
    ...     w += 1
    ...     weights[cell] = w
    ...
    6> print(vprim(maze, cell_map=weights, cache=False))
          Vertex Growing Tree (statistics)
                            visits      207
                        start cell  (1, 5)
                             cells      104
                          passages      103
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |       |   |   |   |   |   |   |   |
    +   +   +   +   +   +---+   +   +   +   +   +   +   +
    |                                                   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

(This is no surprise.  Dictionary order in Python 3 is not very random.)

