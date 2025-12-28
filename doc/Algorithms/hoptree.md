# Hop Trees (Experimental)

These are essentially a first attempt to create growing trees using a changing metric.  I suspect that the algorithm is not sufficiently time-efficient for carving large mazes, but it *might* be of use in creating small and medium-sized mazes for games.

The name *hop tree* is based on the fact that the algorithm extends mazes distances "one hop at a time".  Each time a passage is added, distances to and from the added cell are calculated as one more than the distance from its neighbor.

## Example 1 - farthest distance

The default seems to produce mazes with larger than average diameters, but not as deep as depth-first search mazes.  We start with three imports:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.hoptree import HopTree
```

Now we produce a maze by (a) initializing a grid, (b) applying the "hop search" algorithm, and (c) rendering the image:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(HopTree.on(maze))
          Hop Search (statistics)
                            visits      103
                        start cell  (6, 5)
                            action  furthest
                  selection passes     2579
                             cells      104
                  passages (start)        0
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|           |               |               |   |   |
+   +---+---+   +---+   +---+   +---+   +---+   +   +
|       |           |           |   |               |
+   +---+   +---+---+   +---+---+   +---+   +   +   +
|       |   |   |       |   |   |       |   |   |   |
+   +---+   +   +---+---+   +   +   +---+---+---+   +
|   |           |   |                   |   |       |
+   +---+---+   +   +---+   +---+   +---+   +---+   +
|   |   |   |               |           |   |       |
+   +   +   +   +---+   +---+---+   +---+   +---+   +
|           |   |   |   |               |           |
+   +---+   +---+   +---+---+   +   +---+---+   +   +
|   |       |                   |   |           |   |
+   +---+   +---+   +   +   +   +---+---+   +   +---+
|   |               |   |   |   |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
Each visit results in a passage, so the visits statistic is not particularly useful.  More telling is the selection passes statistic

## Example 2 - additional information

If we save the status, we can garner some additional information.
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(status := HopTree.on(maze))
          Hop Search (statistics)
                            visits      103
                        start cell  (5, 4)
                            action  furthest
                  selection passes     2565
                             cells      104
                  passages (start)        0
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                   |               |               |
+---+   +   +---+   +---+   +---+   +   +---+---+---+
|       |   |           |   |           |   |   |   |
+   +   +---+---+   +---+---+---+---+   +   +   +   +
|   |   |   |       |   |   |   |                   |
+   +---+   +---+   +   +   +   +---+   +---+---+   +
|       |   |                       |   |   |   |   |
+   +---+   +---+   +   +---+   +---+---+   +   +   +
|           |   |   |   |               |           |
+   +   +---+   +---+---+---+---+   +---+   +---+   +
|   |           |           |                   |   |
+---+   +   +---+---+   +---+---+   +   +   +---+   +
|   |   |           |       |   |   |   |   |       |
+   +---+   +   +---+   +---+   +---+---+---+   +   +
|           |               |                   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```

From the status, we can obtain access to every distance in the maze.
```
>>> d = 0
>>> passage = None
>>> for source in maze.grid:
...     for sink in maze.grid:
...         if status.metric.d(source, sink) > d:
...             d = status.metric.d(source, sink)
...             passage = (source, sink)
...
>>> d
44
```
The diameter is 44 edges.  That's about 42% of the grid!  It's high, but DFS would probably average around 50% of the maze.  (See the statistics from 8 October 2025.  Hunt and kill averaged about 30% and DFS about 52% in that study.  But note that those grids had about 7 times as many cells, and linear dimensions in those grids were about 2.6 times the examples in this write-up.) Here are the endpoints of a passage that gives rise to the distance:
```
>>> print(f"{passage[0].index} -- {passage[1].index}")
(2, 4) -- (6, 6)
```

## Example 3 - nearest distance

