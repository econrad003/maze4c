# Pruning tree algorithms

**Contents**

* Section 1 - Depth-first search
* Section 2 - Passage-based search
* Section 3 - Other queuing structures
* Section 4 - Pruning a disconnected maze

**Introduction**

If we have an ovegrown vine-covered tree, to restore its health, we typically prune it.  An *overgrown* maze, then, is a maze that has some circuits.  One approach to restore it is to use the basic wall building algorithm and a circuit locator to find and break circuits.  But the basic wall builders are impractical for large mazes.  The pruning tree algorithms work a bit differently.  With a single circuit, the basic wall builder and its corresponding pruning tree algorithm are essentially the same.  With more than one circuit, the basic wallbuilder calls a new circuit locator to find another circuit, while the pruner, after breaking a circuit, picks up the search for another using all the previously available information.

## Section 1 - Depth-first search

In this section, we will use depth-first search in several ways to create a *perfect maze*.  In each case, we will also use Djikstra's algorithm to display a longest path in the maze.  Our first example will use a pruning tree algorithm:

### Example 1.1 DFS pruning tree (cellular)

First we prepare a complete rectangular maze:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
```

Next we run the algorithm:
```
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> print(PruningTree.on(maze))
          maze algorithm (statistics)
                            visits      478
                 queuing structure  Stack
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (6, 1)
                       unprocessed        0
                          passages      103
              maximum queue length       82
              average queue length       44.3654
```

Now we turn to Dijkstra's algorithm to find a longest path:
```
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                       | *   *   *   *     | *   * |
+   +---+   +---+---+---+   +---+---+   +   +   +   +
|   | T |   | *   *   *   * |   | *   * |   | * | * |
+---+   +   +   +---+---+---+   +   +---+---+   +   +
| *   * |     * |     *   *   * | *   *   * | * | * |
+   +---+---+   +---+   +---+   +---+---+   +   +   +
| *   *   * | *   *   * |     *   S | *   * | * | * |
+---+---+   +---+---+---+---+---+---+   +---+   +   +
|   | *   * | *   *   *   *   *   * | *   *   * | * |
+   +   +---+   +---+---+---+---+   +---+---+---+   +
|   | * |     *   * |       | *   * | *   *   * | * |
+   +   +---+---+   +---+   +   +---+   +---+   +   +
|   | * | *   * | *   * | *   * | *   * | *   * | * |
+   +   +   +   +---+   +   +---+   +---+   +---+   +
|     *   * | *   *   * | *   *   * |     *   *   * |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
It seems to cover about 4/5 of the maze.  Let's check its length:
```
>>> print(f"diameter = {dijkstra.distance(target)}")
diameter = 81
```
81 passages (and thus 82 cells),  And there were a maximum of 82 cells in the stack.  This is, of course, not a coincidence.

Next, let's look at the corresponding passage carver...

### Example 1.2 DFS growing tree (cellular)

We begin by preparing an empty maze:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8,13))
```

Next we use the depth-first search passage carver (a cell-based growing tree):
```
>>> from mazes.Algorithms.dfs_better import DFS
>>> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits      207
                        start cell  (5, 7)
               maximum stack depth       83
                             cells      104
                          passages      103
```

From the stack, we see that the longest path is 82 passages (or 83 cells) in length.  Time for Dijkstra:
```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|         *   * |     *   *   *     | *   *   *   * |
+---+---+   +   +---+   +---+   +---+   +---+---+   +
| *   * | * | *   *   * | *   * | *   * | *   * | * |
+   +   +   +---+---+---+   +---+   +---+   +   +   +
| * | *   * | *   *     | * | S | * | *   * | *   * |
+   +---+---+   +   +---+   +   +   +   +---+---+---+
| * |         * | *   *   * | *   * | *   * | *   * |
+   +---+---+   +---+---+---+---+---+---+   +   +   +
| * | *   * | *   *   *   *   T | *   * | *   * | * |
+   +   +   +---+   +---+---+---+   +   +---+---+   +
| * | * | * |       | *   * | *   * | *   * | *   * |
+   +   +   +---+---+   +   +   +---+---+   +   +---+
| * | * | * | *   *   * | *   * |       | *   * |   |
+   +   +   +   +---+---+---+---+   +   +---+---+   +
| *   * | *   *                     |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
And to confirm the length (in passages):
```
>>> print(f"diameter = {dijkstra.distance(target)}")
diameter = 82
```

And, finally we call on the clunk DFS basic wall builder...

### Example 1.3 DFS basic wallbuilder

We begin by preparing a complete maze:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
```

Next we call the basic wall builder, which defaults to the DFS circuit locator.
```
>>> from mazes.WallBuilders.basic_wallbuilder import BasicWallbuilder
>>> print(BasicWallbuilder.on(maze))
          maze algorithm (statistics)
                            visits       85
                           locator  Circuit Locator
                     finder passes     2975
                           unlinks       84
