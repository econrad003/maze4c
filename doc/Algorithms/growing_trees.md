# Growing Tree Algorithms

The growing tree algorithms are a family of algorithms that use queue-oriented search to carve a maze.  There are several varitions of the algorithm, with the main differences in choice of queuing discipline and in handling of visits.

## Basic algorithm

```
Initialization:
   Mark all cells in the grid as unvisited.
   Choose a cell from the grid and mark it as visited.
   Place the cell in the queue.

Loop:
   While there are cells in the queue:
      consider the first cell in the queue;
      if the cell has unvisited neighbors:
          place an unvisited neighbor in the queue;
          carve a passage from the current cell to the neighbor
          mark the neighbor as visited;
      otherwise:
          remove the current cell from the queue.
```

## Queues

There are many different kinds of queues.  The similarity is that there are basically five methods:

* *is_empty* - if there are objects in the queue, this method returns False, and if there are no objects in the queue, then the method returns True.
* *enter* - this method places objects in the queue.  Depending on the type of queue, it might have take a priority as an additional argument.
* *leave* - this method returns the object that is first in the queue and removes it from the queue.
* *top* - this method returns the object that is first in the queue, but does not remove it.
* *jettison* - this method is essentially the same as *leave*, but it makes sure that the queue hasn't changed since the most recent *top* call.  In other words, it guarantees that the *top* object leaves the queue.

Here are some fairly basic kinds of queues:

* *stack* - a last in, first out (LIFO) queuing structure.  The standard example is a stack of trays in a cafeteria.  When a tray has been washed, it is placed in the stack.  When a customer retrieves a tray from the top of the stack, it will be the most recently placed tray.  (That's why it isn't unusual for cafeteria trays to be wet.)  Python lists work well as stacks.
* *queue* - a first in, first out (FIFO) queuing structure.  The standard example here is a customer in a cafeteria.  Customers enter the line (or queue).  The first in line for service is the first one to enter the line.  Of course in real-world queues, people sometimes jump in front of others, but in a FIFO queue, that isn't allowed.  Python lists work poorly as queues, but the *deque* class defined in the Python *collections* module works quite well for implementing a FIFO queue.
* *random queue* - there isn't a standard name for a random in, first out queuing structure.  The main problem is insuring that the top element is stable.  Module *mazes.active\_list* is what we use to implement random queues
* *priority queue* - there are two flavors, a min-priority queue and a max-priority queue. In a priority queue, objects are entered with a priority. The first in the queue is the one with the lowest priority value (min-priority) or the highest priority value (max-priority).  The Python module *heapq* works well for priority queues based on binary heaps and heapsort.  There are a myriad of other algorithms such as Fibonacci heaps, pagodas, and leftist trees.

## Basic Growing Tree Algorithm v2

Here is a restatement of the basic algorithm that uses three of the five basic queue methods:

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

Notice that jettison is called if and only if the queue hasn't changed since the top element was accessed.

## Example 1 - Depth-first search (naïve)

Depth-first search (also known as *DFS* for short or as *recursive backtracker* because it can in principle be implemented using recursive procedure calls) is the simplest of the growing tree.  It uses a stack for its queuing structure.

In *mazes.Algorithms.dfs*, I carelessly implemented a version of depth-first search.  It works quite well, but it has a serious drawback which I will discuss in Example 2 where the problem is fixed.  Here are some sample results:
```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(5, 8))
    4> from mazes.Algorithms.dfs import DFS
    5> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits       50
                        start cell  (1, 2)
               maximum stack depth       31
                             cells       40
                          passages       39
    6> print(maze)
    +---+---+---+---+---+---+---+---+
    |                   |           |
    +   +---+---+---+   +   +---+---+
    |   |           |   |           |
    +   +---+   +---+   +   +---+   +
    |   |       |       |   |       |
    +   +   +---+   +---+---+   +   +
    |   |   | S     |           |   |
    +   +   +---+---+---+   +---+   +
    |                       |       |
    +---+---+---+---+---+---+---+---+
```
I have marked the start cell with an S.

Note that there are no degree 4 cells, so this spanning tree is a binary tree.  DFS does not guarantee that every tree it produces is binary, but, in general, cells in a DFS maze will tend to have few incident passages.

Also DFS tends to produces mazes with fairly large diameter.  (The diameter of a maze is the length of a longest path.)  In this case the diameter is at least 28 passages in length.  (I think the longest path starts at S and ends in the northeast corner.  It has 29 cells and 28 passages.)

## Example 2 - Depth-first search (fixed)

The module *mazes.Algorithms.dsf\_better* has the fixed version of depth-first search.  I want to emphasize that the naïve algorithm does work.  But it does not generalize well.  If you replace the stack (LIFO) by a queue (FIFO) in order to implement breadth-first search, you will quick overwhelm the queue.

Now let's look at the fix:
```
    7> from mazes.Algorithms.dfs_better import DFS
    8> maze = Maze(OblongGrid(5, 8))
    9> print(DFS.on(maze))
          Depth-first Search (DFS) (statistics)
                            visits       79
                        start cell  (2, 6)
               maximum stack depth       32
                             cells       40
                          passages       39
    10> print(maze)
    +---+---+---+---+---+---+---+---+
    |           |                   |
    +   +   +---+   +---+   +---+---+
    |   |           |   |           |
    +   +---+---+---+   +---+---+   +
    |   |   |           |   | S |   |
    +   +   +   +   +   +   +   +   +
    |   |       |   |   |   |   |   |
    +   +---+---+   +   +   +   +   +
    |               |       |       |
    +---+---+---+---+---+---+---+---+
```