If we choose a frontier node as near as possible to the previous node (typically a neighbor one hop away), the results are similar, but less work is done in selecting frontier cells.
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(status := HopTree.on(maze, action="closest"))
          Hop Search (statistics)
                            visits      103
                        start cell  (6, 0)
                            action  closest
                  selection passes     1255
                             cells      104
                  passages (start)        0
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |               |   |                       |
+   +   +---+   +---+   +   +   +---+   +   +   +---+
|           |   |                   |   |   |       |
+   +   +---+---+---+   +---+   +---+---+---+   +---+
|   |           |   |       |   |                   |
+---+   +   +---+   +   +---+---+---+   +   +   +---+
|   |   |                   |           |   |   |   |
+   +---+   +   +   +   +---+---+   +   +---+---+   +
|       |   |   |   |   |           |   |   |   |   |
+   +---+---+---+---+---+   +   +   +---+   +   +   +
|   |               |       |   |   |               |
+   +   +---+---+---+---+   +---+---+   +---+   +   +
|       |   |   |   |           |   |       |   |   |
+---+   +   +   +   +---+   +---+   +   +---+---+   +
|                                           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> d = 0
>>> passage = None
>>> for source in maze.grid:
...     for sink in maze.grid:
...         if status.metric.d(source, sink) > d:
...             d = status.metric.d(source, sink)
...             passage = (source, sink)
...
>>> d
40
>>> print(f"{passage[0].index} -- {passage[1].index}")
(0, 11) -- (5, 0)
```

## Example 4 - random edge

If we choose a random frontier edge as our next edge, the work in selecting an edge disappears, but the diameter of the spanning tree shrinks.  The effect is similar to what we see in the simplified "Prim" algorithm.  In the October study, simplified Prim yielded an average diameter of about 11% on grids with about seven times as many cells -- the run below achieved about 22%.  And the linear dimensions on those grids were about 2.6 times (21 by 34 *versus* 8 by 13), so comparisons might be misleading.
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(status := HopTree.on(maze, action="random"))
          Hop Search (statistics)
                            visits      103
                        start cell  (7, 1)
                            action  random
                  selection passes        0
                             cells      104
                  passages (start)        0
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|                       |   |   |           |       |
+   +   +---+   +   +---+   +   +   +---+---+   +---+
|   |       |   |   |   |       |               |   |
+---+   +---+---+---+   +   +---+   +---+---+---+   +
|                   |   |   |               |   |   |
+---+---+   +---+   +   +   +   +---+---+---+   +   +
|               |               |           |       |
+---+---+   +---+---+   +---+   +---+   +---+---+   +
|                   |       |                       |
+   +---+   +---+   +---+   +---+---+   +---+   +   +
|   |           |   |               |   |   |   |   |
+---+   +   +   +   +---+   +   +   +   +   +---+---+
|   |   |   |   |   |       |   |   |               |
+   +   +---+---+   +---+   +---+   +---+---+   +---+
|           |           |       |           |       |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> d = 0
>>> passage = None
>>> for source in maze.grid:
...     for sink in maze.grid:
...         if status.metric.d(source, sink) > d:
...             d = status.metric.d(source, sink)
...             passage = (source, sink)
...
>>> d
23
>>> print(f"{passage[0].index} -- {passage[1].index}")
(0, 3) -- (0, 12)
```

## Example 5 - less shuffling

The implementation allows reducing some of the randomness, but we cannot remove all the randomness.
```
>>> maze = Maze(OblongGrid(8, 13))
>>> print(status := HopTree.on(maze, shuffle=False))
          Hop Search (statistics)
                            visits      103
                        start cell  (0, 10)
                            action  furthest
                  selection passes     2485
                             cells      104
                  passages (start)        0
                          passages      103
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |               |                           |   |
+   +---+---+   +---+---+   +   +   +   +---+   +   +
|           |       |       |   |   |   |   |       |
+   +---+---+   +---+---+   +---+---+---+   +   +---+
|       |       |                   |               |
+   +---+---+   +---+   +---+---+---+---+   +---+---+
|   |   |               |   |   |   |       |   |   |
+   +   +---+---+   +---+   +   +   +---+   +   +   +
|           |   |   |                   |           |
+   +---+   +   +---+---+   +---+   +---+---+---+   +
|   |                       |               |   |   |
+   +---+   +   +   +   +   +---+   +---+---+   +   +
|       |   |   |   |   |   |       |               |
+   +   +---+---+---+---+---+---+   +---+   +---+   +
|   |                       |                   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
>>> d = 0
>>> passage = None
>>> for source in maze.grid:
...     for sink in maze.grid:
...         if status.metric.d(source, sink) > d:
...             d = status.metric.d(source, sink)
...             passage = (source, sink)
...
>>> d
52
>>> print(f"{passage[0].index} -- {passage[1].index}")
(0, 6) -- (7, 1)
```