```
Apart from telling us that it did a lot of work to find 84 passages to remove, we don't get much information.  Dijkstra's turn:
```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       | *   *   *   * |   | *   * | S   *   * |   |
+   +---+   +   +---+   +   +   +   +---+   +   +   +
|       | * |   |   | *     | * | *   * |   | *   * |
+   +---+   +---+   +   +   +   +---+   +---+---+   +
|       | *   * |   | * |   | *     | *   *   * | * |
+   +   +---+   +   +   +---+   +   +---+---+   +   +
|   |   |   | *   * | *   T | * |       |   | * | * |
+---+   +   +---+   +---+---+   +---+---+   +   +   +
|       |       | * |   | *   *     |       | *   * |
+   +---+   +---+   +   +   +   +---+   +   +---+   +
|         *   *   * |     * |           |       |   |
+   +   +   +---+---+---+   +---+   +---+---+---+   +
|   |   | *   *   *   *   *     |   |   |   |       |
+   +---+---+---+---+   +---+   +---+   +   +---+---+
|               |           |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Our longest path is significantly shorter...
```
>>> print(f"diameter = {dijkstra.distance(target)}")
diameter = 44
```

### Comments on the examples in Section 1

The similarity in the results in Examples 1.1 and 1.2 arises because DFS pruning tree on a complete subgrid and DFS growing tree on an empty maze achieve the same results in two different ways.  Based solely on the number of visits in the two examples, the pruning tree approach seems to take about twice as long on a *Von Neumann* rectangular grid as the growing tree approach.  Both have run times which are approximately linear in the number of cells.

On a complete maze, the situation changes.  The number of edges grows quadraticly in the number of cells.  So the practicality depends on the underlying grid.  If the number of grid edges is asymptotically linear in the number of cells, the pruner is in the same asymptotic class as the grower -- the choice is implementation dependent.  (Our implementation of grids favors carvers, hence the small grower advantage.)

But, with a quadratic grid, the pruner has a significant hurdle to clear.

As an aside, the DFS passage carver is usually called *recursive backtracker* (here implemented iteratively using a stack).  So the DFS passage carver might be called *reverse recursive backtracker*.

The pruner and the grower represent two ways to achieve the same result. The basic wall builder is only superficially related in its use of depth-first search.  Unlike the pruner, each time a passage is removed, the wall builder completely forgets its place.  That forgetting has two consequences:

1. the wall builder uses a lot more effort to arrive at a perfect maze; and
2. the wall builder arrives in a very different place.

But note that if we don't randomize the results by shuffling the neighborhoods or varying the starting cell, the three algorithms all arrive in exactly the same place.  That suggests that the wall builder is a generalization of the pruner.  It can, in principle, arrive at the same place as the pruner, but, in practice, it rarely does.

## Section 2 - Passage-based search

The *PruningTree* class defaults to placing cells in the queue.  But it can instead enqueue passages.  The option *visit\_type* defaults to "cell":

*  if the visit type is "cell", "vertex" or "node", then cells will be enqueued; and
*  if the visit type is "passage", "join", "edge" or "arc", then passages will be enqueued;
*  any other vertex type raises a *NotImplementedError* exception in the *initialize()* and *configure()* methods; this exception is intended as an aid in writing subclass modules.

### Example 2.1 DFS pruning tree (passage-based)

We start with a complete rectangular maze:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
```

We specify one of the passage options when running the algorithm:
```
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> print(PruningTree.on(maze, visit_type="edge"))
          maze algorithm (statistics)
                            visits      274
                 queuing structure  Stack
                           unlinks       84
                          arrivals      274
                        departures      274
                        visit type  edge
                        start cell  (5, 7)
                     loops removed        0
                       unprocessed        0
                          passages      103
              maximum queue length       93
              average queue length       53.4708
