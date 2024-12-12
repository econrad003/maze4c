# Kruskal's Algorithm

## The algorithm

```
Preliminaries:
    an empty maze, suitable for carving
    a priority queue

Initialize:
    enter all the grid edges into the queue
    assign each cell to a separate component (the cells are isolated)

Loop:
    while there is more than one component and there are items in the queue:
        remove an edge from the queue
        if the edge joins two components:
            carve the edge to form a passage
            merge the components
```

If the grid is connected, the result is a minimum weight spanning tree.

To envision how this works and how it differs from Prim's algorithm, imagine that you are the governor of a province with a number of towns connected by dirt roads.  (The dirt roads are the underlying grid.)  You were elected on a platform of paving roads to modernize the road network.  But your legislature will only budget enough to barely pave enough roads to connect the province by paved roads.  (The paved roads will be a spanning tree -- a minimum cost spanning tree!)

Your first proposal is to start in your home town and build the paved road network from there using Prim's algorithm.  But the opposition part cries foul!  "You are wasting money!" the opposition leader cries.  "The cheapest road can be built from my home town!".

You admit that the opposition leader's objection has some merit, so you decide to build the network using Kruskal's algorithm.  Instead of a growing tree starting from your home town or (heaven forbid!) from the opposition leader's home town, you simply consider each road in turn, starting with the cheapest.  If it joins two town that cannot reach each other by a paved road, you build it.  Sometimes an opposition legislator is happy because his town was connected to the *forest* of paved roads.  Sometimes it is one of your party's legislators.  And eventually the network is completed and everyone is happy.

### Example 1 - Kruskal's algorithm (random weights)

```
    maze4c$ python
    Python 3.10.12.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Algorithms.kruskal import Kruskal
    5> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      152
                 components (init)      104
               queue length (init)      187
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)       35
    6> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |           |           |   |           |
    +   +---+   +---+---+   +   +   +   +   +   +---+---+
    |   |       |   |           |   |                   |
    +---+---+   +   +   +---+---+   +---+   +   +---+   +
    |           |       |           |   |   |   |       |
    +   +---+   +---+---+---+   +   +   +---+   +---+   +
    |   |   |       |   |       |           |   |       |
    +   +   +---+---+   +---+---+   +---+   +   +---+   +
    |               |                   |   |       |   |
    +   +---+---+   +---+   +   +   +   +---+---+   +   +
    |   |       |       |   |   |   |       |       |   |
    +---+---+   +   +   +---+   +---+---+   +---+   +---+
    |           |   |       |       |       |   |       |
    +---+---+   +---+   +   +   +---+   +---+   +---+   +
    |                   |           |           |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The result here is a fairly random spanning tree.  (It is not uniformly random.  But it is a reasonable approximation...  And when too many people get lost travelling from town A to town B, you end up getting thrown out of office.  That's a consequence of minimum cost.)

Let's look at the statistics as they tell a story...  In each visit, we remove an edge from the queue:
```
        change in queue length = 187 - 35 = 152 = number of visits
```

We only carve a passage if it reduces the number of components:
```
        number of visits - passages = 152 - 103 = 49
                                    = unsuccessful visits
```
When there are fewer components, we generally need to discard more edges to find one which joins two components.

## Interface

In Kruskal.Status, we have the following interface
```
    def parse_args(self, setup:(str, callable)="collect",
                   shuffle:bool=False,
                   QueueClass:object=PriorityQueue,
                   priority:callable=None,
                   init:tuple=(tuple(), dict())):
```

The first argument is actually the maze object.  The remaining arguments are the optional keyword arguments that you see here.

To get a feel for this interface, let's replace the PriorityQueue class with the Stack class, and keep the shuffle turned off.

### Example 2A - Kruskal with Stack, no shuffle

```
    maze4c$ python
    Python 3.10.12 (main, Nov  6 2024, 20:22:13) [GCC 11.4.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    1> from mazes.Grids.oblong import OblongGrid
    2> from mazes.maze import Maze
    3> maze = Maze(OblongGrid(8, 13))
    4> from mazes.Queues.stack import Stack
    5> from mazes.Algorithms.kruskal import Kruskal
    6> print(Kruskal.on(maze, QueueClass=Stack))
          Kruskal (statistics)
                            visits      186
                 components (init)      104
               queue length (init)      187
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)        1
    7> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |                                                   |
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
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

