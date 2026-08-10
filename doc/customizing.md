# Customizing a Maze

## 1. Pruning using Prim's algorithm

Suppose you just ran your algorithm of choice to produce a perfect maze.  It's almost what you want, but not quite.  The problem is that you require certain passages where there are walls, but you still want a perfect maze.  One approach is to add the required passages and then prune the maze using Prim's algorithm.  Here we illustrate the idea with a worked-out example example.

### Step 1.1.  Create a maze

First we need a maze...  we will use the hunt and kill algorithm.  (The actual algorithm isn't important -- we just want a perfect maze to start.  But given your particular needs, choose an algorithm that produces a good first step!)

```
    > from mazes.Grids.oblong import OblongGrid
    > from mazes.maze import Maze
    > from mazes.Algorithms.hunt_kill import HuntKill
    > maze = Maze(OblongGrid(10,13))
    > print(HuntKill.on(maze))
          Hunt and Kill (statistics)
                            visits      129
                             cells      130
                          passages      129
                              hunt       15
                              kill      114
                     starting cell  (0, 4)
    > print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |                   |   |
    +   +---+   +   +   +   +   +   +   +---+---+   +   +
    |       |   |   |   |   |   |   |       |       |   |
    +   +   +   +---+   +---+   +---+---+   +   +---+   +
    |   |   |           |       |           |           |
    +   +   +---+---+   +   +   +   +---+---+---+---+---+
    |   |   |       |       |   |   |                   |
    +   +---+   +   +---+---+   +   +---+---+---+---+   +
    |           |           |       |               |   |
    +---+---+   +---+   +---+---+---+   +---+---+   +   +
    |   |       |       |       |   |           |       |
    +   +   +---+---+---+   +   +   +---+---+   +---+---+
    |   |           |       |   |       |           |   |
    +   +---+   +   +---+   +---+   +   +   +   +   +   +
    |   |       |       |           |       |   |       |
    +   +   +---+---+   +   +---+---+   +---+   +---+---+
    |   |   |       |   |       |   |       |   |       |
    +   +   +---+   +   +---+   +   +---+   +   +   +   +
    |               |           |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Step 1.2.  Identify the problems

We need to identify passages that are required.  For this demonstration, we will assume that there are three passages that we need to have, and that we don't have any existing passages that are absolutely mandatory.  (We'll say a little more about that in the epilogue.)

Here are the three passages that we require.
```
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |         @         |   |
    +   +---+   +   +   +   +   +   +   +   +---+   +   +
    |       |   |   |   |   |   |   |     @ |       |   |
    +   +   +   +---+   +---+   +---+---+   +   +---+   +
    |   |   |           |       |           |           |
    +   +   +---+---+   +   +   +   +---+---+---+---+---+
    |   |   |       |       |   |   |                   |
    +   +---+   +   +---+---+   +   +---+---+---+---+   +
    |           |           |       |               |   |
    +---+---+   +---+   +---+---+---+   +---+---+   +   +
    |   |       |     @   @     |   |           |       |
    +   +   +---+---+---+   +   +   +---+---+   +---+---+
    |   |           |       |   |       |           |   |
    +   +---+   +   +---+   +---+   +   +   +   +   +   +
    |   |       | @     |           |       |   |       |
    +   +   +---+   +   +   +---+---+   +---+   +---+---+
    |   |   |     @ |   |       |   |       |   |       |
    +   +   +---+   +   +---+   +   +---+   +   +   +   +
    |               |           |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```
We will need to add them to the maze, saving them.

### Step 1.3.  Adding the passages

We can use grid coordinates and directions to identify the cells.  For demonstration purposes, we will label the cells.

```
    > cell1a = maze.grid[1,3]; cell1b = cell1a.north
```
Here we've identified the cells to be linked.  One of the cells is identified using grid coordinates, the other using its direction from its companion.

```
    > cell1a.is_linked(cell1b)
    False
```
This line is a check.  It's easy to make a mistake using the coordinates.  We want to be sure that these to cells are separated by a wall.  Since they are not linked (*i.e.*, the reply `is_linked==False`), the required wall is present.  (More precisely, since walls are not a data structure, there is no passage between the two cells.)


```
    > edge1 = maze.link(cell1a, cell1b)
```
Now we create the passage.  In graph theoretic terms, since the passage is bidirectional, it is an edge in the graph and not an arc.

```
    > cell1a.label, cell1b.label = '1', '1'
```
For demonstration purposes, we assign labels.  Let's take a peek:

```
    > print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |                   |   |
    +   +---+   +   +   +   +   +   +   +---+---+   +   +
    |       |   |   |   |   |   |   |       |       |   |
    +   +   +   +---+   +---+   +---+---+   +   +---+   +
    |   |   |           |       |           |           |
    +   +   +---+---+   +   +   +   +---+---+---+---+---+
    |   |   |       |       |   |   |                   |
    +   +---+   +   +---+---+   +   +---+---+---+---+   +
    |           |           |       |               |   |
    +---+---+   +---+   +---+---+---+   +---+---+   +   +
    |   |       |       |       |   |           |       |
    +   +   +---+---+---+   +   +   +---+---+   +---+---+
    |   |           |       |   |       |           |   |
    +   +---+   +   +---+   +---+   +   +   +   +   +   +
    |   |       | 1     |           |       |   |       |
    +   +   +---+   +   +   +---+---+   +---+   +---+---+
    |   |   |     1 |   |       |   |       |   |       |
    +   +   +---+   +   +---+   +   +---+   +   +   +   +
    |               |           |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Two more required passages:
```
    > cell2a = maze.grid[4,4]; cell2b = cell2a.east
    > cell2a.is_linked(cell2b)
    False
    > edge2 = maze.link(cell2a, cell2b)
    > cell2a.label, cell2b.label = '2', '2'

    > cell3a = maze.grid[9,9]; cell3b = cell3a.south
    > cell3a.is_linked(cell3b)
    False
    > edge3 = maze.link(cell3a, cell3b); print(maze)
    > cell3a.label, cell3b.label = '3', '3'
```

And the current state:
```
    > print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |         3         |   |
    +   +---+   +   +   +   +   +   +   +   +---+   +   +
    |       |   |   |   |   |   |   |     3 |       |   |
    +   +   +   +---+   +---+   +---+---+   +   +---+   +
    |   |   |           |       |           |           |
    +   +   +---+---+   +   +   +   +---+---+---+---+---+
    |   |   |       |       |   |   |                   |
    +   +---+   +   +---+---+   +   +---+---+---+---+   +
    |           |           |       |               |   |
    +---+---+   +---+   +---+---+---+   +---+---+   +   +
    |   |       |     2   2     |   |           |       |
    +   +   +---+---+---+   +   +   +---+---+   +---+---+
    |   |           |       |   |       |           |   |
    +   +---+   +   +---+   +---+   +   +   +   +   +   +
    |   |       | 1     |           |       |   |       |
    +   +   +---+   +   +   +---+---+   +---+   +---+---+
    |   |   |     1 |   |       |   |       |   |       |
    +   +   +---+   +   +---+   +   +---+   +   +   +   +
    |               |           |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Step 1.4.  Auxiliary passages

In some cases, we might need to add one or more additional passages to insure that the required passages can be added.  The procedure is the same.
```
    > cell4a = maze.grid[6,10]; cell4b = cell4a.north
    > cell4a.is_linked(cell4b)
    False
    > edge4 = maze.link(cell4a, cell4b)
    > cell4a.label, cell4b.label = '4', '4'
    > print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |         3         |   |
    +   +---+   +   +   +   +   +   +   +   +---+   +   +
    |       |   |   |   |   |   |   |     3 |       |   |
    +   +   +   +---+   +---+   +---+---+   +   +---+   +
    |   |   |           |       |           | 4         |
    +   +   +---+---+   +   +   +   +---+---+   +---+---+
    |   |   |       |       |   |   |         4         |
    +   +---+   +   +---+---+   +   +---+---+---+---+   +
    |           |           |       |               |   |
    +---+---+   +---+   +---+---+---+   +---+---+   +   +
    |   |       |     2   2     |   |           |       |
    +   +   +---+---+---+   +   +   +---+---+   +---+---+
    |   |           |       |   |       |           |   |
    +   +---+   +   +---+   +---+   +   +   +   +   +   +
    |   |       | 1     |           |       |   |       |
    +   +   +---+   +   +   +---+---+   +---+   +---+---+
    |   |   |     1 |   |       |   |       |   |       |
    +   +   +---+   +   +---+   +   +---+   +   +   +   +
    |               |           |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Step 1.5.  Build the priority queue

Here we use the edges that we created.  We use a three-tiered priority scheme.  The highest priority (lowest value: 0) is for most desired passages.  The lowest priority (highest value: 2) is for passages we'd prefer not to see.  The middle priority (value: 1) is for passages we treat as neutral.
```
    > priorities = dict()
    > priorities[edge1] = 0
    > priorities[edge2] = 0
    > priorities[edge3] = 0
    > cost = lambda edge: priorities.get(edge, 1)
```

### Step 1.6. Prune the maze

We need two more imports:
```
    > from mazes.WallBuilders.pruning_tree import PruningTree
    > from mazes.Queues.priority_queue import PriorityQueue
```

Now we prune:
```
    > print(PruningTree.on(maze, QueueType=PriorityQueue,
    >     qkwargs={"priority":cost}))
          maze algorithm (statistics)
                            visits      392
                 queuing structure  PriorityQueue
                           unlinks        4
                          arrivals      130
                        departures      130
                        visit type  cell
                        start cell  (1, 1)
                       unprocessed        0
                          passages      129
              maximum queue length       14
              average queue length        8.1615
```

And the result...  Note that the auxiliary passage was removed, but the desired passages were all retained.
```
    > print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |       |       |       | 3         |   |
    +   +---+   +   +   +   +   +   +   +   +---+   +   +
    |       |   |   |   |   |   |   |     3 |       |   |
    +   +   +   +---+   +---+   +---+---+   +   +---+   +
    |   |   |           |       |           | 4         |
    +   +   +---+---+   +   +   +   +---+---+---+---+---+
    |   |   |       |       |   |   |         4         |
    +   +---+   +   +---+---+   +   +---+---+---+---+   +
    |           |           |       |               |   |
    +---+---+   +---+   +---+---+---+   +---+---+   +   +
    |   |       |     2   2     |   |           |       |
    +   +   +---+---+---+   +   +   +---+---+   +---+---+
    |   |   |   |   |       |   |       |           |   |
    +   +---+   +   +---+   +---+   +   +   +   +   +   +
    |   |       | 1     |           |       |   |       |
    +   +   +---+   +   +   +---+---+   +---+   +---+---+
    |   |   |     1 |   |       |   |       |   |       |
    +   +   +---+   +   +---+   +   +---+   +   +   +   +
    |               |           |           |       |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### 1.7 Epilogue:  Identifying existing passages


For an actual application, one might need to include an existing edge in the most desired category (priority 0).  The `Cell.join_for` method will return the desired passage:
```
    > cell5 = maze.grid[0,0]
    > edge = cell5.join_for(cell5.north)
```

We can inspect the edge:
```
    > type(edge)
    <class 'mazes.edge.Edge'>
    > list(edge)
    [SquareCell object, SquareCell object]
```
The `list(edge)` statement returns the two incident cells in some order.

In step 5 above, we would include the desired edge in the priorities table:
```
    > priorities[edge] = 0
```

If, instead, we wanted to make this an undesirable edge, we set its priority to 2:
```
    > priorities[edge] = 2
```

Note that this edge happens to be a bridge in the extended maze as it separates the lower part of the first column from the rest of the maze.  Thus it cannot be removed, regardless of priority.