```

The stack contains extra edges, so we cannot ascertain the diameter from the maximum stack length.  Now for Dijkstra:
```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|     *   *   T |           |       | *   *         |
+---+   +   +---+   +---+   +---+   +   +   +---+   +
| *   * |   |       |   |       | *   * | *   * |   |
+   +---+---+   +---+   +---+   +   +---+---+   +---+
| *   * |       |       |       | * | S   * | *   * |
+---+   +   +---+---+   +---+---+   +---+   +---+   +
| *   * |       | *   * |   | *   * | *   * | *   * |
+   +---+---+   +   +   +   +   +---+   +---+   +   +
| *   *   * |   | * | * |     *   *   * | *   * |   |
+---+---+   +   +   +   +---+---+   +---+   +---+   +
| *   *   * |   | * | * | *   * |   | *   * |   |   |
+   +---+   +   +   +   +   +   +   +   +---+   +   +
| * |       |   | * | * | * | * |   | * |       |   |
+   +---+---+   +   +   +   +   +---+   +   +---+   +
| *   *   *   *   * | *   * | *   *   * |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> print(f"diameter = {dijkstra.distance(target)}")
diameter = 62
```
This only covers 3/5 of the maze, but before we jump to any conclusions, here are results from a followup run:
```
          maze algorithm (statistics)
                            visits      273
                 queuing structure  Stack
                           unlinks       84
                          arrivals      273
                        departures      273
                        visit type  edge
                        start cell  (0, 5)
                     loops removed        0
                       unprocessed        0
                          passages      103
              maximum queue length      119
              average queue length       61.3278
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| *   *   *   *   *   * |             *   *   * |   |
+   +---+---+---+---+   +---+---+---+   +---+   +   +
| *         | *   *   * | *   * | *   * |   | * |   |
+   +---+   +   +---+---+   +   +   +---+   +   +   +
| * |       | * | *   * | * | *   * | *   *   * |   |
+   +   +---+   +   +   +   +---+---+   +---+---+   +
| * |       | *   * | *   * | *   *   * | *   * |   |
+   +---+   +---+---+---+---+   +---+---+   +   +   +
| * |   |   | S   *   *   * | *   *   *   * | * |   |
+   +   +   +---+---+---+   +---+---+---+---+   +   +
| *   * |               | *   *     | *   * | *   * |
+---+   +---+---+---+   +   +   +---+   +   +---+   +
| T | *   *   *   * |   |   | * | *   * | * | *   * |
+   +---+---+---+   +   +   +   +   +---+   +   +---+
| *   *   *   *   * |   |   | *   *     | *   *     |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
diameter = 75
```

Based on the number of visits, the edge-based pruner seems to compete a bit more favorably with the cell-based grower, but there is a bit more work per visit, so the statistics may be misleading.

## Section 3 - Other queuing structures

We are not stuck with depth-first search.  We can drop in a queue for breadth-first search for a dependably boring maze -- very boring but theoretically very important...

### Example 3.1 BFS pruning tree (cellular)
```
>>> from mazes.maze import Maze
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.queue import Queue
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=Queue))
          maze algorithm (statistics)
                            visits      394
                 queuing structure  Queue
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (7, 7)
                       unprocessed        0
                          passages      103
              maximum queue length       15
              average queue length       10.1827
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+---+---+---+---+---+---+---+   +   +---+---+---+---+
|                               |                   |
+---+---+---+---+---+   +   +   +   +   +   +---+---+
|                       |   |   |   |   |           |
+---+---+---+---+   +   +   +   +   +   +   +   +---+
|                   |   |   |   |   |   |   |       |
+---+---+---+---+   +   +   +   +   +   +   +   +---+
|                   |   |   |   |   |   |   |       |
+---+---+---+   +   +   +   +   +   +   +   +   +   +
|               |   |   |   |   |   |   |   |   |   |
+---+---+   +   +   +   +   +   +   +   +   +   +   +
|           |   |   |   |   |   |   |   |   |   |   |
+---+---+   +   +   +   +   +   +   +   +   +   +   +
|           |   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 3.2 a split stack (target size 1)

We can supply arguments to the queue constructor.  For a not-quite DFS maze, we try a split stack with a target size of 1:
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.split_stack import SplitStack
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=SplitStack, qargs=[1]))
          maze algorithm (statistics)
                            visits      394
                 queuing structure  SplitStack
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (6, 6)
                       unprocessed        0
                          passages      103
              maximum queue length       42
              average queue length       24.4423
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |                       |       |
+   +   +---+   +---+---+   +---+   +   +---+   +---+
|   |   |           |           |   |               |
+   +---+---+   +---+---+   +---+---+   +   +   +   +
|       |       |   |   |   |       |   |   |   |   |
+   +---+---+   +   +   +---+   +---+---+---+---+   +
|       |                       |   |   |           |
+   +   +---+   +   +---+   +---+   +   +---+   +   +
|   |       |   |   |       |                   |   |
+---+   +   +---+---+---+   +---+   +   +   +   +---+
|   |   |       |   |               |   |   |   |   |
+   +---+   +---+   +---+   +   +   +---+---+---+   +
|   |           |       |   |   |   |               |
+   +---+   +---+   +---+---+---+---+   +---+   +   +
|                                           |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
A split stack with target length 1 has some stack-like behavior.  But it's also a bit schizophrenic.  We get a moderately large diameter and more dead ends than with depth-first search (*i.e.* with a stack).

**DISCLAIMER**: "Split stack* is my name for the structure.  If you find a reference to a "split stack" somewhere, it probably means something else.

```
>>> from mazes.Algorithms.dijkstra import Dijkstra
>>> dijkstra = Dijkstra(maze, maze.grid[0,0])
>>> source = dijkstra.farthest
>>> dijkstra.calculate(source)
>>> target = dijkstra.farthest
>>> dijkstra.label_path(target)
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
| *   *   *   *     |     *   *   *   *     |       |
+   +   +---+   +---+---+   +---+   +   +---+   +---+
| * |   |     *     |     *   S |   | *   *   *   * |
+   +---+---+   +---+---+   +---+---+   +   +   +   +
| *     |     * |   |   |   |       |   |   |   | * |
+   +---+---+   +   +   +---+   +---+---+---+---+   +
| *   * |     *   *   *   *     |   |   |     *   * |
+   +   +---+   +   +---+   +---+   +   +---+   +   +
|   | *   * |   |   |     * |     *   *   *   * |   |
+---+   +   +---+---+---+   +---+   +   +   +   +---+
|   |   | *     |   |     *   *   * |   |   |   | T |
+   +---+   +---+   +---+   +   +   +---+---+---+   +
|   |     *     |       |   |   |   | *   *   *   * |
+   +---+   +---+   +---+---+---+---+   +---+   +   +
|         *   *   *   *   *   *   *   *     |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> print(f"diameter = {dijkstra.distance(target)}")
diameter = 51
```