Again I marked the start cell as S.

There are no degree 4 cells, so this is a binary tree.  (On small oblong grids, this will often be the case.)  DFS tends to produce cells of low degree.  Degree 2 cells are very common.

Here the diameter is 31.  The longest path starts at S and ends one cell to the left.  It consists of 32 cells and 31 passages.

## Example 3 - Breadth-first search

If we replace the stack by a queue, we get breadth-first search (BFS).  But we should use the second implementation.  Depth-first search (DFS) tends to favor  one very long passage with a lot of degree-2 cells.  With a queue, we should see the start cell joined to each of its neighbors.  (The start cell is entered into the queue first, so it stays there until each of its neighbors has been visited.)  Let's see what really happens...

```
    11> from mazes.Algorithms.bfs import BFS
    12> maze = Maze(OblongGrid(5, 8))
    13> print(BFS.on(maze))
          Breadth-first Search (BFS) (statistics)
                            visits       40
                        start cell  (2, 2)
              maximum queue length       11
                             cells       40
                          passages       39
    14> print(maze)
    +---+---+---+---+---+---+---+---+
    |       |   |   |   |   |   |   |
    +---+   +   +   +   +   +   +   +
    |       |   |   |               | four degree-3
    +---+   +   +   +   +---+---+---+
    |         S                     | three degree-4, two degree-3
    +---+---+   +   +   +   +---+---+
    |           |   |   |           | four degree-3
    +---+   +   +   +   +   +   +---+
    |       |   |   |   |   |       |
    +---+---+---+---+---+---+---+---+
```

I count three degree-4 cells and ten degree-3 cells.  BFS clearly likes high-degree cells.  The diameter seems to be 11, represented by two paths (12 cells, 11 passages), one from the northwest corner to the southeast corner and the other from the northeast corner to the southwest corner.  Both paths go through the three degree-4 cells.

This is obviously not a binary tree.

## Simplified "Prim"

If we replace the stack or queue in DFS or BFS by a random queue, we get an algorithm which apparently is sometimes called Prim's algorithm.  Prim's algorithm finds a minimum weight spanning tree.  This algorithm does that in some sense, provided every grid edge is given equal weight.  But if every edge in the grid is given equal weight, then, since every spanning tree has the same number of passages, it would follow that every spanning tree would have the same weight. (Yes, I think the algorithm needs a better name.)  But it's a perfectly good spanning tree maze carving algorithm: it works!

The first implementation of simplified "Prim" is class *NotPrim* (yes, I renamed it) in the module *mazes.Algorithms.simplified_Prim.  Here is a sample:

```
    15> from mazes.Algorithms.simplified_Prim import NotPrim
    16> maze = Maze(OblongGrid(5, 8))
    17> print(NotPrim.on(maze))
          Simplified "Prim" (statistics)
                            visits       79
                        start cell  (1, 5)
               maximum list length       19
                             cells       40
                          passages       39
    18> print(maze)
    +---+---+---+---+---+---+---+---+
    |               |       |       |
    +   +   +---+   +   +---+---+   +
    |   |   |       |   |           |
    +---+---+   +   +   +   +---+---+
    |           |           |       |
    +   +---+---+---+---+   +   +   +
    |   |                 S     |   |
    +---+---+---+---+---+   +---+---+
    |                               |
    +---+---+---+---+---+---+---+---+
```

(Incidentally, if you are following along, don't forget to create a fresh virgin maze (line 16) before running the algorithm.  Or, better yet, try it and see what the mistake looks like.)

I think a longest path starts just below the northwest corner in cell (3, 0) and ends in the southwest corner in cell (0, 0) for 16 cells and 15 passages.  So the diameter is 15.  There is another longest path (same length) from (1, 0) to (0, 0).

The start cell S is the only degree-4 cell.  Since simplified "Prim" places a random element as the top element, it is reasonable to expect that its behavior to be between the extremes of BFS (first is top) and DFS (last is top).  But if we inspect paths from starting cell S, we find that they seem to be fairly uniform in length, not as uniform as BFS, but the radial structure is still apparent.  This is typical behavior for the algorithm, especially when the start cell is in the center of the grid.

## The next steps

All three algorithms have essentially the same structure.  So why three different modules?  Why indeed!  Following guidance in the Jamis Buck book (◇), implemented two more general growing tree algorithms.  The first is a vertex-based (or equivalently cell-based) growing tree algorithm (*growing\_tree1*) and the second is an arc-based growing tree algorithm.

| **algorithm family** | **implementation**  | **documentation**  |
| :------------------- | :------------------ | :----------------- |
|                      | *mazes/Algorithms*  | *doc/Algorithms*   |
| vertex-based         | *growing\_tree1.py* | *growing\_trees1.md |
| arc-based            | *growing\_tree2.py* | *growing\_trees2.md |

Table 1. Growing tree algorithm families.

Prim's algorithm is easiest to implement in the arc-based family.

See the above-mentioned files for more details and examples.

◇ Jamis Buck.  *Mazes for Programmers.  2015, Pragmatic Bookshelf.  *pp* 183-188, 251.