## Example 6 - uptown maze

So far the results have been underwhelming, but there might be a very nice application here, and possibly some considerations for later work.  So far, all the growing tree algorithms all start with a single seed.  Now imagine a game that models a city with dense infrastructure (such as streets, or perhaps a network of water pipes), surrounded by countryside with light infrastructure.

In the city, we can go around a single block (i.e. a small circuit).  In the countryside, there are no circuits, just road which eventually lead into the city.  We can think of the city as a single node in a maze.  The cells in the countryside form all the other nodes.

We might instead have a dense downtown and a sparse uptown...

And now we proceed (from scratch), starting with three imports:
```
$ python
>>> from mazes.Grids.oblong import OblongGrid
>>> from mazes.maze import Maze
>>> from mazes.Algorithms.hoptree import HopTree
```

We will first build our downtown inside a larger grid.  We just mask the entire uptown area, and then link all the unmasked edges:
```
>>> maze = Maze(OblongGrid(8, 13))
>>> for i in range(8):
...     for j in range(13):
...         if 2 <= i <= 5:
...             if 4 <= j <= 8:
...                 continue
...         maze.grid[i,j].hide()
...
>>> maze.link_all()
```

We need to remove all the masks...  And let's take a preparatory peak:
```
>>> maze.grid.reveal_all()     # IMPORTANT!
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |                   |   |   |   |   |
+---+---+---+---+   +   +   +   +   +---+---+---+---+
|   |   |   |   |                   |   |   |   |   |
+---+---+---+---+   +   +   +   +   +---+---+---+---+
|   |   |   |   |                   |   |   |   |   |
+---+---+---+---+   +   +   +   +   +---+---+---+---+
|   |   |   |   |                   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
The *Grid.reveal_all()* method simply runs through all the cells in the grid and calls the *Cell.reveal()* method.  So hidden cells are no longer hidden.

The dense network of passages in the center is our downtown.  Our uptown cells are undeveloped.

So we develop the uptown:
```
>>> print(status := HopTree.on(maze))
          Hop Search (statistics)
                            visits       84
                            action  furthest
                  selection passes     2248
                             cells      104
                  passages (start)       31
                          passages      115
>>> print(maze)
+---+---+---+---+---+---+---+---+---+---+---+---+---+
|   |   |   |                               |       |
+   +   +   +   +---+---+---+---+---+   +---+   +---+
|               |       |   |   |   |   |           |
+---+   +---+---+---+   +   +   +   +---+   +---+   +
|           |                       |   |       |   |
+---+   +---+---+   +   +   +   +   +   +   +---+   +
|           |                                   |   |
+---+   +---+   +   +   +   +   +   +---+   +---+   +
|   |       |   |                       |   |       |
+   +   +---+---+   +   +   +   +   +---+---+---+   +
|           |                           |           |
+   +---+---+---+   +---+   +   +   +---+---+   +   +
|   |   |   |           |   |   |   |   |       |   |
+   +   +   +---+   +---+---+---+---+   +---+   +---+
|                       |                           |
+---+---+---+---+---+---+---+---+---+---+---+---+---+
```
If we treat the 20-cell downtown as a single cell, we have:
```
        104 - 20 = 84 uptown cells
                    1 downtown (20 cells)
                  ----
                   85 nodes
```
So we need 84 passages uptown, some of which lead downtown.  Each "visit" carves one passage.  And there you have it!  All roads lead (at least eventually) to Rome.