### Example 3.3 a split stack (target size 10)

Increasing the target length increases the schizoid behavior up to a point.  If the target length exceeds the longest queue length, then the search reduces to breadth-first search (*i.e.* a true queue).  And even before that, the BFS-like behavior becomes evident.  The default target length is 10, only because 10 is a small round number.
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.split_stack import SplitStack
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=SplitStack))
          maze algorithm (statistics)
                            visits      394
                 queuing structure  SplitStack
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (7, 5)
                       unprocessed        0
                          passages      103
              maximum queue length       21
              average queue length       13.1442
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+---+---+---+---+   +   +   +   +---+---+---+---+---+
|                   |   |   |                       |
+---+---+---+   +   +   +   +   +---+---+---+   +   +
|               |   |   |   |               |   |   |
+   +   +   +   +   +   +   +   +---+   +---+---+---+
|   |   |   |   |   |   |   |       |               |
+   +   +---+---+   +   +   +   +---+---+   +   +---+
|   |   |           |   |   |           |   |       |
+   +   +---+   +   +   +   +   +   +---+---+   +---+
|   |   |       |   |   |   |   |           |       |
+   +   +---+   +   +   +   +---+   +   +---+   +   +
|   |   |       |   |   |       |   |       |   |   |
+   +   +---+   +   +   +   +   +---+   +---+---+---+
|   |   |       |   |   |   |       |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
How's that for *BFS-like* behavior?

### Example 3.4 a split queue (target size 10)

Another queue structure to play with is a split queue.  (The disclaimer in Example 3.2 applies to split queues as well.)  Let's start with the default, a target size of 10:
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.split_queue import SplitQueue
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=SplitQueue))
          maze algorithm (statistics)
                            visits      407
                 queuing structure  SplitQueue
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (1, 5)
                       unprocessed        0
                          passages      103
              maximum queue length       20
              average queue length       15.7692
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |   |   |   |   |   |   |   |   |
+---+---+---+---+   +   +   +   +   +   +   +   +   +
|                       |   |   |   |   |   |   |   |
+---+---+---+---+---+   +   +   +   +   +   +   +   +
|                       |   |   |   |   |   |   |   |
+---+---+---+---+---+   +   +   +   +   +   +   +   +
|                           |   |   |   |   |   |   |
+---+---+---+---+---+---+   +   +   +   +   +   +   +
|                           |   |   |   |   |   |   |
+   +   +   +   +---+---+   +   +   +   +   +   +   +
|   |   |   |   |       |           |   |           |
+   +   +   +   +   +   +---+---+   +   +   +---+---+
|   |   |   |   |   |   |       |                   |
+   +   +   +   +   +---+   +   +   +---+---+---+---+
|   |   |   |   |           |                       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

There is just a little bit of interesting noise near row 1 column 5.  Elsewhere we see queue-like behavior of the BFS variety.

### Example 3.5 a split queue (target size 80)

Let's increase the target size to 90...
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.split_queue import SplitQueue
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=SplitQueue, qargs=[80]))
          maze algorithm (statistics)
                            visits      478
                 queuing structure  SplitQueue
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (2, 3)
                       unprocessed        0
                          passages      103
              maximum queue length       74
              average queue length       39.1538
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |       |                   |
+   +   +   +   +   +   +   +   +---+   +   +---+   +
|   |       |   |   |       |       |   |       |   |
+   +---+---+   +   +---+---+---+   +---+---+   +---+
|               |   |           |   |       |       |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|               |       |       |       |   |   |   |
+   +---+---+   +---+---+   +---+---+---+   +   +   +
|   |               |       |       |       |   |   |
+   +---+   +---+   +   +   +   +   +   +---+---+   +
|       |   |   |   |   |   |   |   |           |   |
+---+   +---+   +   +   +---+   +   +---+---+   +   +
|   |           |   |           |   |       |   |   |
+   +---+---+---+   +---+---+---+   +   +---+   +   +
|                                   |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 3.5 a split queue (target size 80)

Let's increase the target size to 90...
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.split_queue import SplitQueue
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=SplitQueue, qargs=[80]))
          maze algorithm (statistics)
                            visits      478
                 queuing structure  SplitQueue
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (2, 3)
                       unprocessed        0
                          passages      103
              maximum queue length       74
              average queue length       39.1538
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |       |                   |
+   +   +   +   +   +   +   +   +---+   +   +---+   +
|   |       |   |   |       |       |   |       |   |
+   +---+---+   +   +---+---+---+   +---+---+   +---+
|               |   |           |   |       |       |
+---+---+---+---+   +   +---+   +   +   +   +   +   +
|               |       |       |       |   |   |   |
+   +---+---+   +---+---+   +---+---+---+   +   +   +
|   |               |       |       |       |   |   |
+   +---+   +---+   +   +   +   +   +   +---+---+   +
|       |   |   |   |   |   |   |   |           |   |
+---+   +---+   +   +   +---+   +   +---+---+   +   +
|   |           |   |           |   |       |   |   |
+   +---+---+---+   +---+---+---+   +   +---+   +   +
|                                   |               |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 3.6 reverse Prim's algorithm