This is an artifact of the way CPython implements dictionaries.  It looks like breadth-first search if we start in the northeast corner and work our way systematically through the maze.  (But it's Kruskal and not BFS!)  Note also that we did more work since we need to run through all but one entry in the queue.

### Example 2B Kruskal with Stack, shuffle

Now let's shuffle...

```
    8> maze = Maze(OblongGrid(8, 13))
    9> print(Kruskal.on(maze, QueueClass=Stack, shuffle=True))
          Kruskal (statistics)
                            visits      140
                 components (init)      104
               queue length (init)      187
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)       47
    10> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |   |   |               |   |           |   |
    +   +   +   +   +   +   +---+---+   +---+   +   +   +
    |   |           |   |       |               |       |
    +---+   +---+---+   +---+   +---+   +---+---+   +---+
    |   |           |   |           |   |               |
    +   +   +---+   +---+---+   +   +   +---+   +   +---+
    |           |       |       |           |   |       |
    +---+   +   +---+---+---+---+   +   +---+---+---+   +
    |       |   |           |       |       |           |
    +   +   +---+---+   +---+---+   +---+---+   +---+---+
    |   |   |           |               |               |
    +   +   +   +   +---+   +---+   +---+---+   +   +---+
    |   |       |               |   |           |   |   |
    +   +---+   +   +---+   +   +   +   +   +---+---+   +
    |       |   |   |       |   |   |   |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

This looks a lot like Example 1.  (Both the maze and the statistics!)  We can view the Stack implementation as just a particular arrangement of priorities...  In Example 2A, the lowest weights were assigned to edges in the northeastern part of the grid.  In Example 2B, as in Example 1, edge weights were reasonably independent of the location in the grid.

### Example 2C - Queue, no shuffle

Let's try a queue...  Without shuffling, will will Kruskal look like DFS?  Think about edge weights and how CPython implements dictionary ordering...

```
    11> from mazes.Queues.queue import Queue
    12> maze = Maze(OblongGrid(5, 8))
    13> print(Kruskal.on(maze, QueueClass=Queue))
          Kruskal (statistics)
                            visits       60
                 components (init)       40
               queue length (init)       67
                             cells       40
                          passages       39
                components (final)        1
              queue length (final)        7
    14> print(maze)
    +---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +
    |   |   |   |   |   |   |   |   |
    +   +   +   +   +   +   +   +   +
    |                               |
    +---+---+---+---+---+---+---+---+
```

Not at all like DFS!

### Example 2D - Queue, shuffled

Shuffling should give us results that are indistinuishable from a shuffled Stack implementation.

```
    15> maze = Maze(OblongGrid(8, 13))
    16> print(Kruskal.on(maze, QueueClass=Queue, shuffle=True))
          Kruskal (statistics)
                            visits      162
                 components (init)      104
               queue length (init)      187
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)       25
    17> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |               |   |   |   |   |   |       |   |   |
    +---+   +   +---+   +   +   +   +   +   +---+   +   +
    |       |       |               |   |   |           |
    +   +---+---+   +   +   +   +   +   +   +---+   +---+
    |   |   |   |   |   |   |   |   |                   |
    +   +   +   +---+---+---+---+   +   +---+   +   +   +
    |   |           |                   |       |   |   |
    +   +   +---+   +---+   +---+---+---+---+   +   +---+
    |           |                       |       |   |   |
    +   +   +   +   +---+---+   +   +---+---+   +---+   +
    |   |   |   |   |           |       |   |           |
    +---+---+   +---+---+---+---+---+   +   +   +---+   +
    |               |               |       |       |   |
    +   +---+   +---+---+   +---+   +   +   +---+   +---+
    |       |           |       |       |       |       |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

### Example 2E - RandomQueue, no shuffle