Let's do Prim's algorithm backwards -- we will repeatedly remove the lowest cost passage in the frontier that creates a circuit...
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> from mazes.Queues.priority_queue import PriorityQueue
```

A little help with the constructor...
```
>>> help(PriorityQueue.__init__)
Help on function __init__ in module mazes.Queues.priority_queue:

__init__(self, priority:callable=None, action='unstable', cache=True)
    constructor
```

We need a cost function for the passages, but we can let the priority queue structure determine the actual costs using its cache.  All our cost function needs to do is return the value None.  We could have it return a numerical value for some of or all of the passages, or just let the cache do everything from scratch, but we need to show how to pass keyword arguments to the priority queue through class *PruningTree.Status*...
```
>>> cost = lambda passage: None
```

We will pass it as a keyword argument, so instead of *qargs* and a tuple or list, we use *qkwargs* and a dictionary with the keywords written as character strings.
```
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> print(PruningTree.on(maze, QueueType=PriorityQueue, qkwargs={"priority":cost}))
          maze algorithm (statistics)
                            visits      396
                 queuing structure  PriorityQueue
                           unlinks       84
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (6, 7)
                       unprocessed        0
                          passages      103
              maximum queue length       37
              average queue length       22.3942
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |               |                           |
+   +   +---+   +   +   +---+   +   +   +   +   +   +
|           |   |   |       |   |   |   |   |   |   |
+---+   +---+---+---+---+   +---+---+---+---+   +   +
|   |   |   |   |           |   |               |   |
+   +   +   +   +---+   +   +   +---+   +   +   +   +
|               |   |   |               |   |   |   |
+---+   +---+   +   +---+   +   +---+   +   +---+---+
|       |               |   |   |       |   |       |
+   +---+---+---+---+   +---+   +---+   +---+   +---+
|           |   |                   |   |           |
+   +   +---+   +---+   +   +   +---+---+   +---+   +
|   |   |               |   |   |               |   |
+   +   +---+   +---+   +---+---+   +---+   +---+---+
|   |       |   |                       |           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

## Section 4 - Pruning a disconnected maze

### Example 4.1 How *PruningTree* handled disconnections
First we create a disconnected but otherwise complete rectangular maze:
```
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> maze = Maze(OblongGrid(8,13)); maze.link_all()
>>> for j in range(13):
...     cell = maze.grid[4,j]
...     join = cell.join_for(cell.south)
...     maze.unlink(join)
...
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
That's a nice hard wall splitting the two middle rows.

Let's prune the maze using a stack and see what happens.  We will save the status:
```
>>> status = PruningTree.on(maze); print(status)
          maze algorithm (statistics)
                            visits      226
                 queuing structure  Stack
                           unlinks       36
                          arrivals       52
                        departures       52
                        visit type  cell
                        start cell  (1, 4)
                       unprocessed       52
                          passages      138
              maximum queue length       37
              average queue length       18.6154
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+   +   +   +   +   +   +   +   +   +   +   +   +   +
|                                                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |                       |       |   |
+   +   +---+   +---+---+---+   +---+   +   +   +   +
|   |   |                   |   |       |   |   |   |
+   +   +---+---+---+---+   +   +   +---+   +   +   +
|   |       |       |   |   |   |           |   |   |
+   +---+   +   +---+   +   +   +---+---+---+   +   +
|       |       |               |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Wow! A nice maze in the bottom half!  Note that 52 cells were "unprocessed".

We can resume in the top half, either automatically, or by specifying a start cell:
```
>>> status.resume(); print(status)
          maze algorithm (statistics)
                            visits      452
                 queuing structure  Stack
                           unlinks       72
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (5, 9)
                       unprocessed        0
                          passages      102
              maximum queue length       37
              average queue length       17.9808
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |           |               |
+   +   +---+   +   +---+   +   +---+   +---+   +   +
|   |   |           |       |               |   |   |
+   +   +---+---+   +   +---+---+---+---+   +   +   +
|   |           |   |   |           |   |   |   |   |
+   +---+---+   +---+   +---+   +   +   +---+   +   +
|           |                   |   |           |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |                       |       |   |
+   +   +---+   +---+---+---+   +---+   +   +   +   +
|   |   |                   |   |       |   |   |   |
+   +   +---+---+---+---+   +   +   +---+   +   +   +
|   |       |       |   |   |   |           |   |   |
+   +---+   +   +---+   +   +   +---+---+---+   +   +
|       |       |               |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

And the only thing we need to make this a *perfect maze* is a door to connect these two rooms:
```
>>> from mazes import rng
>>> cell = maze.grid[4, rng.randrange(13)]
>>> cell.label = "X"
>>> maze.link(cell, cell.south)
<Edge object>
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|               |       |           |               |
+   +   +---+   +   +---+   +   +---+   +---+   +   +
|   |   |           |       |               |   |   |
+   +   +---+---+   +   +---+---+---+---+   +   +   +
|   |           |   |   |           |   |   |   |   |
+   +---+---+   +---+   +---+   +   +   +---+   +   +
|           |                   | X |           |   |
+---+---+---+---+---+---+---+---+   +---+---+---+---+
|               |                       |       |   |
+   +   +---+   +---+---+---+   +---+   +   +   +   +
|   |   |                   |   |       |   |   |   |
+   +   +---+---+---+---+   +   +   +---+   +   +   +
|   |       |       |   |   |   |           |   |   |
+   +---+   +   +---+   +   +   +---+---+---+   +   +
|       |       |               |                   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The *PruningTree* class doesn't jump from one component to another.

### Example 4.2 Automatically pruning a cellular automaton maze

Let's create a maze using a cellular automaton:
```
$ python
>>> ca = Automaton2({3}, {1,2,3,4,5}, 8, 13, bias=0.4)
>>> for _ in range(30): ca.next_generation()
...
generation 0: (automaton) 194 alive; (maze) 87 passages.
generation 1: (automaton) 246 alive; (maze) 101 passages.
generation 2: (automaton) 253 alive; (maze) 102 passages.
generation 3: (automaton) 261 alive; (maze) 107 passages.
generation 4: (automaton) 260 alive; (maze) 106 passages.
generation 5: (automaton) 262 alive; (maze) 106 passages.
generation 6: (automaton) 263 alive; (maze) 106 passages.
generation 7: (automaton) 262 alive; (maze) 106 passages.
generation 7: stable configuration
Warning: generation 7: stable configuration
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |   |       |       |   |   |
+   +---+---+   +   +---+   +   +---+   +   +   +   +
|   |           |               |       |       |   |
+---+   +   +---+   +   +---+   +---+---+---+   +---+
|       |   |       |   |       |           |       |
+   +   +---+   +---+   +   +---+   +---+   +---+   +
|   |                   |   |           |           |
+   +---+   +---+   +   +   +   +---+   +---+---+   +
|               |   |   |   |   |   |           |   |
+   +   +---+---+   +   +   +   +   +   +---+---+---+
|       |           |       |       |   |           |
+   +---+   +---+   +   +---+   +   +   +   +   +---+
|               |       |       |   |   |       |   |
+---+   +---+   +   +---+   +---+   +---+   +---+   +
|   |       |   |           |                   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We can see right away that there are *at least* five components.  The four corners are not connected to the interior of the grid.  There are also some obvious circuits.  Let's bring in *PruningTree*:
```
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |   |       |       |   |   |
+   +---+---+   +   +---+   +   +---+   +   +   +   +
|   |           |               |       |       |   |
+---+   +   +---+   +   +---+   +---+---+---+   +---+
|       |   |       |   |       |           |       |
+   +   +---+   +---+   +   +---+   +---+   +---+   +
|   |                   |   |           |           |
+   +---+   +---+   +   +   +   +---+   +---+---+   +
|               |   |   |   |   |   |           |   |
+   +   +---+---+   +   +   +   +   +   +---+---+---+
|       |           |       |       |   |           |
+   +---+   +---+   +   +---+   +   +   +   +   +---+
|               |       |       |   |   |       |   |
+---+   +---+   +   +---+   +---+   +---+   +---+   +
|   |       |   |           |                   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> status = PruningTree.on(ca.maze); print(status)
          maze algorithm (statistics)
                            visits      299
                 queuing structure  Stack
                           unlinks        8
                          arrivals       95
                        departures       95
                        visit type  cell
                        start cell  (3, 0)
                       unprocessed        9
                          passages       98
              maximum queue length       44
              average queue length       24.2579