And finally, let's look at RandomQueue.  We should get reasonably random results without shuffling, and they should be reasonably indistinguishable from Stack or Queue with shuffling, or from PriorityQueue regardless.

```
    18> from mazes.Queues.random_queue import RandomQueue
    19> maze = Maze(OblongGrid(8, 13))
    20> print(Kruskal.on(maze, QueueClass=RandomQueue))
          Kruskal (statistics)
                            visits      135
                 components (init)      104
               queue length (init)      187
                             cells      104
                          passages      103
                components (final)        1
              queue length (final)       52
    21> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |           |           |   |               |       |
    +   +   +---+   +   +---+   +---+---+   +---+   +---+
    |   |           |   |   |                   |   |   |
    +   +---+   +   +   +   +---+---+---+   +---+   +   +
    |   |       |   |       |           |   |       |   |
    +---+   +---+   +---+---+   +---+   +   +---+   +   +
    |           |                   |       |           |
    +---+---+---+---+   +---+   +---+---+   +   +---+   +
    |                   |       |           |   |   |   |
    +---+   +   +   +---+   +---+---+---+---+---+   +   +
    |   |   |   |   |   |       |       |           |   |
    +   +---+---+---+   +   +   +   +---+---+   +---+   +
    |               |   |   |       |           |       |
    +---+---+   +   +   +   +   +---+   +---+   +   +---+
    |           |           |           |               |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Voilà!

## Exercises

Try experimenting with other queuing structures, for example a hybrid stack and random queue which alternates between taking the most recent entry and a random entry.  What happens without shuffling in Kruskal?  How about the growing tree algorithms.

Another queuing structure is a MedianQueue which always removes elements from the middle.

If we view our queuing structures as providing us edges in ascending weight order, the actual queue implementation is irrelevant.

## The setup option - scatter or collect

In addition to *setup="collect"*, there is *setup=scatter*.  In the above examples we could have used *setup=scatter* with absolutely no difference in the outcome.  The run time would have been shorter, but not appreciably so.

The real difference is what happens when the initial maze is not empty.  Scattering ignores any existing passages.  Collecting determines existing component relationships.  Kruskal's algorithm then connects the components.  In the governor story, imagine that inside the towns the roads have already been paved.

### Example 3 - Collecting

In our maze, we start with two towns.  The town center of Stackley is in row 2 column 2 (third row , third column).  Stackley has two paved streets: Broad Street and Long Street which meet in the town center and extend one cell in either direction.  The town center of Queuper is in row 5 column 8.  Queueper also has 2 streets: Main Street and Wide Street which meet in the town center and extend one cell in either direction.  Let's take a look at the map...

```
    22> maze = Maze(OblongGrid(8, 13))
    23> grid = maze.grid
    24> maze.link(grid[1,2], grid[2,2])
    25> maze.link(grid[2,1], grid[2,2])
    26> maze.link(grid[2,3], grid[2,2])
    27> maze.link(grid[3,2], grid[2,2])
    28> grid[1,2].label = 'S'
    29> grid[2,2].label = 'S'
    30> grid[2,1].label = 'S'
    31> grid[2,3].label = 'S'
    32> grid[3,2].label = 'S'
    33> maze.link(grid[5,7], grid[5,8])
    34> maze.link(grid[5,9], grid[5,8])
    35> maze.link(grid[4,8], grid[5,8])
    36> maze.link(grid[6,8], grid[5,8])
    37> grid[5,7].label = 'Q'
    38> grid[5,8].label = 'Q'
    39> grid[5,9].label = 'Q'
    40> grid[4,8].label = 'Q'
    41> grid[6,8].label = 'Q'
    42> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   | Q |   |   |   |   |
    +---+---+---+---+---+---+---+---+   +---+---+---+---+
    |   |   |   |   |   |   |   | Q   Q   Q |   |   |   |
    +---+---+---+---+---+---+---+---+   +---+---+---+---+
    |   |   |   |   |   |   |   |   | Q |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   | S |   |   |   |   |   |   |   |   |   |   |
    +---+---+   +---+---+---+---+---+---+---+---+---+---+
    |   | S   S   S |   |   |   |   |   |   |   |   |   |
    +---+---+   +---+---+---+---+---+---+---+---+---+---+
    |   |   | S |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |   |   |   |   |   |   |   |   |   |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