```
Note that there are 9 unprocessed cells:
```
>>> status["unprocessed"]
9
```
It should be fairly obvious that there are actually no additional circuits as 8 of the nine unprocessed cells for the four corner components.  The remaining unprocessed cell is an isolated cell: top row, third column.   But let's program this to process all the unprocessed cells:
```
>>> while status["unprocessed"] != 0:
...     status.resume()
...
>>> print(status)
          maze algorithm (statistics)
                            visits      316
                 queuing structure  Stack
                           unlinks        8
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (7, 12)
                       unprocessed        0
                          passages       98
              maximum queue length       44
              average queue length       22.2500
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|       |   |           |   |       |       |   |   |
+   +---+---+   +   +---+   +   +---+   +   +   +   +
|   |           |   |           |       |       |   |
+---+   +   +---+   +   +---+   +---+---+---+   +---+
|       |   |       |   |       |           |       |
+   +   +---+   +---+---+   +---+   +---+   +---+   +
|   |       |           |   |           |           |
+---+---+   +---+---+   +   +   +---+   +---+---+   +
|               |   |   |   |   |   |           |   |
+---+---+---+---+   +   +   +   +   +   +---+---+---+
|       |           |       |       |   |           |
+   +---+   +---+   +   +---+   +   +   +   +   +---+
|               |       |       |   |   |   |   |   |
+---+   +---+   +   +---+   +---+   +---+   +---+   +
|   |       |   |           |                   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Now all the cells have been processed.  But we need a 5 more passages for *perfection*.  Kruskal's algorithm comes to our rescue:
```
>>> from mazes.Algorithms.kruskal import Kruskal
>>> print(Kruskal.on(ca.maze))
          Kruskal (statistics)
                            visits        8
                 components (init)        6
               queue length (init)       14
                             cells      104
                          passages        5
                components (final)        1
              queue length (final)        6
>>> print(ca.maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                       |   |       |       |   |   |
+   +---+---+   +   +---+   +   +---+   +   +   +   +
|   |           |   |           |       |           |
+---+   +   +---+   +   +---+   +---+---+---+   +---+
|       |   |       |   |       |           |       |
+   +   +---+   +---+---+   +---+   +---+   +---+   +
|   |       |           |   |           |           |
+---+---+   +---+---+   +   +   +---+   +---+---+   +
|               |   |   |   |   |   |           |   |
+---+---+---+---+   +   +   +   +   +   +---+---+---+
|       |           |       |       |   |           |
+   +---+   +---+   +   +---+   +   +   +   +   +---+
|               |       |       |   |   |   |       |
+---+   +---+   +   +---+   +---+   +---+   +---+   +
|           |   |           |                   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 4.3 Simple binary tree on a torus (sometimes!)

If we run the simple binary tree algorithm on a toroidal grid we have two problems:

1. we will *always* produce a maze with one too many edges to be a tree; and
2. we will *sometimes* produce a maze which is disconnected.

Algorithm class *PruningTree* can easily fix the first problem.  Although it cannot fix the second problem, it can detect the condition.

First an example of a successful run.  We start by running simple binary tree
on a toroidal grid:
```
$ python
>>> from mazes.Grids.torus import TorusGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.simple_binary_tree import BinaryTree
>>> maze = Maze(TorusGrid(8,13))       # create the grid and maze
>>> print(BinaryTree.on(maze))         # run simple binary tree
          Simple Binary Tree (statistics)
                            visits      105
                             cells      104
                          passages      104
                            onward  east
                            upward  north
                              bias        0.5000
```
For this to be a binary tree we would need to satisfy the following three conditions:

* the maze should be connected;
* the number of passages should be less than the number of cells; and
* the maze should have no cells of degree greater than three.

From the information given so far, we cannot immediately verify that the maze is connected.  But class *PruningTree* does check and indirectly report a problem.

We can immediately see that the number of passages is equal to the number of cells, and thus the maze cannot be a tree.

Knowing how the algorithm works tells us immediately that every cell has degree one, two, or three.  In each cell we carve a passage either north or east, but never both.  The torus grid respects direction: stepping west then east returns us to place; likewise stepping north then south.  From another cell, we can only enter from the south or the west.  That gives a minimum of one and a maximum of three incident passages.  (This proof would fail if, for example, two steps east from some cell returned us to the same cell.)

Now we run the pruning tree algorithm.  We will use depth-first search, but any valid queue-based search will work:
```
>>> from mazes.WallBuilders.pruning_tree import PruningTree
>>> print(PruningTree.on(maze))
          maze algorithm (statistics)
                            visits      312
                 queuing structure  Stack
                           unlinks        1
                          arrivals      104
                        departures      104
                        visit type  cell
                        start cell  (7, 4)
                       unprocessed        0  <--- NOTE!
                          passages      103
              maximum queue length       31
              average queue length       16.7596