After having been cast out as governor of one province, you manage to get elected governor of this province because people here like the way you built a  cheap network of paved roads using Kruskal's algorithm.  Being very frugal, the inhabitants of this province don't mind the inconvenience of a maze of twisty little passages all alike...  But can you use existing paved roads?  Of course you can!

```
    43> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits      147
                 components (init)       96
               queue length (init)      179
                             cells      104
                          passages       95
                components (final)        1
              queue length (final)       32
    44> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    |       |   |   |           |                       |
    +---+   +   +   +   +---+   +---+---+   +   +   +   +
    |       |       |   |           | Q |   |   |   |   |
    +   +---+   +---+---+   +---+---+   +   +---+---+---+
    |       |               |     Q   Q   Q |       |   |
    +   +   +   +   +---+   +---+   +   +---+   +---+   +
    |   |   |   |       |   |       | Q                 |
    +---+   +---+---+   +---+---+---+   +---+---+---+---+
    |       | S |   |       |                           |
    +   +   +   +   +   +---+   +---+   +   +---+---+---+
    |   | S   S   S |   |       |       |               |
    +---+   +   +---+   +   +---+---+   +   +---+   +   +
    |       | S             |           |   |       |   |
    +   +   +   +---+   +---+   +---+   +   +   +   +   +
    |   |   |   |       |       |       |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

We started with 8 paved passages and no circuits.   We carved a total of 95 passages for a total of 103 passages, one less than the total number of cells.  This is the right number of passages for a spanning tree -- provided the maze is connected...

And yes!  The resulting maze is connected -- the number of components was reduced to one.  Just what the doctor ordered!

But there's one more observation.  In lines 22 through 42, there was a bit of some maze carving (paving the streets of Stackley and Queueper).  From the earlier examples, there appear to be 187 edges in the grid...
```
    arcs in the interior                   4 x (6 x 11) = 264
    arcs on the perimeter, except corners  3 x (6+11)x2 = 102
    arcs in the corners                           2 x 4 =   8
                                                         -----
    total arcs                                            374
    total edges (2 arcs per edge -- divide by two)        187
```
Correct!  But 8 passages were carved prior to running Kruskal's algorithm.  Notice that we started with 179 grid edges instead of all 187.  The eight carved edges we removed from consideration before processing.  This is the difference between "collect" and "scatter"...  scattering treats the maze as if no passages had already been carved.  And loops in the grid (a loop is a grid edge joining a cell to itself -- a trivial circuit) will be removed in preprocessing, but scattering ignores existing passages.

If there are no passages to start with, collecting is equivalent in result to scattering, but it takes a bit longer.  On the small mazes we're considering, the time difference is not consequential.

### Example 4 - More collecting

Your success in building paved road networks using Kruskal's Algorithm has gained you international reknown.  You have retired as a poorly paid provincial governor are now a highly paid consultant.  The wealthy and heavily populated province of Merginia has hired you.  Over eight generations, the population has grown considerably from the three families.  The following map shows the current generation:
```
    maze4c$ python
    Python 3.10.12.
    1> import mazes.tools.automaton1 as CA
    2> grid, alive = CA.simulate(8, 13, born_at_start=3, generations=8)
    3> print(grid)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 | 2 | 3 | 2 | 2 |   | 2 |   | 2 |   | 2 |   | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 |   | 2 | 2 | 2 | 2 |   | 2 |   | 2 |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 | 2 |   | 2 | 2 | 2 | 2 |   | 2 |   |   |   | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |   | 1 |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 | 2 | 2 | 2 | 2 | 2 |   | 2 |   |   |   |   | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 | 2 |   | 2 | 2 |   | 2 |   | 2 |   |   |   |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 |   | 2 | 2 | 2 | 2 |   | 2 |   | 2 |   |   | 2 |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

The cells marked either 1 or 3 are the sites of the initial settlements.  Cells marked with a 2 or a 3 are the locations of current settlements.  (The site in row 4 column 9 was abandoned and is now vacant.)

Its people unwilling to tolerate dirt roads any longer, the province constructed paved roads connecting neighbors.  But the high cost nearly bankrupted the province.  Unfortunately, some people are isolated.  Here is the current network of paved roads:

```
    4> from mazes.maze import Maze
    5> maze = Maze(grid)
    6> visited = set()
    7> for cell in grid:
    ...     visited.add(cell)
    ...     if cell.label not in {2, 3}:
    ...         continue
    ...     for nbr in cell.neighbors:
    ...         if nbr.label in {2, 3}:
    ...             maze.link(cell, nbr)
    ...
    8> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2   2   3   2   2 |   | 2 |   | 2 |   | 2 |   | 2 |
    +   +---+   +   +   +---+---+---+---+---+---+---+---+
    | 2 |   | 2   2   2   2 |   | 2 |   | 2 |   |   |   |
    +   +---+---+   +   +   +---+---+---+---+---+---+---+
    | 2   2 |   | 2   2   2   2 |   | 2 |   |   |   | 2 |
    +   +   +---+   +   +   +   +---+---+---+---+---+---+
    | 2   2   2   2   2   2   2   2 |   | 1 |   |   |   |
    +   +   +   +   +   +   +---+   +---+---+---+---+---+
    | 2   2   2   2   2   2 |   | 2 |   |   |   |   | 2 |
    +   +   +---+   +   +---+---+---+---+---+---+---+---+
    | 2   2 |   | 2   2 |   | 2 |   | 2 |   |   |   |   |
    +   +---+---+   +   +---+---+---+---+---+---+---+---+
    | 2 |   | 2   2   2   2 |   | 2 |   | 2 |   |   | 2 |
    +   +---+   +   +   +   +---+   +---+   +---+---+---+
    | 2   2   3   2   2   2   2   2   2   2   2   2 |   |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Note that there are a lot of superfluous paved roads in the western half of Merginia.  But these will remain as there is no extra money for demolition.  Your task is to complete the network (*i.e.* create a spanning maze with no *additional* superfluous passages), and to do so at minimum cost.  This is not a problem.  A cost analysis for paving the remaining dirt roads gives you all you need:

```
    9> from mazes.Algorithms.kruskal import Kruskal
    10> print(Kruskal.on(maze))
          Kruskal (statistics)
                            visits       93
                 components (init)       51
               queue length (init)      113
                             cells      104
                          passages       50
                components (final)        1
              queue length (final)       20
    11> print(maze)
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
    | 2   2   3   2   2     | 2 |   | 2     | 2     | 2 |
    +   +---+   +   +   +---+   +   +---+   +---+   +   +
    | 2     | 2   2   2   2       2     | 2         |   |
    +   +---+   +   +   +   +---+   +---+---+---+   +   +
    | 2   2 |   | 2   2   2   2 |   | 2     |       | 2 |
    +   +   +---+   +   +   +   +---+   +---+---+   +   +
    | 2   2   2   2   2   2   2   2 |   | 1             |
    +   +   +   +   +   +   +---+   +   +   +---+   +   +
    | 2   2   2   2   2   2 |   | 2 |   |       |   | 2 |
    +   +   +---+   +   +---+   +   +   +---+   +---+---+
    | 2   2 |     2   2 |     2 |     2     |       |   |
    +   +---+---+   +   +---+   +---+---+---+   +---+   +
    | 2     | 2   2   2   2     | 2 |   | 2           2 |
    +   +---+   +   +   +   +---+   +   +   +---+---+---+
    | 2   2   3   2   2   2   2   2   2   2   2   2     |
    +---+---+---+---+---+---+---+---+---+---+---+---+---+
```

Let's look at the data.  The initial network consisted of 104 cells in 51 components.  To connect these components, we need a minimum of 50 passages.  More than 50 is unnecessary.  We were able to complete the network using
existing paved roads.

## References

1. Jamis Buck.  Mazes for Programmers.  2015, Pragmatic Bookshelf, *pp* 158-163, 252.