```
Every cell was processed, so we know the maze was connected.  One passage was removed, so we know we have a tree (as it is connected as there are fewer passages than cells).  *PruningTree* cannot remove edges that are not contained in circuits, so we know that the maze remains connected and as a result, (i) every cell that was a dead end before remains a dead end after (as connected implies no isolated cells) and (ii) no cell can have more than three incident passages (as this would require that some cell previously had at least four incident passages). Hence it is a binary tree.

Here is our maze.  (Imagine playing *PacMan*™ in this maze!)
```
>>> print(maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏   ┳   ┳━━━┳   ┳━━━┳━━━┳   ┳━━━┳━━━┳━━━┳   ┳━━━┳━━━┓
  7     ┃   ┃       ┃       ┃   ┃               ┃         7
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ┫
  6 ┃   ┃   ┃       ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃ 6
    ┣━━━╋━━━╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━┫
  5             ┃       ┃   ┃       ┃   ┃   ┃       ┃     5
    ┣   ╋   ╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ┫
  4 ┃   ┃   ┃   ┃           ┃   ┃       ┃   ┃       ┃   ┃ 4
    ┣━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋━━━╋   ╋━━━╋━━━╋━━━╋   ┫
  3 ┃       ┃   ┃       ┃   ┃           ┃               ┃ 3
    ┣   ╋━━━╋━━━╋━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋━━━╋   ╋   ┫
  2 ┃   ┃               ┃           ┃   ┃           ┃   ┃ 2
    ┣━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋━━━╋   ╋━━━╋━━━╋━━━╋━━━┫
  1         ┃   ┃       ┃   ┃   ┃       ┃                 1
    ┣━━━╋   ╋━━━╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋━━━┫
  0         ┃           ┃   ┃       ┃   ┃       ┃   ┃     0
    ┗   ┻   ┻━━━┻   ┻━━━┻━━━┻   ┻━━━┻━━━┻━━━┻   ┻━━━┻━━━┛
      A   B   C   D   E   F   G   H   I   J   K   L   M
```

### Example 4.4-1 Simple binary tree on a torus (failure example)

So how could a simple binary tree fail to produce a connected maze on a toroidal grid?  Just one way is to suppose that there were two columns in which all the coin flips were heads (carve north!).  In that case we would have two hard walls blocking eastward movement.

Using that discussion as inspiration, let's try to create such a scenario.  We could certainly use a bias of 1 (*i.e.* 100% heads) to guarantee that we could never move east, but that seems drastic.  Let's try 80%:
```
>>> maze = Maze(TorusGrid(8,13))
>>> print(BinaryTree.on(maze, bias=0.8))
          Simple Binary Tree (statistics)
                            visits      105
                             cells      104
                          passages      104
                            onward  east
                            upward  north
                              bias        0.8000
>>> print(PruningTree.on(maze))
          maze algorithm (statistics)
                            visits      120
                 queuing structure  Stack
                           unlinks        1
                          arrivals       40
                        departures       40
                        visit type  cell
                        start cell  (1, 5)
                       unprocessed       64      <--- NOTE!
                          passages      103
              maximum queue length       21
              average queue length       10.3000
```
Success!  (When you're trying to fail and succeed in doing so, I think it counts as a success and not as a failure.  Oh, I do love paradox!)  Let's look at our maze:
```
>>> print(maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏   ┳━━━┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┳   ┓
  7 ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 7
    ┣   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
  6 ┃   ┃   ┃       ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃ 6
    ┣━━━╋━━━╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
  5 ┃           ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 5
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ┫
  4 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃ 4
    ┣   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ┫
  3 ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃ 3
    ┣   ╋   ╋━━━╋   ╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ┫
  2 ┃   ┃   ┃       ┃   ┃       ┃           ┃   ┃   ┃   ┃ 2
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ┫
  1 ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃ 1
    ┣   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ┫
  0 ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃ 0
    ┗   ┻━━━┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M

   W1                   W2                  W3      W4  W1  (long walls)
```
We have four complete long walls running north and south, so we have at least three components.  (The rightmost and leftmost long walls are the same long wall, so they should be counted as one.

### Example 4.4-2 Simple binary tree on a torus (another failure example)

Here is another example, this one with just two long hard walls:
```
>>> maze = Maze(TorusGrid(8,13))
>>> print(BinaryTree.on(maze, bias=0.8))
          Simple Binary Tree (statistics)
                            visits      105
                             cells      104
                          passages      104
                            onward  east
                            upward  north
                              bias        0.8000
>>> print(PruningTree.on(maze))
          maze algorithm (statistics)
                            visits      264
                 queuing structure  Stack
                           unlinks        1
                          arrivals       88
                        departures       88
                        visit type  cell
                        start cell  (3, 5)
                       unprocessed       16
                          passages      103
              maximum queue length       42
              average queue length       24.8182
>>> print(maze)
      A   B   C   D   E   F   G   H   I   J   K   L   M
    ┏   ┳   ┳   ┳   ┳━━━┳   ┳   ┳   ┳   ┳   ┳━━━┳   ┳   ┓
  7 ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃       ┃   ┃ 7
    ┣   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ╋   ╋   ╋   ╋━━━╋━━━┫
  6     ┃   ┃   ┃   ┃   ┃   ┃       ┃   ┃   ┃   ┃         6
    ┣━━━╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋   ┫
  5 ┃           ┃   ┃   ┃   ┃   ┃   ┃   ┃           ┃   ┃ 5
    ┣   ╋━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
  4 ┃   ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 4
    ┣   ╋   ╋━━━╋   ╋   ╋   ╋   ╋   ╋━━━╋━━━╋   ╋━━━╋   ┫
  3 ┃   ┃   ┃       ┃   ┃   ┃   ┃   ┃           ┃       ┃ 3
    ┣   ╋━━━╋   ╋━━━╋   ╋━━━╋━━━╋   ╋   ╋   ╋   ╋━━━╋   ┫
  2 ┃   ┃       ┃       ┃   ┃       ┃   ┃   ┃   ┃       ┃ 2
    ┣━━━╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ┫
  1 ┃       ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃ 1
    ┣   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋   ╋━━━╋   ┫
  0 ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃   ┃       ┃ 0
    ┗   ┻   ┻   ┻   ┻━━━┻   ┻   ┻   ┻   ┻   ┻━━━┻   ┻   ┛
      A   B   C   D   E   F   G   H   I   J   K   L   M

                            W1      W2                      (long walls)
```
The sixteen unprocessed cells lie in the component east of W1 and west of W2.  It is easy to check that this is a single component.
